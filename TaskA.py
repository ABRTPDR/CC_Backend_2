import os, requests, json
try:
    print("Enter name of text file to which you want to print output, include .txt:")
    outname=input()
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"pokemons.txt"),'r') as pokemons: #pokemons.txt file must be downloaded in the same folder as this python file
        poke_list=[]
        for line in pokemons:
            poke_list.append(line.replace("\n",'')) #last character of every line is escape seq \n
        outp={}
        for i in poke_list:
            response=requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json() #dictionary, to be filtered by keys
            resp=requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{i}").json()
            name=resp["name"]
            outp[name]={}
            outp[name]["id"]=response["id"]
            outp[name]["abilities"]=[]
            for ele in response["abilities"]:
                outp[name]["abilities"].append(ele["ability"]["name"])
            outp[name]["type"]=[]
            for ele in response["types"]:
                outp[name]["type"].append(ele["type"]["name"])
            outp[name]["is_legendary"]=resp["is_legendary"]
            outp[name]["is_mythical"]=resp["is_mythical"]
        output=json.dumps(outp,sort_keys=True,indent=4)
        output=json.dumps(outp,sort_keys=True,indent=4)
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),outname),'w') as outfile:
            outfile.write(output)
except FileNotFoundError:
    print("Read/write file not found.")