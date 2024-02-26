
"""Tool to simplify data preprocessing."""


import pandas as pd

pd.options.mode.chained_assignment = None # disable warning




class PreprocessingTool:
    """Tool to simplify data preprocessing."""

    def __init__(self) -> None:
        self.data_set: pd.DataFrame = None

    def add_data_set(self, data_set: pd.DataFrame) -> None:
        """
        Add a data set.
        Input must be a pandas DataFrame.
        
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
        self.data_set = data_set
    
    def remove_columns(self, column_names: list[str]) -> None:
        """
        
        
        Parameters
        ----------
        

        Returns
        -------
        

        """

    def remove_outliers(self) -> None:
        """
        
        
        Parameters
        ----------
        

        Returns
        -------
        

        """

    def get_data_set(self) -> pd.DataFrame:
        """
        Get the data set.
        
        Parameters
        ----------
        None.

        Returns
        -------
        Data set as pd.DataFrame.

        """
        return self.data_set
        
