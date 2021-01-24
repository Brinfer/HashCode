# HashCode 2020

## Practice Problem :pizza: :pizza: :pizza:

### [Problem description](./src/PracticeProblem/practice_problem.pdf)

You are organizing a HashCode hub and want to order pizza for your hub’s participants.
Luckily, there is a near by pizzeria with really good pizza.

The pizzeria has different types of pizza, and to keep the food offering for your hub interesting, you can only order at most one pizza of each type.
Fortunately, there are many types of pizza to choose from!

Each type of pizza has a specified size: the size is the number of slices in a pizza of this type.
You estimated the maximum number of pizza slices that you want to order for your hub based on the number of registered participants.
In order to reduce food waste, your goal is to order as many pizza slices as possible, but not more than the maximum number.

The solution gets 1 point for each slice of pizza ordered.

### [My solution](./src/PracticeProblem/main.py)

After parsing the entire input file and storing the information.

The pizza list is completely mixed up and I only take the number of pizzas needed (the first ones in the list).
I repeat this operation several times and keep only the list that earns me the most points.

The number of pizzas does not allow me to test all the combinations, so the score will not necessarily be the same if you run the program several times on the same file (the number of possible combinations is a factorial function).

To start the program, open a terminal in this current folder and enter in this terminal the command :
`python ./src/QualificationRound/main.py`

### The extra

It is very easy to test the results, therefore it is a part of the program to test and count the score of an output file.
Errors will be displayed in the terminal.

### Max Score

Scores are those calculated by the Judge System of the HashCode.

<center>

| File           | The Maximum number of slice to command | The number of different type of pizzas | Best Score obtained | Process time |
| -------------- | :------------------------------------: | :------------------------------------: | ------------------: | -----------: |
| a_example.in   |                   17                   |                   4                    |                  16 |    00min 00s |
| b_small.in     |                  100                   |                   10                   |                 100 |    00min 00s |
| c_medium.in    |                  4 500                 |                   50                   |               4 500 |    00min 00s |
| d_quite_big.in |              1 000 000 000             |                  2 000                 |       1 000 000 000 |    04min 26s |
| e_also_big.in  |              505 000 000               |                 10 000                 |         505 000 000 |    04min 13s |
|                |                                        |               __TOTAL__                |   __1 505 004 616__ |__08min 39s__ |

</center>
</br>

## Online Qualification Round :blue_book: :green_book: red_book:

### [Problem Description](./src/QualificationRound/hashcode_2020_online_qualification_round.pdf)

Given a description of libraries and books available, plan which books to scan from which library to maximize the total score of all scanned books, taking into account that each library needs to be signed up before it can ship books.

### [My Solution](./src/QualificationRound/main.py)

After parsing the entire input file and storing the information.

The list of book in the `Library` class are sorted so that the books with the highest scores are at the beginning of the list.
As soon as we select a `Library` I skip __d__ days, __d__ being the number of days to register and we get back the whole list of books.
Thus only one `Library` is processed at a time.
The selected `Library` is the library that earns the most points in the least amount of time ([Library signup](./src/QualificationRound/hashcode_2020_online_qualification_round.pdf)).
The list of its `Book` class are marked as __already borrowed__, and the next day the other `Library` will remove them from their list.
Towards the end of the allotted time, it is not necessarily possible to retrieve all the books from the libraries, the one from which it is possible to retrieve all the books are favored.

The score at each launch of the program will always be the same.

To start the program, open a terminal in this current folder and enter in this terminal the command :
`python ./src/PracticeProblem/main.py`

### Max Score

Scores are those calculated by the Judge System of the HashCode.

<center>

| File                         | Number of different books | Number of libraries | Number of days | Best Score obtained |  Process time |
| ---------------------------- | :-----------------------: | :-----------------: | :------------: | ------------------: | ------------: |
| a_example.txt                |             6             |          2          |       7        |                  21 |     00min 00s |
| b_read_on.txt                |          100000           |         100         |      1000      |           5 822 900 |     00min 01s |
| c_incunabula.txt             |          100000           |        10000        |     100000     |           5 689 822 |     01min 31s |
| d_tough_choices.txt          |           78600           |        1000         |     30001      |           5 029 115 |     12min 54s |
| e_so_many_books.txt          |          100000           |        1000         |      200       |           4 593 379 |     00min 21s |
| f_libraries_of_the_world.txt |          100000           |        1000         |      700       |           5 306 212 |     00min 05s |
|                              |                           |                     |   __TOTAL__    |      __26 441 449__ | __14min 55s__ |

</center>
