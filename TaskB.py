import requests
type_response=requests.get("https://pokeapi.co/api/v2/type/?name").json() #dictionary, to be filtered by keys
types=[]
for x in type_response["results"]: #each x in the list type_response["results"] is a dictionary with keys "name", "url"
    types.append(x["name"])
#types=['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy', 'stellar', 'unknown']
#can ignore "unknown" and "stellar" types, so
del types[-2:]
#types=['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy']
#'normal' will be the first row from the bottom (as defender) then move up with other types next in index, and the first column from the left (as attacker) then move right with other types next in index
#immunity: type takes 0 damage from another type, denoted by '0'
#resistance: type takes half damage from another type, denoted by '0.5'
#neutral: type takes unchanged damage from another type, denoted by '1'
#weakness: type takes double damage from another type, denoted by '2'
entry=[]
type_immunity=['']*len(types)
type_resistance=['']*len(types)
type_weakness=['']*len(types)
arr=[[1.0]*len(types) for z in range(len(types))] #the 2D array
for i in range (len(types)):
    x=types[i]
    data=requests.get(f"https://pokeapi.co/api/v2/type/{x}").json()
    if data["damage_relations"]["no_damage_from"]:
        for ele in data["damage_relations"]["no_damage_from"]:
            entry.append(ele["name"])
        type_immunity[i]=entry
        entry=[]
    if data["damage_relations"]["half_damage_from"]:
        for ele in data["damage_relations"]["half_damage_from"]:
            entry.append(ele["name"])
        type_resistance[i]=entry
        entry=[]
    if data["damage_relations"]["double_damage_from"]:
        for ele in data["damage_relations"]["double_damage_from"]:
            entry.append(ele["name"])
        type_weakness[i]=entry
        entry=[]
#type_immunity=[['ghost'], '', ['ground'], '', ['electric'], '', '', ['normal', 'fighting'], ['poison'], '', '', '', '', '', '', '', ['psychic'], ['dragon']]
#type_resistance=['', ['rock', 'bug', 'dark'], ['fighting', 'bug', 'grass'], ['fighting', 'poison', 'bug', 'grass', 'fairy'], ['poison', 'rock'], ['normal', 'flying', 'poison', 'fire'], ['fighting', 'ground', 'grass'], ['poison', 'bug'], ['normal', 'flying', 'rock', 'bug', 'steel', 'grass', 'psychic', 'ice', 'dragon', 'fairy'], ['bug', 'steel', 'fire', 'grass', 'ice', 'fairy'], ['steel', 'fire', 'water', 'ice'], ['ground', 'water', 'grass', 'electric'], ['flying', 'steel', 'electric'], ['fighting', 'psychic'], ['ice'], ['fire', 'water', 'grass', 'electric'], ['ghost', 'dark'], ['fighting', 'bug', 'dark']]
#type_weakness=[['fighting'], ['flying', 'psychic', 'fairy'], ['rock', 'electric', 'ice'], ['ground', 'psychic'], ['water', 'grass', 'ice'], ['fighting', 'ground', 'steel', 'water', 'grass'], ['flying', 'rock', 'fire'], ['ghost', 'dark'], ['fighting', 'ground', 'fire'], ['ground', 'rock', 'water'], ['grass', 'electric'], ['flying', 'poison', 'bug', 'fire', 'ice'], ['ground'], ['bug', 'ghost', 'dark'], ['fighting', 'rock', 'steel', 'fire'], ['ice', 'dragon', 'fairy'], ['fighting', 'bug', 'fairy'], ['poison', 'steel']]
for i in range (len(types)):
    if type_immunity[i]!='':
        for ele in type_immunity[i]:
            j=types.index(ele)
            arr[len(types)-1-i][j]=0.0
    if type_resistance[i]!='':
        for ele in type_resistance[i]:
            j=types.index(ele)
            arr[len(types)-1-i][j]=0.5
    if type_weakness[i]!='':
        for ele in type_weakness[i]:
            j=types.index(ele)
            arr[len(types)-1-i][j]=2.0
for i in range(len(types)):
    print(f"{types[len(types)-1-i][0:3]}: {arr[i]}")
print("      ",end='')
for i in range(len(types)):
    print(types[i][0:4],end=' ')