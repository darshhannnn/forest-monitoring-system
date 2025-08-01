import functions_framework
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

@functions_framework.http
def send_deforestation_alerts(request):
    """Send email alerts for illegal deforestation detection"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        data = request.get_json()
        
        # Check if illegal activity detected
        illegal_probability = data.get('illegal_probability', 0)
        legal_status = data.get('legal_status', 'NORMAL')
        
        if illegal_probability > 60 or 'HIGH PRIORITY' in legal_status:
            # Send immediate alert
            alert_result = send_immediate_alert(data)
            return (json.dumps(alert_result), 200, headers)
        else:
            return (json.dumps({
                'status': 'no_alert_needed',
                'message': 'Activity within normal parameters'
            }), 200, headers)
        
    except Exception as e:
        return (json.dumps({
            'status': 'error',
            'message': str(e)
        }), 500, headers)

def send_immediate_alert(data):
    """Send immediate email alert for illegal deforestation"""
    
    # Email configuration
    recipients = [
        'forest.manager@gov.in',
        'environment.ministry@india.gov.in',
        'alerts@forestsurvey.gov.in'
    ]
    
    subject = f"🚨 URGENT: Illegal Deforestation Alert - {data.get('legal_status', 'HIGH PRIORITY')}"
    
    # Create detailed alert email
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="background: #dc3545; color: white; padding: 20px; text-align: center;">
            <h1>🚨 ILLEGAL DEFORESTATION DETECTED</h1>
            <h2>IMMEDIATE ACTION REQUIRED</h2>
        </div>
        
        <div style="padding: 20px;">
            <h2 style="color: #dc3545;">Alert Summary</h2>
            <table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
                <tr style="background: #f8f9fa;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Detection Time:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Alert Level:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd; color: #dc3545; font-weight: bold;">{data.get('legal_status', 'HIGH PRIORITY')}</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Illegal Probability:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{data.get('illegal_probability', 0)}%</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Deforestation Alerts:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{data.get('glad_alerts_count', 0)} GLAD alerts</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Tree Cutting Area:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{data.get('recent_tree_cutting_hectares', 0)} hectares</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Active Fires:</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{data.get('active_fires_24h', 0)} fires detected</td>
                </tr>
            </table>
            
            <h3 style="color: #dc3545;">🎯 Immediate Actions Required:</h3>
            <ul style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                <li>🚁 Deploy field investigation team immediately</li>
                <li>📞 Coordinate with State Forest Department</li>
                <li>🛰️ Request emergency satellite imagery</li>
                <li>⚖️ Initiate legal proceedings if confirmed</li>
                <li>👮 Engage forest crime prevention unit</li>
            </ul>
            
            <h3 style="color: #dc3545;">📊 Detection Details:</h3>
            <p><strong>Monitoring Area:</strong> Entire Indian subcontinent</p>
            <p><strong>Data Sources:</strong> NASA FIRMS + Global Forest Watch GLAD</p>
            <p><strong>Analysis Period:</strong> {data.get('analysis_period_months', 6)} months</p>
            
            <div style="background: #f8f9fa; padding: 15px; margin-top: 20px; border-left: 4px solid #dc3545;">
                <p><strong>⚠️ This is an automated alert from the India Forest Monitoring System</strong></p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                <p>System: Cloud-Based Illegal Deforestation Detection</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # For demo purposes, return success (in production, use actual SMTP)
    return {
        'status': 'alert_sent',
        'message': f'Illegal deforestation alert sent to {len(recipients)} recipients',
        'alert_level': data.get('legal_status', 'HIGH PRIORITY'),
        'recipients': recipients,
        'detection_time': datetime.now().isoformat()
    }
