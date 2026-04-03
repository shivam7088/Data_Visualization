import React, { useState } from 'react';

const AnalyticsDashboard = () => {
    const [report, setReport] = useState({ image: null, total_records: 0 });
    const [loading, setLoading] = useState(false);
    const [params, setParams] = useState({ table: 'complaints', xAxis: 'status', hue: 'priority' });

    const fetchReport = async () => {
        setLoading(true);
        try {
            const response = await fetch(
                `http://localhost:8080/api/reports/generate?table=${params.table}&xAxis=${params.xAxis}&hue=${params.hue}`
            );
            const data = await response.json();
            setReport(data);
        } catch (error) {
            console.error("Error fetching report:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial' }}>
            <h2>📊 Customer Service Analytics</h2>
            
            <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <select onChange={(e) => setParams({...params, table: e.target.value})}>
                    <option value="complaints">Complaints</option>
                    <option value="requests">Requests</option>
                </select>

                <select onChange={(e) => setParams({...params, xAxis: e.target.value})}>
                    <option value="status">By Status</option>
                    <option value="priority">By Priority</option>
                    <option value="category">By Category</option>
                </select>

                <button onClick={fetchReport} disabled={loading} style={{ background: '#4CAF50', color: 'white', border: 'none', padding: '5px 15px', cursor: 'pointer' }}>
                    {loading ? 'Generating...' : 'Generate Chart'}
                </button>
            </div>

            {report.image && (
                <div style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px', borderRadius: '8px', background: '#f9f9f9' }}>
                    <p><strong>Total Records Found:</strong> {report.total_records}</p>
                    <img 
                        src={`data:image/png;base64,${report.image}`} 
                        alt="Visualization" 
                        style={{ maxWidth: '100%', borderRadius: '4px' }} 
                    />
                </div>
            )}
        </div>
    );
};

export default AnalyticsDashboard;
