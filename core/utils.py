import json

def load_dict(path : str):
    with open(path, 'r') as file:
        my_dict = json.load(file)
    return my_dict

def save_dict(my_dict : dict, path : str):
    with open(path, 'w') as file:
        json.dump(my_dict, file)