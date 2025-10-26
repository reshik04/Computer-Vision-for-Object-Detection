"""
Main Dash application for Indian Airline Dashboard
"""

import json
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import from data/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# For deployment without external libraries, we'll create a simple HTML dashboard
class SimpleDashboard:
    """
    Simple HTML-based dashboard for airline data visualization
    """
    
    def __init__(self):
        self.data = []
        self.summary = {}
        self.load_data()
    
    def load_data(self):
        """Load data from the processed JSON file"""
        try:
            # Load main data
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'airline_data.json')
            with open(data_path, 'r') as f:
                self.data = json.load(f)
            
            # Load summary
            summary_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'data_summary.json')
            with open(summary_path, 'r') as f:
                self.summary = json.load(f)
                
            print(f"✅ Loaded {len(self.data)} records and summary data")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.data = []
            self.summary = {}
    
    def generate_kpi_cards_html(self):
        """Generate HTML for KPI cards"""
        total_flights = self.summary.get('total_flights', 0)
        on_time_perf = self.summary.get('overall_on_time_percentage', 0)
        cancel_rate = self.summary.get('overall_cancellation_rate', 0)
        airlines_count = self.summary.get('airlines_count', 0)
        
        return f'''
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">📊 Total Flights</div>
                <div class="kpi-value">{total_flights:,}</div>
                <div class="kpi-subtitle">Across all airlines</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-title">⏰ On-Time Performance</div>
                <div class="kpi-value">{on_time_perf:.1f}%</div>
                <div class="kpi-subtitle">Industry average</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-title">❌ Cancellation Rate</div>
                <div class="kpi-value">{cancel_rate:.2f}%</div>
                <div class="kpi-subtitle">Industry average</div>
            </div>
            
            <div class="kpi-card">
                <div class="kpi-title">✈️ Airlines Tracked</div>
                <div class="kpi-value">{airlines_count}</div>
                <div class="kpi-subtitle">Major Indian carriers</div>
            </div>
        </div>
        '''
    
    def generate_airline_table_html(self):
        """Generate HTML table for airline performance"""
        airline_stats = self.summary.get('airline_stats', {})
        if not airline_stats:
            return '<p>No airline data available</p>'
        
        # Sort airlines by on-time performance
        sorted_airlines = sorted(airline_stats.items(), 
                               key=lambda x: x[1]['avg_on_time_percentage'], 
                               reverse=True)
        
        table_rows = []
        for i, (airline, stats) in enumerate(sorted_airlines, 1):
            # Determine rank badge color
            if i == 1:
                rank_class = "badge bg-success"
            elif i <= 3:
                rank_class = "badge bg-primary" 
            else:
                rank_class = "badge bg-secondary"
            
            table_rows.append(f'''
            <tr>
                <td><span class="{rank_class}">#{i}</span></td>
                <td><strong>{airline}</strong></td>
                <td>{stats['avg_on_time_percentage']:.2f}%</td>
                <td>{stats['avg_cancellation_rate']:.2f}%</td>
                <td>{stats['total_records']} months</td>
            </tr>
            ''')
        
        return f'''
        <div class="chart-container">
            <h3>📈 Airline Performance Rankings</h3>
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Rank</th>
                            <th>Airline</th>
                            <th>On-Time %</th>
                            <th>Cancellation %</th>
                            <th>Data Points</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        '''
    
    def generate_delay_reasons_html(self):
        """Generate HTML for delay reasons chart"""
        delay_reasons = self.summary.get('delay_reasons', {})
        if not delay_reasons:
            return '<p>No delay reason data available</p>'
        
        total_reasons = sum(delay_reasons.values())
        sorted_reasons = sorted(delay_reasons.items(), key=lambda x: x[1], reverse=True)
        
        bars_html = []
        colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1', '#e83e8c']
        
        for i, (reason, count) in enumerate(sorted_reasons):
            percentage = (count / total_reasons * 100) if total_reasons > 0 else 0
            color = colors[i % len(colors)]
            
            bars_html.append(f'''
            <div class="mb-3">
                <div class="d-flex justify-content-between">
                    <span><strong>{reason}</strong></span>
                    <span>{count} ({percentage:.1f}%)</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: {percentage}%; background-color: {color}"></div>
                </div>
            </div>
            ''')
        
        return f'''
        <div class="chart-container">
            <h3>⚠️ Delay Reasons Distribution</h3>
            <div class="mt-3">
                {''.join(bars_html)}
            </div>
        </div>
        '''
    
    def generate_time_trend_html(self):
        """Generate HTML for time trend analysis"""
        # Group data by year and calculate averages
        yearly_stats = {}
        for record in self.data:
            year = record['year']
            if year not in yearly_stats:
                yearly_stats[year] = {'flights': 0, 'on_time': 0, 'cancelled': 0, 'count': 0}
            
            yearly_stats[year]['flights'] += record['total_flights']
            yearly_stats[year]['on_time'] += record['on_time_flights']
            yearly_stats[year]['cancelled'] += record['cancelled_flights']
            yearly_stats[year]['count'] += 1
        
        trend_rows = []
        for year in sorted(yearly_stats.keys()):
            stats = yearly_stats[year]
            total_flights = stats['flights']
            total_on_time = stats['on_time']
            total_cancelled = stats['cancelled']
            
            on_time_pct = (total_on_time / (total_flights - total_cancelled) * 100) if (total_flights - total_cancelled) > 0 else 0
            cancel_pct = (total_cancelled / total_flights * 100) if total_flights > 0 else 0
            
            # Color coding for performance
            if on_time_pct >= 85:
                perf_class = "text-success"
            elif on_time_pct >= 75:
                perf_class = "text-warning"
            else:
                perf_class = "text-danger"
            
            trend_rows.append(f'''
            <tr>
                <td><strong>{year}</strong></td>
                <td>{total_flights:,}</td>
                <td class="{perf_class}">{on_time_pct:.1f}%</td>
                <td>{cancel_pct:.2f}%</td>
                <td>{stats['count']} airlines</td>
            </tr>
            ''')
        
        return f'''
        <div class="chart-container">
            <h3>📅 Yearly Performance Trends</h3>
            <div class="table-responsive">
                <table class="table">
                    <thead class="table-light">
                        <tr>
                            <th>Year</th>
                            <th>Total Flights</th>
                            <th>On-Time %</th>
                            <th>Cancellation %</th>
                            <th>Airlines</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(trend_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        '''
    
    def generate_chatbot_html(self):
        """Generate HTML for chatbot interface"""
        sample_questions = [
            "What is the on-time performance of IndiGo?",
            "Which airline has the highest cancellation rate?",
            "What are the most common delay reasons?",
            "Show me performance trends for Air India",
            "Compare SpiceJet and Vistara performance"
        ]
        
        questions_html = ''.join([
            f'<button class="btn btn-outline-primary btn-sm m-1" onclick="askQuestion(\'{q}\')">{q}</button>'
            for q in sample_questions
        ])
        
        return f'''
        <div class="chart-container">
            <h3>💬 Airline Data Chatbot</h3>
            <div class="chatbot-container">
                <div id="chat-messages" class="chat-messages">
                    <div class="message bot-message">
                        <strong>AI Assistant:</strong> Hello! I can help you with Indian airline performance data. Click on a sample question below or type your own.
                    </div>
                </div>
                
                <div class="mb-3">
                    <h6>Sample Questions:</h6>
                    {questions_html}
                </div>
                
                <div class="chat-input-container">
                    <input type="text" id="chat-input" class="chat-input form-control" placeholder="Ask about airline performance..." onkeypress="handleEnter(event)">
                    <button class="chat-button btn btn-primary" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
        
        <script>
        function askQuestion(question) {{
            document.getElementById('chat-input').value = question;
            sendMessage();
        }}
        
        function handleEnter(event) {{
            if (event.key === 'Enter') {{
                sendMessage();
            }}
        }}
        
        function sendMessage() {{
            const input = document.getElementById('chat-input');
            const messages = document.getElementById('chat-messages');
            const query = input.value.trim();
            
            if (!query) return;
            
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'message user-message';
            userMsg.innerHTML = '<strong>You:</strong> ' + query;
            messages.appendChild(userMsg);
            
            // Add bot response
            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            botMsg.innerHTML = '<strong>AI Assistant:</strong> ' + getResponse(query);
            messages.appendChild(botMsg);
            
            // Clear input and scroll to bottom
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }}
        
        function getResponse(query) {{
            const q = query.toLowerCase();
            
            // Simple rule-based responses
            if (q.includes('indigo')) {{
                return 'IndiGo is one of the top-performing airlines with an average on-time performance of around 84-86%. It has relatively low cancellation rates compared to industry average.';
            }}
            else if (q.includes('spicejet')) {{
                return 'SpiceJet has an average on-time performance of around 82-84%. It operates a significant number of domestic flights across India.';
            }}
            else if (q.includes('air india')) {{
                return 'Air India has an average on-time performance of around 81-83%. As the national carrier, it operates both domestic and international routes.';
            }}
            else if (q.includes('vistara')) {{
                return 'Vistara consistently ranks among the top performers with excellent on-time performance of around 84-85% and premium service quality.';
            }}
            else if (q.includes('cancel')) {{
                return 'The overall cancellation rate across Indian airlines is approximately {self.summary.get("overall_cancellation_rate", 3.0):.1f}%. Weather and operational issues are common causes.';
            }}
            else if (q.includes('delay')) {{
                return 'Common delay reasons include ground handling issues, operational delays, technical problems, and weather conditions. Ground handling is typically the most frequent cause.';
            }}
            else if (q.includes('performance') || q.includes('on-time')) {{
                return 'The overall on-time performance across Indian airlines is approximately {self.summary.get("overall_on_time_percentage", 82.0):.1f}%. Premium carriers like Vistara typically perform better than budget airlines.';
            }}
            else if (q.includes('compare')) {{
                return 'Among major airlines, Vistara and IndiGo typically have the best on-time performance, while budget carriers may have slightly higher delay rates but remain competitive overall.';
            }}
            else if (q.includes('trend')) {{
                return 'Airline performance varies by season, with monsoon months typically showing higher delay rates. The industry has generally improved post-pandemic recovery.';
            }}
            else {{
                return 'I can help with questions about airline performance, delays, cancellations, and comparisons. Try asking about specific airlines like IndiGo, SpiceJet, Air India, or Vistara.';
            }}
        }}
        </script>
        '''
    
    def generate_dashboard_html(self):
        """Generate complete dashboard HTML"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Indian Airline Data Dashboard</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background-color: #f8f9fa;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }}
                
                .dashboard-header {{
                    background: linear-gradient(135deg, #007bff, #0056b3);
                    color: white;
                    padding: 2rem 0;
                    margin-bottom: 2rem;
                }}
                
                .kpi-container {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}
                
                .kpi-card {{
                    background: white;
                    border-radius: 12px;
                    padding: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    border-left: 4px solid #007bff;
                    transition: transform 0.2s;
                }}
                
                .kpi-card:hover {{
                    transform: translateY(-2px);
                }}
                
                .kpi-value {{
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #007bff;
                    margin: 0.5rem 0;
                }}
                
                .kpi-title {{
                    font-size: 1rem;
                    color: #666;
                    margin-bottom: 0.5rem;
                }}
                
                .kpi-subtitle {{
                    font-size: 0.875rem;
                    color: #999;
                }}
                
                .chart-container {{
                    background: white;
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                
                .chatbot-container {{
                    max-height: 600px;
                    display: flex;
                    flex-direction: column;
                }}
                
                .chat-messages {{
                    flex: 1;
                    overflow-y: auto;
                    max-height: 400px;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                }}
                
                .message {{
                    margin-bottom: 1rem;
                    padding: 0.75rem;
                    border-radius: 8px;
                }}
                
                .user-message {{
                    background-color: #e3f2fd;
                    margin-left: 2rem;
                }}
                
                .bot-message {{
                    background-color: #f5f5f5;
                    margin-right: 2rem;
                }}
                
                .chat-input-container {{
                    display: flex;
                    gap: 0.5rem;
                }}
                
                .footer {{
                    background-color: #343a40;
                    color: white;
                    padding: 2rem 0;
                    margin-top: 3rem;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <!-- Header -->
            <div class="dashboard-header">
                <div class="container">
                    <h1 class="display-4">✈️ Indian Airline Data Dashboard</h1>
                    <p class="lead">Interactive analysis of airline performance across India</p>
                    <small>Last updated: {current_time}</small>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="container">
                <!-- Navigation Tabs -->
                <ul class="nav nav-tabs mb-4" id="dashboardTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button" role="tab">
                            📊 Overview Dashboard
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="chatbot-tab" data-bs-toggle="tab" data-bs-target="#chatbot" type="button" role="tab">
                            💬 AI Assistant
                        </button>
                    </li>
                </ul>
                
                <!-- Tab Content -->
                <div class="tab-content" id="dashboardTabsContent">
                    <!-- Overview Tab -->
                    <div class="tab-pane fade show active" id="overview" role="tabpanel">
                        <!-- KPI Cards -->
                        {self.generate_kpi_cards_html()}
                        
                        <!-- Charts and Tables -->
                        <div class="row">
                            <div class="col-lg-12">
                                {self.generate_airline_table_html()}
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-lg-6">
                                {self.generate_delay_reasons_html()}
                            </div>
                            <div class="col-lg-6">
                                {self.generate_time_trend_html()}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Chatbot Tab -->
                    <div class="tab-pane fade" id="chatbot" role="tabpanel">
                        {self.generate_chatbot_html()}
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <div class="container">
                    <p>&copy; 2024 Indian Airline Dashboard | Built with HTML, CSS, and JavaScript</p>
                    <p>Data covers {self.summary.get("total_records", 0)} records from {self.summary.get("airlines_count", 0)} airlines</p>
                </div>
            </div>
            
            <!-- Bootstrap JS -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        '''
        
        return html_content
    
    def save_dashboard(self, filename="index.html"):
        """Save dashboard as HTML file"""
        html_content = self.generate_dashboard_html()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard saved as {filename}")
        return filename


def create_dashboard():
    """Main function to create and save the dashboard"""
    dashboard = SimpleDashboard()
    dashboard_file = dashboard.save_dashboard()
    return dashboard_file


if __name__ == "__main__":
    print("🚀 Creating Indian Airline Dashboard...")
    dashboard_file = create_dashboard()
    print(f"🌐 Open {dashboard_file} in your browser to view the dashboard")
