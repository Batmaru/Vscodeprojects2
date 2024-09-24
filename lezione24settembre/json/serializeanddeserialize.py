import json

# dizionario:dict= { "brand": "Ford",
# "electric": False,
# "year": 1964,
# "colors": ["red", "white", "blue"]}



# if type(dizionario_string)==str:
#     print('si')
# else:
#     print('no')

def  Serialize(dict: dict, file_path: str):
    dizionario_string= json.dumps(dict)
    try:
        with open(file_path, 'w') as file:
            file.write(dizionario_string)
        return True
    except Exception as e:
        return False

def Deserialize(file_path: str):
    try:
        with open(file_path, 'r') as file:
            dizionario = json.load(file)  
        return dizionario
    except Exception as e:
        return None
    
dict1={ "brand": "Ford",
"electric": False,
"year": 1964,
"colors": ["red", "white", "blue"]}
prova1= Serialize(dict1,"/home/user/Scrivania/Vscodeprojects2/lezione24settembre/json/prova1.json")
prova2=Deserialize("/home/user/Scrivania/Vscodeprojects2/lezione24settembre/json/prova1.json")
print(prova1)    
print(prova2)