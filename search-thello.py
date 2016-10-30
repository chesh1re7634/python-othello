
from othello import othello, print_board
import hashlib
import math
import random

SCALAR = 1/math.sqrt(2.0)

class State(othello):
    def __init__(self, player="BLACK",board=None):
        othello.__init__(self, player)
        self.player = player
        if board is not None:
            self.board = board

    def next_state(self):
        next_move = self.random_strategy()
        board = self.makeMove(next_move)
        opp = self.getNextPlayer(board)
        next = State(player = opp, board = board)
        return next

    def terminal(self):
        if self.getNextPlayer() is None:
            return True
        return False

    def reward(self, player="BLACK"):
        return float(self.score(player))

    def __hash__(self):
        return int(hashlib.md5(str(self.board)).hexdigest(),16)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

class Node():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent
    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
    def update(self, reward):
        self.reward = reward
        self.visits += 1
    def fully_expanded(self):
        opp = self.state.opponent()
        if self.state.anyLegalMove() == True:
            if len(self.children) == len(self.state.getLegalMoves()):
                return True
        elif self.state.anyLegalMove(opp) == True:
            if len(self.children) == len(self.state.getLegalMoves(player=opp)):
                return True
        return False
    def __repr__(self):
        s = "Node; children: %d, visits: %d, reward: %f" % (len(self.children), self.visits, self.reward)
        return s

def UCTSEARCH(budget, root):
    for iter in range(budget):
        if iter % 100 == 0:
            print iter
        front = TREEPOLICY(root)
        reward = DEFAULTPOLICY(front.state)
        BACKUP(front, reward)
    return BESTCHILD(root,0)

def TREEPOLICY(node):
    while node.state.terminal() is False:
        if node.fully_expanded() is False:
            return EXPAND(node)
        else:
            node = BESTCHILD(node, SCALAR)
    return node

def EXPAND(node):
    tried_child = [c.state for c in node.children]
    next_state = node.state.next_state()
    while next_state in tried_child:
        next_state = node.state.next_state()
    node.add_child(next_state)
    return node.children[-1]

def BESTCHILD(node, scalar):
    bestscore = -10000
    bestchild = []
    for c in node.children:
        exploit = c.reward/c.visits
        explore = math.sqrt(math.log(2*node.visits)/float(c.visits))
        score = exploit + scalar*explore
        if score == bestscore:
            bestchild.append(c)
        if score > bestscore:
            bestchild = [c]
            bestscore = score
    if len(bestchild) == 0:
        raise ValueError("bestchild is empty")
    return random.choice(bestchild)

def DEFAULTPOLICY(state):
    while state.terminal() is False:
        state = state.next_state()
    return state.reward()

def BACKUP(node, reward):
    while node != None:
        node.visits += 1
        node.reward += reward
        node = node.parent
    return

if __name__ == "__main__":
    current_node = Node(State())

    current_node = UCTSEARCH(1000, current_node)

    print current_node.state.__repr__()

    #print current_node.__repr__()



