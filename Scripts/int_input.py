import numpy as np
import math


def get_int_input(prompt, lower_bound=None, upper_bound=None):
    lower_bound, upper_bound = get_bounds(lower_bound, upper_bound)
    int_input = get_int_input_with_bounds(prompt, lower_bound, upper_bound)
    return int_input

def get_bounds(lower_bound, upper_bound):
    lower_bound = get_bound(lower_bound, -np.inf)
    upper_bound = get_bound(upper_bound, np.inf)
    check_valid_bounds(lower_bound, upper_bound)
    return lower_bound, upper_bound

def get_bound(bound, default):
    if bound is None:
        bound = default
    return bound

def check_valid_bounds(lower_bound, upper_bound):
    if lower_bound != -np.inf and upper_bound != np.inf:
        if math.floor(upper_bound) - math.ceil(lower_bound) < 0:
            raise Exception(("Bounds do not contain an integer\n"
                             f"Lower bound: {lower_bound}\n"
                             f"Upper bound: {upper_bound}"))

def get_int_input_with_bounds(prompt, lower_bound, upper_bound):
    input_valid = False
    while input_valid is False:
        int_input, input_valid = attempt_get_int_input(prompt, lower_bound, upper_bound)
    return int_input

def attempt_get_int_input(prompt, lower_bound, upper_bound):
    int_input = input(f"{prompt}")
    check_functions, args = get_int_check_functions(lower_bound, upper_bound)
    int_input, input_valid = check_int_valid(int_input, check_functions, args)
    return int_input, input_valid

def get_int_check_functions(lower_bound, upper_bound):
    check_functions = [check_is_integer, check_lower_bound, check_upper_bound]
    args = ([], [lower_bound], [upper_bound])
    return check_functions, args

def check_int_valid(int_input, check_functions, args):
    for check_function, args in zip(check_functions, args):
         if check_function(int_input, *args) is False:
             return None, False
    return int(int_input), True

def check_is_integer(int_input):
    try:
        int(int_input)
        return True
    except:
        return bad_input_response("Sorry, you must enter an integer")

def check_lower_bound(int_input, lower_bound):
    if lower_bound <= int(int_input):
        return True
    else:
        return bad_input_response(f"Sorry, your input must be at least {lower_bound}")

def check_upper_bound(int_input, upper_bound):
    if int(int_input) <= upper_bound:
        return True
    else:
        return bad_input_response(f"Sorry, your input must be at most {upper_bound}")

def bad_input_response(prompt):
    print(prompt)
    return False


