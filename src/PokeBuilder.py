from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/get-file-data', methods=['GET'])
def get_file_data():
    with open('yourfile.txt', 'r') as f:
        lines = f.read().splitlines()
    return jsonify(lines)

@app.route('/generate-pokemon-team', methods=['POST'])
def generate_pokemon_team():
    user_input = request.json.get('user_input')

    # Extract relevant information from user input (e.g., game type, generation, format, Pokémon)
    game_type, generation, format, pokemon = parse_user_input(user_input)

    # Construct the prompt for Gemini
    prompt = f"I want to build a {game_type} Pokémon team for {generation} {format} built around {pokemon}. Please provide me with 5 other Pokémon that complement my choice, and provide sets for all 6 Pokémon on the team."

    # Make an API call to Gemini
    api_url = "https://gemini.googleapis.com/v1/complete"
    api_key = "AIzaSyCsd4MWaVsHJCUQ4MPdGFlaDQYCfAp4PTc"  # Replace with your actual API key
    payload = {
        "prompt": prompt,
        "max_tokens": 150,  # Adjust as needed
        "temperature": 0.7,  # Adjust for creativity vs. coherence
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        generated_text = response.json().get("choices")[0].get("text")
        return jsonify(generated_text)
    except Exception as e:
        print(f"Error fetching team recommendations: {e}")
        return jsonify("Error generating team recommendations")

def parse_user_input(user_input):
    # Implement your logic to extract game type, generation, format, and Pokémon
    # For example, split the input string and extract relevant parts

    if __name__ == '__main__':
        app.run(port=5000)
