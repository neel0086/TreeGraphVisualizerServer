import sys
import json

sys.setrecursionlimit(10000)

code = sys.stdin.read()

# Define globals for tracking
tree = {
    "nodes": [],
    "edges": {},
    "labels": {},
    "root": None
}
node_id_counter = 0

def trace_calls(func):
    def wrapper(*args):
        global node_id_counter
        current_id = node_id_counter
        node_id_counter += 1

        label = f"{func.__name__}({', '.join(map(str, args))})"
        tree["nodes"].append(current_id)
        tree["labels"][current_id] = label

        if tree["root"] is None:
            tree["root"] = current_id

        children = []
        for result in func(*args):
            children.append(result)

        if children:
            tree["edges"][current_id] = children

        return current_id
    return wrapper

# We'll inject this into the user's code
injected_code = f'''
import json

tree = {{"nodes": [], "edges": {{}}, "labels": {{}}, "root": None}}
node_id_counter = 0

def trace_calls(func):
    def wrapper(*args):
        global node_id_counter
        current_id = node_id_counter
        node_id_counter += 1

        label = f"{{func.__name__}}({{', '.join(map(str, args))}})"
        tree["nodes"].append(current_id)
        tree["labels"][current_id] = label

        if tree["root"] is None:
            tree["root"] = current_id

        children = []
        for result in func(*args):
            children.append(result)

        if children:
            tree["edges"][current_id] = children

        return current_id
    return wrapper

{code}

try:
    root = main()
    output = {{
        "nodes": tree["nodes"],
        "edges": tree["edges"],
        "labels": tree["labels"],
        "root": tree["root"]
    }}
    print(json.dumps(output))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
'''

exec(injected_code)
