import pygame
import math
from gui.constants import *
from gui.board import HasamiShogiGame

FPS = 60


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hasami Shogi')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = math.ceil(x / SQUARE_SIZE)
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    board = HasamiShogiGame()


    while run:
        black_victory = 'CONGRATULATIONS, black has won!'
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                r = chr(row + 97)
                c = str(col)
                rc = r+c
                #piece = board.get_square_occupant(rc)
            if event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                row2, col2 = get_row_col_from_mouse(pos2)
                r2 = chr(row2 + 97)
                c2 = str(col2)
                rc2 = r2+c2
                board.make_move(rc, rc2)
                

        board.draw(WIN)
        pygame.display.update()
        

    pygame.quit()

main()