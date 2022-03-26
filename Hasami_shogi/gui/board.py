import pygame
from .piece import *
from .constants import *

class HasamiShogiGame:
  '''
  Creation of the HasamiShogiGame class
  '''

  def __init__(self):
    '''
    The game state is initialized to be 'UNFINISHED' and the active player as 'BLACK' in the init method
    '''
    self._game_state = 'UNFINISHED'
    self._active_player = 'BLACK'
    


    # the rows
    self._row_a = ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R']
    self._row_b = [None, None, None, None, None, None, None, None, None]
    self._row_c = [None, None, None, None, None, None, None, None, None]
    self._row_d = [None, None, None, None, None, None, None, None, None]
    self._row_e = [None, None, None, None, None, None, None, None, None]
    self._row_f = [None, None, None, None, None, None, None, None, None]
    self._row_g = [None, None, None, None, None, None, None, None, None]
    self._row_h = [None, None, None, None, None, None, None, None, None]
    self._row_i = ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    self._rows = [self._row_a, self._row_b, self._row_c, self._row_d, self._row_e, self._row_f, self._row_g, self._row_h, self._row_i]


  def draw(self, win): # draws in the shogi pieces
    self.draw_squares(win)
    for count, x in enumerate(self._rows):
      for cnt, y in enumerate(x):
        square = str(chr(count+97)) + str(cnt)
        if y == 'R':
          y = Piece(square, 'RED', square[0], square[1])
          y.draw(win)
        if y == 'B':
          y = Piece(square, 'BLACK', square[0], square[1])
          y.draw(win)
        


  def draw_squares(self, win): # draws the checkered squares on the board
    win.fill(TAN)
    for row in range(ROWS):
      for col in range(row % 2, ROWS, 2):
        pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


  def get_game_state(self):
    '''
    Get method for retuning the game state
    :return: 'RED_WON', 'BLACK_WON', or 'UNFINISHED'
    '''
    return self._game_state

  def get_active_player(self):
    '''
    Get method for telling whose turn it is
    :return: 'RED' or 'BLACK'
    '''
    return self._active_player

  def change_active_player(self):
    '''
    A method to change the active player/change whose turn it is. This will be called after every valid
    move is made
    :return: changes self._active_player to be the opposite of the one who just moved
    '''
    if self._active_player == 'RED':
      self._active_player = 'BLACK'
    elif self._active_player == 'BLACK':
      self._active_player = 'RED'

  def get_num_captured_pieces(self, color):
    '''
    Get method for giving the number of captured pieces of the given input color
    :param color: 'RED' or 'BLACK'
    :return: The number of pieces of THAT color that have been captured
    '''
    count_R = 0
    count_B = 0
    for x in self._rows:
      for y in x:
        if y == 'R':
          count_R += 1
        elif y == 'B':
          count_B += 1
    if color == 'RED':
      red_captured = 9 - count_R
      return red_captured
    if color == 'BLACK':
      black_captured = 9 - count_B
      return black_captured

  def get_square_occupant(self, square):
    '''
    Get method for returning the player color who occupies a given square on the board. Returns 'NONE' if
    the square is empty.
    :param square: Entered as a string, i.e. ('b,5')
    :return: 'RED', 'BLACK', or 'NONE'
    '''
    if self._rows[ord(square[0])-97][int(square[1])-1] == 'R':
      return Piece(square, 'RED', square[0], square[1])
    elif self._rows[ord(square[0])-97][int(square[1])-1] == 'B':
      return Piece(square, 'BLACK', square[0], square[1])
    else:
      return 'NONE'


  def make_move(self, moved_from, moved_to):
    '''
    This is the meat and potatoes of the class. When a move is made, the method checks for captures in all three
    directions (captures cannot be made in the direction the pawn was moved from). It also check for corner
    captures, should the pawn be in a corner capture position.
    :param moved_from: Given as a string, i.e. ('a,1')
    :param moved_to: Given as a string, i.e. ('d,1')
    :return: False if: Square being moved FROM is empty
    Square being moved FROM does not contain a piece belonging to the active player
    Square being moved TO is occupied
    Move is diagonal
    Move is illegal because pathway is blocked by another pawn
    Game has already been won
    True if: A valid, legal moved has been made
    Before returning True, this method will remove any captured pawns, update the game state if the moved
    has triggered a player to win, and also change the active player.
    '''

    moved_from_y = ord(moved_from[0])-97
    moved_to_y = ord(moved_to[0])-97

    # our x-coordinates
    moved_from_x_coord = int(moved_from[1]) -1
    moved_to_x_coord = int(moved_to[1]) -1


    if self._rows[moved_from_y][moved_from_x_coord] is None: #if we try to move from square that contains no pawn
      return False
    if self._rows[moved_to_y][moved_to_x_coord] is not None: #if we try to move TO a square that is occupied
      return False
    if self.get_game_state() == 'RED_WON' or self.get_game_state() == 'BLACK_WON':
      return False
    if moved_from[0] != moved_to[0] and moved_from[1] != moved_to[1]: #if both of these are not equal,
      #it would be a diagonal move
      return False

    if self._active_player == 'BLACK':
      pawn = 'B'
      enemy = 'R'
    if self._active_player == 'RED':
      pawn = 'R'
      enemy = 'B'
    if pawn == 'B' and self._rows[moved_from_y][moved_from_x_coord] == 'R':
      print('it is not your turn!')
      return False
    elif pawn == 'R' and self._rows[moved_from_y][moved_from_x_coord] == 'B':
      print('it is not your turn!')
      return False



    if moved_from[0] == moved_to[0]: #horizontal move
      print('horizontal move')
      current_row = self._rows[moved_from_y]
      if moved_from_x_coord < moved_to_x_coord: #moving to the right
        for count, value in enumerate(current_row[moved_from_x_coord+1:moved_to_x_coord+1]):
          if value is not None:
            print('invalid move')
            return False
          elif count+1 == abs(moved_to_x_coord-moved_from_x_coord):
            current_row[moved_to_x_coord] = pawn
            current_row[moved_from_x_coord] = None

            #CHECK FOR CAPTURES TO THE RIGHT
            check_x_coord = int(moved_to[1])
            while check_x_coord < 8:
              if current_row[check_x_coord] == enemy:
                check_x_coord += 1
                if current_row[check_x_coord] == pawn:
                  check_x_coord -= 1
                  while check_x_coord > moved_to_x_coord:
                    current_row[check_x_coord] = None
                    check_x_coord -= 1
                    if check_x_coord == moved_to_x_coord:
                      break
              elif current_row[check_x_coord] is None or current_row[check_x_coord] == pawn:
                break

            #CHECK FOR CAPTURES ABOVE
            check_y_coord = moved_to_y-1
            check_x_coord = int(moved_to[1]) # resetting check_x_coord
            while check_y_coord > 0:
              if self._rows[check_y_coord][check_x_coord-1] == enemy and self._rows[check_y_coord-1][check_x_coord-1] == pawn:
                while check_y_coord < moved_to_y:
                  self._rows[check_y_coord][moved_to_x_coord] = None
                  check_y_coord += 1
                  if check_y_coord == moved_to_y:
                    break
              elif self._rows[check_y_coord][check_x_coord-1] is not enemy:
                break
              else:
                check_y_coord -= 1

            #CHECK FOR CAPTURES BELOW
            check_y_coord_2 = moved_to_y +1
            while check_y_coord_2 < 8:
              if self._rows[check_y_coord_2][moved_to_x_coord] == enemy and self._rows[check_y_coord_2+1][moved_to_x_coord] == pawn:
                while check_y_coord_2 > moved_to_y:
                  self._rows[check_y_coord_2][moved_to_x_coord] = None
                  check_y_coord_2 -= 1
                  if check_y_coord_2 == moved_to_y:
                    break
              elif self._rows[check_y_coord_2][moved_to_x_coord] is not enemy:
                break
              else:
                check_y_coord_2 += 1

            #CHECK FOR CORNER CAPTURE - moving to the right

            if (moved_to == 'b9' and self._rows[0][7] == pawn) or (moved_to == 'a8' and self._rows[1][8] == pawn) and self._rows[0][8] == enemy:
              print('top right corner capture')
              self._rows[0][8] = None

            if (moved_to == 'h9' and self._rows[8][7] == pawn) or (moved_to == 'i8' and self._rows[7][8] == pawn) and self._rows[8][8] == enemy:
              print('bottom right corner capture')
              self._rows[8][8] = None


            self.change_active_player()
            if self.get_num_captured_pieces('RED') == 8 or self.get_num_captured_pieces('RED') == 9:
              self._game_state = 'BLACK_WON'
              print('congratulations! black has won!')
            if self.get_num_captured_pieces('BLACK') == 8 or self.get_num_captured_pieces('BLACK') == 9:
              self._game_state = 'RED_WON'
              print('congratulations! red has won!')
            return True



      elif moved_from_x_coord > moved_to_x_coord: #moving to the left
        for count, value in enumerate(current_row[moved_to_x_coord:moved_from_x_coord]):
          if value is not None:
            print('invalid move')
            return False
          elif count+1 == abs(moved_from_x_coord - moved_to_x_coord):
            current_row[moved_to_x_coord] = pawn
            current_row[moved_from_x_coord] = None


            #CHECK FOR CAPTURES TO THE LEFT
            check_x_coord_2 = int(moved_to[1]) -2
            while check_x_coord_2 >= 0:
              if current_row[check_x_coord_2] == pawn:
                check_x_coord_2 += 1
                while check_x_coord_2 < moved_to_x_coord:
                  current_row[check_x_coord_2] = None
                  check_x_coord_2 += 1
              elif current_row[check_x_coord_2] is None:
                break
              else:
                check_x_coord_2 -= 1

            #CHECK FOR CAPTURES ABOVE
            check_x_coord = int(moved_to[1])
            check_y_coord = moved_to_y-1
            while check_y_coord > 0:
              if self._rows[check_y_coord][check_x_coord-1] == enemy and self._rows[check_y_coord-1][check_x_coord-1] == pawn:
                while check_y_coord < moved_to_y:
                  self._rows[check_y_coord][moved_to_x_coord] = None
                  check_y_coord += 1
                  if check_y_coord == moved_to_y:
                    break
              elif self._rows[check_y_coord][check_x_coord-1] is not enemy:
                break
              else:
                check_y_coord -= 1

            #CHECK FOR CAPTURES BELOW
            check_y_coord_2 = moved_to_y +1
            while check_y_coord_2 < 8:
              if self._rows[check_y_coord_2][moved_to_x_coord] == enemy and self._rows[check_y_coord_2+1][moved_to_x_coord] == pawn:
                while check_y_coord_2 > moved_to_y:
                  self._rows[check_y_coord_2][moved_to_x_coord] = None
                  check_y_coord_2 -= 1
                  if check_y_coord_2 == moved_to_y:
                    for x in self._rows:
                      print(x)
                    break
              elif self._rows[check_y_coord_2][moved_to_x_coord] is not enemy:
                break
              else:
                check_y_coord_2 += 1


            #CHECK FOR CORNER CAPTURE - moving to the left

            if (moved_to == 'b1' and self._rows[0][1] == pawn) or (moved_to == 'a2' and self._rows[1][0] == pawn) and self._rows[0][0] == enemy:
              print('top left corner capture')
              self._rows[0][0] = None

            if (moved_to == 'h1' and self._rows[8][1] == pawn) or (moved_to == 'i2' and self._rows[7][0] == pawn) and self._rows[8][0] == enemy:
              print('bottom left corner capture')
              self._rows[8][0] = None


            self.change_active_player()
            if self.get_num_captured_pieces('RED') == 8 or self.get_num_captured_pieces('RED') == 9:
              self._game_state = 'BLACK_WON'
              print('congratulations! black has won!')
            if self.get_num_captured_pieces('BLACK') == 8 or self.get_num_captured_pieces('BLACK') == 9:
              self._game_state = 'RED_WON'
              print('congratulations! red has won!')
            return True



    if moved_from[1] == moved_to[1]: #vertical move
      print('vertical move')
      current_row = self._rows[moved_to_y]
      x_coord = int(moved_from[1]) -1 #setting x-coordinate to new name to avoid confusion/x-coordinate is the same for vertical moves
      if moved_from_y < moved_to_y: #moving downwards
        for count, value in enumerate(self._rows[moved_from_y+1:moved_to_y+1]):
          if value[x_coord] is not None:
            print('invalid move')
            return False
            break
          elif count+1 == abs(moved_from_y - moved_to_y):
            self._rows[moved_to_y][x_coord] = pawn
            self._rows[moved_from_y][x_coord] = None


            #CHECK FOR CAPTURES TO THE LEFT
            check_x_coord = int(moved_to[1])
            check_x_coord_2 = int(moved_to[1]) -2
            while check_x_coord_2 > 0:
              if current_row[check_x_coord_2] == enemy:
                check_x_coord_2 -= 1
                if current_row[check_x_coord_2] == pawn:
                  check_x_coord_2 += 1
                  current_row[check_x_coord_2] = None
                  while check_x_coord_2 < check_x_coord:
                    current_row[check_x_coord_2] = None
                    check_x_coord_2 += 1
                    if check_x_coord_2 == check_x_coord -1:
                      break
              elif current_row[check_x_coord_2] is None or current_row[check_x_coord_2] == pawn:
                break


            #CHECK FOR CAPTURES TO THE RIGHT
            check_x_coord = int(moved_to[1])
            while check_x_coord < 8:
              if current_row[check_x_coord] == enemy:
                check_x_coord += 1
                if current_row[check_x_coord] == pawn:
                  check_x_coord -= 1
                  while check_x_coord > moved_to_x_coord:
                    current_row[check_x_coord] = None
                    check_x_coord -= 1
                    if check_x_coord == moved_to_x_coord:
                      break
              elif current_row[check_x_coord] is None or current_row[check_x_coord] == pawn:
                break


            #CHECK FOR CAPTURES BELOW
            check_y_coord_2 = moved_to_y +1
            while check_y_coord_2 < 8:
              if self._rows[check_y_coord_2][moved_to_x_coord] == enemy and self._rows[check_y_coord_2+1][moved_to_x_coord] == pawn:
                while check_y_coord_2 > moved_to_y:
                  self._rows[check_y_coord_2][moved_to_x_coord] = None
                  check_y_coord_2 -= 1
                  if check_y_coord_2 == moved_to_y:
                    break
              elif self._rows[check_y_coord_2][moved_to_x_coord] is not enemy:
                break
              else:
                check_y_coord_2 += 1

            #CHECK FOR CORNER CAPTURES - moving downwards

            if (moved_to == 'h1' and self._rows[8][1] == pawn) or (moved_to == 'i2' and self._rows[7][0] == pawn) and self._rows[8][0] == enemy:
              print('bottom left corner capture')
              self._rows[8][0] = None

            if (moved_to == 'h9' and self._rows[8][7] == pawn) or (moved_to == 'i8' and self._rows[7][8] == pawn) and self._rows[8][8] == enemy:
              print('bottom right corner capture')
              self._rows[8][8] = None




            self.change_active_player()
            if self.get_num_captured_pieces('RED') == 8 or self.get_num_captured_pieces('RED') == 9:
              self._game_state = 'BLACK_WON'
              print('congratulations! black has won!')
            if self.get_num_captured_pieces('BLACK') == 8 or self.get_num_captured_pieces('BLACK') == 9:
              self._game_state = 'RED_WON'
              print('congratulations! red has won!')
            return True



      if moved_from_y > moved_to_y: #moving upwards
        for count, value in enumerate(self._rows[moved_to_y:moved_from_y]):
          if value[x_coord] is not None:
            print('invalid move')
            return False
          elif count+1 == abs(moved_from_y - moved_to_y):
            self._rows[moved_to_y][x_coord] = pawn
            self._rows[moved_from_y][x_coord] = None


            #CHECK FOR CAPTURES TO THE LEFT
            check_x_coord = int(moved_to[1])
            check_x_coord_2 = int(moved_to[1]) -2
            while check_x_coord_2 > 0:
              if current_row[check_x_coord_2] == enemy:
                check_x_coord_2 -= 1
                if current_row[check_x_coord_2] == pawn:
                  check_x_coord_2 += 1
                  current_row[check_x_coord_2] = None
                  while check_x_coord_2 < check_x_coord:
                    current_row[check_x_coord_2] = None
                    check_x_coord_2 += 1
                    if check_x_coord_2 == check_x_coord -1:
                      break
              elif current_row[check_x_coord_2] is None or current_row[check_x_coord_2] == pawn:
                break

            #CHECK FOR CAPTURES TO THE RIGHT
            check_x_coord = int(moved_to[1])
            while check_x_coord < 8:
              if current_row[check_x_coord] == enemy:
                check_x_coord += 1
                if current_row[check_x_coord] == pawn:
                  check_x_coord -= 1
                  while check_x_coord > moved_to_x_coord:
                    current_row[check_x_coord] = None
                    check_x_coord -= 1
                    if check_x_coord == moved_to_x_coord:
                      break
              elif current_row[check_x_coord] is None or current_row[check_x_coord] == pawn:
                break

            #CHECK FOR CAPTURES ABOVE
            check_x_coord = int(moved_to[1])
            check_y_coord = moved_to_y-1
            while check_y_coord > 0:
              if self._rows[check_y_coord][check_x_coord-1] == enemy and self._rows[check_y_coord-1][check_x_coord-1] == pawn:
                while check_y_coord < moved_to_y:
                  self._rows[check_y_coord][moved_to_x_coord] = None
                  check_y_coord += 1
                  if check_y_coord == moved_to_y:
                    break
              elif self._rows[check_y_coord][check_x_coord-1] is not enemy:
                break
              else:
                check_y_coord -= 1

            #CHECK FOR CORNER CAPTURES - moving upwards
            if (moved_to == 'b1' and self._rows[0][1] == pawn) or (moved_to == 'a2' and self._rows[1][0] == pawn) and self._rows[0][0] == enemy:
              print('top left corner capture')
              self._rows[0][0] = None

            if (moved_to == 'b9' and self._rows[0][7] == pawn) or (moved_to == 'a8' and self._rows[1][8] == pawn) and self._rows[0][8] == enemy:
              print('top right corner capture')
              self._rows[0][8] = None



            self.change_active_player()
            if self.get_num_captured_pieces('RED') == 8 or self.get_num_captured_pieces('RED') == 9:
              self._game_state = 'BLACK_WON'
              print('congratulations! black has won!')
            if self.get_num_captured_pieces('BLACK') == 8 or self.get_num_captured_pieces('BLACK') == 9:
              self._game_state = 'RED_WON'
              print('congratulations! red has won!')
            return True

  def print_board(self):
    '''
    An extra little function to be called to print out the board
    :return: Prints out the current board state
    '''
    for x in self._rows:
      for count, y in enumerate(x):
        if y == 'R' or y == 'B':
          print('|', y, end=" ")
          if count == 8:
            print('|')
        elif y is None:
          print('|', '-', end=" ")
          if count == 8:
            print('|')


# shogi = HasamiShogiGame()
# print(shogi.make_move('i1', 'f1'))
# shogi.print_board()

# shogi = HasamiShogiGame()
# for count, x in enumerate(shogi._rows):
#   for cnt, y in enumerate(x):
#     square = str(chr(count+97)) + str(cnt)
#     if y == 'R':
#       print(square, 'red pawn')
#     elif y == 'B':
#       print(square, 'black pawn')




