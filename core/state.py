import json
import os

FILE = "data/state.json"

import json
import os

FILE = "data/state.json"

def load_state():
    if not os.path.exists(FILE):
        state = {"objects": []}
        save_state(state)
        return state

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        state = {"objects": []}
        save_state(state)
        return state


def save_state(state):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
def clear_state():
    save_state({"objects": []})
