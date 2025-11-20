"""
API views for the Chemical Equipment Parameter Visualizer.
"""
import os
import io
import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .models import UploadedDataset
from .serializers import UserSerializer, UploadedDatasetSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint."""
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload and process CSV file.
    Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file size (5MB max)
    if file.size > 5 * 1024 * 1024:
        return Response(
            {'error': 'File size exceeds 5MB limit'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file extension
    if not file.name.endswith('.csv'):
        return Response(
            {'error': 'Only CSV files are allowed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response(
                {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate summary statistics
        summary = {
            'total_equipment': len(df),
            'average_flowrate': float(df['Flowrate'].mean()),
            'average_pressure': float(df['Pressure'].mean()),
            'average_temperature': float(df['Temperature'].mean()),
            'type_distribution': df['Type'].value_counts().to_dict(),
            'min_flowrate': float(df['Flowrate'].min()),
            'max_flowrate': float(df['Flowrate'].max()),
            'min_pressure': float(df['Pressure'].min()),
            'max_pressure': float(df['Pressure'].max()),
            'min_temperature': float(df['Temperature'].min()),
            'max_temperature': float(df['Temperature'].max()),
        }
        
        # Save file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_name = f"{request.user.username}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(upload_dir, file_name)
        
        # Reset file pointer and save
        file.seek(0)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Create database record
        dataset = UploadedDataset.objects.create(
            user=request.user,
            file_path=file_path,
            summary_json=summary
        )
        
        # Maintain only last 5 uploads per user
        user_datasets = UploadedDataset.objects.filter(user=request.user)
        if user_datasets.count() > 5:
            old_datasets = user_datasets[5:]
            for old_dataset in old_datasets:
                # Delete old file
                if os.path.exists(old_dataset.file_path):
                    os.remove(old_dataset.file_path)
                old_dataset.delete()
        
        return Response({
            'id': dataset.id,
            'message': 'File uploaded successfully',
            'summary': summary
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id):
    """Get summary statistics for a specific dataset."""
    try:
        dataset = UploadedDataset.objects.get(id=dataset_id, user=request.user)
        
        # Read the CSV file
        df = pd.read_csv(dataset.file_path)
        
        # Return detailed data including the actual records
        return Response({
            'id': dataset.id,
            'uploaded_at': dataset.uploaded_at,
            'summary': dataset.summary_json,
            'data': df.to_dict(orient='records')
        }, status=status.HTTP_200_OK)
        
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error retrieving summary: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get history of last 5 uploaded datasets."""
    datasets = UploadedDataset.objects.filter(user=request.user)[:5]
    serializer = UploadedDatasetSerializer(datasets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, dataset_id):
    """Generate PDF report for a specific dataset."""
    try:
        dataset = UploadedDataset.objects.get(id=dataset_id, user=request.user)
        
        # Read the CSV file
        df = pd.read_csv(dataset.file_path)
        summary = dataset.summary_json
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("Chemical Equipment Parameter Report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Upload information
        upload_info = Paragraph(
            f"<b>Report Generated:</b> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            f"<b>Dataset ID:</b> {dataset.id}<br/>"
            f"<b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        )
        elements.append(upload_info)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Summary Statistics
        summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
        elements.append(summary_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment Count', str(summary['total_equipment'])],
            ['Average Flowrate', f"{summary['average_flowrate']:.2f}"],
            ['Average Pressure', f"{summary['average_pressure']:.2f}"],
            ['Average Temperature', f"{summary['average_temperature']:.2f}"],
            ['Min Flowrate', f"{summary['min_flowrate']:.2f}"],
            ['Max Flowrate', f"{summary['max_flowrate']:.2f}"],
            ['Min Pressure', f"{summary['min_pressure']:.2f}"],
            ['Max Pressure', f"{summary['max_pressure']:.2f}"],
            ['Min Temperature', f"{summary['min_temperature']:.2f}"],
            ['Max Temperature', f"{summary['max_temperature']:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Type Distribution
        type_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
        elements.append(type_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in summary['type_distribution'].items():
            type_data.append([str(eq_type), str(count)])
        
        type_table = Table(type_data, colWidths=[3 * inch, 2 * inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(type_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Return PDF as response
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset_id}.pdf"'
        
        return response
        
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating report: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

