import functions_framework
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

@functions_framework.http
def send_alert_email(request):
    """Send email alerts for forest deforestation detection"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        data = request.get_json()
        
        # Email configuration (for demo - in production use environment variables)
        sender_email = "forest.monitor@example.com"
        recipient_emails = ["forest.manager@agency.gov", "alerts@conservation.org"]
        
        # Create email content based on alert level
        alert_level = data.get('alert_level', 'UNKNOWN')
        forest_loss = data.get('forest_loss_sqm', 0)
        coordinates = data.get('coordinates', 'Unknown')
        
        subject = f"🚨 FOREST ALERT - {alert_level} Priority"
        
        # HTML email body
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background: #d9534f; color: white; padding: 20px; text-align: center;">
                <h1>🌲 Forest Monitoring Alert</h1>
            </div>
            
            <div style="padding: 20px;">
                <h2 style="color: #d9534f;">Alert Details</h2>
                <table style="border-collapse: collapse; width: 100%;">
                    <tr><td><strong>Alert Level:</strong></td><td style="color: #d9534f; font-weight: bold;">{alert_level}</td></tr>
                    <tr><td><strong>Forest Loss:</strong></td><td>{forest_loss:,.0f} sq meters ({forest_loss/1000000:.3f} sq km)</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{coordinates}</td></tr>
                    <tr><td><strong>Detection Time:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    <tr><td><strong>Forest Cover:</strong></td><td>{data.get('forest_cover_percentage', 0):.1f}%</td></tr>
                </table>
                
                <h3 style="color: #d9534f;">Recommended Actions:</h3>
                <ul>
                    <li>🚁 Dispatch field team for ground verification</li>
                    <li>🔍 Investigate potential illegal logging activities</li>
                    <li>📞 Coordinate with local forest authorities</li>
                    <li>📊 Update conservation database records</li>
                    <li>📸 Request high-resolution satellite imagery</li>
                </ul>
                
                <div style="background: #f8f9fa; padding: 15px; margin-top: 20px; border-left: 4px solid #d9534f;">
                    <p><strong>System Information:</strong></p>
                    <p>Analysis Method: {data.get('processing_method', 'NDVI Change Detection')}</p>
                    <p>Data Source: {data.get('data_source', 'Satellite Analysis')}</p>
                    <p>Images Analyzed: {data.get('satellite_images_analyzed', 0)}</p>
                </div>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    This is an automated alert from the Cloud-Based Forest Monitoring System.<br>
                    For technical support, contact the system administrator.
                </p>
            </div>
        </body>
        </html>
        """
        
        # For demo purposes, we'll simulate email sending
        # In production, you would use actual SMTP or SendGrid
        
        result = {
            'status': 'success',
            'message': f'Alert email prepared for {alert_level} priority event',
            'recipients': recipient_emails,
            'subject': subject,
            'alert_details': {
                'forest_loss_sqm': forest_loss,
                'forest_cover_percentage': data.get('forest_cover_percentage', 0),
                'alert_level': alert_level,
                'coordinates': coordinates
            },
            'note': 'Email sending simulated for demo - would be sent via SMTP/SendGrid in production'
        }
        
        return (json.dumps(result), 200, headers)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'message': str(e)
        }
        return (json.dumps(error_result), 500, headers)
