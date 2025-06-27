import requests

BASE_URL = "http://localhost:5000/weather"


def format_weather(data):
    print("\nLocation:", data["location"])

    print("Current Weather:")
    print(f"  Temperature: {data['current']['temperature']}°C")
    print(f"  Description: {data['current']['description'].capitalize()}")

    print("Forecast:")
    print(f"  Temperature: {data['forecast']['temperature']}°C")
    print(f"  Description: {data['forecast']['description'].capitalize()}\n")


def main():
    print("Command-Line Weather Tool (Type 'exit' to quit)")

    while True:
        user_input = input("Enter city name or 6-digit Indian PIN code: ").strip()

        if user_input.lower() == "exit":
            print("Closing App")
            break

        if not user_input:
            print("Please enter a valid input.")
            continue

        params = {}
        if user_input.isdigit() and len(user_input) == 6:
            params["pincode"] = user_input
        else:
            params["city"] = user_input

        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                format_weather(response.json())
            else:
                print(f"Error: {response.json().get('error', 'Something went wrong.')}")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")


if __name__ == '__main__':
    main()