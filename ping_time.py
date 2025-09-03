import requests
import time

def ping_timer(func):
    """
    Decorator that measures and prints the execution time of the decorated function
    in seconds and milliseconds.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.time()
            ping_time = end_time - start_time
            print(f"\nRequest completed in {ping_time:.2f} OR {ping_time *1000:.2f} ms\n")
        return result
    return wrapper


@ping_timer
def ping_request():
    """
    Prompts the user for a website address, sends a GET request, and prints the status code,
    resolved URL, and content size. Returns a tuple of (status_code, url).
    If the request fails, prints an error and returns (None, url).
    """
    user_input = input("Enter a website address:").strip()

    # Ensure the user input is a valid URL
    if not user_input.startswith(("http://", "https://")):
        user_input = "https://" + user_input

    try:
        response = requests.get(user_input, timeout=5)
        print(f"\nStatus code is : {response.status_code}")
        print(f"Website exact URL is : {response.url}")
        print(f"Content size is : {len(response.content)} bytes")
        return response.status_code, response.url
    
    except requests.exceptions.RequestException as e:
        print(f"Error : Couldn't reach the website! ({e})")
        # Ensure trailing slash for consistency with successful requests
        if not user_input.endswith("/"):
            user_input += "/"
        return None, user_input

    
if __name__ == "__main__":
    ping_request()
