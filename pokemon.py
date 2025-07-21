import requests
import json
import random

# Function to fetch a Pokémon's data from the API by name
def get_pokemon_data(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    response = requests.get(url)
    if response.status_code != 200:
        print("Pokémon not found.")
        exit()
    return json.loads(response.text)

# Function to get a random Pokémon (by ID from 1 to 151 - Gen 1 only)
def get_random_pokemon():
    poke_id = random.randint(1, 151)
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_id}'
    response = requests.get(url)
    return json.loads(response.text)

# Function to print basic stats about a Pokémon
def print_stats(pokemon):
    name = pokemon['name'].capitalize()
    height = pokemon['height'] / 10  # Convert from decimeters to meters
    weight = pokemon['weight'] / 10  # Convert from hectograms to kilograms
    ability = pokemon['abilities'][0]['ability']['name']  # Use the first ability
    print(f"\n{name}'s stats:")
    print(f"- Height: {height} m")
    print(f"- Weight: {weight} kg")
    print(f"- Ability: {ability}")

# Function to get a specific stat (like 'attack', 'defense', etc.) from a Pokémon
def get_stat(pokemon, stat_name):
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return 10  # Fallback value in case the stat is missing

# Main battle function where two Pokémon fight until one faints
def fight(player_poke, cpu_poke):
    # Extract key stats for both Pokémon
    player_hp = get_stat(player_poke, 'hp')
    cpu_hp = get_stat(cpu_poke, 'hp')
    player_attack = get_stat(player_poke, 'attack')
    cpu_attack = get_stat(cpu_poke, 'attack')
    player_defense = get_stat(player_poke, 'defense')
    cpu_defense = get_stat(cpu_poke, 'defense')

    print("\n--- Battle Start! ---")
    print(f"{player_poke['name'].capitalize()} vs {cpu_poke['name'].capitalize()}\n")
    
    turn = 0  # Keeps track of battle turns

    # Loop until one Pokémon's HP reaches zero or below
    while player_hp > 0 and cpu_hp > 0:
        turn += 1
        print(f"--- Turn {turn} ---")
        
        # Player attacks CPU
        damage = int((player_attack / cpu_defense) * random.randint(10, 20))
        cpu_hp -= damage
        print(f"You attack and deal {damage} damage! CPU HP: {max(cpu_hp, 0)}")

        # Check if CPU has fainted
        if cpu_hp <= 0:
            print("\n You win!")
            break

        # CPU attacks player
        damage = int((cpu_attack / player_defense) * random.randint(10, 20))
        player_hp -= damage
        print(f"CPU attacks and deals {damage} damage! Your HP: {max(player_hp, 0)}")

        # Check if player has fainted
        if player_hp <= 0:
            print("\n You lost!")
            break

# --- Main Game Flow ---

# Fetch a small list of Pokémon for the player to choose from (limit to first 20)
print("Fetching Pokémon list...")
url = 'https://pokeapi.co/api/v2/pokemon?limit=20'
response = requests.get(url)
pokemon_list = json.loads(response.text)['results']

# Display list of Pokémon names
print("\nChoose your Pokémon from this list:")
for poke in pokemon_list:
    print("- " + poke['name'].capitalize())

# Ask the player to choose their Pokémon
choice = input("\nEnter your Pokémon: ").lower()

# Fetch the chosen Pokémon's data
player_pokemon = get_pokemon_data(choice)

# Randomly generate a CPU Pokémon
cpu_pokemon = get_random_pokemon()

# Display stats for both Pokémon
print_stats(player_pokemon)
print_stats(cpu_pokemon)

# Start the battle!
fight(player_pokemon, cpu_pokemon)
