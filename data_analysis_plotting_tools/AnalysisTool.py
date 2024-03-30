
"""Tool to facilitate data set analysis."""

import pandas as pd

pd.options.mode.chained_assignment = None # disable warning



class AnalysisTool:
    """Tool to facilitate data set analysis."""

    def __init__(self,
                 city_name: str,
                 pandas_data_frame: pd.DataFrame) -> None:
        """Add a data set. Input must be a pandas DataFrame.
        
        Parameters
        ----------
        city_name : str
            Name to give the data set.
        pandas_data_frame : pd.DataFrame
            Pandas DataFrame to be analyzed.

        Returns
        -------
        None.

        """

        self.city_name = city_name
        self.pandas_df = pandas_data_frame

        self.columns_to_drop = None
        self.columns_to_check = None

        self.create_file = None
        self.disable_feedback = None

    def preprocess_data_set(self,
                            columns_to_drop: list[str],
                            columns_to_check: list[str],
                            create_file: bool = False,
                            disable_feedback: bool = False) -> None:
        """Specify the columns to be dropped based on the statistical summary.
        
        Parameters
        ----------
        columns_to_drop : list[str]
            Choose which numeric variables to remove.
        columns_to_check : list[str]
            Choose which numeric variables to analyze.
        create_file : bool
            Whether to create a csv file of the preprocessed data set or not.
        disable_feedback : bool
            Whether to print feedbacks, like data set previews, into the console.

        Returns
        -------
        None.

        """

        self.columns_to_drop = columns_to_drop
        self.columns_to_check = columns_to_check

        self.create_file = create_file
        self.disable_feedback = disable_feedback

        if not self.disable_feedback:
            print(f"Processing data for {self.city_name}...")

        self._clean_and_preprocess()

    def _clean_and_preprocess(self) -> None:
        """
        Private Method.
        Cleans the data set.
        """

        # Drop specified columns
        self.pandas_df.drop(columns=self.columns_to_drop, axis=1, inplace=True)
        # Remove outliers
        self._remove_outliers()
        # Fix inconsistencies
        self._fix_inconsistencies()
        # Create file
        if self.create_file:
            self.pandas_df.to_csv(f'{self.city_name}_cleaned_data.csv', index=False)

    def _remove_outliers(self) -> None:
        """
        Private Method.
        Removes outliers in the data set.
        """

        for column in self.columns_to_check:
            q1 = self.pandas_df[column].quantile(0.25)
            q3 = self.pandas_df[column].quantile(0.75)
            iqr = q3 - q1

            outliers = self.pandas_df[(self.pandas_df[column] < q1 - 1.5 * iqr) | (self.pandas_df[column] > q3 + 1.5 * iqr)]

            if not self.disable_feedback:
                print(f"Outliers in '{column}':")
                print(outliers[['date', column]])

            self.pandas_df = self.pandas_df[~((self.pandas_df[column] < q1 - 1.5 * iqr) | (self.pandas_df[column] > q3 + 1.5 * iqr))]

        if not self.disable_feedback:
            print("After Fixing the Outliers:")
            print(self.pandas_df.head())

    def _fix_inconsistencies(self) -> None:
        """
        Private Method.
        Fixes inconsistent values in the data set.
        """

        missing_values_summary = self.pandas_df[self.columns_to_check].isnull().sum()

        if not self.disable_feedback:
            print("Missing Values Summary:")
            print(missing_values_summary)

        self.pandas_df[self.columns_to_check] = self.pandas_df[self.columns_to_check].fillna(self.pandas_df[self.columns_to_check].mean())

        if not self.disable_feedback:
            print("\nDataFrame after fixing missing values:")
            print(self.pandas_df.head())

    def get_statistical_summary(self) -> pd.DataFrame:
        """Returns a statistical summary of the preprocessed data set. 
        
        Parameters
        ----------
        None.

        Returns
        -------
        pandas DataFrame.
        
        """
        return self.pandas_df.describe(include='all')

    def get_data_frame(self) -> pd.DataFrame:
        """Returns the preprocessed data set as pandas DataFrame.
        
        Parameters
        ----------
        None.

        Returns
        -------
        pandas DataFrame.

        """
        return self.pandas_df
