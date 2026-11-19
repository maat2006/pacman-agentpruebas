# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""
## nuevo
import contest.util as util
from contest.game import Directions
from contest.util import nearest_point



class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in obj-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# def addSuccessors(problem, addCost=True):

class SearchNode:
    def __init__(self, parent, node_info):
        """
            parent: parent SearchNode.

            node_info: tuple with three elements => (coord, action, cost)

            coord: (x,y) coordinates of the node position

            action: Direction of movement required to reach node from
            parent node. Possible values are defined by class Directions from
            game.py

            cost: cost of reaching this node from the starting node.
        """

        self.__state = node_info[0]
        self.action = node_info[1]
        self.cost = node_info[2] if parent is None else node_info[2] + parent.cost
        self.parent = parent

    # The coordinates of a node cannot be modified, se we just define a getter.
    # This allows the class to be hashable.
    @property
    def state(self):
        return self.__state

    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        path.reverse()
        return path
    
    # Consider 2 nodes to be equal if their coordinates are equal (regardless of everything else)
    # def __eq__(self, __o: obj) -> bool:
    #     if (type(__o) is SearchNode):
    #         return self.__state == __o.__state
    #     return False

    # # def __hash__(self) -> int:
    # #     return hash(self.__state)


"""  QUESTION 1  """

def initial_dfs(problem): 
    """
    Our initial solution to the problem.
    We cleaned and improved the code, which is the function depth_first_search() defined below.
    
    NOT OUR FINAL SOLUTION
    """
    
    expandedNodes = []                          # We create one array for explored nodes
    expandedCaminos = []                        # Another array for storing the path to the current point
    frontier = util.Stack()                     # Stack frontier
    caminosFrontier = util.Stack()              # Stack for paths
    frontier.push(problem.get_start_state())    # We introduce the initial state to the frontier
    caminosFrontier.push([])                    # The initial path is no move
    condition = True

    while condition:        
        if frontier.is_empty():  # If the frontier is empty and we have not reached the goal, we return an empty path (no solution)
            return []
        valorCamino = caminosFrontier.pop() # We pop the frontier value in both stacks
        valor = frontier.pop()
        if valor in expandedNodes:        # If the node is already expanded, we go to the next iteration
            continue
        expandedCaminos = expandedCaminos + [valorCamino]       # If not, we add a new value to the path arrays
        expandedNodes = expandedNodes + [valor]
        # Goal check
        if (problem.is_goal_state(expandedNodes[-1])):
            condition = False  # If we find a solution, we exit the loop
            break
        for i in (problem.get_successors(expandedNodes[len(expandedNodes)-1])):  # A loop to check all the successors of the last expanded node
            if not(i[0] in expandedNodes):   # If the element is not already explored, we add it to the frontier. We don't care if it's in the frontier, as we are using a stack. In the stack, we check the last inserted element.
                frontier.push(i[0])
                caminosFrontier.push(expandedCaminos[-1] + [i[1]])  # For creating the new path, we add the current one for the expanded node. After that we add the movement of the successor.
    caminoFinal = expandedCaminos[-1]      # The path we return contains the entire route to the last expanded node. If we have reached the goal node, this path is the current solution.
    return caminoFinal

            
def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.get_start_state())
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))

    THIS IS OUR FINAL SOLUTION
    """
    # Initialization
    expandedNodes = []
    frontier = util.Stack() # The frontier is a stack that will hold (current position, path)
    frontier.push((problem.get_start_state(), []))  # We push the initial state and an empty initial path 
    # Loop
    while not frontier.is_empty():  # Loop until the frontier is empty
        node, path = frontier.pop()    # Pop the frontier value
        # Goal check
        if problem.is_goal_state(node): # If it is a goal state,
            return path                 # We return the path to it

        if node not in expandedNodes:   # If the current node has not been explored,
            expandedNodes.append(node)  # We add it to the expanded nodes
            for successor, action, cost in problem.get_successors(node):  # For every successor
                if successor not in expandedNodes:      # If the successor is not already explored, we push it to frontier
                    frontier.push((successor, path + [action]))

    return []   # If we exit the loop without reaching goal state, we return an empty path   


"""  QUESTION 2  """

def initial_bfs(problem):
    """
    Our initial solution to the problem.
    We cleaned and improved the code, which is the function breadth_first_search() defined below.
    
    NOT OUR FINAL SOLUTION
    """

    expandedNodes = []                          # We create one array for explored nodes
    expandedCaminos = []                        # Another array for storing the path to the current point
    frontier = util.Queue()                     # Frontier queue
    caminosFrontier = util.Queue()              # Paths queue
    frontier.push(problem.get_start_state())    # We introduce the initial state to the frontier
    caminosFrontier.push([])                    # The initial path is no move
    condition = True

    while condition:
        if frontier.is_empty() == True: # If the frontier is empty and we have not reached the goal, we return an empty path (no solution)
            return []
        valorCamino = caminosFrontier.pop() # We pop the frontier value in both queues
        valor = frontier.pop()
        if valor in expandedNodes:        # If the node is already expanded, we go to the next iteration
            continue
        expandedCaminos = expandedCaminos + [valorCamino] # If not, we add a new value to the path arrays
        expandedNodes = expandedNodes + [valor]
        # Goal check
        if (problem.is_goal_state(expandedNodes[len(expandedNodes)-1])):
            condition = False # If we find a solution, we exit the loop
            break
        for i in (problem.get_successors(expandedNodes[len(expandedNodes)-1])): # A loop to check all the successors of the last expanded node
            if not(i[0] in expandedNodes):  # If the element is not already explored, we add it to the frontier.
                frontier.push(i[0])
                caminosFrontier.push(expandedCaminos[len(expandedCaminos)-1]+[i[1]])    # For creating the new path, we add the current one for the expanded node. After that we add the movement of the successor.

    caminoFinal = expandedCaminos[len(expandedCaminos)-1] # The path we return contains the entire route to the last expanded node. If we have reached the goal node, this path is the current solution.
    return caminoFinal


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    
    THIS IS OUR FINAL SOLUTION
    """
    # Initialization
    expandedNodes = []  
    frontier = util.Queue() # The frontier is a QUEUE that will hold (current position, path)
    frontier.push((problem.get_start_state(), [])) # We queue the initial state and an empty initial path
    while not frontier.is_empty():      # Loop until the frontier is empty
        node, path = frontier.pop()     # Dequeue frontier
        # Goal check
        if problem.is_goal_state(node): # If it is a goal state,
            return path                 # We return the path to it

        if node not in expandedNodes:   # If the current node has not been explored,
            expandedNodes.append(node)  # We add it to the expanded nodes
            for successor, action, cost in problem.get_successors(node):    # For every successor
                if successor not in expandedNodes:                          # If the successor is not already explored, we queue it into the frontier
                    frontier.push((successor, path + [action]))             # We update the frontier (node and path)

    return []   # If we exit the loop without reaching goal state, we return an empty path 


"""  QUESTION 3  """

def initial_ucs(problem):
    """
    Our initial solution to the problem.
    We cleaned and improved the code, which is the function uniform_cost_search() defined below.
    
    NOT OUR FINAL SOLUTION
    """

    # We initialize 3 arrays (nodes, paths and costs)
    expandedNodes = []
    expandedCaminos = []
    expandedCoste = []
    # We now use PRIORITY QUEUES
    frontier = util.PriorityQueue()         # One for the frontier
    caminosFrontier = util.PriorityQueue()  # Another one for the paths
    costeFrontier = util.PriorityQueue()    # And another one for the costs
    # We initialize with the start state, empty path and cost 0
    frontier.push(problem.get_start_state(), 0)
    caminosFrontier.push([], 0)
    costeFrontier.push(0, 0)
    condition = True

    while condition:
        if frontier.is_empty() == True:
            return []   # If the frontier is empty and we have not reached the goal, we return an empty path (no solution)
        valorCamino = caminosFrontier.pop()     # We dequeue the frontier values in the queues
        valor = frontier.pop()
        valorCoste = costeFrontier.pop()
        if valor in expandedNodes:             # If the node is already expanded, we go to the next iteration
            continue
        # If not, we add new values to the path arrays
        expandedCaminos = expandedCaminos + [valorCamino]
        expandedNodes = expandedNodes + [valor]
        expandedCoste = expandedCoste + [valorCoste]
        # Goal check
        if (problem.is_goal_state(expandedNodes[len(expandedNodes)-1])):
            condition = False   # If we find a solution, we exit the loop
            break
        for i in (problem.get_successors(expandedNodes[len(expandedNodes)-1])): # We check all the successors of the last expanded node
            if not(i[0] in expandedNodes): # If the element is not already explored, we add it to the frontier.
                # We must update the cost, the frontier and the path
                costeee = i[2] + expandedCoste[len(expandedCoste)-1]
                frontier.push(i[0], costeee)
                caminosFrontier.push(expandedCaminos[len(expandedCaminos)-1]+[i[1]], costeee)
                costeFrontier.push(costeee, costeee)
    caminoFinal = expandedCaminos[len(expandedCaminos)-1]   # The path we return contains the entire route to the last expanded node. If we have reached the goal node, this path is the current solution.
    return caminoFinal


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    
    THIS IS OUR FINAL SOLUTION
    """
    # Initialization
    expandedNodes = []
    frontier = util.PriorityQueue()         # The frontier is a PRIORITY QUEUE holding (state, path, cost), with cost priority
    frontier.push((problem.get_start_state(), [], 0), 0)  # We push the initial state, an empty initial path and an initial cost of 0, and a priority same as cost
    # Loop
    while not frontier.is_empty():          # Loop until the frontier is empty
        node, path, cost = frontier.pop()   # Dequeue frontier
        # Goal check
        if problem.is_goal_state(node):     # If it is a goal state
            return path                     # We return the path to it
        
        if node not in expandedNodes:       # If the current node has not been explored,
            expandedNodes.append(node)      # We add it to the expanded nodes
            for successor, action, cost2 in problem.get_successors(node):   # For every successor
                if successor not in expandedNodes: 
                    newCost = cost + cost2  # The new cost is the sum of the cost for reaching the current node + cost for arriving to the successor
                    frontier.push((successor, path + [action], newCost), newCost)
    return []   # If we exit the loop without reaching goal state, we return an empty path 


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


"""  QUESTION 4  """

def initial_a_star(problem, heuristic=null_heuristic):
    """
    Our initial solution to the problem.
    We cleaned and improved the code, which is the function a_star_search() defined below.
    
    NOT OUR FINAL SOLUTION
    """
    # We initialize 3 arrays (nodes, paths and costs)
    expandedNodes = []
    expandedCaminos = []
    expandedCoste = []
    # Priority queues for frontier, paths, and costs
    frontier = util.PriorityQueue()
    caminosFrontier = util.PriorityQueue()
    costeFrontier = util.PriorityQueue()
    # Calculate initial priority f(start) = g(start) + h(start)
    startState = problem.get_start_state()
    startPriority = 0 + heuristic(startState, problem)
    # We initialize with start state, empty path, cost 0, and start priority f(start)
    frontier.push(startState, startPriority)
    caminosFrontier.push([], startPriority)
    costeFrontier.push(0, startPriority)
    condition = True

    while condition:
        if frontier.is_empty(): # If the frontier is empty and we have not reached the goal, we return an empty path (no solution)
            return []
        valorCamino = caminosFrontier.pop()  # We dequeue the frontier values in the queues
        valor = frontier.pop()
        valorCoste = costeFrontier.pop()
        if valor in expandedNodes:           # If the node is already expanded, we go to the next iteration
            continue
        # If not, we add new values to the path arrays
        expandedCaminos = expandedCaminos + [valorCamino]
        expandedNodes = expandedNodes + [valor]
        expandedCoste = expandedCoste + [valorCoste]
        # Goal check
        if (problem.is_goal_state(expandedNodes[len(expandedNodes)-1])):
            condition = False   # If we find a solution, we exit the loop
            break
        for i in (problem.get_successors(expandedNodes[len(expandedNodes)-1])):
            if not (i[0] in expandedNodes): # If the element is not already explored, we add it to the frontier
                # We must update the cost, the frontier and the path
                costeee = i[2] + expandedCoste[-1]  # g(n)
                h = heuristic(i[0], problem)        # h(n)
                f = costeee + h                     # f(n) = g(n) + h(n)
                frontier.push(i[0], f)
                caminosFrontier.push(expandedCaminos[len(expandedCaminos)-1]+[i[1]], f)
                costeFrontier.push(costeee, f)
    caminoFinal = expandedCaminos[len(expandedCaminos)-1]   # The path we return contains the entire route to the last expanded node. If we have reached the goal node, this path is the current solution.
    return caminoFinal


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    
    THIS IS OUR FINAL VERSION
    """
    # Initialization
    expandedNodes = []
    frontier = util.PriorityQueue() # The frontier is a PRIORITY QUEUE holding (state, path, cost), with f = g + h priority
    startState = problem.get_start_state()
    frontier.push((startState, [], 0), 0 + heuristic(startState, problem))  # We queue the initial state, an empty initial path and an initial cost of 0, and the priority f = 0 + h(start)
    # Loop
    while not frontier.is_empty():              # Loop until the frontier is empty
            node, path, cost = frontier.pop()   # Dequeue frontier
            # Goal check
            if problem.is_goal_state(node):     # If it is a goal state
                return path                     # We return the path to it
            
            if node not in expandedNodes:       # If the current node has not been explored,
                expandedNodes.append(node)      # We add it to the expanded nodes
                for successor, action, cost2 in problem.get_successors(node):   # For every successor
                    if successor not in expandedNodes:      # If successor is not already explored, calculate f = g + h and queue
                        newCost = cost + cost2              # Cumulative path cost g(n)
                        h = heuristic(successor, problem)   # Heuristic cost h(n)
                        f = newCost + h                     # Total estimated cost f(n) = g(n) + h(n)
                        frontier.push((successor, path + [action], newCost), f)
    return [] # If we exit the loop without reaching goal state, we return an empty path 

class FoodSearchProblem():
    def __init__(self, game_state, my_pos, food_list, ghosts=[], blocked=set()):
        self.walls = game_state.get_walls()
        self.start = nearest_point(my_pos)
        self.food = set(food_list)
        # for attack
        self.ghosts = ghosts
        # for defence
        self.blocked = blocked

    def get_start_state(self):
        return self.start

    def is_goal_state(self, state):
        return state in self.food

    def get_successors(self, state):
        successors = []
        x, y = state
        moves = [
            (Directions.NORTH, (0, 1)),
            (Directions.SOUTH, (0, -1)),
            (Directions.EAST, (1, 0)),
            (Directions.WEST, (-1, 0)),
        ]
        for action, (dx, dy) in moves:
            nx, ny = x + dx, y + dy
            if not self.walls[nx][ny] and (nx, ny) not in self.blocked:
                cost = 1
                # added penalization for ghost distance
                for ghost_pos in self.ghosts:
                    dist = util.manhattan_distance((nx, ny), ghost_pos)
                    if dist <= 1:
                        cost += 1000
                    elif dist == 2:
                        cost += 600
                    elif dist == 3:
                        cost += 200
                successors.append(((nx, ny), action, cost))
        return successors

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
