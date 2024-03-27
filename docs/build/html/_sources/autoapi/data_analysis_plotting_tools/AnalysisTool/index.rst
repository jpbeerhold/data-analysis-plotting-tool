:py:mod:`data_analysis_plotting_tools.AnalysisTool`
===================================================

.. py:module:: data_analysis_plotting_tools.AnalysisTool

.. autoapi-nested-parse::

   Module to simplify data set analysis.

   ..
       !! processed by numpydoc !!


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   data_analysis_plotting_tools.AnalysisTool.AnalysisTool




.. py:class:: AnalysisTool(city_name: str, pandas_data_frame: pandas.DataFrame)


   
   Tool to simplify data set analysis.
















   ..
       !! processed by numpydoc !!
   .. py:method:: preprocess_data_set(columns_to_drop: list[str], columns_to_check: list[str], create_file: bool = False, disable_feedback: bool = False) -> None

      
      Specify the columns to be dropped based on the statistical summary.

      :param columns_to_drop: Explanation here.
      :type columns_to_drop: list[str]
      :param columns_to_check: Explanation here.
      :type columns_to_check: list[str]
      :param create_file: Whether to create a csv file of the preprocessed data set or not.
      :type create_file: bool
      :param disable_feedback: Whether to print feedbacks, like data set previews, into the console.
      :type disable_feedback: bool

      :rtype: None.















      ..
          !! processed by numpydoc !!

   .. py:method:: _clean_and_preprocess() -> None


   .. py:method:: _remove_outliers() -> None


   .. py:method:: _fix_inconsistencies() -> None


   .. py:method:: get_statistical_summary() -> pandas.DataFrame

      
      Returns a statistical summary of the preprocessed data set.

      :param None.:

      :rtype: pandas DataFrame.















      ..
          !! processed by numpydoc !!

   .. py:method:: get_data_frame() -> pandas.DataFrame

      
      Returns the preprocessed data set as pandas DataFrame.

      :param None.:

      :rtype: pandas DataFrame.















      ..
          !! processed by numpydoc !!


