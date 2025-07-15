import pandas as pd
from modules.logger import logging
from modules.exceptions import MentalHealthChatBotException

class DialectDataProcessor:
    def __init__(self, file_path: str):
        """
        Initializes the DialectDataProcessor by loading a DataFrame from an Excel file.

        Args:
            file_path (str): The path to the Excel file containing the dialect data.

        Raises:
            Exception: If there is an error loading the DataFrame.
        """
        # Load the DataFrame
        try:
            self.df = pd.read_excel(file_path, header=None)
            self.df.columns = ['Term', 'Modern Standard Arabic', 'Omani Arabic Dialect']  
            logging.info("DataFrame loaded successfully.")
        except Exception as e:
            logging.exception("Failed to load the DataFrame.")
            raise Exception(f"Error loading data: {str(e)}")

    def get_omani_response(self, input_term: str) -> str:
        """
        Retrieves the Omani Arabic dialect equivalent of a given Modern Standard Arabic term.

        Args:
            input_term (str): The Modern Standard Arabic term to be translated.

        Returns:
            str: The Omani Arabic dialect equivalent if found; otherwise, returns the input term.

        Raises:
            Exception: If there is an error retrieving the term.
        """
        try:
            if input_term in self.df['Modern Standard Arabic'].values:
                result = self.df.loc[self.df['Modern Standard Arabic'] == input_term, 'Omani Arabic Dialect'].values[0]
                logging.info(f"Retrieved Omani Arabic term: {result} for input term: {input_term}")
                return result
            else:
                logging.warning(f"Term not found. Returning input term: {input_term}")
                return input_term  
        except Exception as e:
            logging.exception("Failed to retrieve Omani Arabic term.")
            raise Exception(f"Error retrieving term: {str(e)}")
        