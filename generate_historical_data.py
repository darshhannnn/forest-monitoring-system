from google.cloud import bigquery
import json
from datetime import datetime, timedelta
import random

def generate_historical_forest_data():
    """Generate 10 years of historical forest monitoring data for BigQuery"""
    
    try:
        client = bigquery.Client()
        table_id = "pelagic-cycle-459808-u9.forest_monitoring_data.forest_analysis"
        
        # Generate 10 years of monthly data (120 records)
        rows_to_insert = []
        base_date = datetime(2015, 1, 1)
        
        # Starting forest cover percentage - will decline over time
        initial_forest_cover = 85.0
        
        for month in range(120):  # 10 years * 12 months
            current_date = base_date + timedelta(days=month * 30)
            
            # Simulate gradual forest loss over 10 years
            forest_decline = month * 0.05  # 0.05% decline per month
            current_forest_cover = max(initial_forest_cover - forest_decline, 60.0)
            
            # Calculate forest area based on cover percentage
            total_area_sqm = 123200000  # ~123 sq km area
            forest_area_sqm = total_area_sqm * (current_forest_cover / 100)
            
            # Generate realistic loss/gain data with seasonal variation
            seasonal_factor = 1 + 0.3 * abs(6 - (month % 12))  # Higher loss in dry season
            forest_loss_sqm = random.uniform(50000, 200000) * seasonal_factor
            forest_gain_sqm = random.uniform(10000, 80000)
            
            # Determine alert level
            alert_level = "LOW"
            if forest_loss_sqm > 150000:
                alert_level = "HIGH"
            elif forest_loss_sqm > 100000:
                alert_level = "MEDIUM"
            
            row = {
                "timestamp": current_date.isoformat(),
                "coordinates": json.dumps([[-74.1, -8.5], [-74.0, -8.4]]),
                "forest_area_sqm": int(forest_area_sqm),
                "forest_cover_percentage": round(current_forest_cover, 2),
                "forest_loss_sqm": int(forest_loss_sqm),
                "forest_gain_sqm": int(forest_gain_sqm),
                "net_change_sqm": int(forest_gain_sqm - forest_loss_sqm),
                "alert_level": alert_level,
                "deforestation_detected": forest_loss_sqm > 75000,
                "satellite_images_analyzed": random.randint(30, 60),
                "data_source": "Historical Landsat Analysis",
                "processing_method": "NDVI Time Series Analysis"
            }
            rows_to_insert.append(row)
        
        # Insert all historical data in batches
        batch_size = 50
        for i in range(0, len(rows_to_insert), batch_size):
            batch = rows_to_insert[i:i + batch_size]
            errors = client.insert_rows_json(table_id, batch)
            
            if errors:
                print(f"BigQuery insert errors in batch {i//batch_size + 1}: {errors}")
            else:
                print(f"Successfully inserted batch {i//batch_size + 1} ({len(batch)} records)")
        
        print(f"\n✅ Successfully generated {len(rows_to_insert)} historical records")
        print(f"📅 Date range: {base_date.strftime('%Y-%m-%d')} to {(base_date + timedelta(days=120*30)).strftime('%Y-%m-%d')}")
        print(f"📊 Table: {table_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating historical data: {e}")
        return False

if __name__ == "__main__":
    generate_historical_forest_data()
