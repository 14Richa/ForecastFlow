# import streamlit as st
# import pandas as pd
# from datetime import datetime, timedelta
# from elexonpy.api_client import ApiClient
# from elexonpy.api.generation_forecast_api import GenerationForecastApi
# import plotly.graph_objects as go

# # Function to fetch and process data
# def fetch_forecast_data(api_func, start_date, end_date, process_type, business_type):
#     try:
#         with st.spinner(f"Fetching {business_type} forecast data for process type '{process_type}'..."):
#             response = api_func(
#                 _from=start_date.isoformat(),
#                 to=end_date.isoformat(),
#                 process_type=process_type,
#                 format="json",
#             )
#             if not response.data:
#                 return pd.DataFrame()

#             df = pd.DataFrame([item.to_dict() for item in response.data])
#             filtered_df = df[df["business_type"] == business_type]
#             filtered_df["start_time"] = pd.to_datetime(filtered_df["start_time"])
#             filtered_df = filtered_df.set_index("start_time")

#             if not filtered_df.empty:
#                 filtered_df = filtered_df.resample("30T")["quantity"].sum().reset_index()

#             return filtered_df
#     except Exception as e:
#         st.error(f"Error fetching data for process type '{process_type}': {e}")
#         return pd.DataFrame()

# # Initialize Elexon API client
# api_client = ApiClient()
# forecast_api = GenerationForecastApi(api_client)
# forecast_generation_wind_and_solar_day_ahead_get = (
#     forecast_api.forecast_generation_wind_and_solar_day_ahead_get
# )

# # Streamlit app
# st.title("Elexon Solar and Wind Forecast")

# # Process Description
# st.sidebar.header("Process Overview")
# st.sidebar.text(
#     """
#     **Process Overview:**
#     1. **User Input**: Select the start and end date for the forecast data.
#     2. **Fetch Data**: Click 'Fetch Data' to start retrieving forecast data from the Elexon API.
#     3. **Data Processing**: The fetched data is processed and aggregated for solar and wind generation.
#     4. **Display Data**: Raw data tables and forecast graphs are displayed.
#     """
# )

# # Get user input for start and end date
# start_datetime_utc = st.date_input("Start Date", datetime.utcnow() - timedelta(days=3))
# end_datetime_utc = st.date_input("End Date", datetime.utcnow() + timedelta(days=3))

# if st.button("Fetch Data"):
#     if start_datetime_utc < end_datetime_utc:
#         process_types = ["Day Ahead", "Intraday Process", "Intraday Total"]
#         colors = ["red", "blue", "green"]

#         # Show raw data for solar forecasts
#         st.subheader("Raw Solar Forecast Data")
#         with st.spinner("Fetching and displaying solar forecast data..."):
#             solar_forecasts = {pt: fetch_forecast_data(forecast_generation_wind_and_solar_day_ahead_get, start_datetime_utc, end_datetime_utc, pt, "Solar generation") for pt in process_types}
#             for pt in process_types:
#                 st.write(f"**{pt} Solar Forecast Data**")
#                 st.dataframe(solar_forecasts[pt].reset_index())

#         # Show raw data for wind forecasts
#         st.subheader("Raw Wind Forecast Data")
#         with st.spinner("Fetching and displaying wind forecast data..."):
#             wind_forecasts = {pt: fetch_forecast_data(forecast_generation_wind_and_solar_day_ahead_get, start_datetime_utc, end_datetime_utc, pt, "Wind generation") for pt in process_types}
#             for pt in process_types:
#                 st.write(f"**{pt} Wind Forecast Data**")
#                 st.dataframe(wind_forecasts[pt].reset_index())

#         # Plot solar forecast data
#         st.subheader("Solar Forecast Graphs")
#         fig_solar = go.Figure()
#         st.text("Processing solar forecast data for plotting...")
#         for pt in process_types:
#             forecast = solar_forecasts[pt]
#             if forecast.empty:
#                 st.write(f"No data available for solar process type: {pt}")
#                 continue

#             forecast = forecast[forecast["quantity"].notna() & (forecast["quantity"] > 0)]
#             full_time_range = pd.date_range(start=start_datetime_utc, end=end_datetime_utc, freq='30T', tz=forecast["start_time"].dt.tz)
#             full_time_df = pd.DataFrame(full_time_range, columns=['start_time'])

#             forecast = full_time_df.merge(forecast, on='start_time', how='left')

#             fig_solar.add_trace(go.Scatter(
#                 x=forecast["start_time"],
#                 y=forecast["quantity"],
#                 mode='lines',
#                 name=pt,
#                 line=dict(color=colors[process_types.index(pt)]),
#                 connectgaps=False
#             ))

#         fig_solar.update_layout(
#             title="Elexon Solar Forecast",
#             xaxis_title="Date and Time",
#             yaxis_title="Forecast (MW)",
#             xaxis=dict(
#                 tickformat='%Y-%m-%d %H:%M',
#                 tickangle=45
#             ),
#             legend_title="Process Type"
#         )

#         st.plotly_chart(fig_solar)

#         # Plot wind forecast data
#         st.subheader("Wind Forecast Graphs")
#         fig_wind = go.Figure()
#         st.text("Processing wind forecast data for plotting...")
#         for pt in process_types:
#             forecast = wind_forecasts[pt]
#             if forecast.empty:
#                 st.write(f"No data available for wind process type: {pt}")
#                 continue

#             forecast = forecast[forecast["quantity"].notna() & (forecast["quantity"] > 0)]
#             full_time_range = pd.date_range(start=start_datetime_utc, end=end_datetime_utc, freq='30T', tz=forecast["start_time"].dt.tz)
#             full_time_df = pd.DataFrame(full_time_range, columns=['start_time'])

#             forecast = full_time_df.merge(forecast, on='start_time', how='left')

#             fig_wind.add_trace(go.Scatter(
#                 x=forecast["start_time"],
#                 y=forecast["quantity"],
#                 mode='lines',
#                 name=pt,
#                 line=dict(color=colors[process_types.index(pt)]),
#                 connectgaps=False
#             ))

#         fig_wind.update_layout(
#             title="Elexon Wind Forecast",
#             xaxis_title="Date and Time",
#             yaxis_title="Forecast (MW)",
#             xaxis=dict(
#                 tickformat='%Y-%m-%d %H:%M',
#                 tickangle=45
#             ),
#             legend_title="Process Type"
#         )

#         st.plotly_chart(fig_wind)

#     else:
#         st.warning("End date must be after start date.")



import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from elexonpy.api_client import ApiClient
from elexonpy.api.generation_forecast_api import GenerationForecastApi
import plotly.graph_objects as go

# Function to fetch and process data
def fetch_forecast_data(api_func, start_date, end_date, process_type, business_type):
    try:
        with st.spinner(f"Fetching {business_type} forecast data for process type '{process_type}'..."):
            response = api_func(
                _from=start_date.isoformat(),
                to=end_date.isoformat(),
                process_type=process_type,
                format="json",
            )
            if not response.data:
                return pd.DataFrame()

            df = pd.DataFrame([item.to_dict() for item in response.data])
            filtered_df = df[df["business_type"] == business_type]
            filtered_df["start_time"] = pd.to_datetime(filtered_df["start_time"])
            filtered_df = filtered_df.set_index("start_time")

            if not filtered_df.empty:
                filtered_df = filtered_df.resample("30T")["quantity"].sum().reset_index()

            return filtered_df
    except Exception as e:
        st.error(f"Error fetching data for process type '{process_type}': {e}")
        return pd.DataFrame()

# Initialize Elexon API client
api_client = ApiClient()
forecast_api = GenerationForecastApi(api_client)
forecast_generation_wind_and_solar_day_ahead_get = (
    forecast_api.forecast_generation_wind_and_solar_day_ahead_get
)

# Streamlit app
st.title("Elexon Solar and Wind Forecast")

# Display the sequence diagram
st.subheader("Process Overview")
st.text("Below is a sequence diagram illustrating the process flow:")

# Load and display the sequence diagram
st.image("SequenceDigramElexon.png", caption="Process Flow")

# Get user input for start and end date
start_datetime_utc = st.date_input("Start Date", datetime.utcnow() - timedelta(days=3))
end_datetime_utc = st.date_input("End Date", datetime.utcnow() + timedelta(days=3))

if st.button("Fetch Data"):
    if start_datetime_utc < end_datetime_utc:
        process_types = ["Day Ahead", "Intraday Process", "Intraday Total"]
        colors = ["red", "blue", "green"]

        # Plot solar forecast data
        st.subheader("Solar Forecast Graphs")
        fig_solar = go.Figure()
        st.text("Processing solar forecast data for plotting...")
        solar_forecasts = {pt: fetch_forecast_data(forecast_generation_wind_and_solar_day_ahead_get, start_datetime_utc, end_datetime_utc, pt, "Solar generation") for pt in process_types}
        for pt in process_types:
            forecast = solar_forecasts[pt]
            if forecast.empty:
                st.write(f"No data available for solar process type: {pt}")
                continue

            forecast = forecast[forecast["quantity"].notna() & (forecast["quantity"] > 0)]
            full_time_range = pd.date_range(start=start_datetime_utc, end=end_datetime_utc, freq='30T', tz=forecast["start_time"].dt.tz)
            full_time_df = pd.DataFrame(full_time_range, columns=['start_time'])

            forecast = full_time_df.merge(forecast, on='start_time', how='left')

            fig_solar.add_trace(go.Scatter(
                x=forecast["start_time"],
                y=forecast["quantity"],
                mode='lines',
                name=pt,
                line=dict(color=colors[process_types.index(pt)]),
                connectgaps=False
            ))

        fig_solar.update_layout(
            title="Elexon Solar Forecast",
            xaxis_title="Date and Time",
            yaxis_title="Forecast (MW)",
            xaxis=dict(
                tickformat='%Y-%m-%d %H:%M',
                tickangle=45
            ),
            legend_title="Process Type"
        )

        st.plotly_chart(fig_solar)

        # Plot wind forecast data
        st.subheader("Wind Forecast Graphs")
        fig_wind = go.Figure()
        st.text("Processing wind forecast data for plotting...")
        wind_forecasts = {pt: fetch_forecast_data(forecast_generation_wind_and_solar_day_ahead_get, start_datetime_utc, end_datetime_utc, pt, "Wind generation") for pt in process_types}
        for pt in process_types:
            forecast = wind_forecasts[pt]
            if forecast.empty:
                st.write(f"No data available for wind process type: {pt}")
                continue

            forecast = forecast[forecast["quantity"].notna() & (forecast["quantity"] > 0)]
            full_time_range = pd.date_range(start=start_datetime_utc, end=end_datetime_utc, freq='30T', tz=forecast["start_time"].dt.tz)
            full_time_df = pd.DataFrame(full_time_range, columns=['start_time'])

            forecast = full_time_df.merge(forecast, on='start_time', how='left')

            fig_wind.add_trace(go.Scatter(
                x=forecast["start_time"],
                y=forecast["quantity"],
                mode='lines',
                name=pt,
                line=dict(color=colors[process_types.index(pt)]),
                connectgaps=False
            ))

        fig_wind.update_layout(
            title="Elexon Wind Forecast",
            xaxis_title="Date and Time",
            yaxis_title="Forecast (MW)",
            xaxis=dict(
                tickformat='%Y-%m-%d %H:%M',
                tickangle=45
            ),
            legend_title="Process Type"
        )

        st.plotly_chart(fig_wind)

    else:
        st.warning("End date must be after start date.")



