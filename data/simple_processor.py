"""
Simplified data processor for Indian Airline Dashboard
Creates mock data in basic Python without external dependencies for demonstration
"""

import json
import os
import random
from datetime import datetime, timedelta


class SimpleDataProcessor:
    """
    Simplified data processor that creates mock airline data
    """
    
    def __init__(self):
        self.raw_data_path = "data/raw"
        self.processed_data_path = "data/processed"
        
        # Indian airline names
        self.airlines = [
            "IndiGo", "SpiceJet", "Air India", "GoAir", "Vistara", 
            "AirAsia India", "Alliance Air", "Akasa Air"
        ]
        
        # Common delay reasons
        self.delay_reasons = [
            "Weather", "Technical Issues", "Air Traffic Control", 
            "Operational", "Security", "Ground Handling", "Crew Issues"
        ]
    
    def create_sample_data(self, start_year=2020, end_year=2024):
        """
        Creates sample airline performance data
        """
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)
        
        all_data = []
        
        # Generate data for each year/month/airline combination
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                for airline in self.airlines:
                    # Base performance metrics (realistic ranges)
                    total_flights = random.randint(800, 2000)
                    on_time_rate = random.uniform(0.65, 0.95)  # 65-95% on-time
                    
                    # Calculate dependent metrics
                    on_time_flights = int(total_flights * on_time_rate)
                    cancellation_rate = random.uniform(0.01, 0.05)  # 1-5% cancellation
                    cancelled_flights = int(total_flights * cancellation_rate)
                    
                    # Adjust for cancelled flights
                    operated_flights = total_flights - cancelled_flights
                    on_time_flights = min(on_time_flights, operated_flights)
                    delayed_flights = operated_flights - on_time_flights
                    
                    # Average delay time for delayed flights
                    avg_delay_minutes = random.uniform(15, 120)
                    
                    # Calculate percentages
                    on_time_percentage = (on_time_flights / operated_flights * 100) if operated_flights > 0 else 0
                    delay_rate = (delayed_flights / operated_flights * 100) if operated_flights > 0 else 0
                    cancellation_percentage = (cancelled_flights / total_flights * 100)
                    
                    # Create record
                    record = {
                        'year': year,
                        'month': month,
                        'airline': airline,
                        'total_flights': total_flights,
                        'operated_flights': operated_flights,
                        'on_time_flights': on_time_flights,
                        'delayed_flights': delayed_flights,
                        'cancelled_flights': cancelled_flights,
                        'average_delay_minutes': round(avg_delay_minutes, 2),
                        'on_time_percentage': round(on_time_percentage, 2),
                        'delay_rate': round(delay_rate, 2),
                        'cancellation_rate': round(cancellation_percentage, 2),
                        'primary_delay_reason': random.choice(self.delay_reasons),
                        'date': f"{year}-{month:02d}-01"  # First day of month
                    }
                    all_data.append(record)
        
        # Save as JSON for easy loading
        output_file = f"{self.processed_data_path}/airline_data.json"
        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"✅ Created {len(all_data)} records of sample airline data")
        print(f"📁 Saved to: {output_file}")
        print(f"📊 Airlines: {len(self.airlines)}")
        print(f"📅 Date range: {start_year}-{end_year}")
        
        return all_data
    
    def load_data(self):
        """
        Load the processed airline data
        """
        data_file = f"{self.processed_data_path}/airline_data.json"
        
        if not os.path.exists(data_file):
            print("No data file found, creating sample data...")
            return self.create_sample_data()
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} records from {data_file}")
        return data
    
    def get_summary_stats(self, data):
        """
        Calculate summary statistics
        """
        if not data:
            return {}
        
        # Calculate overall metrics
        total_flights = sum(record['total_flights'] for record in data)
        total_on_time = sum(record['on_time_flights'] for record in data)
        total_cancelled = sum(record['cancelled_flights'] for record in data)
        total_operated = sum(record['operated_flights'] for record in data)
        
        # Calculate averages by airline
        airline_stats = {}
        for airline in self.airlines:
            airline_records = [r for r in data if r['airline'] == airline]
            if airline_records:
                avg_on_time = sum(r['on_time_percentage'] for r in airline_records) / len(airline_records)
                avg_cancel = sum(r['cancellation_rate'] for r in airline_records) / len(airline_records)
                airline_stats[airline] = {
                    'avg_on_time_percentage': round(avg_on_time, 2),
                    'avg_cancellation_rate': round(avg_cancel, 2),
                    'total_records': len(airline_records)
                }
        
        # Get delay reasons distribution
        delay_reason_counts = {}
        for record in data:
            reason = record['primary_delay_reason']
            delay_reason_counts[reason] = delay_reason_counts.get(reason, 0) + 1
        
        summary = {
            'total_records': len(data),
            'total_flights': total_flights,
            'overall_on_time_percentage': round((total_on_time / total_operated * 100) if total_operated > 0 else 0, 2),
            'overall_cancellation_rate': round((total_cancelled / total_flights * 100) if total_flights > 0 else 0, 2),
            'airlines_count': len(self.airlines),
            'date_range': {
                'start': min(record['date'] for record in data),
                'end': max(record['date'] for record in data)
            },
            'airline_stats': airline_stats,
            'delay_reasons': delay_reason_counts
        }
        
        return summary
    
    def process(self):
        """
        Main processing function
        """
        print("🚀 Starting Indian Airline Data Processing...")
        print("=" * 50)
        
        # Load or create data
        data = self.load_data()
        
        # Get summary statistics
        summary = self.get_summary_stats(data)
        
        # Save summary
        summary_file = f"{self.processed_data_path}/data_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📈 DATA SUMMARY")
        print("-" * 30)
        print(f"Total Records: {summary['total_records']:,}")
        print(f"Total Flights: {summary['total_flights']:,}")
        print(f"Overall On-Time Performance: {summary['overall_on_time_percentage']}%")
        print(f"Overall Cancellation Rate: {summary['overall_cancellation_rate']}%")
        print(f"Airlines: {summary['airlines_count']}")
        print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        
        print(f"\n🏢 TOP PERFORMING AIRLINES (On-Time %)")
        print("-" * 40)
        sorted_airlines = sorted(summary['airline_stats'].items(), 
                               key=lambda x: x[1]['avg_on_time_percentage'], 
                               reverse=True)
        for airline, stats in sorted_airlines[:5]:
            print(f"{airline}: {stats['avg_on_time_percentage']}%")
        
        print(f"\n⚠️  DELAY REASONS DISTRIBUTION")
        print("-" * 30)
        sorted_reasons = sorted(summary['delay_reasons'].items(), 
                              key=lambda x: x[1], 
                              reverse=True)
        for reason, count in sorted_reasons:
            percentage = (count / summary['total_records'] * 100)
            print(f"{reason}: {count} ({percentage:.1f}%)")
        
        print(f"\n✅ Processing complete! Data saved to {self.processed_data_path}/")
        return data, summary


if __name__ == "__main__":
    processor = SimpleDataProcessor()
    data, summary = processor.process()
