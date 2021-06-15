import requests, json

request = requests.get('https://www.canalti.com.br/api/pokemons.json')
pokedex = request.json()

class Formatter:
    def get_types(poke_input):
        types = []
        for type in pokedex['pokemon'][poke_input]['type']:
            types.append(type)
        strtypes = ', '.join(types)
        print(types)
        return strtypes

    def get_weaknesses(poke_input):
        weaks = []
        for weak in pokedex['pokemon'][poke_input]['weaknesses']:
            weaks.append(weak)
        strweaks = ', '.join(weaks)
        return strweaks
    
    def get_photo(poke_input):
        pokephoto = pokedex['pokemon'][poke_input]['img']
        return pokephoto

    def get_prev_evolutions(poke_input):
        prevevo = []       
        try:
            for evo in pokedex['pokemon'][poke_input]['prev_evolution']:
                prevevo.append(evo['name'])
            strprevevo = ", ".join(prevevo)
            return (strprevevo)
        except KeyError as k:
            return ('No previous evolution.')
    
    def get_next_evolutions(poke_input):    
        nextevo = []
        try:
            for evo in pokedex['pokemon'][poke_input]['next_evolution']:
                nextevo.append(evo['name'])
            strnextevo = ", ".join(nextevo)
            return (strnextevo)
        except KeyError as k:
            print ('Final Evolution.')
