import numpy

import numpy as np
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
class Square:
    def __init__(self, pieceType, position):
        self.pieceType = pieceType
        self.posx = position[0]
        self.posy = position[1]
        self.position = position


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
        return legal_moves



    def check_legality(self, sq1, sq2):
        if (sq1.pieceType).islower() and self.turn == "w":
            return False
        if (sq1.pieceType).isupper() and self.turn == "b":
            return False

        legal_moves = self.get_pieces_legal_move(sq1)
        print(sq2.position, legal_moves)

        if list(sq2.position) in legal_moves or sq1.pieceType.lower() == "p":
            return True
        else:
            return False
    def in_check(self):
        #use the gamestate to determine if a king is in check
        return True

    def move_piece(self, p1, p2):
        p1 = list(str(coords[p1[0]]) + str(coords[p1[1]])) #p1 position 1
        p2 = list(str(coords[p2[0]]) + str(coords[p2[1]])) #p2 position 2

        p1_sq = self.gameState[int(p1[0])][int(p1[1])] #square object at p1
        p2_sq = self.gameState[int(p2[0])][int(p2[1])] #square object at p2

        if self.check_legality(p1_sq, p2_sq):
            p2_sq.pieceType = p1_sq.pieceType  # changes one squares piece to another
            p1_sq.pieceType = "-"  # makes the original square that the piece was on empty


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


b1 = Board(8, 8, [Square("-", (x, y)) for x in range(8) for y in range(8)], 'b')
b1.FENimport('8/8/8/8/4N3/k7/8/K7 w')

b1.move_piece('e4', 'g6')

b1.display()
