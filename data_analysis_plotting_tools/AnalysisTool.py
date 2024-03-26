
import pandas as pd

pd.options.mode.chained_assignment = None # disable warning



class AnalysisTool:
    """Tool to simplify data set analysis."""

    def __init__(self,
                 city_name: str,
                 pandas_data_frame: pd.DataFrame) -> None:
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

        self.city_name = city_name
        self.pandas_df = pandas_data_frame

    def preprocess_data_set(self,
                            columns_to_drop: list[str],
                            columns_to_check: list[str],
                            create_file: bool = False,
                            disable_feedback: bool = False) -> None:
        """
        Specify the columns to be dropped based on the statistical summary.
        
        Parameters
        ----------
        columns_to_drop : list[str]
            Explanation here.
        columns_to_check : list[str]
            Explanation here.

        Returns
        -------
        dict.
        Displays the dataframe after the requried columns have been dropped. 

        """

        self.columns_to_drop = columns_to_drop
        self.columns_to_check = columns_to_check

        self.create_file = create_file
        self.disable_feedback = disable_feedback
        
        if not self.disable_feedback:
            print(f"Processing data for {self.city_name}...")
        
        self._clean_and_preprocess()

    def _clean_and_preprocess(self) -> None:
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
        
        for column in self.columns_to_check:
            Q1 = self.pandas_df[column].quantile(0.25)
            Q3 = self.pandas_df[column].quantile(0.75)
            IQR = Q3 - Q1

            outliers = self.pandas_df[(self.pandas_df[column] < Q1 - 1.5 * IQR) | (self.pandas_df[column] > Q3 + 1.5 * IQR)]

            if not self.disable_feedback:
                print(f"Outliers in '{column}':")
                print(outliers[['date', column]])

            self.pandas_df = self.pandas_df[~((self.pandas_df[column] < Q1 - 1.5 * IQR) | (self.pandas_df[column] > Q3 + 1.5 * IQR))]

        if not self.disable_feedback:
            print("After Fixing the Outliers:")
            print(self.pandas_df.head())

    def _fix_inconsistencies(self) -> None:

        missing_values_summary = self.pandas_df[self.columns_to_check].isnull().sum()

        if not self.disable_feedback:
            print("Missing Values Summary:")
            print(missing_values_summary)

        self.pandas_df[self.columns_to_check] = self.pandas_df[self.columns_to_check].fillna(self.pandas_df[self.columns_to_check].mean())

        if not self.disable_feedback:
            print("\nDataFrame after fixing missing values:")
            print(self.pandas_df.head())

    def get_statistical_summary(self) -> pd.DataFrame:
        """
        Statistical summary is presented after pre-processing the data. 
        
        Parameters
        ----------
        None.

        Returns
        -------
        pandas DataFrame.
        
        """
        return self.pandas_df.describe(include='all')

    def get_data_frame(self) -> pd.DataFrame:
        """
        Explanation here.
        
        Parameters
        ----------
        columns_to_drop : list[str]
            Explanation here.
        columns_to_check : list[str]
            Explanation here.

        Returns
        -------
        dict.
        Explanation here.

        """
        return self.pandas_df


