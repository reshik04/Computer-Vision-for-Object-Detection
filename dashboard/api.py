"""
API endpoints for the Indian Airline Dashboard
Vercel-compatible serverless functions
"""

from flask import Flask, jsonify, request
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)

def load_airline_data():
    """Load airline data and summary"""
    try:
        # Load main data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'airline_data.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Load summary
        summary_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'data_summary.json')
        with open(summary_path, 'r') as f:
            summary = json.load(f)
        
        return data, summary
    except Exception as e:
        return [], {}

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all airline data"""
    data, summary = load_airline_data()
    return jsonify({
        'data': data,
        'summary': summary,
        'status': 'success'
    })

@app.route('/api/airlines', methods=['GET'])
def get_airlines():
    """Get list of airlines"""
    data, summary = load_airline_data()
    airlines = list(set(record['airline'] for record in data))
    return jsonify({
        'airlines': sorted(airlines),
        'status': 'success'
    })

@app.route('/api/performance/<airline>', methods=['GET'])
def get_airline_performance(airline):
    """Get performance data for specific airline"""
    data, summary = load_airline_data()
    airline_data = [record for record in data if record['airline'] == airline]
    
    if not airline_data:
        return jsonify({'error': 'Airline not found', 'status': 'error'}), 404
    
    return jsonify({
        'airline': airline,
        'data': airline_data,
        'status': 'success'
    })

@app.route('/api/chatbot', methods=['POST'])
def chatbot_query():
    """Handle chatbot queries"""
    try:
        query = request.json.get('query', '')
        
        # Simple rule-based responses
        response = process_chatbot_query(query)
        
        return jsonify({
            'query': query,
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

def process_chatbot_query(query):
    """Process chatbot query and return response"""
    data, summary = load_airline_data()
    q = query.lower()
    
    # Simple keyword-based responses
    if any(word in q for word in ['hi', 'hello', 'hey']):
        return "Hello! I can help you with Indian airline performance data. Ask me about specific airlines, performance metrics, or comparisons."
    
    elif 'indigo' in q:
        return "IndiGo is India's largest airline by market share, known for its punctuality and low-cost operations. It typically maintains good on-time performance."
    
    elif 'spicejet' in q:
        return "SpiceJet is a major budget airline in India with a significant domestic network. Performance varies seasonally."
    
    elif 'air india' in q:
        return "Air India is India's national flag carrier, operating both domestic and international routes. Performance has been improving in recent years."
    
    elif 'vistara' in q:
        return "Vistara is a premium full-service carrier, joint venture between Tata Group and Singapore Airlines. Known for high service quality."
    
    elif 'performance' in q or 'on-time' in q:
        overall_perf = summary.get('overall_on_time_percentage', 82)
        return f"The overall on-time performance across Indian airlines is approximately {overall_perf:.1f}%. Premium carriers typically perform better."
    
    elif 'cancel' in q:
        cancel_rate = summary.get('overall_cancellation_rate', 3)
        return f"The average cancellation rate across Indian airlines is approximately {cancel_rate:.1f}%. Weather and operational issues are common causes."
    
    elif 'delay' in q:
        return "Common delay reasons include ground handling issues, weather conditions, technical problems, and air traffic control delays."
    
    else:
        return "I can help with questions about airline performance, delays, cancellations, and specific airlines. Try asking about IndiGo, SpiceJet, Air India, or Vistara."

# For Vercel serverless deployment
def handler(event, context):
    """Serverless handler for Vercel"""
    return app(event, context)

if __name__ == '__main__':
    # For local development
    app.run(debug=True, port=5000)
