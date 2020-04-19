import json

DEFAULT_MESSAGE = {}

def save(value, module):
    with open(f'config/jsons/{module}.json', 'w', encoding= 'utf-8') as f:
        return json.dump(value, f, ensure_ascii=False, indent=4)

def load(module):
    try:
        with open(f'config/jsons/{module}.json', encoding='utf-8') as f:
            return json.load(f)

    except OSError:
        
        save(DEFAULT_MESSAGE, module)


def save_key(module, key: str, value, key_ = None):
    load_module = load(module)
    if not key_ is None:
        if not load_module.get(key):
            load_module[key] = {}
            
            
            load_module[key][key_] = value
            save(load_module, 'ousama_')

    else:
        if not load_module.get(key):
            load_module[key] = {}
            load_module[key] = value
            save(load_module, module)