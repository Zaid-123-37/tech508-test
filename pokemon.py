import requests
import json
import random

def get_pokemon_data(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    response = requests.get(url)
    if response.status_code != 200:
        print("Pokémon not found.")
        exit()
    return json.loads(response.text)

def get_random_pokemon():
    poke_id = random.randint(1, 151)  # Original 151
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_id}'
    response = requests.get(url)
    return json.loads(response.text)

def print_stats(pokemon):
    name = pokemon['name'].capitalize()
    height = pokemon['height'] / 10
    weight = pokemon['weight'] / 10
    ability = pokemon['abilities'][0]['ability']['name']
    print(f"\n{name}'s stats:")
    print(f"- Height: {height} m")
    print(f"- Weight: {weight} kg")
    print(f"- Ability: {ability}")
    
def get_stat(pokemon, stat_name):
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return 10  # default fallback

def fight(player_poke, cpu_poke):
    player_hp = get_stat(player_poke, 'hp')
    cpu_hp = get_stat(cpu_poke, 'hp')
    
    player_attack = get_stat(player_poke, 'attack')
    cpu_attack = get_stat(cpu_poke, 'attack')

    player_defense = get_stat(player_poke, 'defense')
    cpu_defense = get_stat(cpu_poke, 'defense')

    print("\n--- Battle Start! ---")
    print(f"{player_poke['name'].capitalize()} vs {cpu_poke['name'].capitalize()}\n")
    
    turn = 0
    while player_hp > 0 and cpu_hp > 0:
        turn += 1
        print(f"--- Turn {turn} ---")
        
        # Player attacks
        damage = int((player_attack / cpu_defense) * random.randint(10, 20))
        cpu_hp -= damage
        print(f"You attack and deal {damage} damage! CPU HP: {max(cpu_hp, 0)}")

        if cpu_hp <= 0:
            print("\n🎉 You win!")
            break

        # CPU attacks
        damage = int((cpu_attack / player_defense) * random.randint(10, 20))
        player_hp -= damage
        print(f"CPU attacks and deals {damage} damage! Your HP: {max(player_hp, 0)}")

        if player_hp <= 0:
            print("\n💀 You lost!")
            break

# --- Main Game ---

# Get Pokémon list and show user some names
print("Fetching Pokémon list...")
url = 'https://pokeapi.co/api/v2/pokemon?limit=20'  # just show first 20 for simplicity
response = requests.get(url)
pokemon_list = json.loads(response.text)['results']

print("\nChoose your Pokémon from this list:")
for poke in pokemon_list:
    print("- " + poke['name'].capitalize())

# Get user's choice
choice = input("\nEnter your Pokémon: ").lower()
player_pokemon = get_pokemon_data(choice)
cpu_pokemon = get_random_pokemon()

# Show stats
print_stats(player_pokemon)
print_stats(cpu_pokemon)

# Start fight
fight(player_pokemon, cpu_pokemon)
