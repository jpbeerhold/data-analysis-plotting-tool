
"""Tool to simplify data analysis and plotting."""

from os.path import dirname

import random
import pandas as pd
from dateutil.parser import parse
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource, DataRange1d, Select, Line, LinearAxis, Grid
from bokeh.plotting import figure
from bokeh.palettes import Blues4, Dark2_5
from bokeh.layouts import column, row

pd.options.mode.chained_assignment = None # disable warning




class EasyPlottingTool:
    """Tool to simplify data analysis and plotting."""

    def __init__(self) -> None:
        self.collection_data_sets: dict[pd.DataFrame] = {}

    def __start_local_bokeh_server(self, bkapp) -> None:
        server = Server({'/': bkapp}, num_procs=1)
        server.start()
        if __name__ == '__main__':
            server.io_loop.add_callback(server.show, "/")
            server.io_loop.start()

    def __get_random_color_code(self) -> str:
        return "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

    def __is_date(self, string: str, fuzzy: bool = False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            if type(string) != str: return False
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def add_data_set(self, name: str, path: str) -> None:
        """Add a dataset to be used later.
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

    def plot_interactive(self, data_sets: dict) -> None:
        """Plot data sets on a preset 2D interactive chart.
        
        Parameters
        ----------
        dataset : dict
            Specifies the data sets to use. First mentioned will be on x-axis.
            Columns given as x-axis must be same in every data set.
                Example:
                {'berlin': ['date', 'temperature'], 'paris': ['date', 'temperature']}

        Returns
        -------
        None.

        """

        def _bkapp(doc):

            def _get_data_set(name: str) -> tuple:
                # nonlocal plot
                if name not in all_data_sets:
                    print(f'>>> WARNING: data set "{name}" not found')
                    quit()
                else:
                    # use_datetime = False
                    # get data frame
                    columns_to_use = data_sets[name]
                    df = self.collection_data_sets[name][columns_to_use]
                    # convert to datetime if possible
                    for column in columns_to_use:
                        if self.__is_date(df.at[0, column]):
                            df[column] = pd.to_datetime(df[column])
                            # use_datetime = True
                    # if plot == None:
                    #     if use_datetime:
                    #         plot = figure(x_axis_type="datetime")
                    #     else:
                    #         plot = figure()
                    df.set_index([columns_to_use[0]], inplace=True)
                    df.sort_index(inplace=True)
                    return ColumnDataSource(data=df)

            def _make_plot():
                nonlocal source, plot
                plot = figure(x_axis_type="datetime")
                for name, columns_to_use in data_sets.items():
                    source = _get_data_set(name)
                    for i in range(1, len(columns_to_use)):
                        plot.line(x=columns_to_use[0], y=columns_to_use[i], source=source, color=self.__get_random_color_code())

            def _update_plot(attrname, old, new):
                name = data_set_select.value
                src = _get_data_set(name)
                source.data.update(src.data)

            all_names = sorted(data_sets.keys())
            all_data_sets = self.collection_data_sets.keys()

            data_set_select = Select(options=all_names)

            plot = None
            source = None
            _make_plot()

            data_set_select.on_change('value', _update_plot)

            doc.add_root(row(plot, data_set_select))

        self.__start_local_bokeh_server(_bkapp)


# -> Ziel: bei Auswahl unterschiedlich viele data sets anzeigen können



ds = dirname(__file__)+'/../historical_weather_data/bangkok_2020-01-01_2024-01-27.csv'
ds2 = ds.replace('bangkok', 'paris')

a = EasyPlottingTool()

a.add_data_set('bangkok', ds)
a.add_data_set('paris', ds2)

d = {'bangkok': ['date', 'temperature_2m_max', 'temperature_2m_min'], 'paris': ['date', 'temperature_2m_max']}

a.plot_interactive(data_sets=d)
