import sys, json, array
import os

class TLLException(Exception):
    pass

def check(condition, message):
    if not condition:
        raise TLLException(message)

def log(flag, message):
    if flag:
        print(message)

def do_add(env, args):
    check(len(args) == 2, "Operation 'add' requires exactly 2 arguments")
    log(env.get("trace", False), f"adding {args[0]} and {args[1]}")
    left = do(env, args[0])
    right = do(env, args[1])
    result = left + right
    log(env.get("trace", False), f"result of add: {result}")
    return result

def do_abs(env, args):
    check(len(args) == 1, "Operation 'abs' requires exactly 1 argument")
    val = do(env, args[0])
    result = abs(val)
    log(env.get("trace", False), f"result of abs: {result}")
    return result

def do_get(env, args):
    check(isinstance(args, str) or len(args) == 1, "Argument must be a string, or a list with one element")
    check(args in env if isinstance(args, str) else args[0] in env, "args is not present in env")
    result = env[args if isinstance(args, str) else args[0]]

    log(env.get("trace", False), f"result of get: {result}")
    return result

def do_set(env, args):
    check(len(args) == 2, "Operation 'set' requires exactly 2 arguments")
    check(isinstance(args[0], str), "First argument must be a string")
    value = do(env, args[1])
    env[args[0]] = value
    log(env.get("trace", False), f"set {args[0]} to {value}")
    return value

def do_seq(env, args):
    check(len(args) > 0, "Operation 'seq' requires at least 1 argument")
    for item in args:
        result = do(env, item)
    log(env.get("trace", False), f"result of seq: {result}")
    return result

def do_array(env, args):
    check(len(args) == 1, "Operation 'array' requires exactly 1 argument")
    dim = do(env, args[0])
    result = array.array('b', [0 for _ in range(dim)])
    log(env.get("trace", False), f"created array of size {dim}")
    return result

def do_get_array(env, args):
    check(len(args) == 2, "Operation 'get_array' requires exactly 2 arguments")
    import pdb; pdb.set_trace()
    check(type(args[0]) is str, "First argument must be a string")
    index = do(env, args[1])
    array = do_get(env, args[0])
    value = array[:index]
    log(env.get("trace", False), f"get_array at index {index}: {value}")
    return value

def do_set_array(env, args):
    check(len(args) == 3, "Operation 'set_array' requires exactly 3 arguments")
    check(type(args[0]) is str, "First argument must be a string")
    index = do(env, args[1])
    value = do(env, args[2])
    array = do_get(env, args[0])
    array[index] = value
    log(env.get("trace", False), f"set_array at index {index} to {value}")
    return array

def do_print(env, args):
    check(len(args) == 2, "print function wait for two args , name and value")
    value = do(env, args[1])
    log(env.get("trace", False), f"printing: {args[0]} {value}")
    print(f"{args[0]} {value}")

def do_repeat(env, args):
    check(len(args) == 2, "the number of args to iter is 2")
    iteration = do(env, args[0])
    log(env.get("trace", False), f"repeating {iteration} times")
    for iter_ in range(iteration):
        do(env, args[1])

def do_if(env, args):
    check(len(args) == 3, "if statement has to have exactly 3 element")
    result_condition = do(env, args[0])
    log(env.get("trace", False), f"if condition: {result_condition}")
    if result_condition:
        do(env, args[1])
    else:
        do(env, args[2])

def do_leq(env, args):
    check(len(args) == 2, "need two args to be comparred")
    right = do(env, args[0])
    left = do(env, args[1])
    result = right == left
    log(env.get("trace", False), f"leq comparison: {right} == {left} -> {result}")
    return result

OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

def do(env, expr):
    
    if isinstance(expr, int):
        return expr
    check(isinstance(expr, list), "Expression must be a list")
    check(expr[0] in OPS, f"Unknown operation {expr[0]}")
    func = OPS[expr[0]]
    log(env.get("trace", False), f"executing operation: {expr[0]}")
    return func(env, expr[1:])

def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--trace', action='store_true')
    parser.add_argument('-file_name', default='data_debuug.json')

    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, args.file_name)

    with open(file_path, "r") as reader:
        program = json.load(reader)

    env= {}
    try:
        result = do(env, program)
        print(f"=> {result}")
    except TLLException as e:
        print(f"error ; {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()