from flask import Flask, jsonify, request
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

total_user_input=[]

@app.route('/get-file-data/<generation>', methods=['GET'])
def get_file_data(generation):
    newGen = generation_switch(generation)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, f'Gen {newGen}.txt')
    with open(file_path, 'r') as f:
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
    api_key = "AIzaSyCsd4MWaVsHJCUQ4MPdGFlaDQYCfAp4PTc"
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
    
def generation_switch(generation):
    if generation == "I":
        return "1"
    elif generation == "II":
        return "2"
    elif generation == "III":
        return "3"
    elif generation == "IV":
        return "4"
    elif generation == "V":
        return "5"
    elif generation == "VI":
        return "6"
    elif generation == "VII":
        return "7"
    elif generation == "VIII":
        return "8"
    elif generation == "IX":
        return "9"
    
def parse_user_input(user_input):
    if len(total_user_input)==4:
        # Assuming total_user_input is a list of strings like ['game_type', 'generation', 'format', 'pokemon']
        game_type = total_user_input[0]
        generation = total_user_input[1]
        format = total_user_input[2]
        pokemon = total_user_input[3]
    else:
        game_type = " "
        generation = " "
        format = " "
        pokemon = " "

    return game_type, generation, format, pokemon


if __name__ == '__main__':
    app.run(port=5000)
