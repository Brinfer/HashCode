import os
import time
import random

""" Path to text files containing input information . """
PATH_INPUT_FOLDER = "./Input/"
PATH_INPUT_1 = PATH_INPUT_FOLDER + "a_example.in"
PATH_INPUT_2 = PATH_INPUT_FOLDER + "b_little_bit_of_everything.in"
PATH_INPUT_3 = PATH_INPUT_FOLDER + "c_many_ingredients.in"
PATH_INPUT_4 = PATH_INPUT_FOLDER + "d_many_pizzas.in"
PATH_INPUT_5 = PATH_INPUT_FOLDER + "e_many_teams.in"

""" Path to text files containing output information (pizza list) """
PATH_OUTPUT_FOLDER = "./Output/"
PATH_OUTPUT_1 = PATH_OUTPUT_FOLDER + "a_output.txt"
PATH_OUTPUT_2 = PATH_OUTPUT_FOLDER + "b_output.txt"
PATH_OUTPUT_3 = PATH_OUTPUT_FOLDER + "c_output.txt"
PATH_OUTPUT_4 = PATH_OUTPUT_FOLDER + "d_output.txt"
PATH_OUTPUT_5 = PATH_OUTPUT_FOLDER + "e_output.txt"

""" List associating the paths of input and output files. """
TUPLE_PATH = (
    (PATH_INPUT_1, PATH_OUTPUT_1),
    (PATH_INPUT_2, PATH_OUTPUT_2),
    (PATH_INPUT_3, PATH_OUTPUT_3),
    (PATH_INPUT_4, PATH_OUTPUT_4),
    (PATH_INPUT_5, PATH_OUTPUT_5),
)

NB_TEST = 10000

g_list_pizza = []
g_command = []
g_score = 0
g_nb_team = 0
g_nb_pizza = 0
g_nb_people = 0
g_nb_team_2 = 0
g_nb_team_3 = 0
g_nb_team_4 = 0


def read_data(file_path: str):
    global g_list_pizza, g_nb_pizza, g_nb_team_2, g_nb_team_3, g_nb_team_4, g_nb_people, g_nb_team

    with open(file_path, "r") as file:
        g_nb_pizza, g_nb_team_2, g_nb_team_3, g_nb_team_4 = map(
            int, file.readline().strip().split(" ")
        )
        g_nb_people = 2 * g_nb_team_2 + 3 * g_nb_team_3 + 4 * g_nb_team_4
        g_nb_team = g_nb_team_2 + g_nb_team_3 + g_nb_team_4

        for pizza_id in range(g_nb_pizza):
            line = file.readline().strip().split(" ")

            pizza_temp = {
                "id": pizza_id,
                "nb_ingredient": line[0],
                "ingredient": line[1:],
            }
            g_list_pizza.append(pizza_temp)


def write_data(file_path: str):
    global g_command

    with open(file_path, "w") as file:
        file.write(str(len(g_command)) + "\n")

        while len(g_command) > 0:
            command = g_command.pop()

            line = " ".join((str(len(command)), *command)) + "\n"
            file.write(line)


def select_pizza(p_nb_pizza_to_take):
    global g_list_pizza

    l_set_different_ingredient_max = set()
    l_set_common_ingredient_min = set()
    l_list_pizza_selected_best = []

    l_nb_test = NB_TEST if len(g_list_pizza) >= NB_TEST // 2 else len(g_list_pizza) * 3

    for _ in range(l_nb_test):
        l_list_random_index = random.sample(
            range(0, len(g_list_pizza)), p_nb_pizza_to_take
        )
        l_list_pizza_selected_temp = [g_list_pizza[l_list_random_index[0]]]
        l_set_different_ingredient_temp = set(
            l_list_pizza_selected_temp[0]["ingredient"]
        )
        l_set_common_ingredient_temp = set()

        for index in l_list_random_index[1:]:
            l_list_pizza_selected_temp.append(g_list_pizza[index])

            l_set_different_ingredient_temp ^= set(g_list_pizza[index]["ingredient"])
            l_set_common_ingredient_temp |= (
                set(g_list_pizza[index]["ingredient"]) - l_set_different_ingredient_temp
            )

        if (
            len(l_set_different_ingredient_temp) > len(l_set_different_ingredient_max)
        ) or (
            len(l_set_different_ingredient_temp) == len(l_set_different_ingredient_max)
            and len(l_set_common_ingredient_temp) < len(l_set_common_ingredient_min)
        ):
            l_set_different_ingredient_max = l_set_different_ingredient_temp
            l_set_common_ingredient_min = l_set_common_ingredient_temp
            l_list_pizza_selected_best = l_list_pizza_selected_temp

    return l_list_pizza_selected_best, len(l_set_different_ingredient_max) ** 2


def main():
    global g_score, g_list_pizza, g_command, g_nb_team_2, g_nb_team_3, g_nb_team_4, g_nb_people

    l_selected_pizza = []
    l_number_pizza_to_command = 0

    for l_team_counter in range(g_nb_team):
        if g_nb_team_4 > 0:
            l_number_pizza_to_command = 4
            g_nb_team_4 -= 1
        elif g_nb_team_3 > 0:
            l_number_pizza_to_command = 3
            g_nb_team_3 -= 1
        elif g_nb_team_2 > 0:
            l_number_pizza_to_command = 2
            g_nb_team_2 -= 1
        else:
            break

        if len(g_list_pizza) >= l_number_pizza_to_command:
            l_command_temp = []
            l_selected_pizza, score_selection = select_pizza(l_number_pizza_to_command)

            g_score += score_selection
            g_nb_people -= l_number_pizza_to_command

            for pizza in l_selected_pizza:
                g_list_pizza.remove(pizza)
                l_command_temp.append(str(pizza["id"]))

            g_command.append(tuple(l_command_temp))

    pr = ""
    pr += "\nPeople to serve: {0:,}".format(g_nb_people)
    pr += "\nTeam 4 to serve: {0:,}".format(g_nb_team_4)
    pr += "\nTeam 3 to serve: {0:,}".format(g_nb_team_3)
    pr += "\nTeam 2 to serve: {0:,}".format(g_nb_team_2)
    pr += "\nPizza available: {0:,}".format(len(g_list_pizza))
    pr += "\nScore: {0:,}".format(g_score)
    pr += "\nTime passed: " + time.strftime(
        "%Hh %Mmin %Ss", time.gmtime(time.time() - chronoStart)
    )
    pr += "\n"
    print(pr)


if __name__ == "__main__":
    # clean the terminal automatically
    print("\033[2J\033[;H")

    if not os.path.exists(PATH_OUTPUT_FOLDER):
        os.makedirs(PATH_OUTPUT_FOLDER)

    chronoStart = time.time()

    for path in TUPLE_PATH:
        g_list_pizza = []
        g_command = []
        g_score = 0
        g_nb_pizza = 0
        g_nb_team = 0
        g_nb_people = 0
        g_nb_team_2 = 0
        g_nb_team_3 = 0
        g_nb_team_4 = 0

        print(100 * "#")
        print("Start file", path[0], "\n")

        read_data(path[0])
        main()
        write_data(path[1])

        print(100 * "#" + 2 * "\n")
