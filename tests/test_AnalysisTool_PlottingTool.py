
from os import walk
import pytest
import statsmodels
import pandas as pd
from data_analysis_plotting_tools.AnalysisTool import AnalysisTool
from data_analysis_plotting_tools.PlottingTool import PlottingTool



# Create preprocessed data sets

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

# Read all file names in directory
filenames = next(walk('historical_weather_data/raw_data/'), (None, None, []))[2]

# Create lists to collect results
all_preprocessed = []
all_summaries = []

for file in filenames:
    # Read from every file
    df = pd.read_csv('historical_weather_data/raw_data/'+file)

    # Initialize the AnalysisTool class
    analysis_tool = AnalysisTool('foo', df)

    # Preprocess data sets and append results
    analysis_tool.preprocess_data_set(columns_to_drop, columns_to_check, disable_feedback=True)
    all_preprocessed.append(analysis_tool.get_data_frame())
    all_summaries.append(analysis_tool.get_statistical_summary())


# Run tests on results

@pytest.mark.parametrize("preprocessed_data_frame", [(df) for df in all_preprocessed])
def test_preprocessed(preprocessed_data_frame):
    assert isinstance(preprocessed_data_frame, pd.DataFrame)


@pytest.mark.parametrize("summary", [(s) for s in all_summaries])
def test_preprocessed(summary):
    assert isinstance(summary, pd.DataFrame)




# run tests using preprocessed data sets

@pytest.mark.parametrize("example_data_frame", [(df) for df in all_preprocessed])
def test_plot_data(example_data_frame):
    # Initialize the PlottingTool class
    plotting_tool = PlottingTool()

    # Call the add_data_set method to add the data set
    plotting_tool.add_data_set('foo', example_data_frame, disable_feedback=True)

    target_variable = 'precipitation_sum'

    predictor_variables = ['temperature_2m_max',
                           'temperature_2m_min',
                           'daylight_duration']

    # Get the model summary
    model_summary = plotting_tool.get_regression_model_summary('foo', target_variable, predictor_variables,
                                                               disable_feedback=True, disable_plotting=True)

    # Perform assertion on the result
    assert isinstance(model_summary, statsmodels.iolib.summary.Summary)
