import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

LIMIT = 1010
URL = "https://www.pokemon.com/us/pokedex/"

data = []
data_json = []

for index in range(1, LIMIT + 1):
    new_url = URL + str(index)
    page = requests.get(new_url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Get Pokémon's name and id
    pokemon_title_element = soup.find("div", class_="pokedex-pokemon-pagination-title").text.strip()
    name = pokemon_title_element[:-5].strip()
    id = int(pokemon_title_element[-4:].strip())
    
    # Get Pokémon's image and description
    pokemon_section = soup.find("section", class_="pokedex-pokemon-details")
    img = pokemon_section.find("img", class_="active")["src"]
    desc = pokemon_section.find("p", class_="version-x").text.strip()
    
    # Get Pokémon's height and weight by first choosing the block that contains these info
    pokemon_ability_info = pokemon_section.find("div", class_="pokemon-ability-info")
    pokemon_size = pokemon_ability_info.find("div", class_="column-7").contents[1].find_all(class_="attribute-value")
    height = pokemon_size[0].text
    weight = pokemon_size[1].text

    # Get Pokémon's abilities
    pokemon_info = pokemon_ability_info.find("div", class_="push-7").contents[1].find_all(class_="attribute-value")
    category = pokemon_info[0].text
    abilities = pokemon_info[1:]
    abilities = list(map(lambda ability: ability.text, abilities))

    # Get Pokémon's type(s)
    pokemon_type_list = soup.find("div", class_="dtm-type").contents[1].find_next_sibling("ul")
    pokemon_type = pokemon_type_list.find_all("li")
    pokemon_type = list(map(lambda type: type.text.strip(), pokemon_type))

    # Get Pokémon's Weaknesses
    pokemon_weaknesses_list = soup.find("div", class_="dtm-weaknesses").contents[1].find_next_sibling("ul")
    pokemon_weaknesses = pokemon_weaknesses_list.find_all("li")
    pokemon_weaknesses = list(map(lambda weakness: weakness.text.strip(), pokemon_weaknesses))

    # Get Pokémon's stats
    pokemon_stats = [] 
    pokemon_stats_block = soup.find("div", class_="pokemon-stats-info").contents[3].find_all("li", class_="meter")
    for pokemon_stats_block_item in pokemon_stats_block:
        pokemon_stats.append(pokemon_stats_block_item["data-value"])
    
    # Map all values into a dictionary
    pokemon_stats_dict = {
        "HP": int(pokemon_stats[0]),
        "Attack": int(pokemon_stats[1]),
        "Defense": int(pokemon_stats[2]),
        "Special Attack": int(pokemon_stats[3]),
        "Special Defense": int(pokemon_stats[4]),
        "Speed": int(pokemon_stats[5])
    }

    data.append([id, name, img, desc, height, weight, category, abilities, pokemon_type, pokemon_weaknesses, pokemon_stats_dict])
    data_json.append({'id': id, 'name': name, 'image-url': img, 'description': desc, 'height': height,
                        'weight': weight, 'category': category, 'abilities': abilities, 'type': pokemon_type,
                        'weaknesses': pokemon_weaknesses, 'stats': pokemon_stats_dict})
    print(f"{index} pokemon is added...")

# Save data in the .csv file using Pandas
df = pd.DataFrame(data, columns=["ID", "Name", "Image URL", "Description", "Height", "Weight", "Categoty", "Abilities", "Type", "Weaknesses", "Stats"])
df.to_csv("pokemon.csv")

jsondict = json.dumps(data_json)
# Save data in the .json file using json package
with open("pokemon.json", "w") as outfile:
    outfile.write(jsondict)

print("Done.")
