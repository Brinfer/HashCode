class Book ():
    """Class representing a book according to
    its score and rank in the list of books.
    """

    def __init__(self, rank: int, score: int):
        """Builder of the `Book` class.

        Parameters
        ----------
        rank : int
            The rank of the book in the book list.
        score : int
            The point value of the book.
        """
        self.__score = score
        self.__rank = rank
        self.__borrow = False

    def __str__(self) -> str:
        """Overloading the string representation.

        Returns
        -------
        str
            Returns the rank of the book in `str` format.
        """
        return str(self.__rank)

    def __eq__(self, other) -> bool:
        """Comparison Operator Overload.

        Returns
        -------
        bool
            Returns True if both books have the same rank, False if not.
        """
        return self.__rank == other.rank

    @property
    def score(self) -> int:
        """Property  of a book, its score.

        Returns
        -------
        int
            The point value of the book.
        """
        return self.__score

    def isAvailable(self) -> bool:
        """Indicates if the book has already been borrowed or not.

        Returns
        -------
        bool
            True if the book has not already been borrowed False otherwise.
        """
        return not self.__borrow

    @property
    def rank(self) -> int:
        """Property  of a book, its rank in the list of all books.

        Returns
        -------
        int
            The rank of the book.
        """
        return self.__rank

    def borrowBook(self):
        """Borrows the book.
        """
        self.__borrow = True
