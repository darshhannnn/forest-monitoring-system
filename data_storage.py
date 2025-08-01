import functions_framework
from google.cloud import bigquery
import json
from datetime import datetime

@functions_framework.http
def store_forest_data(request):
    """Store forest analysis results in BigQuery"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        data = request.get_json()
        
        # Initialize BigQuery client
        client = bigquery.Client()
        table_id = "pelagic-cycle-459808-u9.forest_monitoring_data.forest_analysis"
        
        # Prepare data for insertion
        rows_to_insert = [{
            "timestamp": datetime.now().isoformat(),
            "coordinates": json.dumps(data.get('coordinates', [])),
            "forest_area_sqm": data.get('total_forest_area_sqm', 0),
            "forest_cover_percentage": data.get('forest_cover_percentage', 0),
            "forest_loss_sqm": data.get('forest_loss_sqm', 0),
            "forest_gain_sqm": data.get('forest_gain_sqm', 0),
            "net_change_sqm": data.get('net_change_sqm', 0),
            "alert_level": data.get('alert_level', 'UNKNOWN'),
            "deforestation_detected": data.get('deforestation_detected', False),
            "satellite_images_analyzed": data.get('satellite_images_analyzed', 0),
            "data_source": data.get('data_source', 'Unknown'),
            "processing_method": data.get('processing_method', 'Unknown')
        }]
        
        # Insert data
        errors = client.insert_rows_json(table_id, rows_to_insert)
        
        if errors:
            raise Exception(f"BigQuery insert errors: {errors}")
        
        result = {
            'status': 'success',
            'message': 'Data stored successfully in BigQuery',
            'rows_inserted': len(rows_to_insert),
            'table_id': table_id
        }
        
        return (json.dumps(result), 200, headers)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'message': str(e)
        }
        return (json.dumps(error_result), 500, headers)
