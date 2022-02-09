import glob
import os
import platform
import time
from typing import Dict, List, Optional, Set, Tuple

PATH_OUTPUT_FOLDER: str = "./output"
"""The path to the output folder."""

PATH_INPUT_FOLDER: str = "./input"
"""The path to the input folder."""

INPUT_FILE_EXTENSION: str = ".in"
"""The extension of the inputs files."""

OUTPUT_FILE_EXTENSION: str = ".out"
"""The extension of the output files."""

CLIENT_DATA_LIKED_KEY = "like"
"""The key for the ingredients liked by a customer in a dictionary representing a customer."""

CLIENT_DATA_DISLIKED_KEY = "dislike"
"""The key for the ingredients disliked by a customer in a dictionary representing a customer."""


def readInputData(p_path: str) -> Tuple[List[Dict], Set[str], Set[str]]:
    """Read the input files.

    - The first line contains one integer 1≤C≤10⁵ - the number of potential clients.
    - The following 2xC lines describe the clients’ preferences in the following format:
        - First line contains integer 1≤L≤5, followed by L names of ingredients a client likes, delimited by spaces.
        - Second line contains integer 0≤D≤5, followed by D names of ingredients a client dislikes, delimited by spaces.

    Each ingredient name consists of between 1 and 15 ASCII characters.
    Each character is one of the lowercase letters (a-z) or a digit (0-9).

    The data are sorted and returned in this form:
    - A `list` containing all the customer data. The customer information is represented as a dictionary or:
        - `CLIENT_DATA_LIKED_KEY` is the list of ingredients that the customer likes
        - `CLIENT_DATA_DISLIKED_KEY` is the list of ingredients that the customer dislike.
    - A `set` containing all the liked ingredients.
    - A `set` containing all the disliked ingredients.

    Args:
        p_path (str): the path to the file.

    Returns:
        Tuple[List[Dict], Set[str], Set[str]]: All the information of potential customers, and all the ingredients
                                               (liked then liked).
    """
    with open(p_path, "r") as file:
        client_list: list = list()  # The list of clients
        ingredients_liked_set: set = set()  # The set of the liked ingredients
        ingredients_disliked_set: set = set()  # The set of the disliked ingredients

        # the number of potential clients
        number_client = int(file.readline().strip())

        for client_id in range(number_client):
            client_data: Dict[str, Optional[List[str]]] = {
                CLIENT_DATA_LIKED_KEY: None,
                CLIENT_DATA_DISLIKED_KEY: None,
            }

            # names of ingredients client likes
            ingredients_liked = file.readline().strip().split()
            if int(ingredients_liked[0]) > 0:
                client_data[CLIENT_DATA_LIKED_KEY] = ingredients_liked[1:]
                ingredients_liked_set.update(client_data[CLIENT_DATA_LIKED_KEY])  # type: ignore[arg-type]

            # names of ingredients client dislikes
            ingredients_disliked = file.readline().strip().split()
            if int(ingredients_disliked[0]) > 0:
                client_data[CLIENT_DATA_DISLIKED_KEY] = ingredients_disliked[1:]
                ingredients_disliked_set.update(client_data[CLIENT_DATA_DISLIKED_KEY])  # type: ignore[arg-type]

            client_list.append(client_data)

        return client_list, ingredients_liked_set, ingredients_disliked_set


def writeOutputData(p_ingredients: Set[str], p_path: str) -> None:
    """Write the output data in the file.

    The output consist of one line consisting of a single number 0≤N followed by a list of N ingredients to put on the
    only pizza available in the pizzeria, separated by spaces.

    Args:
        p_ingredients (Set[str]): The `set` of ingredients to write in the file.
        p_path (str): The path to file where write the ingredient.
    """
    with open(p_path, "w") as file:
        file.write("{} {}".format(str(len(p_ingredients)), " ".join(p_ingredients)))


if __name__ == "__main__":
    # clean the terminal automatically
    if platform.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")

    # Create the output folder if not exist
    if not os.path.exists(PATH_OUTPUT_FOLDER):
        os.makedirs(PATH_OUTPUT_FOLDER)

    file_pattern_to_find = PATH_INPUT_FOLDER + "/*" + INPUT_FILE_EXTENSION  # pattern of the file
    # Find all the files in the folder PATH_INPUT_FOLDER whose paterne respects file_pattern_to_find
    # the files are sorted by name
    files_path = sorted(glob.glob(file_pattern_to_find))

    # Executes the program file by file
    for file_index in range(len(files_path)):
        print(80 * "#")
        print("Working on the file:", files_path[file_index])

        # Start the chrono
        start_time = time.time()

        # Read the input data
        clients, liked_ingredient, disliked_ingredient = readInputData(files_path[file_index])

        # File to write: In the PATH_OUTPUT_FOLDER folder, with the name of the input file
        # and the value of OUTPUT_FILE_EXTENSION extension
        file_to_write = (
            PATH_OUTPUT_FOLDER
            + "/"
            + os.path.splitext(files_path[file_index])[0].split("/")[-1]
            + OUTPUT_FILE_EXTENSION
        )
        # Write the output data
        writeOutputData(liked_ingredient, file_to_write)

        # Stop the chrono
        end_time = time.time() - start_time

        print("Total time:", time.strftime("%Hh %Mmin %Ss", time.gmtime(end_time)))
        print(80 * "#" + "\n")
