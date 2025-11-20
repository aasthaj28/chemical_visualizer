"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5 GUI with Matplotlib visualization
"""
import sys
import os
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QTabWidget, QListWidget,
    QStackedWidget, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


API_BASE_URL = 'http://localhost:8000/api'


class LoginWindow(QWidget):
    """Login window for user authentication."""
    
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #667eea; margin: 20px;')
        layout.addWidget(title)
        
        # Login form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        form_layout.addRow('Username:', self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.returnPressed.connect(self.login)
        form_layout.addRow('Password:', self.password_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        btn_layout.addWidget(login_btn)
        
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.show_register)
        register_btn.setStyleSheet('''
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        ''')
        btn_layout.addWidget(register_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.main_app.set_token(data['access'])
                self.main_app.set_user(data['user'])
                self.main_app.show_dashboard()
                self.close()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Login failed: {str(e)}')
    
    def show_register(self):
        self.main_app.show_register()
        self.close()


class RegisterWindow(QWidget):
    """Registration window for new users."""
    
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Register')
        self.setGeometry(100, 100, 400, 350)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Register New Account')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #667eea; margin: 20px;')
        layout.addWidget(title)
        
        # Registration form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        form_layout.addRow('Username:', self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter email')
        form_layout.addRow('Email:', self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter password')
        form_layout.addRow('Password:', self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText('Confirm password')
        self.confirm_password_input.returnPressed.connect(self.register)
        form_layout.addRow('Confirm Password:', self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        btn_layout.addWidget(register_btn)
        
        back_btn = QPushButton('Back to Login')
        back_btn.clicked.connect(self.back_to_login)
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        ''')
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/register/',
                json={'username': username, 'email': email, 'password': password}
            )
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
                self.back_to_login()
            else:
                error_msg = response.json().get('username', ['Registration failed'])[0]
                QMessageBox.warning(self, 'Error', error_msg)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Registration failed: {str(e)}')
    
    def back_to_login(self):
        self.main_app.show_login()
        self.close()


class DashboardWindow(QMainWindow):
    """Main dashboard window for data visualization."""
    
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.current_dataset = None
        self.history = []
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Dashboard')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        title = QLabel('Chemical Equipment Parameter Visualizer')
        title.setStyleSheet('font-size: 24px; font-weight: bold; color: #667eea;')
        header.addWidget(title)
        
        header.addStretch()
        
        user_label = QLabel(f"Welcome, {self.main_app.user.get('username', 'User')}!")
        user_label.setStyleSheet('font-size: 14px; margin-right: 10px;')
        header.addWidget(user_label)
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet('''
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        ''')
        header.addWidget(logout_btn)
        
        layout.addLayout(header)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV File')
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        upload_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_file)
        upload_layout.addWidget(browse_btn)
        
        upload_btn = QPushButton('Upload')
        upload_btn.clicked.connect(self.upload_file)
        upload_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        ''')
        upload_layout.addWidget(upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_tab = QWidget()
        self.init_summary_tab()
        self.tabs.addTab(self.summary_tab, 'Summary')
        
        # Data tab
        self.data_tab = QWidget()
        self.init_data_tab()
        self.tabs.addTab(self.data_tab, 'Data Table')
        
        # Charts tab
        self.charts_tab = QWidget()
        self.init_charts_tab()
        self.tabs.addTab(self.charts_tab, 'Charts')
        
        # History tab
        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, 'History')
        
        layout.addWidget(self.tabs)
        
        central_widget.setLayout(layout)
    
    def init_summary_tab(self):
        layout = QVBoxLayout()
        
        self.summary_label = QLabel('Upload a CSV file to see summary statistics')
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setStyleSheet('font-size: 16px; padding: 20px;')
        layout.addWidget(self.summary_label)
        
        self.download_report_btn = QPushButton('Download PDF Report')
        self.download_report_btn.clicked.connect(self.download_report)
        self.download_report_btn.setEnabled(False)
        self.download_report_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        layout.addWidget(self.download_report_btn)
        
        layout.addStretch()
        self.summary_tab.setLayout(layout)
    
    def init_data_tab(self):
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        layout.addWidget(self.data_table)
        
        self.data_tab.setLayout(layout)
    
    def init_charts_tab(self):
        layout = QVBoxLayout()
        
        # Type distribution chart
        self.type_chart = MatplotlibCanvas(self, width=10, height=4)
        layout.addWidget(self.type_chart)
        
        # Averages chart
        self.avg_chart = MatplotlibCanvas(self, width=10, height=4)
        layout.addWidget(self.avg_chart)
        
        self.charts_tab.setLayout(layout)
    
    def init_history_tab(self):
        layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.load_dataset_from_history)
        layout.addWidget(self.history_list)
        
        self.history_tab.setLayout(layout)
    
    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        if file_name:
            self.selected_file = file_name
            self.file_label.setText(os.path.basename(file_name))
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, 'Error', 'Please select a file first')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Bearer {self.main_app.token}'}
                
                response = requests.post(
                    f'{API_BASE_URL}/upload/',
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 201:
                    data = response.json()
                    QMessageBox.information(self, 'Success', 'File uploaded successfully!')
                    self.load_dataset(data['id'])
                    self.load_history()
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    QMessageBox.warning(self, 'Error', error_msg)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def load_dataset(self, dataset_id):
        try:
            headers = {'Authorization': f'Bearer {self.main_app.token}'}
            response = requests.get(
                f'{API_BASE_URL}/summary/{dataset_id}/',
                headers=headers
            )
            
            if response.status_code == 200:
                self.current_dataset = response.json()
                self.update_display()
                self.download_report_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Error', 'Failed to load dataset')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def update_display(self):
        if not self.current_dataset:
            return
        
        summary = self.current_dataset['summary']
        data = self.current_dataset['data']
        
        # Update summary
        summary_text = f"""
        <h2>Dataset Summary</h2>
        <p><b>Total Equipment:</b> {summary['total_equipment']}</p>
        <p><b>Average Flowrate:</b> {summary['average_flowrate']:.2f}</p>
        <p><b>Average Pressure:</b> {summary['average_pressure']:.2f}</p>
        <p><b>Average Temperature:</b> {summary['average_temperature']:.2f}</p>
        <br>
        <h3>Range Values:</h3>
        <p><b>Flowrate:</b> {summary['min_flowrate']:.2f} - {summary['max_flowrate']:.2f}</p>
        <p><b>Pressure:</b> {summary['min_pressure']:.2f} - {summary['max_pressure']:.2f}</p>
        <p><b>Temperature:</b> {summary['min_temperature']:.2f} - {summary['max_temperature']:.2f}</p>
        """
        self.summary_label.setText(summary_text)
        self.summary_label.setTextFormat(Qt.RichText)
        self.summary_label.setAlignment(Qt.AlignLeft)
        
        # Update data table
        self.data_table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(row['Equipment Name'])))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(row['Type'])))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(row['Flowrate'])))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(row['Pressure'])))
            self.data_table.setItem(i, 4, QTableWidgetItem(str(row['Temperature'])))
        
        # Update charts
        self.update_charts()
    
    def update_charts(self):
        if not self.current_dataset:
            return
        
        summary = self.current_dataset['summary']
        
        # Type distribution pie chart
        self.type_chart.figure.clear()
        ax1 = self.type_chart.figure.add_subplot(111)
        
        types = list(summary['type_distribution'].keys())
        counts = list(summary['type_distribution'].values())
        
        ax1.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Equipment Type Distribution')
        self.type_chart.draw()
        
        # Averages bar chart
        self.avg_chart.figure.clear()
        ax2 = self.avg_chart.figure.add_subplot(111)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        averages = [
            summary['average_flowrate'],
            summary['average_pressure'],
            summary['average_temperature']
        ]
        
        ax2.bar(parameters, averages, color='#667eea')
        ax2.set_title('Average Parameter Values')
        ax2.set_ylabel('Value')
        self.avg_chart.draw()
    
    def load_history(self):
        try:
            headers = {'Authorization': f'Bearer {self.main_app.token}'}
            response = requests.get(f'{API_BASE_URL}/history/', headers=headers)
            
            if response.status_code == 200:
                self.history = response.json()
                self.history_list.clear()
                
                for dataset in self.history:
                    item_text = f"Dataset #{dataset['id']} - {dataset['uploaded_at']}"
                    self.history_list.addItem(item_text)
        except Exception as e:
            print(f'Failed to load history: {str(e)}')
    
    def load_dataset_from_history(self, item):
        # Extract dataset ID from item text
        text = item.text()
        dataset_id = int(text.split('#')[1].split(' ')[0])
        self.load_dataset(dataset_id)
    
    def download_report(self):
        if not self.current_dataset:
            return
        
        dataset_id = self.current_dataset['id']
        
        try:
            headers = {'Authorization': f'Bearer {self.main_app.token}'}
            response = requests.get(
                f'{API_BASE_URL}/report/{dataset_id}/',
                headers=headers
            )
            
            if response.status_code == 200:
                file_name, _ = QFileDialog.getSaveFileName(
                    self, 'Save Report', f'report_{dataset_id}.pdf', 'PDF Files (*.pdf)'
                )
                
                if file_name:
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'Report downloaded successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to download report')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Download failed: {str(e)}')
    
    def logout(self):
        self.main_app.logout()
        self.close()


class MatplotlibCanvas(FigureCanvas):
    """Canvas for embedding matplotlib charts."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)
        self.setParent(parent)


class ChemicalVisualizerApp:
    """Main application controller."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.token = None
        self.user = None
        self.login_window = None
        self.register_window = None
        self.dashboard_window = None
    
    def set_token(self, token):
        self.token = token
    
    def set_user(self, user):
        self.user = user
    
    def show_login(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
    
    def show_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
    
    def show_dashboard(self):
        self.dashboard_window = DashboardWindow(self)
        self.dashboard_window.show()
    
    def logout(self):
        self.token = None
        self.user = None
        self.show_login()
    
    def run(self):
        self.show_login()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = ChemicalVisualizerApp()
    app.run()

