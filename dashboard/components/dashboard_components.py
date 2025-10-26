"""
Dashboard components for Indian Airline Dashboard
Reusable components for KPIs, charts, and UI elements
"""

def create_kpi_card(title, value, subtitle="", icon="📊", color="primary"):
    """
    Create a KPI card component
    
    Args:
        title: Card title
        value: Main metric value
        subtitle: Additional information
        icon: Icon for the card
        color: Bootstrap color class
    """
    return {
        'title': title,
        'value': value,
        'subtitle': subtitle,
        'icon': icon,
        'color': color,
        'html': f'''
        <div class="card border-{color} mb-3" style="max-width: 18rem;">
            <div class="card-header bg-{color} text-white">
                <i class="fas fa-chart-line"></i> {icon} {title}
            </div>
            <div class="card-body">
                <h2 class="card-title text-{color}">{value}</h2>
                <p class="card-text text-muted">{subtitle}</p>
            </div>
        </div>
        '''
    }


def create_time_series_chart_config(data, airlines):
    """
    Create configuration for time series chart
    """
    return {
        'data': [],  # Will be populated dynamically
        'layout': {
            'title': 'On-Time Performance Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'On-Time Percentage (%)'},
            'hovermode': 'x unified',
            'template': 'plotly_white'
        },
        'config': {
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
        }
    }


def create_comparison_chart_config():
    """
    Create configuration for airline comparison chart
    """
    return {
        'layout': {
            'title': 'Airline Performance Comparison',
            'xaxis': {'title': 'Airlines'},
            'yaxis': {'title': 'Percentage (%)'},
            'barmode': 'group',
            'template': 'plotly_white'
        },
        'config': {
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
        }
    }


def create_pie_chart_config():
    """
    Create configuration for delay reasons pie chart
    """
    return {
        'layout': {
            'title': 'Distribution of Delay Reasons',
            'template': 'plotly_white'
        },
        'config': {
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
        }
    }


def create_chatbot_interface():
    """
    Create chatbot interface structure
    """
    return {
        'sample_questions': [
            "What is the on-time performance of IndiGo?",
            "Which airline has the highest cancellation rate?",
            "What are the most common delay reasons?",
            "Show me performance trends for 2023",
            "Compare SpiceJet and Air India performance"
        ],
        'responses': {
            'greeting': "Hello! I can help you with Indian airline performance data. Ask me about on-time performance, cancellations, or specific airlines.",
            'help': "I can answer questions about airline performance, delays, cancellations, and comparisons. Try asking about specific airlines or metrics.",
            'unknown': "I'm not sure about that. Try asking about airline performance, delays, or cancellations."
        }
    }


class ChatbotResponder:
    """
    Simple rule-based chatbot for airline data queries
    """
    
    def __init__(self, data, summary):
        self.data = data
        self.summary = summary
        self.airlines = ['IndiGo', 'SpiceJet', 'Air India', 'GoAir', 'Vistara', 
                        'AirAsia India', 'Alliance Air', 'Akasa Air']
    
    def process_query(self, query):
        """
        Process user query and return appropriate response
        """
        query_lower = query.lower()
        
        # Greeting responses
        if any(word in query_lower for word in ['hi', 'hello', 'hey', 'help']):
            return self.get_greeting_response()
        
        # On-time performance queries
        if 'on-time' in query_lower or 'ontime' in query_lower or 'performance' in query_lower:
            return self.get_performance_response(query_lower)
        
        # Cancellation queries
        if 'cancel' in query_lower or 'cancelled' in query_lower:
            return self.get_cancellation_response(query_lower)
        
        # Delay queries
        if 'delay' in query_lower or 'delayed' in query_lower:
            return self.get_delay_response(query_lower)
        
        # Comparison queries
        if 'compare' in query_lower or 'comparison' in query_lower:
            return self.get_comparison_response(query_lower)
        
        # Specific airline queries
        for airline in self.airlines:
            if airline.lower() in query_lower:
                return self.get_airline_specific_response(airline)
        
        # Default response
        return {
            'type': 'text',
            'message': "I'm not sure about that. Try asking about airline performance, delays, cancellations, or specific airlines like IndiGo, SpiceJet, or Air India."
        }
    
    def get_greeting_response(self):
        return {
            'type': 'text',
            'message': "Hello! I'm here to help you with Indian airline performance data. I can tell you about:\n\n• On-time performance of airlines\n• Cancellation rates\n• Delay reasons\n• Airline comparisons\n\nWhat would you like to know?"
        }
    
    def get_performance_response(self, query):
        overall_performance = self.summary.get('overall_on_time_percentage', 0)
        
        # Check for specific airline
        for airline in self.airlines:
            if airline.lower() in query:
                airline_stats = self.summary.get('airline_stats', {}).get(airline, {})
                if airline_stats:
                    return {
                        'type': 'text',
                        'message': f"{airline} has an average on-time performance of {airline_stats['avg_on_time_percentage']}%. The industry average is {overall_performance}%."
                    }
        
        # General performance
        return {
            'type': 'text',
            'message': f"The overall on-time performance across all Indian airlines is {overall_performance}%. Would you like to know about a specific airline?"
        }
    
    def get_cancellation_response(self, query):
        overall_cancellation = self.summary.get('overall_cancellation_rate', 0)
        
        # Check for specific airline
        for airline in self.airlines:
            if airline.lower() in query:
                airline_stats = self.summary.get('airline_stats', {}).get(airline, {})
                if airline_stats:
                    return {
                        'type': 'text',
                        'message': f"{airline} has an average cancellation rate of {airline_stats['avg_cancellation_rate']}%. The industry average is {overall_cancellation}%."
                    }
        
        # General cancellation info
        return {
            'type': 'text',
            'message': f"The overall cancellation rate across all Indian airlines is {overall_cancellation}%. Would you like to know about a specific airline?"
        }
    
    def get_delay_response(self, query):
        delay_reasons = self.summary.get('delay_reasons', {})
        top_reason = max(delay_reasons.items(), key=lambda x: x[1]) if delay_reasons else ("Unknown", 0)
        
        return {
            'type': 'text',
            'message': f"The most common delay reason is '{top_reason[0]}' with {top_reason[1]} occurrences. Other common reasons include technical issues, weather, and operational delays."
        }
    
    def get_comparison_response(self, query):
        airline_stats = self.summary.get('airline_stats', {})
        if not airline_stats:
            return {'type': 'text', 'message': "No comparison data available."}
        
        # Get top and worst performers
        sorted_airlines = sorted(airline_stats.items(), 
                               key=lambda x: x[1]['avg_on_time_percentage'], 
                               reverse=True)
        
        if len(sorted_airlines) >= 2:
            best = sorted_airlines[0]
            worst = sorted_airlines[-1]
            
            return {
                'type': 'text',
                'message': f"Performance Comparison:\n\n🏆 Best: {best[0]} with {best[1]['avg_on_time_percentage']}% on-time\n📉 Lowest: {worst[0]} with {worst[1]['avg_on_time_percentage']}% on-time\n\nWould you like details about any specific airline?"
            }
        
        return {'type': 'text', 'message': "Not enough data for comparison."}
    
    def get_airline_specific_response(self, airline):
        airline_stats = self.summary.get('airline_stats', {}).get(airline, {})
        if not airline_stats:
            return {
                'type': 'text',
                'message': f"Sorry, I don't have performance data for {airline}."
            }
        
        return {
            'type': 'text',
            'message': f"{airline} Performance Summary:\n\n• On-time Performance: {airline_stats['avg_on_time_percentage']}%\n• Cancellation Rate: {airline_stats['avg_cancellation_rate']}%\n• Data Points: {airline_stats['total_records']} months\n\nWould you like to compare with other airlines?"
        }


# CSS styles for the dashboard
DASHBOARD_STYLES = {
    'main': """
    .main-container {
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .kpi-card {
        flex: 1;
        min-width: 250px;
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #007bff;
    }
    
    .kpi-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #007bff;
        margin: 10px 0;
    }
    
    .kpi-title {
        font-size: 1.1em;
        color: #666;
        margin-bottom: 5px;
    }
    
    .kpi-subtitle {
        font-size: 0.9em;
        color: #999;
    }
    
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .chatbot-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        max-height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        max-height: 400px;
    }
    
    .chat-input-container {
        display: flex;
        gap: 10px;
    }
    
    .chat-input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .chat-button {
        padding: 10px 20px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .message {
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 4px;
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: 20px;
    }
    
    .bot-message {
        background: #f5f5f5;
        margin-right: 20px;
    }
    """,
    
    'bootstrap_cdn': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'
}
