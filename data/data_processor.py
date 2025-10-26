"""
Data processor module for Indian Airline Dashboard
Handles data ingestion, consolidation, and preprocessing
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random
from typing import List, Dict, Union


class DataProcessor:
    """
    Handles loading, consolidating and preprocessing of airline data
    """
    
    def __init__(self):
        self.raw_data_path = "data/raw"
        self.processed_data_path = "data/processed"
        self.main_df = None
        
        # Indian airline names for realistic data
        self.airlines = [
            "IndiGo", "SpiceJet", "Air India", "GoAir", "Vistara", 
            "AirAsia India", "Alliance Air", "Akasa Air"
        ]
        
        # Common delay reasons
        self.delay_reasons = [
            "Weather", "Technical Issues", "Air Traffic Control", 
            "Operational", "Security", "Ground Handling", "Crew Issues"
        ]
    
    def create_sample_data(self, start_year: int = 2020, end_year: int = 2024) -> None:
        """
        Creates sample airline performance data for demonstration
        This simulates multiple Excel files that would typically be provided
        """
        os.makedirs(self.raw_data_path, exist_ok=True)
        
        # Generate data for each year
        for year in range(start_year, end_year + 1):
            monthly_data = []
            
            for month in range(1, 13):
                for airline in self.airlines:
                    # Base performance metrics (realistic ranges)
                    total_flights = random.randint(800, 2000)
                    on_time_rate = random.uniform(0.65, 0.95)  # 65-95% on-time
                    
                    # Calculate dependent metrics
                    on_time_flights = int(total_flights * on_time_rate)
                    delayed_flights = total_flights - on_time_flights
                    cancellation_rate = random.uniform(0.01, 0.05)  # 1-5% cancellation
                    cancelled_flights = int(total_flights * cancellation_rate)
                    
                    # Adjust for cancelled flights
                    operated_flights = total_flights - cancelled_flights
                    on_time_flights = min(on_time_flights, operated_flights)
                    delayed_flights = operated_flights - on_time_flights
                    
                    # Average delay time for delayed flights
                    avg_delay_minutes = random.uniform(15, 120)
                    
                    # Create row data
                    row = {
                        'Year': year,
                        'Month': month,
                        'Airline': airline,
                        'Total_Flights': total_flights,
                        'Operated_Flights': operated_flights,
                        'On_Time_Flights': on_time_flights,
                        'Delayed_Flights': delayed_flights,
                        'Cancelled_Flights': cancelled_flights,
                        'Average_Delay_Minutes': avg_delay_minutes,
                        'On_Time_Percentage': (on_time_flights / operated_flights) * 100 if operated_flights > 0 else 0,
                        'Cancellation_Rate': (cancelled_flights / total_flights) * 100,
                        'Primary_Delay_Reason': random.choice(self.delay_reasons)
                    }
                    monthly_data.append(row)
            
            # Create DataFrame and save as Excel
            year_df = pd.DataFrame(monthly_data)
            filename = f"{self.raw_data_path}/airline_data_{year}.xlsx"
            year_df.to_excel(filename, index=False)
            print(f"Created sample data file: {filename}")
    
    def load_excel_files(self) -> pd.DataFrame:
        """
        Load and consolidate all Excel files from the raw data directory
        """
        excel_files = [f for f in os.listdir(self.raw_data_path) if f.endswith('.xlsx')]
        
        if not excel_files:
            print("No Excel files found. Creating sample data...")
            self.create_sample_data()
            excel_files = [f for f in os.listdir(self.raw_data_path) if f.endswith('.xlsx')]
        
        all_dataframes = []
        
        for file in excel_files:
            file_path = os.path.join(self.raw_data_path, file)
            try:
                df = pd.read_excel(file_path)
                df['Source_File'] = file
                all_dataframes.append(df)
                print(f"Loaded: {file} with {len(df)} rows")
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if all_dataframes:
            consolidated_df = pd.concat(all_dataframes, ignore_index=True)
            print(f"Consolidated {len(all_dataframes)} files into {len(consolidated_df)} total rows")
            return consolidated_df
        else:
            raise ValueError("No data could be loaded from Excel files")
    
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names for consistency
        """
        # Define column mapping for standardization
        column_mapping = {
            'total_flights': 'Total_Flights',
            'totalflights': 'Total_Flights',
            'flights_total': 'Total_Flights',
            'operated_flights': 'Operated_Flights',
            'operatedflights': 'Operated_Flights',
            'on_time_flights': 'On_Time_Flights',
            'ontimeflights': 'On_Time_Flights',
            'ontime_flights': 'On_Time_Flights',
            'delayed_flights': 'Delayed_Flights',
            'delayedflights': 'Delayed_Flights',
            'cancelled_flights': 'Cancelled_Flights',
            'cancelledflights': 'Cancelled_Flights',
            'cancellations': 'Cancelled_Flights',
            'average_delay_minutes': 'Average_Delay_Minutes',
            'avg_delay_minutes': 'Average_Delay_Minutes',
            'delay_minutes': 'Average_Delay_Minutes',
            'on_time_percentage': 'On_Time_Percentage',
            'ontimepercentage': 'On_Time_Percentage',
            'cancellation_rate': 'Cancellation_Rate',
            'cancellationrate': 'Cancellation_Rate',
            'primary_delay_reason': 'Primary_Delay_Reason',
            'delay_reason': 'Primary_Delay_Reason',
            'airline': 'Airline',
            'airline_name': 'Airline',
            'year': 'Year',
            'month': 'Month'
        }
        
        # Apply column mapping (case-insensitive)
        df_copy = df.copy()
        for old_col in df_copy.columns:
            clean_col = old_col.lower().strip()
            if clean_col in column_mapping:
                df_copy.rename(columns={old_col: column_mapping[clean_col]}, inplace=True)
        
        return df_copy
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        """
        df_copy = df.copy()
        
        # Fill numeric columns with appropriate values
        numeric_columns = ['Total_Flights', 'Operated_Flights', 'On_Time_Flights', 
                          'Delayed_Flights', 'Cancelled_Flights', 'Average_Delay_Minutes']
        
        for col in numeric_columns:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].fillna(0)
        
        # Fill percentage columns
        if 'On_Time_Percentage' in df_copy.columns:
            df_copy['On_Time_Percentage'] = df_copy['On_Time_Percentage'].fillna(
                df_copy['On_Time_Percentage'].mean()
            )
        
        if 'Cancellation_Rate' in df_copy.columns:
            df_copy['Cancellation_Rate'] = df_copy['Cancellation_Rate'].fillna(0)
        
        # Fill categorical columns
        if 'Primary_Delay_Reason' in df_copy.columns:
            df_copy['Primary_Delay_Reason'] = df_copy['Primary_Delay_Reason'].fillna('Unknown')
        
        if 'Airline' in df_copy.columns:
            df_copy['Airline'] = df_copy['Airline'].fillna('Unknown')
        
        return df_copy
    
    def convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure proper data types for all columns
        """
        df_copy = df.copy()
        
        # Integer columns
        int_columns = ['Year', 'Month', 'Total_Flights', 'Operated_Flights', 
                      'On_Time_Flights', 'Delayed_Flights', 'Cancelled_Flights']
        
        for col in int_columns:
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0).astype(int)
        
        # Float columns
        float_columns = ['Average_Delay_Minutes', 'On_Time_Percentage', 'Cancellation_Rate']
        
        for col in float_columns:
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0.0).astype(float)
        
        # String columns
        string_columns = ['Airline', 'Primary_Delay_Reason']
        
        for col in string_columns:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype(str)
        
        return df_copy
    
    def create_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create new high-level metrics for analysis
        """
        df_copy = df.copy()
        
        # Ensure we have the required base columns
        required_cols = ['Operated_Flights', 'On_Time_Flights', 'Cancelled_Flights', 
                        'Total_Flights', 'Delayed_Flights', 'Average_Delay_Minutes']
        
        # Calculate On-Time Percentage if not present or needs recalculation
        if 'Operated_Flights' in df_copy.columns and 'On_Time_Flights' in df_copy.columns:
            df_copy['On_Time_Percentage'] = np.where(
                df_copy['Operated_Flights'] > 0,
                (df_copy['On_Time_Flights'] / df_copy['Operated_Flights']) * 100,
                0
            )
        
        # Calculate Cancellation Rate if not present
        if 'Total_Flights' in df_copy.columns and 'Cancelled_Flights' in df_copy.columns:
            df_copy['Cancellation_Rate'] = np.where(
                df_copy['Total_Flights'] > 0,
                (df_copy['Cancelled_Flights'] / df_copy['Total_Flights']) * 100,
                0
            )
        
        # Calculate Delay Rate
        if 'Operated_Flights' in df_copy.columns and 'Delayed_Flights' in df_copy.columns:
            df_copy['Delay_Rate'] = np.where(
                df_copy['Operated_Flights'] > 0,
                (df_copy['Delayed_Flights'] / df_copy['Operated_Flights']) * 100,
                0
            )
        
        # Calculate Total Delay Minutes
        if 'Delayed_Flights' in df_copy.columns and 'Average_Delay_Minutes' in df_copy.columns:
            df_copy['Total_Delay_Minutes'] = df_copy['Delayed_Flights'] * df_copy['Average_Delay_Minutes']
        
        # Calculate Average Delay Per Flight (across all flights)
        if 'Total_Delay_Minutes' in df_copy.columns and 'Total_Flights' in df_copy.columns:
            df_copy['Average_Delay_Per_Flight'] = np.where(
                df_copy['Total_Flights'] > 0,
                df_copy['Total_Delay_Minutes'] / df_copy['Total_Flights'],
                0
            )
        
        return df_copy
    
    def create_time_series_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create proper date column and set as index for time-series analysis
        """
        df_copy = df.copy()
        
        # Create date column from Year and Month
        if 'Year' in df_copy.columns and 'Month' in df_copy.columns:
            df_copy['Date'] = pd.to_datetime(df_copy[['Year', 'Month']].assign(day=1))
            # Keep original columns but also create the date index
            df_copy['Date_Index'] = df_copy['Date']
        
        return df_copy
    
    def process_data(self) -> pd.DataFrame:
        """
        Main function to process all data through the pipeline
        """
        print("Starting data processing pipeline...")
        
        # Step 1: Load and consolidate data
        print("\n1. Loading Excel files...")
        df = self.load_excel_files()
        
        # Step 2: Standardize column names
        print("\n2. Standardizing column names...")
        df = self.standardize_columns(df)
        
        # Step 3: Handle missing values
        print("\n3. Handling missing values...")
        df = self.handle_missing_values(df)
        
        # Step 4: Convert data types
        print("\n4. Converting data types...")
        df = self.convert_data_types(df)
        
        # Step 5: Create derived metrics
        print("\n5. Creating derived metrics...")
        df = self.create_derived_metrics(df)
        
        # Step 6: Create time series index
        print("\n6. Creating time series index...")
        df = self.create_time_series_index(df)
        
        # Store processed data
        self.main_df = df
        
        # Save processed data
        os.makedirs(self.processed_data_path, exist_ok=True)
        processed_file = f"{self.processed_data_path}/consolidated_airline_data.csv"
        df.to_csv(processed_file, index=False)
        
        print(f"\n✅ Data processing complete!")
        print(f"Final dataset shape: {df.shape}")
        print(f"Processed data saved to: {processed_file}")
        print(f"Airlines in dataset: {sorted(df['Airline'].unique())}")
        print(f"Date range: {df['Year'].min()}-{df['Year'].max()}")
        
        return df
    
    def get_data_summary(self) -> Dict:
        """
        Get a summary of the processed data
        """
        if self.main_df is None:
            self.process_data()
        
        df = self.main_df
        
        summary = {
            'total_records': len(df),
            'airlines': sorted(df['Airline'].unique().tolist()),
            'date_range': {
                'start_year': int(df['Year'].min()),
                'end_year': int(df['Year'].max()),
                'total_months': len(df['Date'].unique()) if 'Date' in df.columns else 0
            },
            'key_metrics': {
                'avg_on_time_percentage': float(df['On_Time_Percentage'].mean()),
                'avg_cancellation_rate': float(df['Cancellation_Rate'].mean()),
                'total_flights': int(df['Total_Flights'].sum()),
                'total_cancellations': int(df['Cancelled_Flights'].sum())
            },
            'columns': df.columns.tolist()
        }
        
        return summary


if __name__ == "__main__":
    # Test the data processor
    processor = DataProcessor()
    processed_df = processor.process_data()
    summary = processor.get_data_summary()
    
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    print(f"Total Records: {summary['total_records']}")
    print(f"Airlines: {len(summary['airlines'])}")
    print(f"Date Range: {summary['date_range']['start_year']}-{summary['date_range']['end_year']}")
    print(f"Average On-Time Performance: {summary['key_metrics']['avg_on_time_percentage']:.1f}%")
    print(f"Average Cancellation Rate: {summary['key_metrics']['avg_cancellation_rate']:.2f}%")
