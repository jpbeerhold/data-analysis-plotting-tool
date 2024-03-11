
# Using the pandas module is mandatory
import pandas as pd

# Importing tools and data set according to the folder structure
import sys
sys.path.append("..")







from AnalysisTool import AnalysisTool


# Convert Berlin data set to pandas DataFrame
df = pd.read_csv('../../historical_weather_data/raw_data/berlin_2020-01-01_2024-01-27.csv')
df.rename(columns={'Unnamed: 0': 'index'}, inplace=True)


# Create object
DA = AnalysisTool('berlin', df)


# Decide which columns not to use
columns_to_drop = ['index',
                   'temperature_2m_mean',
                   'apparent_temperature_max',
                   'apparent_temperature_min',
                   'sunrise', 
                   'sunset', 
                   'wind_speed_10m_max', 
                   'wind_gusts_10m_max', 
                   'wind_direction_10m_dominant', 
                   'shortwave_radiation_sum', 
                   'et0_fao_evapotranspiration']


# Decide which columns to use
columns_to_check = ['weather_code', 
                    'temperature_2m_max', 
                    'temperature_2m_min', 
                    'apparent_temperature_mean',
                    'daylight_duration', 
                    'sunshine_duration', 
                    'precipitation_sum', 
                    'rain_sum', 
                    'snowfall_sum',
                    'precipitation_hours']


# Preprocess the data set to be used for plotting later
DA.preprocess_data_set(columns_to_drop, columns_to_check, create_file=False, disable_feedback=True)


preprocessed_df = DA.get_data_frame()
print(preprocessed_df)


summary = DA.get_statistical_summary()
print(summary)







from PlottingTool import PlottingTool


# Create object
PT = PlottingTool()


# Add preprocessed pandas DataFrame from before
PT.add_data_set(preprocessed_df, disable_feedback=True)


## Plot added pandas DataFrame in various ways

PT.plot_univariate_graphs(number_columns_unvariate_graphs=3)


# In this example the columns used for plotting bivariate graphs
# are the same as the ones to keep
PT.plot_bivariate_graphs(numeric_variables=columns_to_check)

PT.plot_correlation_heatmap(numeric_variables=columns_to_check)


# Create a regression model 

target_variable = 'precipitation_sum'

predictor_variables = ['temperature_2m_max', 
                       'temperature_2m_min', 
                       'daylight_duration']

regression_model_summary = PT.get_regression_model_summary(target_variable, predictor_variables, disable_feedback=True)
print(regression_model_summary)


