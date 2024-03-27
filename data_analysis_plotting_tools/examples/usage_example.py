
# Using the pandas module is mandatory
import pandas as pd

# Importing tools and data set according to the folder structure
import sys
sys.path.append("..")







from AnalysisTool import AnalysisTool


# Convert Berlin data set to pandas DataFrame
df_berlin = pd.read_csv('../../historical_weather_data/raw_data/berlin_2020-01-01_2024-01-27.csv')


# Create object
df_name_berlin = 'berlin'
analysis_tool = AnalysisTool(df_name_berlin, df_berlin)


# Decide which columns NOT to use
columns_to_drop = ['Unnamed: 0',
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
analysis_tool.preprocess_data_set(columns_to_drop, columns_to_check, disable_feedback=True)


preprocessed_df = analysis_tool.get_data_frame()
print(preprocessed_df)


summary = analysis_tool.get_statistical_summary()
print(summary)







from PlottingTool import PlottingTool


# Create object
plotting_tool = PlottingTool()


# Add preprocessed pandas DataFrame from before
plotting_tool.add_data_set(df_name_berlin, preprocessed_df, disable_feedback=True)

# Add a second time for plotting
df_name_berlin_2 = df_name_berlin+'_2'
plotting_tool.add_data_set(df_name_berlin_2, preprocessed_df, disable_feedback=True)

## Plot added pandas DataFrames in various ways

plotting_tool.plot_interactive({
    df_name_berlin: ['date', 'temperature_2m_max'],
    df_name_berlin_2: ['date', 'rain_sum']})

plotting_tool.plot_univariate_graphs(df_name_berlin, number_columns_unvariate_graphs=4)


# In this example the columns used for plotting bivariate graphs
# are the same as the ones to keep
# plotting_tool.plot_bivariate_graphs(df_name_berlin, numeric_variables=columns_to_check)

plotting_tool.plot_correlation_heatmap(df_name_berlin, numeric_variables=columns_to_check)


# Create a regression model 

target_variable = 'precipitation_sum'

predictor_variables = ['temperature_2m_max', 
                       'temperature_2m_min', 
                       'daylight_duration']

regression_model_summary = plotting_tool.get_regression_model_summary(df_name_berlin, target_variable, predictor_variables, disable_feedback=True)
print(type(regression_model_summary))


