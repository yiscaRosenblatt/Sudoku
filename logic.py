import pygame
import sys
from settings import *
import random


class Logic:
    def __init__(self):
        self.new_bord = [[None for _ in range(9)] for _ in range(9)]
        self.build_new_bord(0,0)

    def build_new_bord(self, row, col):
        if row == 9:
            return True
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numbers)

        for number in numbers:
            if self.is_valid(row, col, number):
                self.new_bord[row][col] = number
                next_col = (col + 1) % 9
                next_row = row + 1 if next_col == 0 else row
                if self.build_new_bord(next_row, next_col):
                    return True
                else:
                    self.new_bord[row][col] = None
        return False

    def check_row(self, row, number):
        for col in range(9):
            if self.new_bord[row][col] == number:
                return False
        return True

    def check_col(self, col, number):
        for row in range(9):
            if self.new_bord[row][col] == number:
                return False
        return True

    def check_cube(self, row, col, number):
        start_cube_row = (row // 3) * 3
        start_cube_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.new_bord[start_cube_row + i][start_cube_col + j] == number:
                    return False
        return True

    def is_valid(self, row, col, number):
        return (
                self.check_row(row, number)
                and self.check_col(col, number)
                and self.check_cube(row, col, number)
        )















