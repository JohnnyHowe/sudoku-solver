
class Section:
    """ Class to represent a section of the sudoku board.
    Splits the section into 9 other sections. """

    def __init__(self):
        """ Initialize the Section, sets each slot to None. """
        self._slots = [None, ] * 9

    def get_at(self, x, y):
        """ Get the item in the slot at (x, y).
        x and y must be between 0 and 2 (inclusive).

        Parameters:
            x (int): x ordinate
            y (int): y ordinate
        Returns:
            item (object): item at (x, y)
        """
        if not (0 <= x <= 2 and 0 <= y <= 2):
            raise IndexError("Can't get item at ({}, {})".format(x, y))
        return self._slots[x + y * 3]

    def set_at(self, item, x, y):
        """ Set the item at (x, y) to item.
        Parameters:
            item (object): object to set item to at the position (x, y)
            x (int): x ordinate
            y (int): y ordinate
        """
        self._slots[x + y * 3] = item

    def __str__(self):
        """ Return a basic string representation. """
        column_widths = [1, ] * 3
        for x in range(3):
            for y in range(3):
                column_widths[x] = max(column_widths[x], len(str(self.get_at(x, y))))

        string = ""
        for y in range(3):
            for x in range(3):
                cell = self.get_at(x, y)
                string += str(cell) + " " * (1 + column_widths[x] - len(str(cell)))
            string += "\n"
        return string[:-1]


class Board(Section):
    """ Class to represent the board,
    Is really just a section class but each slot is another section rather than a number. """

    def __init__(self):
        Section.__init__(self)
        self.set_sections()

    def load_board(self, filename="game.txt"):
        """ Load the board at filename into this
        The file is to be layed out in a 9x9 grid of characters directly representing the game.
        Blanks are to be left as spaces. """
        file = open(filename, "r")
        board_raw = file.read()
        file.close()
        for y, line in enumerate(board_raw.splitlines()):
            for x, char in enumerate(line):
                if x >= 9:
                    break
                if char != " ":
                    self.set_board_item(int(char), x, y)

    def get_copy(self):
        """ Return a copy of the board. """
        new_board = Board()
        for x in range(9):
            for y in range(9):
                new_board.set_board_item(self.get_board_item(x, y), x, y)
        return new_board

    def set_sections(self):
        """ Set all the sections of self to new sections. """
        for x in range(3):
            for y in range(3):
                self.set_at(Section(), x, y)

    def set_board_item(self, number, x, y):
        """ Set the item at x, y on the board.
        x and y are to between 0 and 8 (inclusive)

        Parameters:
            number (int): number to set
            x (int): x ordinate
            y (int): y ordinate
        """
        self.get_at(x // 3, y // 3).set_at(number, x % 3, y % 3)

    def contains_value(self, x, y):
        """ Is the cell at (x, y) occupied by an integer?
        Parameters:
            x (int): x ordinate
            y (int): y ordinate
        """
        return type(self.get_board_item(x, y)) == int

    def get_board_item(self, x, y):
        """ Get the item at x, y on the board.
        x and y are to between 0 and 8 (inclusive)

        Parameters:
            x (int): x ordinate
            y (int): y ordinate
        Returns:
            item (number): the number on the board at (x, y)
        """
        if not (0 <= x <= 8 and 0 <= y <= 8):
            raise IndexError("Cannot get item at ({}, {})".format(x, y))
        return self.get_at(x // 3, y // 3).get_at(x % 3, y % 3)

    def get_column(self, x):
        """ Get a copy of the column at y
        Parameters:
            x (int): x ordinate of row to get
        Returns:
            row (list): list of items in row (includes the lists of candidates)
        """
        return [self.get_board_item(x, y) for y in range(9)]

    def get_row(self, y):
        """ Get a copy of the row at y
        Parameters:
            y (int): y ordinate of row to get
        Returns:
            row (list): list of items in row (includes the lists of candidates)
        """
        return [self.get_board_item(x, y) for x in range(9)]

    def is_solved(self):
        """ Is the board solved?
        Is solved if it is valid and there are no blank spots. """
        for x in range(9):
            for y in range(9):
                if self.get_board_item(x, y) is None:
                    return False    # There's a blank spot!
        # Only gets to this line if there are no blanks
        return self.is_valid()

    def is_valid(self):
        """ Is the board valid?
        If a cell has a list it is ignored
        Does it violate any of the constraints?
        - is there two or more of the same numbers in the same section
        - are there two or more of the same numbers in the same line
        """
        # All vertical lines
        for x in range(9):
            if not self.is_line_valid_vertical(x):
                return False
        # All horizontal lines
        for y in range(9):
            if not self.is_line_valid_horizontal(y):
                return False
        # All sections
        for x in range(3):
            for y in range(3):
                if not self.is_section_valid(x, y):
                    return False
        return True

    def is_line_valid_horizontal(self, y):
        """ Is the horizontal line valid?
        Line is valid if no number is repeated twice or more.
        If the cell has a list it is ignored
        Returns:
            valid (bool): whether the line is valid
        """
        taken_numbers = [0, ] * 9
        for x in range(9):
            number = self.get_board_item(x, y)
            if number is not None and type(number) == int:
                index = int(number) - 1
                if taken_numbers[index]:
                    return False
                taken_numbers[index] = 1
        return True

    def is_line_valid_vertical(self, x):
        """ Is the vertical line valid?
        Line is valid if no number is repeated twice or more.
        If a cell has a list it is ignored
        Returns:
            valid (bool): whether the line is valid
        """
        taken_numbers = [0, ] * 9
        for y in range(9):
            number = self.get_board_item(x, y)
            if number is not None and type(number) == int:
                index = int(number) - 1
                if taken_numbers[index]:
                    return False
                taken_numbers[index] = 1
        return True

    def is_section_valid(self, section_x, section_y):
        """ Is the section valid?
        If a cell has a list it is ignored
        invalid if there are two or more of the same number in the section. """
        section = self.get_at(section_x, section_y)
        taken_numbers = [0, ] * 9
        for x in range(3):
            for y in range(3):
                number = section.get_at(x, y)
                if number is not None and type(number) == int:
                    index = number - 1
                    if taken_numbers[index] > 0:
                        return False
                    taken_numbers[index] = 1
        return True

    def __str__(self):
        """ Create a nice string representation of the board. """

        # Find how wide each column has to be
        column_widths = [1, ] * 9
        for x in range(9):
            for y in range(9):
                column_widths[x] = max(column_widths[x], len(str(self.get_board_item(x, y))))
        total_width = sum(column_widths) + 12

        string = ""
        for y in range(9):
            for x in range(9):

                cell = self.get_board_item(x, y)
                string += str(cell) + " " * (column_widths[x] - len(str(cell)) + 1)

                # Vertical section split
                if x == 2 or x == 5:
                    string += "| "

            string += "\n"

            # Horizontal section split
            if y == 2 or y == 5:
                string += "-" * total_width + "\n"

        return string[:-1]  # Gotta remove the last newline
