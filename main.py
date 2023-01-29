import numpy
import numpy as np
import pygame
import sys
from pygame.locals import *

pygame.init()

fps = 60

rows = 8
columns = 8
squareSize = 80
WHITE = (230, 151, 99)
BLACK = (230, 61, 9)

fpsClock = pygame.time.Clock()


width, height = squareSize*columns, squareSize*rows
screen = pygame.display.set_mode((width, height))

coords = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,

    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0

}
DEFAULT_IMAGE_SIZE = (squareSize, squareSize)
# images
# sample: carImg = pygame.image.load('racecar.png')
Black_Pawn = pygame.image.load('Pieces/Black_Pawn.png')
Black_Knight = pygame.image.load('Pieces/Black_Knight.png')
Black_Bishop = pygame.image.load('Pieces/Black_Bishop.png')
Black_King = pygame.image.load('Pieces/Black_King.png')
Black_Queen = pygame.image.load('Pieces/Black_Queen.png')
Black_Rook = pygame.image.load('Pieces/Black_Rook.png')

White_Pawn = pygame.image.load('Pieces/White_Pawn.png')
White_Knight = pygame.image.load('Pieces/White_Knight.png')
White_Bishop = pygame.image.load('Pieces/White_Bishop.png')
White_King = pygame.image.load('Pieces/White_King.png')
White_Queen = pygame.image.load('Pieces/White_Queen.png')
White_Rook = pygame.image.load('Pieces/White_Rook.png')

Black_Pawn = pygame.transform.scale(Black_Pawn, DEFAULT_IMAGE_SIZE)
Black_Knight = pygame.transform.scale(Black_Knight, DEFAULT_IMAGE_SIZE)
Black_Bishop = pygame.transform.scale(Black_Bishop, DEFAULT_IMAGE_SIZE)
Black_King = pygame.transform.scale(Black_King, DEFAULT_IMAGE_SIZE)
Black_Queen = pygame.transform.scale(Black_Queen, DEFAULT_IMAGE_SIZE)
Black_Rook = pygame.transform.scale(Black_Rook, DEFAULT_IMAGE_SIZE)

White_Pawn = pygame.transform.scale(White_Pawn, DEFAULT_IMAGE_SIZE)
White_Knight = pygame.transform.scale(White_Knight, DEFAULT_IMAGE_SIZE)
White_Bishop = pygame.transform.scale(White_Bishop, DEFAULT_IMAGE_SIZE)
White_King = pygame.transform.scale(White_King, DEFAULT_IMAGE_SIZE)
White_Queen = pygame.transform.scale(White_Queen, DEFAULT_IMAGE_SIZE)
White_Rook = pygame.transform.scale(White_Rook, DEFAULT_IMAGE_SIZE)

class Square:
    def __init__(self, pieceType, position):
        self.pieceType = pieceType
        self.posx = position[0]
        self.posy = position[1]
        self.position = position
        self.colour = (255, 0, 0)
        if sum(position) % 2 == 1:
            self.colour = WHITE
        else:
            self.colour = BLACK


class Board:
    def __init__(self, columns, rows, gameState, turn):
        self.columns = columns
        self.rows = rows
        self.gameState = np.empty((rows, columns), dtype=numpy.object_)  # creates a np array to fit objects
        for sq in gameState:
            self.gameState[sq.posx][sq.posy] = sq  # places objects in their subsequent positions

        self.Eval = None
        self.turn = turn
    def check_directions(self, directions, piece, distance):
        legal_moves = []
        for dir in directions:
            Stopped = False
            counter = 1
            while not Stopped:
                lookerX = piece.posx + dir[0] * counter
                lookerY = piece.posy + dir[1] * counter

                if lookerX <= 7 and lookerY <= 7 and lookerX >= 0 and lookerY >= 0 and counter < distance:
                    if self.gameState[lookerX][lookerY].pieceType != "-":
                        if (self.gameState[lookerX][lookerY].pieceType).isupper() == (
                        piece.pieceType).isupper():  # blocked by own pieces
                            Stopped = True
                        elif (self.gameState[lookerX][lookerY].pieceType).isupper() == (
                        piece.pieceType).isupper():  # capture
                            Stopped = True
                            legal_moves.append([lookerX, lookerY])
                    else:
                        legal_moves.append([lookerX, lookerY])
                    counter += 1
                else:
                    Stopped = True
        return legal_moves
    def get_pieces_legal_move(self, piece):
        legal_moves = []
        if (piece.pieceType).lower() == "r":
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]  #list of cardinal directions
            legal_moves = self.check_directions(directions, piece, 100)
            return legal_moves

        if (piece.pieceType).lower() == "n":
            directions = [[1, 2], [2, 1], [-1, -2], [-2, -1], [-1, 2], [-2, 1], [1, -2], [2, -1]]  # list of cardinal directions
            legal_moves = self.check_directions(directions, piece, 2)

            return legal_moves

        if (piece.pieceType).lower() == "b":
            directions = [[1, 1], [-1, -1], [-1, 1], [1, -1]]  # list of cardinal directions
            legal_moves = self.check_directions(directions, piece, 100)
            return legal_moves


        if (piece.pieceType).lower() == "q":
            directions = [[1, 1], [-1, -1], [-1, 1], [1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]  # list of cardinal directions
            legal_moves = self.check_directions(directions, piece, 100)
            return legal_moves

        if (piece.pieceType).lower() == "k":
            directions = [[1, 1], [-1, -1], [-1, 1], [1, -1], [0, 1], [0, -1], [1, 0],
                          [-1, 0]]  # list of cardinal directions
            legal_moves = self.check_directions(directions, piece, 2)
            return legal_moves

        if (piece.pieceType).lower() == "p":
            if piece.pieceType.isupper():  # very hardcoded but i don't see much of another way
                if self.get_piece((piece.posx, piece.posy - 1)) == '-':   # move forward 1
                    legal_moves.append([piece.posx, piece.posy - 1])
                    if piece.posy == 6 and self.get_piece((piece.posx, piece.posy - 2)) == '-':  # double move
                        legal_moves.append([piece.posx, piece.posy - 2])
                if self.get_piece((piece.posx + 1, piece.posy - 1)).islower():  # capture sideways
                    legal_moves.append([piece.posx + 1, piece.posy - 1])
                if self.get_piece((piece.posx - 1, piece.posy - 1)).islower():  # capture sideways
                    legal_moves.append([piece.posx - 1, piece.posy - 1])
                if piece.posy == 0:  # reach back rank
                    piece.pieceType = "Q"  # promote to queen


            if piece.pieceType.islower():
                if self.get_piece((piece.posx, piece.posy + 1)) == '-':
                    legal_moves.append([piece.posx, piece.posy + 1])
                    if piece.posy == 1 and self.get_piece((piece.posx, piece.posy + 2)) == '-':
                        legal_moves.append([piece.posx, piece.posy + 2])
                if self.get_piece((piece.posx + 1, piece.posy + 1)).isupper():
                    legal_moves.append([piece.posx + 1, piece.posy + 1])
                if self.get_piece((piece.posx - 1, piece.posy + 1)).isupper():
                    legal_moves.append([piece.posx - 1, piece.posy + 1])

            return legal_moves

    def check_legality(self, sq1, sq2):
        if (sq1.pieceType).islower() and self.turn == "w":
            return False
        if (sq1.pieceType).isupper() and self.turn == "b":
            return False

        legal_moves = self.get_pieces_legal_move(sq1)
        print(legal_moves)
        if list(sq2.position) in legal_moves:
            return True
        else:
            return False
    def in_check(self):
        
        #use the gamestate to determine if a king is in check
        return True

    def move_piece(self, p1_sq, p2_sq):
        #p1 = list(str(coords[p1[0]]) + str(coords[p1[1]])) #p1 position 1
        #p2 = list(str(coords[p2[0]]) + str(coords[p2[1]])) #p2 position 2

        #p1_sq = self.gameState[int(p1[0])][int(p1[1])] #square object at p1
        #p2_sq = self.gameState[int(p2[0])][int(p2[1])] #square object at p2

        if self.check_legality(p1_sq, p2_sq):
            p2_sq.pieceType = p1_sq.pieceType  # changes one squares piece to another
            p1_sq.pieceType = "-"  # makes the original square that the piece was on empty

            if p2_sq.pieceType == 'p' and p2_sq.posy == 7:  # reach back rank
                p2_sq.pieceType = "q"  # promote to queen
            if p2_sq.pieceType == 'P' and p2_sq.posy == 0:  # reach back rank
                p2_sq.pieceType = "Q"  # promote to queen

            if self.turn == "w":
                self.turn = "b"
            elif self.turn == "b":
                self.turn = "w"
        else:
            print("move is illegal")


    def get_piece(self, position):
        return self.gameState[position[0]][position[1]].pieceType

    def add_piece(self, position, pieceType):
        self.gameState[position[0]][position[1]].pieceType = pieceType


    def FENimport(self, FEN):
        #rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
        column = 0
        row = 0
        parody = False

        for i, ch in enumerate(FEN):
            if parody:
                self.turn = ch  # sets turn

            elif ch == '/':
                column += 1
                row = 0
            elif ch.isdigit():
                row += int(ch)
            elif ch == ' ':
                parody = True
            else:
                self.add_piece((row,column), ch)
                row += 1


    def display(self):
        pieceboard = []
        for row in self.gameState:
            for sq in row:
                pieceboard.append(str(sq.pieceType))
        pieceboard = np.array(pieceboard)
        pieceboard = pieceboard.reshape((8, 8))

        print(np.swapaxes(pieceboard, 0, 1))  # swaps axis for easy visualization
        #print('   a   b   c   d   e   f   g   h')


b1 = Board(rows, columns, [Square("-", (x, y)) for x in range(rows) for y in range(columns)], 'b')
b1.FENimport('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w')

#b1.move_piece('e3', 'f6')
#b1.move_piece('e3', 'f4')

def draw_board(board):
    for sq in board.gameState.flatten():
        pygame.draw.rect(screen, sq.colour,
                         pygame.Rect(sq.posx * squareSize, sq.posy * squareSize, squareSize, squareSize))

def draw_pieces(board):
    for sq in board.gameState.flatten():
        if sq.pieceType != "-":
            if sq.pieceType == "p":
                screen.blit(Black_Pawn, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))
            if sq.pieceType == "n":
                screen.blit(Black_Knight, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))
            if sq.pieceType == "b":
                screen.blit(Black_Bishop, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "k":
                screen.blit(Black_King, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "q":
                screen.blit(Black_Queen, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "r":
                screen.blit(Black_Rook, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))

            if sq.pieceType == "P":
                screen.blit(White_Pawn, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))
            if sq.pieceType == "N":
                screen.blit(White_Knight, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))
            if sq.pieceType == "B":
                screen.blit(White_Bishop, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "K":
                screen.blit(White_King, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "Q":
                screen.blit(White_Queen, (sq.posx * squareSize, sq.posy * squareSize))
            if sq.pieceType == "R":
                screen.blit(White_Rook, (sq.posx * squareSize - 3, sq.posy * squareSize + 3))

selected_squares = []
def get_mouse_inputs(x, y, board):
    global selected_squares
    for sq in board.gameState.flatten():
        if x > sq.posx*squareSize and x < sq.posx*squareSize + squareSize:
            if y > sq.posy*squareSize and y < sq.posy*squareSize + squareSize:
                if len(selected_squares) == 0 and sq.pieceType != "-": #first click and clicked on a piece
                    selected_squares.append(sq)
                elif len(selected_squares) == 1:
                    selected_squares.append(sq)
                    board.move_piece(selected_squares[0], selected_squares[1]) #passes 2 squares to move pieces from
                    selected_squares = []


# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            get_mouse_inputs(x, y, b1)

    # Update.

    draw_board(b1)
    draw_pieces(b1)
    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
