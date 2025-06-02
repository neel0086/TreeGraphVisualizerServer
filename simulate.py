import sys
import json

sys.setrecursionlimit(10000)

# Read the full Python function from stdin
code_input = sys.stdin.read()

# Define containers to store tree information
nodes = []
edges = {}
labels = {}
node_id_counter = [0]  # Mutable container to keep track inside inner function

# Global trace function
def trace_calls(frame, event, arg):
    if event != 'call':
        return

    func_name = frame.f_code.co_name
    args = frame.f_locals

    # Assign a new node ID for this call
    curr_id = node_id_counter[0]
    node_id_counter[0] += 1
    nodes.append(curr_id)

    # Label it like func(3) or fib(3)
    arg_str = ", ".join(f"{k}={v}" for k, v in args.items())
    labels[curr_id] = f"{func_name}({arg_str})"

    # Attach to parent if any
    parent_id = getattr(trace_calls, 'current', None)
    if parent_id is not None:
        if parent_id not in edges:
            edges[parent_id] = []
        edges[parent_id].append(curr_id)

    # Set current node as parent for children
    trace_calls.current = curr_id

    def local_trace(frame, event, arg):
        return local_trace

    return trace_calls

# Prepare the execution environment
exec_globals = {}
exec_locals = {}

try:
    # Compile and execute the code to define the function
    exec(code_input, exec_globals, exec_locals)

    # Get the user-defined function name (first function)
    func_name = [k for k in exec_locals if callable(exec_locals[k])][0]
    user_func = exec_locals[func_name]

    # Set the tracer
    import sys
    sys.settrace(trace_calls)

    # Call the user function (hardcoded example for now)
    user_func(3)

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
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
