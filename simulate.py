import sys
import ast
import json
import builtins

sys.setrecursionlimit(10000)

call_id = 0
edges = []
nodes = []
ignored_first_call = False  # track first <module> call


call_stack = []


def trace_calls(frame, event, arg):
    global call_id, edges, nodes, ignored_first_call, call_stack

    if event == 'call':
        code = frame.f_code
        func_name = code.co_name

        if not ignored_first_call and func_name == '<module>':
            ignored_first_call = True
            return trace_calls

        args = frame.f_locals
        call_id += 1
        node_id = f"{func_name}_{call_id}"

        try:
            arg_str = ", ".join(repr(v) for v in args.values())
        except Exception:
            arg_str = "..."

        nodes.append({
            "id": node_id,
            "label": f"{func_name}({arg_str})"
        })

        if call_stack:
            edges.append({"from": call_stack[-1], "to": node_id})

        call_stack.append(node_id)

    elif event == 'return':
        if call_stack:
            node_id = call_stack.pop()
            for node in nodes:
                if node["id"] == node_id:
                    try:
                        node["return"] = repr(arg)
                    except Exception:
                        node["return"] = "<unrepresentable>"
                    break

    return trace_calls


def run_user_code(code: str):
    global call_id, edges, nodes
    # Reset state
    call_id = 0
    edges = []
    nodes = []
    trace_calls.last_id = None
    globals_dict = {}

    try:
        compiled = compile(code, "<string>", "exec")
        sys.settrace(trace_calls)
        exec(compiled, globals_dict)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    finally:
        sys.settrace(None)

    print(json.dumps({"nodes": nodes, "edges": edges}))


if __name__ == "__main__":
    code_input = sys.stdin.read()
    run_user_code(code_input)
