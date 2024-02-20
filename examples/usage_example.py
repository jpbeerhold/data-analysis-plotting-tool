# Data-Analysis-Plotting-Tool

from main import DataAnalysisPlottingTool


## Add data sets

from os.path import dirname

dapt = DataAnalysisPlottingTool()

ds1 = dirname(__file__)+'/../historical_weather_data/data/bangkok_2020-01-01_2024-01-27.csv'
ds2 = ds1.replace('bangkok', 'paris')

dapt.add_data_set('bangkok', ds1)
dapt.add_data_set('paris', ds2)


# Plot added data sets

data_sets_to_plot = {
    'bangkok': ['date', 'rain_sum'],
    'paris': ['date', 'temperature_2m_max', 'temperature_2m_min']
}

dapt.plot_interactive(data_sets_to_plot)
