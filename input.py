# input_handler.py
import colorama
from colorama import Fore

def get_user_input():
    # Initialize colorama
    colorama.init(autoreset=True)

    while True:
        # Get input from the user in the form of "URL -parameter"
        user_input = input(Fore.CYAN + "Please enter your URL and method (e.g., http://www.hamed.ir -b) or \\q to exit: ").strip()

        # Check if the user wants to quit
        if user_input == "\\q":
            print(Fore.GREEN + "Exiting the program.")
            return None, None  # Return None if the user wants to exit

        # Split the input into parts
        parts = user_input.split()
        # if len(parts) != 2:
        #     print(Fore.RED + "Invalid input format. Please enter in the format: URL -b or URL -t.")
        #     print(Fore.YELLOW + "Enter \\q to exit.")
        #     continue  # Continue the loop to allow the user to try again

        url = parts[0]
        #parameter = parts[1]
        parameter = []
        #
        # # Validate the parameter
        # if parameter not in ["-b", "-t"]:
        #     print(Fore.RED + "Invalid parameter. Use -b for boolean or -t for time base.")
        #     print(Fore.YELLOW + "Enter \\q to exit.")
        #     continue  # Continue the loop to allow the user to try again

        return url, parameter  # Return the valid URL and parameter
