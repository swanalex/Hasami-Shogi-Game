from .constants import *
import pygame

class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, square, color, row, col):
        self.square = square
        self.color = color
        self.row = row
        self.col = col

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.x3 = 0
        self.y3 = 0
        self.calc_pos()

    def calc_pos(self):

        self.x1 = SQUARE_SIZE * int(self.col) + SQUARE_SIZE // 2
        self.y1 = SQUARE_SIZE * int(ord(self.row)-97) + SQUARE_SIZE // 2 - 30
        self.x2 = SQUARE_SIZE * int(self.col) + SQUARE_SIZE // 2 - 30
        self.y2 = SQUARE_SIZE * int(ord(self.row)-97) + SQUARE_SIZE // 2 + 30
        self.x3 = SQUARE_SIZE * int(self.col) + SQUARE_SIZE // 2 + 30
        self.y3 = SQUARE_SIZE * int(ord(self.row)-97) + SQUARE_SIZE // 2 + 30



    def draw(self, win): 
        pygame.draw.polygon(win, GREY, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)))
        pygame.draw.polygon(win, self.color, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)))

    def __repr__(self):
        return self.color
