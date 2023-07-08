# Pokémon Scraper
Simple Python Web Scraper to get some basic info from the official [Pokémon website](https://www.pokemon.com/us/pokedex).

## JSON Output
An example of the output to the .json file.
``` json
{
    "id": 1,
    "name": "Bulbasaur",
    "image-url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/001.png",
    "description": "There is a plant seed on its back right from the day this Pok\u00e9mon is born. The seed slowly grows larger.",
    "height": "2' 04\"",
    "weight": "15.2 lbs",
    "category": "Seed",
    "abilities": ["Overgrow"],
    "type": ["Grass", "Poison"],
    "weaknesses": ["Fire", "Psychic", "Flying", "Ice"],
    "stats": {
      "HP": 3,
      "Attack": 3,
      "Defense": 3,
      "Special Attack": 4,
      "Special Defense": 4,
      "Speed": 3
    }
  }
```
