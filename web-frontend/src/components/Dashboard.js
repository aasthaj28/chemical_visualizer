import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import './Dashboard.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard({ onLogout }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await axios.get('/history/');
      setHistory(response.data);
    } catch (err) {
      console.error('Error loading history:', err);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('File uploaded successfully!');
      setFile(null);
      
      // Load the dataset details
      loadDataset(response.data.id);
      loadHistory();
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const loadDataset = async (datasetId) => {
    try {
      const response = await axios.get(`/summary/${datasetId}/`);
      setCurrentDataset(response.data);
    } catch (err) {
      setError('Error loading dataset details');
    }
  };

  const downloadReport = async (datasetId) => {
    try {
      const response = await axios.get(`/report/${datasetId}/`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Error downloading report');
    }
  };

  const getTypeDistributionChart = () => {
    if (!currentDataset?.summary?.type_distribution) return null;

    const types = Object.keys(currentDataset.summary.type_distribution);
    const counts = Object.values(currentDataset.summary.type_distribution);

    return {
      labels: types,
      datasets: [
        {
          label: 'Equipment Count',
          data: counts,
          backgroundColor: [
            'rgba(102, 126, 234, 0.8)',
            'rgba(118, 75, 162, 0.8)',
            'rgba(237, 100, 166, 0.8)',
            'rgba(255, 159, 64, 0.8)',
            'rgba(75, 192, 192, 0.8)',
          ],
          borderColor: [
            'rgba(102, 126, 234, 1)',
            'rgba(118, 75, 162, 1)',
            'rgba(237, 100, 166, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const getAveragesChart = () => {
    if (!currentDataset?.summary) return null;

    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average Values',
          data: [
            currentDataset.summary.average_flowrate,
            currentDataset.summary.average_pressure,
            currentDataset.summary.average_temperature,
          ],
          backgroundColor: 'rgba(102, 126, 234, 0.8)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
        },
      ],
    };
  };

  return (
    <div className="dashboard">
      <nav className="navbar">
        <div className="container">
          <h1>Chemical Equipment Visualizer</h1>
          <div className="nav-right">
            <span>Welcome, {user?.username}!</span>
            <button onClick={onLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        {/* Upload Section */}
        <div className="card">
          <h2>Upload CSV File</h2>
          <div className="upload-section">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="file-input"
            />
            <button
              onClick={handleUpload}
              className="btn btn-primary"
              disabled={uploading || !file}
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
          {error && <div className="error">{error}</div>}
          {success && <div className="success">{success}</div>}
        </div>

        {/* Current Dataset Summary */}
        {currentDataset && (
          <>
            <div className="card">
              <div className="summary-header">
                <h2>Dataset Summary</h2>
                <button
                  onClick={() => downloadReport(currentDataset.id)}
                  className="btn btn-primary"
                >
                  Download PDF Report
                </button>
              </div>
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Total Equipment</h3>
                  <p className="stat-value">{currentDataset.summary.total_equipment}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Flowrate</h3>
                  <p className="stat-value">{currentDataset.summary.average_flowrate.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Pressure</h3>
                  <p className="stat-value">{currentDataset.summary.average_pressure.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Temperature</h3>
                  <p className="stat-value">{currentDataset.summary.average_temperature.toFixed(2)}</p>
                </div>
              </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
              <div className="chart-container">
                <h3>Equipment Type Distribution</h3>
                {getTypeDistributionChart() && (
                  <Pie data={getTypeDistributionChart()} />
                )}
              </div>
              <div className="chart-container">
                <h3>Average Parameters</h3>
                {getAveragesChart() && (
                  <Bar 
                    data={getAveragesChart()}
                    options={{
                      responsive: true,
                      plugins: {
                        legend: {
                          position: 'top',
                        },
                      },
                    }}
                  />
                )}
              </div>
            </div>

            {/* Data Table */}
            <div className="card">
              <h2>Equipment Data</h2>
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>Equipment Name</th>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentDataset.data.map((row, index) => (
                      <tr key={index}>
                        <td>{row['Equipment Name']}</td>
                        <td>{row.Type}</td>
                        <td>{row.Flowrate}</td>
                        <td>{row.Pressure}</td>
                        <td>{row.Temperature}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}

        {/* History */}
        <div className="card">
          <h2>Upload History (Last 5)</h2>
          {history.length === 0 ? (
            <p>No upload history yet</p>
          ) : (
            <div className="history-list">
              {history.map((dataset) => (
                <div key={dataset.id} className="history-item">
                  <div className="history-info">
                    <strong>Dataset #{dataset.id}</strong>
                    <span>{new Date(dataset.uploaded_at).toLocaleString()}</span>
                  </div>
                  <div className="history-actions">
                    <button
                      onClick={() => loadDataset(dataset.id)}
                      className="btn btn-secondary"
                    >
                      View
                    </button>
                    <button
                      onClick={() => downloadReport(dataset.id)}
                      className="btn btn-primary"
                    >
                      Download Report
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

