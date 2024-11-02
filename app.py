

import assciiPrint
from checkforSQLi import checkforSQLi
from input import  get_user_input


def main():
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
    print(f"Method: {method}")
    check_url=checkforSQLi(url)
    if check_url.hasSQLi():
        print(f'Warning: The site may be vulnerable to SQL Injection! Your method is {check_url.get_method()}')
        print(f'Data Base length: {check_url.get_database_length()}')
    else:
        print("The site appears to be secure from SQL Injection.")



if __name__ == "__main__":

    main()