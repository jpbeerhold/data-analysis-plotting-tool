
"""Tool to simplify data analysis."""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm

pd.options.mode.chained_assignment = None # disable warning



class AnalysisTool:
    """Tool to simplify data analysis."""

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

    def process_data_for_cities(self,
                                columns_to_drop: list[str],
                                columns_to_check: list[str],
                                numeric_variables: list[str],
                                target_variable: str,
                                predictor_variables: list[str],
                                number_columns_unvariate_graphs: int,
                                create_file: bool = True,
                                disable_feedback: bool = False,
                                disable_plotting: bool = False) -> dict:
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

        self.columns_to_drop = columns_to_drop
        self.columns_to_check = columns_to_check
        self.numeric_variables = numeric_variables

        self.target_variable = target_variable
        self.predictor_variables = predictor_variables

        self.number_columns_unvariate_graphs = number_columns_unvariate_graphs

        self.create_file = create_file
        self.disable_feedback = disable_feedback
        self.disable_plotting = disable_plotting
        
        if not self.disable_feedback:
            print(f"Processing data for {self.city_name}...")
        
        self._clean_and_preprocess()
        analysis_result = self._analyze_and_return_result()
        
        return analysis_result

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

    def _analyze_and_return_result(self) -> dict:
        
        result = {}
        result['statistical_summaries'] = self._display_statistical_summaries()
        result['regression_model'] = self._build_regression_model()
        
        if not self.disable_plotting:
            self._univariate_graphs()
            self._bivariate_plots()
            self._correlation_heatmap()
        
        return result

    def _display_statistical_summaries(self) -> pd.DataFrame:
        statistical_summaries = self.pandas_df.describe(include='all')
        if not self.disable_feedback:
            print('Statistical summaries for all variables:')
            print(statistical_summaries)
        return statistical_summaries

    def _univariate_graphs(self) -> None:
        num_columns = self.pandas_df.select_dtypes(exclude='object').columns
        nRows = len(num_columns) // self.number_columns_unvariate_graphs + 1
        fig, axes = plt.subplots(nRows, self.number_columns_unvariate_graphs, figsize=(25, 25))
        for ind, col in enumerate(num_columns):
            sns.histplot(x=col, bins=15, data=self.pandas_df, ax=axes.flatten()[ind])
        plt.show()

    def _bivariate_plots(self) -> None:
        numeric_df = self.pandas_df[self.numeric_variables]
        sns.PairGrid(numeric_df)
        plt.show()

    def _correlation_heatmap(self) -> None:
        numeric_df = self.pandas_df[self.numeric_variables]
        correlation_matrix = numeric_df.corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap of Numeric Variables')
        plt.show()

    def _build_regression_model(self):

        for col in self.predictor_variables:
            if col not in self.pandas_df.columns:
                print(f"Column '{col}' not found in the DataFrame.")

        model_df = self.pandas_df[[self.target_variable] + self.predictor_variables]
        train_data, test_data = train_test_split(model_df, test_size=0.2, random_state=42)
        X_train = sm.add_constant(train_data[self.predictor_variables])
        y_train = train_data[self.target_variable]
        model = sm.OLS(y_train, X_train).fit()

        if not self.disable_feedback:
            print(model.summary())

        X_test = sm.add_constant(test_data[self.predictor_variables])
        y_pred = model.predict(X_test)
        mse = mean_squared_error(test_data[self.target_variable], y_pred)
        
        if not self.disable_feedback:
            print(f"\nMean Squared Error on Test Set: {mse}")

        if not self.disable_plotting:
            plt.scatter(test_data[self.target_variable], y_pred)
            plt.xlabel('Actual Precipitation')
            plt.ylabel('Predicted Precipitation')
            plt.title('Actual vs. Predicted Precipitation')
            plt.show()

        return model.summary()



