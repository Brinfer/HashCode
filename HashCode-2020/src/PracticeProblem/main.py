from random import shuffle
from math import factorial
import os as os
import platform as plt
import tqdm as tqdm


""" Path to text files containing input information . """
PATH_INPUT_FOLDER = "./HashCode-2020/src/PracticeProblem/Input/"
PATH_INPUT_1 = PATH_INPUT_FOLDER + "a_example.in"
PATH_INPUT_2 = PATH_INPUT_FOLDER + "b_small.in"
PATH_INPUT_3 = PATH_INPUT_FOLDER + "c_medium.in"
PATH_INPUT_4 = PATH_INPUT_FOLDER + "d_quite_big.in"
PATH_INPUT_5 = PATH_INPUT_FOLDER + "e_also_big.in"

""" Path to text files containing output information (pizza list) """
PATH_OUTPUT_FOLDER = "./HashCode-2020/src/PracticeProblem/Output/"
PATH_OUTPUT_1 = PATH_OUTPUT_FOLDER + "a_output.txt"
PATH_OUTPUT_2 = PATH_OUTPUT_FOLDER + "b_output.txt"
PATH_OUTPUT_3 = PATH_OUTPUT_FOLDER + "c_output.txt"
PATH_OUTPUT_4 = PATH_OUTPUT_FOLDER + "d_output.txt"
PATH_OUTPUT_5 = PATH_OUTPUT_FOLDER + "e_output.txt"

""" List associating the paths of input and output files. """
LIST_PATH = [[PATH_INPUT_1, PATH_OUTPUT_1],
             [PATH_INPUT_2, PATH_OUTPUT_2],
             [PATH_INPUT_3, PATH_OUTPUT_3],
             [PATH_INPUT_4, PATH_OUTPUT_4],
             [PATH_INPUT_5, PATH_OUTPUT_5]]

""" Dictionary containing ANSII codes to color messages in the terminal. """
COLOR_THEME = {"default":      "\033[0m",
               # Text Color
               "red":          "\033[31m",
               "green":        "\033[32m",
               "yellow":       "\033[33m",
               "magenta":      "\033[35m",
               # Font color
               "on_red":       "\033[41m",
               "on_green":     "\033[42m",
               "on_magenta":   "\033[45m"}

""" To test the output with Google's criteria. """
TEST = True

""" If you want to check the score of the output files rather than recalculate them. """
CHECK_OUTPUT = False

""" The maximum of test that we can make on only one file. """
MAXTEST = 300000

sumScoreOld = 0
__listPizza = []
listSelectedPizza = []
nbPeople = 0 
sumNewScore = 0 


def main(pathInput: str, pathOutput: str):
    """Launch the program on given file.

    Parameters
    ----------
    pathInput : str
        The path to the input file.
    pathOutput : str
        The path to the output file.
    """
    global __listPizza, listSelectedPizza, nbPeople, sumNewScore, sumScoreOld

    readInputFile(pathInput)

    print(129 * "*")
    print("Test on the file : \t\t", " " + chr(LIST_PATH.index(path) + 65))
    print("Number of participant : ", format(nbPeople, "10"))

    scoreMax = 0
    listSelectedPizza = ()
    listShufflePizza = list(__listPizza).copy()
    nbBoucle = MAXTEST if (len(__listPizza) > 8) else factorial(len(__listPizza))

    print()
    bar = tqdm.tqdm(total=nbBoucle, desc="Process in Progress")
    for shake in range(nbBoucle):
        scoreMaxTemp = nbPizzaSelected = 0
        bar.update()
        for pizzas in listShufflePizza:
            if scoreMaxTemp + pizzas <= nbPeople:
                # You can't have more shares than there are people
                scoreMaxTemp += pizzas
                nbPizzaSelected += 1
            else:
                break
        if scoreMaxTemp > scoreMax:
            scoreMax = scoreMaxTemp
            # Copying the exact number of pizzas required
            listSelectedPizza = (listShufflePizza[:nbPizzaSelected]).copy()
            if scoreMax == nbPeople:
                # If the score is equal to the number of people it's useless
                # to continue, it's impossible to make better
                # Forces the loading bar to be at 100%.
                bar.update(n=nbBoucle - shake - 1)
                break
        shuffle(listShufflePizza)  # Mixing the list

    bar.close()
    print()
    for k in range(len(listSelectedPizza)):
        # We retrieve the index of selected pizzas
        listSelectedPizza[k] = __listPizza.index(listSelectedPizza[k])
    listSelectedPizza = sorted(listSelectedPizza)
    # Several pizzas can have the same number of slices,
    # but you can only order one pizza at a time.
    for k in range(1, len(listSelectedPizza)):
        # The pizzas are listed in ascending order of share
        while listSelectedPizza[k] <= listSelectedPizza[k - 1]:
            listSelectedPizza[k] += 1

    sumNewScore += scoreMax
    saveNewCommand = saveNewScore(pathOutput, scoreMax)
    checkListSelectedPizza(listSelectedPizza)  # You don't necessarily have to make the test.
    if saveNewCommand:
        with open(pathOutput, "w") as file:  # Save the new best score
            file.write(str(len(listSelectedPizza)) + "\n")
            file.write(" ".join(str(indexPizza)
                                for indexPizza in listSelectedPizza))

    print("Score : ",
          format(scoreMax, "18"),
          "\nDifference : ",
          format((nbPeople - scoreMax), "13"),
          "\nNumber of pizza : ",
          format(len(listSelectedPizza), "8"))
    print("Best score : ",
          COLOR_THEME["green"] + "YES" if saveNewCommand else COLOR_THEME["red"] + "NO",
          COLOR_THEME["default"])
    print(129 * "*" + "\n")


def readInputFile(path: str):
    """Reads the given input file.

    Extract from the file the number of people,
    the number of pizzas and the list of pizzas.

    Parameters
    ----------
    path : str
        The path to the file
    """

    global __listPizza, nbPeople
    with open(path, "r") as file:  # Extrat data from the input file
        nbPeople, nbTypePizza = map(int, file.readline().strip().split(" "))
        __listPizza = list(map(int, file.readline().strip().split(" ")))


def saveNewScore(pathOutputOld: str, scoreNew: int) -> bool:
    """Verify if the score of this section is better than the previous one saved.

    The old file will be read and the associated score will be recalculated.
    If the old file does not exist, then it is automatically return True.

    Parameters
    ----------
    pathOutputOld : str
        The path to the old file.
    scoreNew : int
        The new calculated score.

    Returns
    -------
    bool
        True if the section must be saved, false otherwise.
    """
    global sumScoreOld
    scoreOld = calculScoreInFile(pathOutputOld)[0]

    if scoreOld is None:
        return True
    else:
        sumScoreOld += scoreOld
        return scoreOld < scoreNew


def calculScoreInFile(path: str):
    """Calculate the score in the given file.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    int
        The score of the file. If the file doesn't exit return 0.
    """
    scoreOld = 0
    listOldPizza = []
    try:
        with open(path, "r") as fileOld:
            lengthListOld = int(fileOld.readline())
            listOldPizza = fileOld.readline().split()

        for k in range(lengthListOld):
            scoreOld += __listPizza[int(listOldPizza[k])]

    except IOError:  # If the file does not exit
        pass

    return scoreOld, listOldPizza


def checkListSelectedPizza(listPizza: list) -> str:
    """Verify if the selection meets all the criteria.

    Returns
    -------
    str
        the list of every error.

    Notes
    -----
    All the criteria can be found in the pdf file: `src/Pizzas/practice_problem.pdf`.
    """
    textError = ""
    if TEST:
        error = ""
        listPizza = list(map(int, listPizza))
        
        comptPart = 0
        listPizzaOrdered = []
        for k in listPizza:
            comptPart += __listPizza[k]
            if k not in listPizzaOrdered:
                listPizzaOrdered.append(k)
            else:
                error += "\tMistake, the pizza " + \
                    str(k) + " is ordered several times\n"
        if comptPart > nbPeople:
            error += "\tError, the number of units ordered \
                        is highter than the number of persons."

        if len(error) == 0:
            textError = COLOR_THEME["green"] + "\tNone"
        else:
            textError = COLOR_THEME["magenta"] + error + COLOR_THEME["default"]

    else:
        textError = COLOR_THEME["yellow"] + "\tNot tested" + COLOR_THEME["default"]

    print("List of Error : \n" + textError, COLOR_THEME["default"])



if __name__ == "__main__":
    # clean the terminal automatically
    if plt.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")

    if not os.path.exists(PATH_OUTPUT_FOLDER):
        os.makedirs(PATH_OUTPUT_FOLDER)

    sumNewScore = 0
    sumScoreOld = 0
    for path in LIST_PATH:
        if CHECK_OUTPUT:
            readInputFile(path[0])  # In order to get the list of pizzas
            scoreFile, listOldPizza = calculScoreInFile(path[1])
            print("Score in file", path[1], "is", scoreFile)
            print(checkListSelectedPizza(listOldPizza))

        else:
            main(*path)
    differenceScore = sumNewScore - sumScoreOld

    print(COLOR_THEME["on_magenta"] + 30 * "_" +
        "Process terminated" + 31 * "_" + COLOR_THEME["default"] + "\n")

    if not CHECK_OUTPUT:
        colour = COLOR_THEME["on_red"] if differenceScore <= 0 else COLOR_THEME["on_green"]
        print("Ancient total score : ", format(sumScoreOld, "35"))
        print("New total score : ", format(sumNewScore, "39"))
        print(colour + "Difference beetwen the new and the ancient: ",
            format(abs(differenceScore), "13"), COLOR_THEME["default"])
