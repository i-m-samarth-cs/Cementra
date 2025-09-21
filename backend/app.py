from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json
import random
from datetime import datetime, timedelta
import os
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Mock data storage (In production, use proper database)
class PlantDataStore:
    def __init__(self):
        self.workers = self.generate_mock_workers()
        self.safety_violations = []
        self.production_metrics = {
            'production_rate': 2450,
            'efficiency': 87.3,
            'temperature': 1480,
            'energy_consumption': 85.2,
            'co2_emissions': -12
        }
        self.schedules = self.generate_mock_schedules()
    
    def generate_mock_workers(self) -> List[Dict]:
        """Generate mock worker data"""
        workers = []
        statuses = ['Safe', 'PPE Missing', 'Training Required', 'Off Duty']
        zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D']
        
        for i in range(1, 51):  # 50 workers
            worker = {
                'id': f'W{1000 + i}',
                'name': f'Worker {i}',
                'age': random.randint(22, 60),  # Ensures no underage workers
                'zone': random.choice(zones),
                'status': random.choice(statuses),
                'ppe_compliance': random.choice([True, False]),
                'certification_valid': True,
                'last_safety_training': datetime.now() - timedelta(days=random.randint(1, 90))
            }
            workers.append(worker)
        return workers
    
    def generate_mock_schedules(self) -> List[Dict]:
        """Generate mock shift schedules"""
        return [
            {
                'shift_id': 'A001',
                'shift_name': 'Morning Shift',
                'start_time': '06:00',
                'end_time': '14:00',
                'workers_assigned': 25,
                'supervisor': 'John Supervisor',
                'tasks': ['Production', 'Quality Control', 'Maintenance']
            },
            {
                'shift_id': 'B001',
                'shift_name': 'Afternoon Shift',
                'start_time': '14:00',
                'end_time': '22:00',
                'workers_assigned': 22,
                'supervisor': 'Mary Manager',
                'tasks': ['Production', 'Equipment Check', 'Safety Audit']
            },
            {
                'shift_id': 'C001',
                'shift_name': 'Night Shift',
                'start_time': '22:00',
                'end_time': '06:00',
                'workers_assigned': 15,
                'supervisor': 'Bob Controller',
                'tasks': ['Maintenance', 'Deep Cleaning', 'System Check']
            }
        ]

# Global data store
plant_data = PlantDataStore()

@app.route('/')
def index():
    """Serve the main dashboard"""
    try:
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Frontend not found. Please ensure index.html exists in frontend folder'}), 404

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'ai_engine': 'online',
            'safety_monitor': 'online',
            'database': 'online'
        }
    })

@app.route('/api/operations/metrics', methods=['GET'])
def get_operations_metrics():
    """Get current plant operational metrics"""
    # Simulate real-time data with slight variations
    metrics = plant_data.production_metrics.copy()
    metrics['production_rate'] += random.randint(-50, 50)
    metrics['efficiency'] += random.uniform(-2, 2)
    metrics['temperature'] += random.randint(-20, 20)
    
    return jsonify({
        'status': 'success',
        'data': metrics,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/safety/workers', methods=['GET'])
def get_worker_safety_status():
    """Get safety status of all workers"""
    workers = plant_data.workers
    
    # Calculate safety statistics
    total_workers = len(workers)
    safe_workers = len([w for w in workers if w['status'] == 'Safe'])
    ppe_compliant = len([w for w in workers if w['ppe_compliance']])
    violations = len([w for w in workers if w['status'] in ['PPE Missing', 'Training Required']])
    
    return jsonify({
        'status': 'success',
        'data': {
            'workers': workers[:10],  # Return first 10 for display
            'statistics': {
                'total_workers': total_workers,
                'safe_workers': safe_workers,
                'ppe_compliance_rate': round((ppe_compliant / total_workers) * 100, 1),
                'violations_today': violations,
                'safety_score': round((safe_workers / total_workers) * 100, 1)
            }
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/safety/violations', methods=['GET'])
def get_safety_violations():
    """Get recent safety violations"""
    violations = [
        {
            'id': 'V001',
            'worker_id': 'W1047',
            'worker_name': 'Ahmed Hassan',
            'violation_type': 'PPE Missing',
            'location': 'Zone B',
            'severity': 'Medium',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'resolved': False
        },
        {
            'id': 'V002',
            'worker_id': 'W1023',
            'worker_name': 'Lisa Chen',
            'violation_type': 'Unauthorized Zone Access',
            'location': 'Zone D',
            'severity': 'High',
            'timestamp': (datetime.now() - timedelta(hours=5)).isoformat(),
            'resolved': True
        }
    ]
    
    return jsonify({
        'status': 'success',
        'data': violations,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/schedule/current', methods=['GET'])
def get_current_schedule():
    """Get current shift schedules"""
    current_time = datetime.now().hour
    
    # Determine current shift
    if 6 <= current_time < 14:
        current_shift = 'Morning Shift'
    elif 14 <= current_time < 22:
        current_shift = 'Afternoon Shift'
    else:
        current_shift = 'Night Shift'
    
    return jsonify({
        'status': 'success',
        'data': {
            'schedules': plant_data.schedules,
            'current_shift': current_shift,
            'current_time': datetime.now().strftime('%H:%M')
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/schedule/optimize', methods=['POST'])
def optimize_schedule():
    """Trigger AI schedule optimization"""
    # Simulate AI optimization process
    optimization_result = {
        'optimization_id': f'OPT_{random.randint(1000, 9999)}',
        'improvements': {
            'efficiency_gain': f'{random.randint(5, 15)}%',
            'energy_savings': f'₹{random.randint(10000, 50000)}/day',
            'safety_score_improvement': f'{random.randint(2, 8)} points'
        },
        'recommended_changes': [
            'Redistribute workers from Zone A to Zone C during peak hours',
            'Schedule maintenance during low-production periods',
            'Implement staggered break times to maintain productivity'
        ],
        'status': 'completed'
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Schedule optimization completed',
        'data': optimization_result,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/compliance/status', methods=['GET'])
def get_compliance_status():
    """Get regulatory compliance status"""
    compliance_data = {
        'age_verification': {
            'status': 'compliant',
            'verified_workers': 50,
            'total_workers': 50,
            'compliance_rate': 100
        },
        'safety_training': {
            'status': 'mostly_compliant',
            'completed_training': 48,
            'total_workers': 50,
            'compliance_rate': 96
        },
        'environmental': {
            'status': 'compliant',
            'emissions_target': -10,
            'current_emissions': -12,
            'compliance_rate': 120  # Exceeding target
        },
        'labor_standards': {
            'status': 'compliant',
            'working_hours_violations': 0,
            'overtime_compliance': 100,
            'break_time_compliance': 98
        }
    }
    
    return jsonify({
        'status': 'success',
        'data': compliance_data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI Assistant chat endpoint"""
    user_message = request.json.get('message', '')
    
    # Simple AI response simulation (In production, integrate with Gemini API)
    ai_responses = [
        f"Based on your query about '{user_message}', I recommend optimizing kiln temperature to 1470°C for better efficiency.",
        f"Regarding '{user_message}', all safety protocols are currently being followed. Worker compliance is at 96%.",
        f"For '{user_message}', I suggest scheduling preventive maintenance during the next low-production period.",
        f"Analyzing '{user_message}': Energy consumption can be reduced by 8% through parameter adjustments.",
        f"About '{user_message}': Current production rate is optimal. Consider adjusting only if demand increases.",
        f"Concerning '{user_message}': All environmental targets are being met. CO2 emissions are 12% below target."
    ]
    
    response = random.choice(ai_responses)
    
    return jsonify({
        'status': 'success',
        'data': {
            'user_message': user_message,
            'ai_response': response,
            'confidence': random.uniform(0.85, 0.98),
            'suggestions': [
                'Would you like me to implement this recommendation?',
                'Should I schedule this change for the next maintenance window?',
                'Would you like a detailed analysis report?'
            ]
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/reports/safety', methods=['POST'])
def generate_safety_report():
    """Generate comprehensive safety report"""
    report_data = {
        'report_id': f'RPT_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'period': request.json.get('period', 'daily'),
        'summary': {
            'total_incidents': random.randint(0, 3),
            'ppe_compliance_avg': random.uniform(94, 98),
            'safety_training_completion': random.uniform(95, 100),
            'safety_score': random.uniform(92, 98)
        },
        'recommendations': [
            'Increase safety training frequency in Zone B',
            'Install additional PPE monitoring cameras',
            'Implement reward system for safety compliance'
        ],
        'generated_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Safety report generated successfully',
        'data': report_data,
        'download_url': f'/api/reports/download/{report_data["report_id"]}'
    })

@app.route('/api/emergency/stop', methods=['POST'])
def emergency_stop():
    """Emergency stop procedure"""
    stop_id = f'ESTOP_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    # In production, this would trigger actual emergency procedures
    emergency_response = {
        'stop_id': stop_id,
        'initiated_by': request.json.get('user_id', 'system'),
        'reason': request.json.get('reason', 'Manual emergency stop'),
        'affected_systems': [
            'Production Line 1',
            'Production Line 2',
            'Kiln Operations',
            'Conveyor Systems'
        ],
        'response_time': '< 5 seconds',
        'status': 'emergency_stop_active'
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Emergency stop activated successfully',
        'data': emergency_response,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting CementAI Platform Backend...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/*")
    print("💡 AI Assistant ready for optimization tasks")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )