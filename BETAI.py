import requests
import json

API_KEY = 'xai-jqAEC5fSalN1lnPTDDOPlOi9UN8pVzLufCPonaXm971eQ2DcgG85LGGiPl6b7ZqMnY54X5e4bmQ8HoBS'

def fetch_parlay_data(sport, wager, desired_payout, num_legs):
    url = 'https://api.x.ai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    prompt = (
        f"Build a betting parlay for {sport} with the following details:\n"
        f"Wager: ${wager}\n"
        f"Desired Payout: ${desired_payout}\n"
        f"Number of Legs: {num_legs}\n"
        f"Include all types of bets: player props, moneyline, spread, over/under."
    )

    data = {
        "model": "grok-beta",  # or the specific model you want to use
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_parlay(parlay_text):
    # This is a simplified parsing example. You might need to adjust based on Grokai's output format.
    parlay_list = parlay_text.split('\n')
    return parlay_list

def main():
    selected_sport = input("Enter the sport you want to bet on: ")
    wager_amount = float(input("How much do you want to wager? "))
    desired_payout = float(input("How much money would you like to receive (minimum)? "))
    num_legs = int(input("How many legs in the parlay? "))

    parlay_text = fetch_parlay_data(selected_sport, wager_amount, desired_payout, num_legs)
    if parlay_text is None:
        print("Failed to retrieve data.")
        return

    parlay_list = parse_parlay(parlay_text)
    print("Generated Parlay:")
    for bet in parlay_list:
        print(bet)

if __name__ == "__main__":
    main()