#-*- coding: utf-8 -*- #
import random


def print_board(board):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in xrange(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    print rep

class othello():
    EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
    # To refer to neighbor squares we can add a direction to a square.
    UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
    UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
    DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

    def __init__(self, player="BLACK"):
        self.initial_board()
        self.player = player

    def squares(self):
        return [i for i in range(11,89) if 1 <= (i % 10) <= 8]

    def initial_board(self):
        board = self.board = [self.OUTER] * 100

        for sq in self.squares():
            board[sq] = self.EMPTY

        board[44], board[45] = self.BLACK, self.WHITE
        board[54], board[55] = self.WHITE, self.BLACK

        return board

    def __repr__(self):
        rep = ''
        rep += 'PLAYER : %s\n\n' % self.player
        rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
        for row in xrange(1, 9):
            begin, end = 10 * row + 1, 10 * row + 9
            rep += '%d %s\n' % (row, ' '.join(self.board[begin:end]))
        return rep

    def opponent(self, player=None):
        if player is None:
            return "BLACK" if self.player is "WHITE" else "WHITE"
        else:
            return "BLACK" if player is "WHITE" else "WHITE"

    def getNextPlayer(self,board = None):
        opp = self.opponent()
        board = self.board if board is None else board
        if self.anyLegalMove(player=opp, board=board):
            return opp
        elif self.anyLegalMove(player=None, board=board):
            return self.player

        return None

    def isOwnerSqaure(self, owner, square, board=None):
        board = self.board if board is None else board
        if owner is "BLACK":
            if board[square] == self.BLACK:
                return True
            else:
                return False
        elif owner is "WHITE":
            if board[square] == self.WHITE:
                return True
            else:
                return False

    def findBracket(self, move, direction, player=None,board=None):
        player = self.player if player is None else player
        opp = self.opponent(player)
        board = self.board if board is None else board

        if board[move] is not self.EMPTY:
            return None
        bracket = move + direction
        if self.isOwnerSqaure(opp, bracket,board) is False:
            return None
        while self.isOwnerSqaure(opp, bracket,board):
            bracket += direction
        return bracket if self.isOwnerSqaure(player, bracket,board) else None

    def isLegalMove(self, move, player=None, board=None):
        player = self.player if player is None else player
        board = self.board if board is None else board
        hasbracket = lambda direction: self.findBracket(move, direction, player, board)
        return self.board[move] == self.EMPTY and any(map(hasbracket, self.DIRECTIONS))

    def getLegalMoves(self,player=None, board=None):
        player = self.player if player is None else player
        board = self.board if board is None else board
        return [sq for sq in self.squares() if self.isLegalMove(sq, player, board)]

    def anyLegalMove(self, player=None,board=None):
        player = self.player if player is None else player
        board= self.board if board is None else board
        return any(self.isLegalMove(sq, player, board) for sq in self.squares())

    def makeMove(self, move):
        board = list(self.board)
        for d in self.DIRECTIONS:
            self.makeFlips(move, d, board)
        board[move] = self.BLACK if self.player is "BLACK" else self.WHITE
        return board

    def makeFlips(self, move, direction, board=None):
        piece = self.BLACK if self.player is "BLACK" else self.WHITE
        board = self.board if board is None else board

        bracket = self.findBracket(move=move, direction=direction, board=board)
        if not bracket:
            return
        square = move + direction
        while square != bracket:
            board[square] = piece
            square += direction

    def random_strategy(self):
        moves = self.getLegalMoves()
        if len(moves) == 0:
            raise ValueError("player : %s \n" % self.player)
        return random.choice(self.getLegalMoves())

    def score(self, player=None):
        player = self.player if player is None else player
        opp = self.opponent(player)
        mine, theirs = 0, 0

        for sq in self.squares():
            if self.isOwnerSqaure(player, sq):
                mine += 1
            elif self.isOwnerSqaure(opp, sq):
                theirs += 1
        return mine - theirs

    @property
    def player(self):
        return self.player

    @player.setter
    def player(self, value):
        self.player = value

    @property
    def board(self):
        return self.board

    @board.setter
    def board(self, value):
        self.board = value



if __name__ == "__main__":
    game = othello()

    for i in range(100):
        move = game.random_strategy()
        board = game.makeMove(move)
        game.board = board
        if game.getNextPlayer() is not None:
            game.player = game.getNextPlayer()
        else:
            break



    print game.__repr__()















