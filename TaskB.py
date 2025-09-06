import requests

type_response=requests.get("https://pokeapi.co/api/v2/type/?name").json() #dictionary, to be filtered by keys
types=[]
for x in type_response["results"]: #each x in the list type_response["results"] is a dictionary with keys "name", "url"
    types.append(x["name"].capitalize())
#types=['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy', 'Stellar', 'Unknown']
#can ignore "unknown" and "stellar" types, so
del types[-2:]
#types=['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']
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
            entry.append(ele["name"].capitalize())
        type_immunity[i]=entry
        entry=[]
    if data["damage_relations"]["half_damage_from"]:
        for ele in data["damage_relations"]["half_damage_from"]:
            entry.append(ele["name"].capitalize())
        type_resistance[i]=entry
        entry=[]
    if data["damage_relations"]["double_damage_from"]:
        for ele in data["damage_relations"]["double_damage_from"]:
            entry.append(ele["name"].capitalize())
        type_weakness[i]=entry
        entry=[]
#type_immunity=[['Ghost'], '', ['Ground'], '', ['Electric'], '', '', ['Normal', 'Fighting'], ['Poison'], '', '', '', '', '', '', '', ['Psychic'], ['Dragon']]
#type_resistance=['', ['Rock', 'Bug', 'Dark'], ['Fighting', 'Bug', 'Grass'], ['Fighting', 'Poison', 'Bug', 'Grass', 'Fairy'], ['Poison', 'Rock'], ['Normal', 'Flying', 'Poison', 'Fire'], ['Fighting', 'Ground', 'Grass'], ['Poison', 'Bug'], ['Normal', 'Flying', 'Rock', 'Bug', 'Steel', 'Grass', 'Psychic', 'Ice', 'Dragon', 'Fairy'], ['Bug', 'Steel', 'Fire', 'Grass', 'Ice', 'Fairy'], ['Steel', 'Fire', 'Water', 'Ice'], ['Ground', 'Water', 'Grass', 'Electric'], ['Flying', 'Steel', 'Electric'], ['Fighting', 'Psychic'], ['Ice'], ['Fire', 'Water', 'Grass', 'Electric'], ['Ghost', 'Dark'], ['Fighting', 'Bug', 'Dark']]
#type_weakness=[['Fighting'], ['Flying', 'Psychic', 'Fairy'], ['Rock', 'Electric', 'Ice'], ['Ground', 'Psychic'], ['Water', 'Grass', 'Ice'], ['Fighting', 'Ground', 'Steel', 'Water', 'Grass'], ['Flying', 'Rock', 'Fire'], ['Ghost', 'Dark'], ['Fighting', 'Ground', 'Fire'], ['Ground', 'Rock', 'Water'], ['Grass', 'Electric'], ['Flying', 'Poison', 'Bug', 'Fire', 'Ice'], ['Ground'], ['Bug', 'Ghost', 'Dark'], ['Fighting', 'Rock', 'Steel', 'Fire'], ['Ice', 'Dragon', 'Fairy'], ['Fighting', 'Bug', 'Fairy'], ['Poison', 'Steel']]
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
print()
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type","text/plain")
            self.end_headers()
            query=urlparse(self.path).query
            params=parse_qs(query)
            if len(params)==1:
                identity=list((params.keys()))[0]
                if identity=="attacker":
                    type_input=params["attacker"][0]
                    n=types.index(type_input)
                    x="["
                    for i in range (len(arr)-1,-1,-1):
                        x+=f"{arr[i][n]}, "
                    x=x[:-2]+"]"
                    self.wfile.write(bytes(x,"utf8"))
                elif identity=="defender":
                    type_input=params["defender"][0]
                    x=str(arr[len(arr)-1-(types.index(type_input))])
                    self.wfile.write(bytes(x,"utf8"))
            elif len(params)==2:
                att_type_input=def_type_input=0
                for ele in params:
                    if ele=="attacker":
                        att_type_input=params["attacker"][0]
                    elif ele=="defender":
                        def_type_input=params["defender"][0]
                row=arr[len(arr)-1-(types.index(def_type_input))]
                entry=str(row[types.index(att_type_input)])
                self.wfile.write(bytes(entry,"utf8"))
        except (BrokenPipeError,ConnectionAbortedError) as err:
                print(f"Connection aborted by client: {err}")
        except Exception as err:
                print(f"An unexpected error occurred: {err}")
with HTTPServer(('', 8000),handler) as server:
    print("Server now running!")
    server.serve_forever()