
import sys
import random
import numpy as np
import pandas as pd
from dateutil.parser import parse
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource, DataRange1d, Select, Line, LinearAxis, Grid
from bokeh.plotting import figure
from bokeh.palettes import Blues4, Dark2_5
from bokeh import layouts
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

pd.options.mode.chained_assignment = None # disable warning




class PlottingTool:
    """Tool to simplify data set plotting."""

    def __start_local_bokeh_server(self, bkapp) -> None:
        """
        Private Method.
        Starts Bokeh to run in Browser.
        """
        server = Server({'/': bkapp}, num_procs=1)
        server.start()
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()

    def __get_random_color_code(self) -> str:
        """
        Private Method.
        Returns random hexadecimal color code.
        """
        return "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

    def __is_date(self, string: str, fuzzy: bool = False):
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

    def add_data_set(self, data_set: pd.DataFrame, disable_feedback: bool = False) -> None:
        """
        Add a data set to be used.
        
        Parameters
        ----------
        data_set : pd.DataFrame
            Data set as pandas DataFrame.
        disable_feedback : bool
            Decide whether a confirmation message should be displayed or not.

        Returns
        -------
        None.

        """
        self.pandas_df = data_set
        if not disable_feedback:
            print(f'Data set added!')
            print(data_set.head())

    def plot_interactive(self, data_sets: dict) -> None:
        """
        Plot data sets on a preset 2D interactive chart.
        
        Parameters
        ----------
        dataset : dict
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
                to_compare_with: pd.Series = self.pandas_df[all_names[0]][x_axis_label]
                for i in range(1, len(all_names)):
                    current_very_first_mentioned: str = data_sets[all_names[i]][0] # 'date'
                    current_to_compare_with: pd.Series = self.pandas_df[all_names[i]][current_very_first_mentioned]
                    if to_compare_with.to_list() != current_to_compare_with.to_list():
                        print(">>> ERROR: Columns mentioned for being on the x-axis must all be exactly the same.")
                        sys.exit()

            def _get_data_set(name: str):
                nonlocal use_datetime
                if name not in all_data_sets:
                    print(f'>>> ERROR: Data set "{name}" not found.')
                    sys.exit()
                else:
                    columns_to_use: list = data_sets[name]
                    df: pd.DataFrame = self.pandas_df[name][columns_to_use]

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
                for columns_to_use in data_sets.values():
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

            all_names: list = sorted(data_sets.keys()) # ['bangkok', 'paris']
            x_axis_label: str = data_sets[all_names[0]][0] # 'date'
            all_columns = [i for l in data_sets.values() for i in l]
            all_data_sets = self.pandas_df.keys()

            _check_all()
            data_set_select = Select(options=all_names)

            use_datetime = False
            source = _get_data_set(all_names[0])
            plot = _make_plot()

            plot.xaxis.axis_label = x_axis_label

            data_set_select.on_change('value', _update_plot)

            doc.add_root(layouts.row(plot, data_set_select, sizing_mode='scale_both'))

        self.__start_local_bokeh_server(_bkapp)

    def plot_univariate_graphs(self, number_columns_unvariate_graphs: int) -> None:
        num_columns = self.pandas_df.select_dtypes(exclude='object').columns
        nRows = len(num_columns) // number_columns_unvariate_graphs + 1
        fig, axes = plt.subplots(nRows, number_columns_unvariate_graphs, figsize=(25, 25))
        for ind, col in enumerate(num_columns):
            sns.histplot(x=col, bins=15, data=self.pandas_df, ax=axes.flatten()[ind])
        plt.show()

    def plot_bivariate_graphs(self, numeric_variables: list[str]) -> None:
        numeric_df = self.pandas_df[numeric_variables]
        sns.PairGrid(numeric_df)
        plt.show()

    def plot_correlation_heatmap(self, numeric_variables: list[str]) -> None:
        numeric_df = self.pandas_df[numeric_variables]
        correlation_matrix = numeric_df.corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap of Numeric Variables')
        plt.show()

    def get_regression_model_summary(self,
                             target_variable: str,
                             predictor_variables: list[str],
                             disable_feedback: bool = False,
                             disable_plotting: bool = False) -> None:

        for col in predictor_variables:
            if col not in self.pandas_df.columns:
                print(f"Column '{col}' not found in the DataFrame.")

        model_df = self.pandas_df[[target_variable] + predictor_variables]
        train_data, test_data = train_test_split(model_df, test_size=0.2, random_state=42)
        X_train = sm.add_constant(train_data[predictor_variables])
        y_train = train_data[target_variable]
        model = sm.OLS(y_train, X_train).fit()

        if not disable_feedback:
            print(model.summary())

        X_test = sm.add_constant(test_data[predictor_variables])
        y_pred = model.predict(X_test)
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


