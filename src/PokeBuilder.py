from flask import Flask, jsonify, request
from flask_cors import CORS
import textwrap, os
import google.generativeai as genai

my_api_key= "AIzaSyCsd4MWaVsHJCUQ4MPdGFlaDQYCfAp4PTc"
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)
# User input array is global for easy access
total_user_input=[]

# Function to grab a particular generation file
@app.route('/get-file-data/<generation>', methods=['GET'])
def get_file_data(generation):
    newGen = generation_switch(generation)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, f'Gen {newGen}.txt')
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return jsonify(lines)

# Function to prompt the AI and generate a pokemon team
@app.route('/generate-pokemon-team', methods=['POST'])
def generate_pokemon_team():
    # Extract relevant information from user input (e.g., game type, generation, format, Pokémon)
    game_type, generation, format, pokemon = parse_user_input()

    # Construct the prompt for Gemini
    prompt = f"I want to build a {game_type} Pokémon team for Generation {generation} {format} built around {pokemon}. Please provide me with 5 other Pokémon that complement my choice, and provide sets for all 6 Pokémon on the team. Describe how to use the team."
    if game_type and generation and format and pokemon != '':
        prompt_complete=True
    else:
        prompt_complete=False
    
    if prompt_complete:
        try:
            response = model.generate_content(prompt)
            generated_text = response.text.replace("*","")            
            print(generated_text)

            #Clear all strings
            game_type=game_type.replace(game_type, "")
            generation=generation.replace(generation, "")
            format = format.replace(format, "")
            pokemon =pokemon.replace(pokemon, "")
            total_user_input.clear()

            return jsonify({'generated_text': generated_text})
        except Exception as e:
            print(f"Error fetching team recommendations: {e}")
            return jsonify("Error generating team recommendations")
    else:
        total_user_input.clear()
        return jsonify({'generated_text': "Team could not be generated"})
    
# Function to add user input to the array of total input
@app.route('/add-user-route', methods=['POST'])
def add_user_input():
    user_input = request.json.get('user_input')
    total_user_input.append(user_input)
   
# Function that acts as a switch to convert roman numerals to integers (still a string) 
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

# Function to check the legitimacy of the user's input, and, if possible, initialize or assign local variables    
def parse_user_input():
    if len(total_user_input)==4:
        # Assuming total_user_input is a list of strings like ['game_type', 'generation', 'format', 'pokemon']       
        try:
            #The following code requires initialized variables
            game_type =game_type.replace(game_type,total_user_input[0]) 
            generation =generation.replace(generation,total_user_input[1]) 
            format =format.replace(format,total_user_input[2]) 
            pokemon =pokemon.replace(pokemon,(total_user_input[3])[6:]) 
            
        except:
            # Check for whether the string variables have already been initialized
            game_type = total_user_input[0]
            generation = total_user_input[1]
            format = total_user_input[2]
            pokemon = (total_user_input[3])[6:]
    else:
        game_type = ""
        generation = ""
        format = ""
        pokemon = ""

    return game_type, generation, format, pokemon


if __name__ == '__main__':
    app.run(port=5000)
