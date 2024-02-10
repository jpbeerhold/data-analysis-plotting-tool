
"""Tool to simplify data analysis and plotting."""

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

pd.options.mode.chained_assignment = None # disable warning




class DataAnalysisPlottingTool:
    """Tool to simplify data analysis and plotting."""

    def __init__(self) -> None:
        self.collection_data_sets: dict[pd.DataFrame] = {}

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

    def add_data_set(self, name: str, path: str, disable_feedback: bool = False) -> None:
        """
        Add a dataset to be used later.
        Dataset has to have columns with headers and must be in csv format.
        
        Parameters
        ----------
        name : str
            Name to give the dataset.
        path : str
            Complete path to the file.

        Returns
        -------
        None.

        """
        self.collection_data_sets[name] = pd.read_csv(path)
        if not disable_feedback:
            print(f'Data set "{name}" added!')

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
                # get very first mentioned data set and use first mentioned column
                to_compare_with = self.collection_data_sets[all_names[0]][x_axis_label]
                for i in range(1, len(all_names)):
                    current_very_first_mentioned = data_sets[all_names[i]][0]
                    current_to_compare_with = self.collection_data_sets[all_names[i]][current_very_first_mentioned]
                    if to_compare_with.to_list() != current_to_compare_with.to_list():
                        print(">>> ERROR: Columns mentioned for being on the x-axis must all be exactly the same.")
                        sys.exit()

            def _get_data_set(name: str) -> tuple:
                nonlocal use_datetime
                if name not in all_data_sets:
                    print(f'>>> ERROR: Data set "{name}" not found.')
                    sys.exit()
                else:
                    columns_to_use = data_sets[name]
                    df = self.collection_data_sets[name][columns_to_use]

                    # add empty columns
                    for column in all_columns:
                        if column not in columns_to_use:
                            df[column] = np.nan

                    # convert to datetime
                    to_x_axis = columns_to_use[0]
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

            all_names = sorted(data_sets.keys())
            x_axis_label = data_sets[all_names[0]][0]
            all_columns = [i for l in data_sets.values() for i in l]
            all_data_sets = self.collection_data_sets.keys()

            _check_all()
            data_set_select = Select(options=all_names)

            use_datetime = False
            source = _get_data_set(all_names[0])
            plot = _make_plot()

            plot.xaxis.axis_label = x_axis_label

            data_set_select.on_change('value', _update_plot)

            doc.add_root(layouts.row(plot, data_set_select, sizing_mode='scale_both'))

        self.__start_local_bokeh_server(_bkapp)
