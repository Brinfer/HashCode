class Library ():
    """Class representing a library according to
    its list of books, the number of days required to register,
    the number of books that can be borrowed and rank in the list of library.
    """

    def __init__(self, listBook: list, daySingUp: int, borrowDay: int, rank: int):
        """Builder of the `Library` class.

        Parameters
        ----------
        listBook : list
            The list of books available in the library.
        daySingUp : int
            The number of days required to register.
        borrowDay : int
            The number of books that can be borrowed per day.
        rank : int
            The rank of the library in the list of libraries.
        """
        self.__listBook = listBook
        self.__daySingUp = daySingUp
        self.__borrowDay = borrowDay
        self.__rank = rank
        self.__score = 0

        self.__sortBook()
        self.calculScore(self.nbBook)

    def __sortBook(self):
        """Sorts the list of books in descending order of the book scores.
        """
        self.__listBook.sort(key=lambda p: p.score, reverse=True)

    def calculRatio(self, dayRemaining: int) -> tuple:
        """Calculates the score that can be achieved based
        on the number of days remaining.

        Parameters
        ----------
        dayRemaining : int
            Number of days remaining.

        Returns
        -------
        tuple
            A tuple containing the score that can be achieved and
            indicating if all books will be borrowed.
        """
        if self.daySingUp < dayRemaining:
            overdelay = False
            self.majListBook()
            dayRemaining -= self.daySingUp

            if self.nbBook / self.borrowDay >= dayRemaining:
                self.calculScore(self.borrowDay * dayRemaining)
                overdelay = True
            else:
                self.calculScore(self.nbBook)
            return self.score / self.daySingUp, overdelay
        else:
            return 0, True

    def calculScore(self, nbBook: int):
        """Re-calculate the maximum score that can be made
        based on the number of books that can be borrowed.

        Parameters
        ----------
        nbBook : int
            The number of books that can be borrowed.

        See Also
        --------
        `score`
        """
        self.__score = 0
        for k in self.__listBook[:nbBook]:
            self.__score += k.score

    def majListBook(self):
        """Removes from the list the books already borrowed.
        """
        for k in self.__listBook:
            if not k.isAvailable():
                self.__listBook.remove(k)

    def listBookBorrowing(self, limitTime: int) -> list:
        """Returns the list of books that can be borrowed in the allotted time.

        If the number of days is less than or equal to 0,
        then the entire book list is returned.

        Parameters
        ----------
        limitTime : int
            The number of days on which you want to borrow a book.

        Returns
        -------
        list
            The list of books that can be borrowed.
        """
        if limitTime <= 0:
            return self.__listBook[:]
        else:
            return self.__listBook[:(self.borrowDay * limitTime)]

    @property
    def rank(self) -> int:
        """Property  of a library, its rank in the list of all libraries.

        Returns
        -------
        int
            The rank of the library.
        """
        return self.__rank

    @property
    def daySingUp(self) -> int:
        """Property  of a library, its number of days required to register.

        Returns
        -------
        int
            The number of days required to register.

        See Also
        --------
        `nbBook`
        """
        return self.__daySingUp

    @property
    def listBook(self) -> list:
        """Property  of a library, its list of books.

        Returns
        -------
        list
            The list of books not borrowed in the library.
        """
        return self.__listBook

    @property
    def nbBook(self) -> int:
        """Property  of a library, its number of book.

        Returns
        -------
        int
            The number of books available in the library's book list.

        See Also
        --------
        `listBook`

        """
        return len(self.__listBook)

    @property
    def score(self) -> int:
        """Property  of a library, the score of the library.

        Returns
        -------
        int
            The sum of the book scores available in the list of books.

        See Also
        --------
        `calculScore`
        """
        return self.__score

    @property
    def borrowDay(self) -> int:
        """Property  of a library, it's number of books that can be borrowed in the same day.

        Returns
        -------
        int
            The number of books that can be borrowed in the same day.
        """
        return self.__borrowDay
