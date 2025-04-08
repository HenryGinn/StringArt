import matplotlib.colors as mcolors


colors = set(list(mcolors.TABLEAU_COLORS.keys()) +
              list(mcolors.CSS4_COLORS.keys()) +
              list(mcolors.XKCD_COLORS.keys()))

hex_characters = list(range(1, 11)) + ["A", "B", "C", "D", "E", "F"]

def get_color_input(prompt):
    input_valid = False
    while not input_valid:
        input_valid, color_input = do_get_color_input(prompt)
    return color_input

def do_get_color_input(prompt):
    color_input = str(input(prompt))
    if is_color_valid(color_input):
        return True, color_input
    else:
        print("\nSorry, that is not a valid color. Try again")
        return False, None

def is_color_valid(color_input):
    if color_not_named(color_input):
        if color_not_hex(color_input):
            return False
    return True

def color_not_named(color_input):
    color_not_in_named_list = (color_input not in colors)
    return color_not_in_named_list

def color_not_hex(color_input):
    if len(color_input) != 7:
        return True
    if color_input[0] != "#":
        return True
    return color_not_hex_characters(color_input)

def color_not_hex_characters(color_input):
    for character in color_input[1:]:
        if character not in hex_characters:
            return True
    return False
