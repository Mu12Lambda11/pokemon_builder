from flask import Flask, jsonify, request
from flask_cors import CORS
import textwrap, os
import google.generativeai as genai

my_api_key= "AIzaSyCsd4MWaVsHJCUQ4MPdGFlaDQYCfAp4PTc"
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-pro')

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
    total_user_input.append(user_input)

    # Extract relevant information from user input (e.g., game type, generation, format, Pokémon)
    game_type, generation, format, pokemon = parse_user_input()

    # Construct the prompt for Gemini
    prompt = f"I want to build a {game_type} Pokémon team for Generation {generation} {format} built around {pokemon}. Please provide me with 5 other Pokémon that complement my choice, and provide sets for all 6 Pokémon on the team."

    if game_type and generation and format and pokemon != ' ':
            response = model.generate_content(prompt)
            generated_text = response.text
            return jsonify(generated_text)
    else: return jsonify("Team is pending")
    
    
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
    
def parse_user_input():
    if len(total_user_input)==4:
        # Assuming total_user_input is a list of strings like ['game_type', 'generation', 'format', 'pokemon']
        game_type = total_user_input[0]
        generation = total_user_input[1]
        format = total_user_input[2]
        pokemon = (total_user_input[3])[6:]
    else:
        game_type = " "
        generation = " "
        format = " "
        pokemon = " "

    return game_type, generation, format, pokemon


if __name__ == '__main__':
    app.run(port=5000)
