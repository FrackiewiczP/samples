from copy import deepcopy
from typing import List


class MatrixCoordinates:
    def __init__(self, row, column):
        self.row: int = row
        self.column: int = column


class MatchingFinder:
    def __init__(self, matrix):
        # Step 0
        self.input_matrix = deepcopy(matrix)
        self.matrix = matrix
        self.n = len(matrix)

        self.starred_elements: List[MatrixCoordinates] = []
        self.primed_elements: List[MatrixCoordinates] = []

        self.covered_columns: List[int] = []
        self.covered_rows: List[int] = []

    # Step 1
    def subtract_lowest_value_from_each_row(self):
        for i in range(self.n):
            self.subtract_lowest_value_from_row(i)
        return self.star_zeros()

    # Step 2
    def star_zeros(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][
                    j
                ] == 0 and not self.check_if_element_has_starred_zero_in_its_row_or_column(
                    i, j
                ):
                    self.starred_elements.append(MatrixCoordinates(i, j))
        return self.cover_columns_containing_a_starred_zero()

    # Step 3
    def cover_columns_containing_a_starred_zero(self):
        for s in self.starred_elements:
            self.covered_columns.append(s.column)
        if len(self.covered_columns) == self.n:
            return self.starred_elements
        else:
            return self.prime_non_covered_zeros()

    # Step 4
    def prime_non_covered_zeros(self):
        non_covered_zero = self.find_non_covered_zero()
        while non_covered_zero is not None:
            self.primed_elements.append(
                MatrixCoordinates(non_covered_zero.row, non_covered_zero.column)
            )
            starred_zero = list(
                filter(lambda x: x.row == non_covered_zero.row, self.starred_elements)
            )
            if len(starred_zero) == 0:
                return self.construct_series_of_zeros(non_covered_zero)
            else:
                self.covered_rows.append(non_covered_zero.row)
                self.covered_columns.remove(starred_zero[0].column)
            non_covered_zero = self.find_non_covered_zero()
        value = self.find_smallest_uncovered_value()
        return self.subtract_found_value(value)

    # Step 5
    def construct_series_of_zeros(self, z0):
        PRIMED = "PRIMED"
        STARRED = "STARRED"
        sequence = [(z0, PRIMED)]
        starred_zero = self.find_starred_zero_in_the_column(z0)
        while starred_zero is not None:
            primed_zero = self.find_primed_zero_in_the_row(starred_zero)
            sequence.append((starred_zero, STARRED))
            sequence.append((primed_zero, PRIMED))
            starred_zero = self.find_starred_zero_in_the_column(primed_zero)
        for e in sequence:
            if e[1] == STARRED:
                self.starred_elements.remove(e[0])
            else:
                self.starred_elements.append(e[0])
        self.primed_elements = []
        self.covered_rows = []
        self.covered_columns = []

        return self.cover_columns_containing_a_starred_zero()

    # Step 6
    def subtract_found_value(self, value):
        for i in self.covered_rows:
            for j in range(self.n):
                self.matrix[i][j] += value
        for i in range(self.n):
            for j in range(self.n):
                if j in self.covered_columns:
                    continue
                else:
                    self.matrix[i][j] -= value
        return self.prime_non_covered_zeros()

    def check_if_element_has_starred_zero_in_its_row_or_column(self, row, column):
        return any(row == x.row for x in self.starred_elements) or any(
            column == x.column for x in self.starred_elements
        )

    def subtract_lowest_value_from_row(self, row_index):
        lowest_value = min(self.matrix[row_index])
        for i in range(self.n):
            self.matrix[row_index][i] -= lowest_value

    def find_non_covered_zero(self):
        for i in range(self.n):
            for j in range(self.n):
                if (
                    self.matrix[i][j] == 0
                    and i not in self.covered_rows
                    and j not in self.covered_columns
                ):
                    return MatrixCoordinates(i, j)
        return None

    def find_smallest_uncovered_value(self):
        smallest_value = None
        for i in range(self.n):
            if i in self.covered_rows:
                continue
            for j in range(self.n):
                if j in self.covered_columns:
                    continue
                if smallest_value is None:
                    smallest_value = self.matrix[i][j]
                else:
                    if self.matrix[i][j] < smallest_value:
                        smallest_value = self.matrix[i][j]
        return smallest_value

    def find_starred_zero_in_the_column(self, coordinates: MatrixCoordinates):
        starred_zeros = list(
            filter(lambda x: x.column == coordinates.column, self.starred_elements)
        )
        if len(starred_zeros) == 0:
            return None
        else:
            return starred_zeros[0]

    def find_primed_zero_in_the_row(self, coordinates: MatrixCoordinates):
        primed_zeros = list(
            filter(lambda x: x.row == coordinates.row, self.primed_elements)
        )
        if len(primed_zeros) == 0:
            return None
        else:
            return primed_zeros[0]

    def find_matching(self):
        pairs = self.subtract_lowest_value_from_each_row()
        similarity = 0
        for p in pairs:
            similarity += self.input_matrix[p.row][p.column]
        matching = [(x.row, x.column) for x in pairs]
        return similarity, matching