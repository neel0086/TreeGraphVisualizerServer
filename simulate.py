import sys
import json

sys.setrecursionlimit(10000)

try:
    # Read JSON input from Node
    input_data = json.loads(sys.stdin.read())

    code = input_data.get("code", "")
    func_name = input_data.get("funcName", "")
    arg = input_data.get("arg", 0)

    if not code or not func_name:
        raise ValueError("Missing function or name")

    nodes = []
    edges = {}
    labels = {}
    node_id = [0]

    def trace_calls(frame, event, arg_val):
        if event != "call":
            return
        curr_id = node_id[0]
        node_id[0] += 1
        nodes.append(curr_id)
        args = frame.f_locals
        label = f"{frame.f_code.co_name}(" + ", ".join(f"{k}={v}" for k, v in args.items()) + ")"
        labels[curr_id] = label
        parent_id = getattr(trace_calls, 'current', None)
        if parent_id is not None:
            if parent_id not in edges:
                edges[parent_id] = []
            edges[parent_id].append(curr_id)
        trace_calls.current = curr_id
        return trace_calls

    exec_globals = {}
    exec_locals = {}

    exec(code, exec_globals, exec_locals)

    if func_name not in exec_locals:
        raise NameError(f"Function '{func_name}' not defined.")

    sys.settrace(trace_calls)

    # Call the user function with argument (assume single int for now)
    exec_locals[func_name](arg)

    sys.settrace(None)

    result = {
        "nodes": nodes,
        "edges": edges,
        "labels": labels,
        "root": 0
    }

    print(json.dumps(result))

except Exception as e:
    sys.settrace(None)
    print(json.dumps({ "error": str(e) }))
    sys.exit(1)
