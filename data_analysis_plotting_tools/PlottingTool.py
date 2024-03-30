
"""Tool to facilitate data set plotting."""

import sys
import random
from threading import Thread
import numpy as np
import pandas as pd
from dateutil.parser import parse
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh import layouts
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

pd.options.mode.chained_assignment = None # disable warning



class PlottingTool:
    """Tool to facilitate data set plotting."""

    def __init__(self) -> None:
        """Tool to facilitate data set plotting.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        self.all_data_sets: dict[str, pd.DataFrame] = {}

    def __start_local_bokeh_server(self, bkapp) -> None:
        """
        Private Method.
        Starts Bokeh to run in Browser.
        """
        def _run():
            server = Server({'/': bkapp}, num_procs=1)
            server.start()
            server.io_loop.add_callback(server.show, "/")
            server.io_loop.start()
        Thread(target=_run).start()

    def __get_random_color_code(self) -> str:
        """
        Private Method.
        Returns random hexadecimal color code.
        """
        return "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

    def __is_date(self,
                  string: str,
                  fuzzy: bool = False):
        """
        Private Method.
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            if not isinstance(string, str):
                return False
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def add_data_set(self,
                     df_name: str,
                     data_frame: pd.DataFrame,
                     disable_feedback: bool = False) -> None:
        """Add a data set to be used.
        
        Parameters
        ----------
        df_name : str
            Name to give the data set.
        data_frame : pd.DataFrame
            Data set as pandas DataFrame.
        disable_feedback : bool
            Decide whether a confirmation message should be displayed or not.

        Returns
        -------
        None.

        """
        self.all_data_sets[df_name] = data_frame
        if not disable_feedback:
            print('Data set added!')
            print(data_frame.head())

    def plot_interactive(self,
                         data_frames: dict) -> None:
        """Plot data sets on a preset 2D interactive chart.
        
        Parameters
        ----------
        data_frames : dict
            Specifies the data sets and columns to use. First mentioned column will be on x-axis.
            Columns specified as x-axis must be exactly the same.
                Example:
                {'berlin': ['date', 'rain_sum'], 'paris': ['date', 'temperature']}

        Returns
        -------
        None.

        """

        def _bkapp(doc):

            def _check_all() -> None:
                # check if data for x-axis is exactly the same due to figure(x_axis_type="datetime")
                # get data set and use first mentioned column
                to_compare_with: pd.Series = self.all_data_sets[all_names[0]][x_axis_label]
                for i in range(1, len(all_names)):
                    current_very_first_mentioned: str = data_frames[all_names[i]][0] # 'date'
                    current_to_compare_with: pd.Series = self.all_data_sets[all_names[i]][current_very_first_mentioned]
                    if to_compare_with.to_list() != current_to_compare_with.to_list():
                        print(">>> ERROR: Columns mentioned for being on the x-axis must all be exactly the same.")
                        sys.exit()

            def _get_data_set(name: str):
                nonlocal use_datetime
                if name not in all_data_sets:
                    print(f'>>> ERROR: Data set "{name}" not found.')
                    sys.exit()
                else:
                    columns_to_use: list = data_frames[name]
                    df: pd.DataFrame = self.all_data_sets[name][columns_to_use]

                    # add empty columns
                    for column in all_columns:
                        if column not in columns_to_use:
                            df[column] = np.nan

                    # convert to datetime
                    to_x_axis: str = columns_to_use[0]
                    if self.__is_date(df.at[0, to_x_axis]):
                        df[to_x_axis] = pd.to_datetime(df[to_x_axis])
                        use_datetime = True

                    df.set_index([to_x_axis], inplace=True)
                    df.sort_index(inplace=True)
                    return ColumnDataSource(data=df)

            def _make_plot():
                # creates and returns Bokeh object
                tools = "pan,wheel_zoom,box_zoom,reset,crosshair,save"
                if use_datetime:
                    plot = figure(x_axis_type="datetime", tools=tools)
                else:
                    plot = figure(tools=tools)
                # add mentioned columns as sources
                for columns_to_use in data_frames.values():
                    for i in range(1, len(columns_to_use)):
                        plot.line(
                            x=columns_to_use[0],
                            y=columns_to_use[i],
                            source=source,
                            color=self.__get_random_color_code(),
                            legend_label=columns_to_use[i])
                return plot

            def _update_plot(attrname, old, new) -> None:
                name = data_set_select.value
                src = _get_data_set(name)
                source.data.update(src.data)

            all_names: list = sorted(data_frames.keys()) # ['bangkok', 'paris']
            x_axis_label: str = data_frames[all_names[0]][0] # 'date'
            all_columns = [i for l in data_frames.values() for i in l]
            all_data_sets = self.all_data_sets.keys()

            _check_all()
            data_set_select = Select(options=all_names)

            use_datetime = False
            source = _get_data_set(all_names[0])
            plot = _make_plot()

            plot.xaxis.axis_label = x_axis_label

            data_set_select.on_change('value', _update_plot)

            doc.add_root(layouts.row(plot, data_set_select, sizing_mode='scale_both'))

        self.__start_local_bokeh_server(_bkapp)

    def plot_univariate_graphs(self,
                               df_name: str,
                               number_columns_unvariate_graphs: int) -> None:
        """Plot an univariate pairplot from the numeric variables in the data set.

        Parameters
        ----------
        df_name : str
            Name of the data set to be plotted.
        number_columns_unvariate_graphs : int
            Decide on how many rows the plots should be displayed. 

        Returns
        -------
        None.

        """
        num_columns = self.all_data_sets[df_name].select_dtypes(exclude='object').columns
        n_rows = len(num_columns) // number_columns_unvariate_graphs + 1
        fig, axes = plt.subplots(n_rows, number_columns_unvariate_graphs, figsize=(25, 25))
        for ind, col in enumerate(num_columns):
            sns.histplot(x=col, bins=15, data=self.all_data_sets[df_name], ax=axes.flatten()[ind])
        plt.show()

    def plot_bivariate_graphs(self,
                              df_name: str,
                              numeric_variables: list[str]) -> None:
        """Plot a bivariate pairplot from the numeric variables in the data set.
        
        Parameters
        ----------
        df_name : str
            Name of the data set to be plotted.
        numeric_variables : list[str]
            Choose numeric variables to plot by entering the name of the variable in the list.

        Returns
        -------
        None. 

        """
        numeric_df = self.all_data_sets[df_name][numeric_variables]
        sns.pairplot(numeric_df)
        plt.show()

    def plot_correlation_heatmap(self,
                                 df_name: str,
                                 numeric_variables: list[str]) -> None:
        """Plot a correlation heatmap using the numeric variables in the data set. 
        
        Parameters
        ----------
        df_name : str
            Name of the data set to be plotted.
        numeric_variables : list[str]
            Choose numeric variables to plot by entering the name of the variable in the list.

        Returns
        -------
        None.

        """
        numeric_df = self.all_data_sets[df_name][numeric_variables]
        correlation_matrix = numeric_df.corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap of Numeric Variables')
        plt.show()

    def get_regression_model_summary(self,
                                     df_name: str,
                                     target_variable: str,
                                     predictor_variables: list[str],
                                     disable_feedback: bool = False,
                                     disable_plotting: bool = False):
        """Plot a regression model based on variables to be studied. 
        
        Parameters
        ----------
        df_name : str
            Name of the data set to be plotted.
        target_variable : str
            Variable to be predicted.
        predictor_variables : list[str]
            Input variables on which the output would be based.
        disable_feedback : bool
            Whether to print feedbacks, like a model summary, into the console.
        disable_plotting : bool
            Whether the regression model should be plotted.
  
        Returns
        -------
        Model summary.

        """

        for col in predictor_variables:
            if col not in self.all_data_sets[df_name].columns:
                print(f"Column '{col}' not found in the DataFrame.")

        model_df = self.all_data_sets[df_name][[target_variable] + predictor_variables]
        train_data, test_data = train_test_split(model_df, test_size=0.2, random_state=42)
        x_train = sm.add_constant(train_data[predictor_variables])
        y_train = train_data[target_variable]
        model = sm.OLS(y_train, x_train).fit()

        if not disable_feedback:
            print(model.summary())

        x_test = sm.add_constant(test_data[predictor_variables])
        y_pred = model.predict(x_test)
        mse = mean_squared_error(test_data[target_variable], y_pred)

        if not disable_feedback:
            print(f"\nMean Squared Error on Test Set: {mse}")

        if not disable_plotting:
            plt.scatter(test_data[target_variable], y_pred)
            plt.xlabel('Actual Precipitation')
            plt.ylabel('Predicted Precipitation')
            plt.title('Actual vs. Predicted Precipitation')
            plt.show()

        return model.summary()
