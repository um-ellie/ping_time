import requests
import time

def ping_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.time()
            ping_time = end_time - start_time
            print(f"\nRequest completed in {ping_time:.2f} OR {ping_time *1000:.2f} ms")
        return result
    return wrapper


@ping_timer
def ping_request():
    user_input = input("Enter a website address:").strip()

    if not user_input.startswith(("http://", "https://")):
        user_input = "https://" + user_input

    try:
        response = requests.get(user_input, timeout=5)
        print(f"Status code is : {response.status_code}")
        print(f"Website exact URL is : {response.url}")
        print(f"Content size is : {len(response.content)} bytes")
        return response.status_code, response.url
    
    except requests.exceptions.RequestException as e:
        print(f"Error : Couldn't reach the website! ({e})")
        return user_input
    
if __name__ == "__main__":
    ping_request()
