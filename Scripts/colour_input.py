import matplotlib.colors as mcolors


colours = set(list(mcolors.TABLEAU_COLORS.keys()) +
              list(mcolors.CSS4_COLORS.keys()) +
              list(mcolors.XKCD_COLORS.keys()))

hex_characters = list(range(1, 11)) + ["A", "B", "C", "D", "E", "F"]

def get_colour_input(prompt):
    input_valid = False
    while not input_valid:
        input_valid, colour_input = do_get_colour_input(prompt)
    return colour_input

def do_get_colour_input(prompt):
    colour_input = str(input(prompt))
    if is_colour_valid(colour_input):
        return True, colour_input
    else:
        print("\nSorry, that is not a valid colour. Try again")
        return False, None

def is_colour_valid(colour_input):
    if colour_not_named(colour_input):
        if colour_not_hex(colour_input):
            return False
    return True

def colour_not_named(colour_input):
    colour_not_in_named_list = (colour_input not in colours)
    return colour_not_in_named_list

def colour_not_hex(colour_input):
    if len(colour_input) != 7:
        return True
    if colour_input[0] != "#":
        return True
    return colour_not_hex_characters(colour_input)

def colour_not_hex_characters(colour_input):
    for character in colour_input[1:]:
        if character not in hex_characters:
            return True
    return False
