# Indian Airline Data Dashboard

## Project Overview
An interactive web-based dashboard and chatbot for analyzing and visualizing Indian airline performance data. Built with Plotly Dash and designed for deployment on Vercel.

## Features
- **Interactive Dashboard**: Multi-page dashboard with KPIs, time-series charts, and comparative visualizations
- **Rule-based Chatbot**: Simple chatbot interface for querying airline performance data
- **Data Consolidation**: Robust system for handling multiple Excel data sources
- **Responsive Design**: Works across different screen sizes and devices

## Technical Stack
- **Backend/Dashboard**: Plotly Dash (Python)
- **Hosting**: Vercel (serverless functions)
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Version Control**: Git & GitHub

## Project Structure
```
├── dashboard/
│   ├── app.py              # Main Dash application
│   ├── components/         # Reusable dashboard components
│   └── pages/             # Multi-page dashboard modules
├── data/                  # Data files and processing
│   ├── raw/              # Original Excel files
│   ├── processed/        # Cleaned and consolidated data
│   └── data_processor.py # Data ingestion and preprocessing
├── utils/                # Utility functions
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment configuration
└── README.md            # This file
```

## Modules

### Module 1: Data Ingestion & Consolidation
Loads and consolidates multiple Excel files containing Indian airline performance metrics into a single pandas DataFrame.

### Module 2: Data Preprocessing & Feature Engineering
- Standardizes column names
- Handles missing values
- Creates derived metrics (OnTimePercentage, CancellationRate)
- Implements time-series indexing

### Module 3: Interactive Dashboard
**Page 1: Overview Dashboard**
- KPI cards with key performance metrics
- Time-series charts with airline filtering
- Comparative bar charts
- Delay/cancellation reason pie charts

**Page 2: Chatbot Interface**
- Rule-based query system
- Pre-programmed responses for common questions
- Interactive chat interface

### Module 4: Deployment & Documentation
- Vercel-ready configuration
- Comprehensive documentation
- Git repository setup

## Installation & Setup

### Local Development
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd indian-airline-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python dashboard/app.py
   ```

5. Open your browser to `http://localhost:8050`

### Deployment
The application is configured for automatic deployment to Vercel when connected to a GitHub repository.

## Data Sources
This project works with Indian airline performance datasets containing metrics such as:
- On-time arrivals and departures
- Flight cancellations
- Delay reasons and durations
- Airline-specific performance indicators

## Key Insights
The dashboard provides insights into:
- Overall airline industry performance trends
- Comparative analysis between different airlines
- Seasonal patterns in delays and cancellations
- Most common reasons for flight disruptions

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License
MIT License - see LICENSE file for details

## Contact
For questions or support, please open an issue in the GitHub repository.
