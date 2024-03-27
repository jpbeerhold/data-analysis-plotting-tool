:py:mod:`data_analysis_plotting_tools.PlottingTool`
===================================================

.. py:module:: data_analysis_plotting_tools.PlottingTool

.. autoapi-nested-parse::

   Module to plot the data set.

   ..
       !! processed by numpydoc !!


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   data_analysis_plotting_tools.PlottingTool.PlottingTool




.. py:class:: PlottingTool


   
   Tool to simplify data set plotting.
















   ..
       !! processed by numpydoc !!
   .. py:method:: __start_local_bokeh_server(bkapp) -> None

      
      Private Method.
      Starts Bokeh to run in Browser.
















      ..
          !! processed by numpydoc !!

   .. py:method:: __get_random_color_code() -> str

      
      Private Method.
      Returns random hexadecimal color code.
















      ..
          !! processed by numpydoc !!

   .. py:method:: __is_date(string: str, fuzzy: bool = False)

      
      Private Method.
      Return whether the string can be interpreted as a date.

      :param string: str, string to check for date
      :param fuzzy: bool, ignore unknown tokens in string if True















      ..
          !! processed by numpydoc !!

   .. py:method:: add_data_set(df_name: str, data_frame: pandas.DataFrame, disable_feedback: bool = False) -> None

      
      Add a data set to be used.

      :param df_name: Name to give the data set.
      :type df_name: str
      :param data_frame: Data set as pandas DataFrame.
      :type data_frame: pd.DataFrame
      :param disable_feedback: Decide whether a confirmation message should be displayed or not.
      :type disable_feedback: bool

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: plot_interactive(data_frames: dict) -> None

      
      Plot data sets on a preset 2D interactive chart.

      :param data_frames: Specifies the data sets and columns to use. First mentioned column will be on x-axis.
                          Columns specified as x-axis must be exactly the same.
                              Example:
                              {'berlin': ['date', 'rain_sum'], 'paris': ['date', 'temperature']}
      :type data_frames: dict

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: plot_univariate_graphs(df_name: str, number_columns_unvariate_graphs: int) -> None

      
      Plot an univariate pairplot from the numeric variables in the data set.

      :param df_name: Name of the data set to be plotted.
      :type df_name: str
      :param number_columns_unvariate_graphs: Decide on how many rows the plots should be displayed.
      :type number_columns_unvariate_graphs: int

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: plot_bivariate_graphs(df_name: str, numeric_variables: list[str]) -> None

      
      Plot a bivariate pairplot from the numeric variables in the data set.

      :param df_name: Name of the data set to be plotted.
      :type df_name: str
      :param numeric_variables: Choose numeric variables to plot by entering the name of the variable in the list.
      :type numeric_variables: list[str]

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: plot_correlation_heatmap(df_name: str, numeric_variables: list[str]) -> None

      
      Plot a correlation heatmap using the numeric variables in the data set.

      :param df_name: Name of the data set to be plotted.
      :type df_name: str
      :param numeric_variables: Choose numeric variables to plot by entering the name of the variable in the list.
      :type numeric_variables: list[str]

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: get_regression_model_summary(df_name: str, target_variable: str, predictor_variables: list[str], disable_feedback: bool = False, disable_plotting: bool = False)

      
      Plot a regression model based on variables to be studied.

      :param df_name: Name of the data set to be plotted.
      :type df_name: str
      :param target_variable: Variable to be predicted.
      :type target_variable: str
      :param predictor_variables: Input variables on which the output would be based.
      :type predictor_variables: list[str]
      :param disable_feedback: Whether to print feedbacks, like a model summary, into the console.
      :type disable_feedback: bool
      :param disable_plotting: Whether the regression model should be plotted.
      :type disable_plotting: bool

      :rtype: Model summary.















      ..
          !! processed by numpydoc !!


