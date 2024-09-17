## ForecastFlow

ForecastFlow is a web application built with Streamlit that visualizes solar and wind power forecasts from Elexon. The app uses the [elexonpy](https://pypi.org/project/elexonpy/) package, ForecastFlow fetches and displays forecast data through interactive graphs, making it easier to interpret and analyze solar and wind power trends.

## Features
1. Real-Time Data: Access up-to-date solar and wind power forecast data.
2. Customizable Date Ranges: Filter data by specific date and time ranges.
3. Interactive Visualizations: Explore forecast data through dynamic graphs and charts.

## Dependencies

ForecastFlow requires the following Python packages:

1. `streamlit` – For building the interactive web interface.
2. `elexonpy` – For fetching forecast data from Elexon.
3. `pandas` – For data manipulation and analysis.
4. `matplotlib` – For creating static, interactive, and animated visualizations.
5. `plotly` – For interactive graphing.

## Project Structure

```plaintext
ForecastFlow/
│
├── SequenceDiagramElexon.png
├── elexon_solar-forecast.py    
├── requirements.txt            
└── README.md
```                  


Here’s a preview of the dashboard: 

![image](https://github.com/user-attachments/assets/3f4b1dfd-af3e-4e70-a05c-21d1feb6546f) Below is the sequence diagram that illustrates the process flow of the application:


### Below is the diagram that illustrates the process flow of the application

![image](https://github.com/user-attachments/assets/5bece05e-a2dc-4231-8915-419e79436472)


