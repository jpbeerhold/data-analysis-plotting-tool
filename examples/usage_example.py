# Import Easy-Plotting-Tool

from data_analysis_plotting_tool.main import EasyPlottingTool

## Create new object

ept = EasyPlottingTool()

## Add data sets to Plotting Tool

from os.path import dirname

ds1 = dirname(__file__)+'/../historical_weather_data/data/bangkok_2020-01-01_2024-01-27.csv'
ds2 = ds1.replace('bangkok', 'paris')

ept.add_data_set('bangkok', ds1)
ept.add_data_set('paris', ds2)

# Plot added data sets

data_sets_to_plot = {
    'bangkok': ['date', 'rain_sum'],
    'paris': ['date', 'temperature_2m_max', 'temperature_2m_min']
}

ept.plot_interactive(data_sets_to_plot)