from Class.Book import Book
from Class.Library import Library
import tqdm as tqdm
import os as os
import platform as plt
import time as time

""" Path to text files containing input information . """
PATH_INPUT_FOLDER = "./HashCode-2020/src/QualificationRound/Input/"
PATH_INPUT_1 = "a_example.txt"
PATH_INPUT_2 = "b_read_on.txt"
PATH_INPUT_3 = "c_incunabula.txt"
PATH_INPUT_4 = "d_tough_choices.txt"
PATH_INPUT_5 = "e_so_many_books.txt"
PATH_INPUT_6 = "f_libraries_of_the_world.txt"

""" Path to text files containing output information (pizza list) """
PATH_OUTPOUT_FOLDER = "./HashCode-2020/src/QualificationRound/Output/"
PATH_OUTPUT_1 = "A_output.txt"
PATH_OUTPUT_2 = "B_output.txt"
PATH_OUTPUT_3 = "C_output.txt"
PATH_OUTPUT_4 = "D_output.txt"
PATH_OUTPUT_5 = "E_output.txt"
PATH_OUTPUT_6 = "F_output.txt"

""" List associating the paths of input and output files. """
LIST_PATH = [[PATH_INPUT_1, PATH_OUTPUT_1],
             [PATH_INPUT_2, PATH_OUTPUT_2],
             [PATH_INPUT_3, PATH_OUTPUT_3],
             [PATH_INPUT_4, PATH_OUTPUT_4],
             [PATH_INPUT_5, PATH_OUTPUT_5],
             [PATH_INPUT_6, PATH_OUTPUT_6]]

""" To write in direct the output file, or in the end of the process. """
DIRECT_WRITE = False

__listBooks = []            # The list of book in the input files
__listLibrary = []          # The list of libraries in the input files
__listLibrarySelected = []  # The list of libraries in the output files (evolve during the process)
__nbDays = 0                # The total number of days to make the best score
__day = 0                   # The number of days elapsed (evolve during the process)
__scoreTotal = 0            # The total score made by borrowing books (imprecise)
__timeTotal = 0             # The total time of the process (evolve during the process)

def getInput(path: str):
    """Extract the data from the file whose path is set as a parameter.

    Parameters
    ----------
    path : str
        Path to the file.
    """

    global __nbDays, __listBooks

    with open(path, "r") as file:
        # Recovery of global information
        line = [int(i) for i in file.readline().strip().split()]
        nbBooks, nbLibrary, __nbDays = line[0], line[1], line[2]

        # Recovery of book data
        line = [int(i) for i in file.readline().strip().split()]

        for k in range(nbBooks):
            book = Book(k, line[k])
            __listBooks.append(book)

        # Recovery of library data
        for k in range(nbLibrary):
            line = [int(i) for i in file.readline().strip().split()]
            dayProcess, bookDay = line[1], line[2]
            line = [int(i) for i in list(set(file.readline().strip().split()))]
            listBooksLib = []
            for i in line:
                listBooksLib.append(__listBooks[i])

            library = Library(listBooksLib, dayProcess, bookDay, k)
            __listLibrary.append(library)


def borrowingBook(dayRemaining: int):
    """Borrows the maximum number of lines according to the number of days remaining.

    The library selected is the one that gives the maximum number of
    points in the least amount of time, it is not necessarily the one
    that has the most books.

    Parameters
    ----------
    dayRemaining : int
        Number of days remaining.
    """

    ratioMax = ratioTemp = 0
    exceedLimitTime = exceedMaxTimeLimit = False
    librarySelected = None

    for k in __listLibrary:
        # Searching for the library that earns the most
        # points in a minimum of time, based on the number of days left.
        ratioTemp, exceedLimitTime = k.calculRatio(dayRemaining)
        if ratioTemp > ratioMax:
            ratioMax = ratioTemp
            librarySelected = k
            exceedMaxTimeLimit = exceedLimitTime

        elif ratioMax == ratioTemp and exceedLimitTime < exceedMaxTimeLimit:
            # Favours bookstores that return all their books
            # and do not exceed deadlines
            ratioMax = ratioTemp
            librarySelected = k
            exceedMaxTimeLimit = exceedLimitTime

        elif not ratioTemp:
            # Removing libraries that no longer earn points
            __listLibrary.remove(k)

    # Memorizes the new bookstore from which it was borrowed.
    __listLibrarySelected.append(librarySelected)
    if librarySelected is not None:
        __listLibrary.remove(librarySelected)
        for k in librarySelected.listBookBorrowing(limitTime=__day - librarySelected.daySingUp):
            k.borrowBook()


def writeOutput(path: str):
    """Writes the output file to the given file.

    The list of books borrowed from all bookshops
    from which to borrow is written down.

    Parameters
    ----------
    path : str
        The path to the destination file.
    """
    with open(path, "w") as file:
        line = str(len(__listLibrarySelected)) + "\n"
        file.write(line)
        for k in __listLibrarySelected[:]:
            line = str(k.rank) + " " + str(len(k.listBook)) + "\n"
            file.write(line)
            line = " ".join(str(i) for i in k.listBook) + "\n"
            file.write(line)


def scanFile(path: str) -> tuple:
    """Read the given file and borrows the books.

    If the constant `DIRECT_WRITE` is set to True
    then the output file is written as soon as
    a library is selected otherwise the entire file
    will be written at the end of the process.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    tuple
        A tuple containing the score obtained but
        also the time needed to finish the process on this file.
    """
    global __day

    scoreFile = 0
    print(81 * "#" + "\n")
    print("Launched on the file : " + path[0])
    startTimeFile = time.time()

    getInput(PATH_INPUT_FOLDER + path[0])

    bar = tqdm.tqdm(total=__nbDays, desc="Flow of days")
    while __day < __nbDays:
        borrowingBook(__nbDays - __day)
        if __listLibrarySelected[-1] is not None:
            __day += __listLibrarySelected[-1].daySingUp
            bar.update(__listLibrarySelected[-1].daySingUp)
            scoreFile += __listLibrarySelected[-1].score
            if DIRECT_WRITE:
                writeOutput(PATH_OUTPOUT_FOLDER + path[1])

        else:
            del __listLibrarySelected[-1]
            break

    if __day < __nbDays:
        bar.update(__nbDays - __day)
    bar.close()
    chrono = time.time() - startTimeFile

    if not DIRECT_WRITE:
        writeOutput(PATH_OUTPOUT_FOLDER + path[1])

    print("Finish for the file", path[1], ",", len(__listLibrarySelected), "library")
    print("Score of the file (inacurate): ", '{0:,}'.format(scoreFile))
    print("Time elapsed :", time.strftime("%Hh %Mmin %Ss", time.gmtime(chrono)))
    print("\n" + 81 * "#" + 2 * "\n")

    return scoreFile, chrono


if __name__ == "__main__":
    # Cleans the terminal automatically
    if plt.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")

    if not os.path.exists(PATH_OUTPOUT_FOLDER):
        os.makedirs(PATH_OUTPOUT_FOLDER)

    print(28 * "+", "Starting", 28 * "+", 2 * "\n")

    for path in LIST_PATH:
        __listBooks = []
        __listLibrary = []
        __listLibrarySelected = []
        listBookSelected = []

        scoreFile, chrono = scanFile(path)

        __nbDays = __day = 0
        __scoreTotal += scoreFile
        __timeTotal += chrono

    print(32 * "+", "Ending", 32 * "+", "\n")
    print("Total Score (inacurate): ", '{0:,}'.format(__scoreTotal))
    print("Total time:", time.strftime("%Hh %Mmin %Ss", time.gmtime(__timeTotal)), "\n")
    print(2 * "\n")
