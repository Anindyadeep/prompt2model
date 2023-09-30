import os
import pyfiglet
from colorama import init, Fore
from typing import Optional

init(autoreset=True)
color_to_id_map = {
    'red': Fore.LIGHTRED_EX,
    'yellow': Fore.YELLOW,
    'blue': Fore.LIGHTCYAN_EX,
    'green': Fore.LIGHTGREEN_EX, 
}

def line_print(input_str: str, color : Optional[str]=None) -> None:
    """Print the given input string surrounded by horizontal lines.

    Args:
        input_str: The string to be printed.
        color: The color of the string that is printed. Defaults to None
    
    Available colors: red, yellow, blue, green
    If no color is choosen, then simply the text will be printed
    """
    if color is not None:
        assert color in list(color_to_id_map.keys()), \
        "Color not available, choose from: red, yellow, blue, green"
        print(color_to_id_map[color] + f"{input_str}")
    else:
        print(f"{input_str}")


def print_logo():
    """Print the logo of Prompt2Model."""
    figlet = pyfiglet.Figlet(width=200)
    # Create ASCII art for each word and split into lines
    words = ["Prompt", "2", "Model"]
    colors = ["red", "green", "blue"]
    ascii_art_parts = [figlet.renderText(word).split("\n") for word in words]
    max_height = max(len(part) for part in ascii_art_parts)
    for part in ascii_art_parts:
        while len(part) < max_height:
            part.append("")
    ascii_art_lines = []
    for lines in zip(*ascii_art_parts):
        colored_line = " ".join(
            color_to_id_map[color] + line for line, color in zip(lines, colors)
        )
        ascii_art_lines.append(colored_line)
    ascii_art = "\n".join(ascii_art_lines)
    term_width = os.get_terminal_size().columns
    centered_ascii_art = "\n".join(
        line.center(term_width) for line in ascii_art.split("\n")
    )
    line_print(centered_ascii_art)


def parse_yaml_and_select_state(status: dict) -> None:
    # Todo:
    # First show the json as it is 
    # Then accordingly parse all the key value and then give the options 
    # Take the option from user side
    # and store it somewhere 
    
    """Format and print a YAML string with colored keys and values.

    Args:
        yaml_str: The YAML string to be formatted and printed.
    """
    line_print("Here is the current status of the all the steps", color='red')
    for key, value in status.items():
        formatted_key = Fore.YELLOW + f"> {key}"
        formatted_value = Fore.LIGHTGREEN_EX + str(value) 
        line = f"{formatted_key}: {formatted_value}"
        print(line)
    print()

    status_dict = {
        "propmt_has_been_parsed": status.get("prompt_has_been_parsed", False),
        "dataset_has_been_retrieved": status.get("dataset_has_been_retrieved", False),
        "model_has_been_retrieved": status.get("model_has_been_retrieved", False),
        "dataset_has_been_generated": status.get("dataset_has_been_generated", False),
        "model_has_been_trained": status.get("model_has_been_trained", False)
    }
    
    key_indices = dict(zip(range(5), list(status_dict.keys())))

    # now provide all these status and let the user choose
    line_print('Choose From which step to start from', color='blue')
    line_print(f"(1)> Parse the prompt: {status_dict['propmt_has_been_parsed']}", color='green')
    line_print(f"(2)> Retrieve the dataset: {status_dict['dataset_has_been_retrieved']}", color='green')
    line_print(f"(3)> Retrieve the model: {status_dict['model_has_been_retrieved']}", color='green')
    line_print(f"(4)> Generate additional synthetic dataset: {status_dict['dataset_has_been_generated']}", color='green')
    line_print(f"(5)> Train the model: {status_dict['model_has_been_trained']}", color='green')

    while True:
        line = input()
        try:
            to_choose = int(line)
            assert to_choose <= 5 and status_dict[key_indices[to_choose-1]] == True
            break 
        except Exception:
            line_print("Invalid Input. Please enter a number and the stage should be marked as True", color='red')
    return to_choose-1


def parse_model_size_limit(line: str, default_size=3e9) -> float:
    """Parse the user input for the maximum size of the model.

    Args:
        line: The user input.
        default_size: The default size to use if the user does not specify a size.
    """
    if len(line.strip()) == 0:
        return default_size
    model_units = {"B": 1e0, "KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12, "PB": 1e15}
    unit_disambiguations = {
        "B": ["b", "bytes"],
        "KB": ["Kb", "kb", "kilobytes"],
        "MB": ["Mb", "mb", "megabytes"],
        "GB": ["Gb", "gb", "gigabytes"],
        "TB": ["Tb", "tb", "terabytes"],
        "PB": ["Pb", "pb", "petabytes"],
    }
    unit_matched = False
    for unit, disambiguations in unit_disambiguations.items():
        for unit_name in [unit] + disambiguations:
            if line.strip().endswith(unit_name):
                unit_matched = True
                break
        if unit_matched:
            break
    if unit_matched:
        numerical_part = line.strip()[: -len(unit_name)].strip()
    else:
        numerical_part = line.strip()
    if not str.isdecimal(numerical_part):
        raise ValueError(
            "Invalid input. Please enter a number (integer " + "or number with units)."
        )
    scale_factor = model_units[unit] if unit_matched else 1
    return int(numerical_part) * scale_factor

