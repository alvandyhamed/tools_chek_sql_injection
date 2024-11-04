import itertools
import time
from abc import ABC, abstractmethod


class ExtractStrategy(ABC):
    def __init__(self):
        self.stop_spinner = False
        self.payload_get_number_of_table = ''


    def set_payloads(self, payloads):
        pass

    @abstractmethod
    def get_database_length(self):
        pass

    @abstractmethod
    def get_extract_database_name(self):
        pass

    @abstractmethod
    def get_number_of_tables(self):
        pass

    @abstractmethod
    def extract_table_names(self):
        pass

    @abstractmethod
    def extract_fields_for_table(self):
        pass

    @abstractmethod
    def extract_data(self):
        pass

    def spinner(self):
        """Show a simple spinner."""
        for spin in itertools.cycle('/-\\|'):
            if self.stop_spinner:  # Check if the spinner should stop
                break
            print(f'\r{spin}', end='', flush=True)
            time.sleep(0.2)


class ExtractDataBoolean(ExtractStrategy):
    def __init__(self):
        super().__init__()
        self.set_payloads('and 1=IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE())>',
                          "Test-specific payload2")


class ExtractDataTimbase(ExtractStrategy):
    pass
