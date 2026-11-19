# my_team.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random
import contest.util as util
import search

from contest.capture_agents import CaptureAgent
from contest.game import Directions
from contest.util import nearest_point


#################
# Team creation #
#################

def create_team(first_index, second_index, is_red,
                first='OffensiveMinimaxAgent', second='DefensiveAlphaBetaAgent', num_training=0):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --red_opts and --blue_opts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    return [eval(first)(first_index), eval(second)(second_index)]


##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that choose score-maximizing actions
    """

    def __init__(self, index, time_for_computing=.1):
        super().__init__(index, time_for_computing)
        self.start = None

    def register_initial_state(self, game_state):
        self.start = game_state.get_agent_position(self.index)
        CaptureAgent.register_initial_state(self, game_state)

    def choose_action(self, game_state):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = game_state.get_legal_actions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(game_state, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        max_value = max(values)
        best_actions = [a for a, v in zip(actions, values) if v == max_value]

        food_left = len(self.get_food(game_state).as_list())

        if food_left <= 2:
            best_dist = 9999
            best_action = None
            for action in actions:
                successor = self.get_successor(game_state, action)
                pos2 = successor.get_agent_position(self.index)
                dist = self.get_maze_distance(self.start, pos2)
                if dist < best_dist:
                    best_action = action
                    best_dist = dist
            return best_action

        return random.choice(best_actions)

    def get_successor(self, game_state, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = game_state.generate_successor(self.index, action)
        pos = successor.get_agent_state(self.index).get_position()
        if pos != nearest_point(pos):
            # Only half a grid position was covered
            return successor.generate_successor(self.index, action)
        else:
            return successor

    def evaluate(self, game_state, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.get_features(game_state, action)
        weights = self.get_weights(game_state, action)
        return features * weights

    def get_features(self, game_state, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.get_successor(game_state, action)
        features['successor_score'] = self.get_score(successor)
        return features

    def get_weights(self, game_state, action):
        """
        Normally, weights do not depend on the game state.  They can be either
        a counter or a dictionary.
        """
        return {'successor_score': 1.0}


class OffensiveReflexAgent(ReflexCaptureAgent):
    """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """

    def get_features(self, game_state, action):
        features = util.Counter()
        successor = self.get_successor(game_state, action)
        food_list = self.get_food(successor).as_list()
        features['successor_score'] = -len(food_list)  # self.getScore(successor)

        # Compute distance to the nearest food

        if len(food_list) > 0:  # This should always be True,  but better safe than sorry
            my_pos = successor.get_agent_state(self.index).get_position()
            min_distance = min([self.get_maze_distance(my_pos, food) for food in food_list])
            features['distance_to_food'] = min_distance
        return features

    def get_weights(self, game_state, action):
        return {'successor_score': 100, 'distance_to_food': -1}


class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def get_features(self, game_state, action):
        features = util.Counter()
        successor = self.get_successor(game_state, action)

        my_state = successor.get_agent_state(self.index)
        my_pos = my_state.get_position()

        # Computes whether we're on defense (1) or offense (0)
        features['on_defense'] = 1
        if my_state.is_pacman: features['on_defense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]
        invaders = [a for a in enemies if a.is_pacman and a.get_position() is not None]
        features['num_invaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.get_maze_distance(my_pos, a.get_position()) for a in invaders]
            features['invader_distance'] = min(dists)

        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def get_weights(self, game_state, action):
        return {'num_invaders': -1000, 'on_defense': 100, 'invader_distance': -10, 'stop': -100, 'reverse': -2}




############ EMMA NO SABE LO Q ESTA PASANDO

##### LAB 1 SUPONGO YOQSE

class OffensiveAStarAgent(ReflexCaptureAgent):
    def register_initial_state(self, game_state):
        super().register_initial_state(game_state)
        # Override to add home_border
        width = game_state.data.layout.width
        height = game_state.data.layout.height
        border_x = (width // 2) - 1 if self.red else (width // 2)
        self.home_border = [
            (border_x, y) for y in range(height)
            if not game_state.has_wall(border_x, y)
        ]

    def a_star_heuristic(self, state, problem):
        if not problem.food:
            return 0
        return min(self.get_maze_distance(state, goal) for goal in problem.food)

    def choose_action(self, game_state):
        my_state = game_state.get_agent_state(self.index)
        my_pos = game_state.get_agent_position(self.index)
        food_list = self.get_food(game_state).as_list()

        # find ghosts
        enemies = [game_state.get_agent_state(i) for i in self.get_opponents(game_state)]
        ghosts = [
            nearest_point(e.get_position()) for e in enemies
            if not e.is_pacman and e.get_position() is not None and e.scared_timer <= 1
        ]

        if my_state.num_carrying >= 3 or len(food_list) <= 2:
            goals = self.home_border
        else:
            goals = food_list

        problem = search.FoodSearchProblem(game_state, my_pos, goals, ghosts)
        path = search.a_star_search(problem, self.a_star_heuristic)

        if path:
            return path[0]
        
        return Directions.STOP

class DefensiveAStarAgent(ReflexCaptureAgent):

    def register_initial_state(self, game_state):
        super().register_initial_state(game_state)
        width = game_state.data.layout.width
        height = game_state.data.layout.height
        self.mid_y = height // 2
        border_x = (width // 2) - 1 if self.red else (width // 2)

        # Block enemy territory
        enemy_xs = range(border_x + 1, width) if self.red else range(0, border_x)
        self.enemy_territory = {(x, y) for x in enemy_xs for y in range(height)}

        # Vertical defense zone (within 3 steps of border)
        xs = [border_x - d for d in range(4)] if self.red else [border_x + d for d in range(4)]
        self.patrol_zone = [
            (x, y) for x in xs for y in range(height)
            if not game_state.has_wall(x, y)
        ]
        self.patrol_target = None

    def a_star_heuristic(self, state, problem):
        if not problem.food:
            return 0
        return min(self.get_maze_distance(state, goal) for goal in problem.food)

    def choose_action(self, game_state):
        my_pos = nearest_point(game_state.get_agent_position(self.index))
        opponents = self.get_opponents(game_state)
        enemies = [game_state.get_agent_state(i) for i in opponents]

        # 1. If an enemy Pacman is visible, chase
        visible = [
            nearest_point(e.get_position()) for e in enemies
            if e.is_pacman and e.get_position() is not None
        ]
        if visible:
            self.patrol_target = None
            goals = visible
        else:
            # 2. Pick a patrol point in the 3-tile zone and stick to it until reached
            if self.patrol_target is None or my_pos == self.patrol_target:
                dists = game_state.get_agent_distances()
                min_dist = min(dists[i] for i in opponents)

                if min_dist > 10:
                    if my_pos[1] < self.mid_y:
                        candidates = [p for p in self.patrol_zone if p[1] >= self.mid_y]
                    else:
                        candidates = [p for p in self.patrol_zone if p[1] < self.mid_y]
                else:
                    candidates = [p for p in self.patrol_zone if abs(p[1] - my_pos[1]) <= 3]

                if not candidates:
                    candidates = self.patrol_zone
                self.patrol_target = min(candidates, key=lambda p: self.get_maze_distance(my_pos, p))

            goals = [self.patrol_target]

        problem = search.FoodSearchProblem(game_state, my_pos, goals, blocked=self.enemy_territory)
        path = search.a_star_search(problem, self.a_star_heuristic)

        if path:
            return path[0]
        
        return Directions.STOP

##### LAB 2 ??
 
class OffensiveMinimaxAgent(OffensiveAStarAgent):

    def __init__(self, index, time_for_computing=.1):
        super().__init__(index, time_for_computing)
        self.depth = 2

    def choose_action(self, game_state):
        my_pos = nearest_point(game_state.get_agent_position(self.index))

        nearby_ghosts = []
        for i in self.get_opponents(game_state):
            enemy = game_state.get_agent_state(i)
            if not enemy.is_pacman and enemy.get_position() is not None and enemy.scared_timer <= 1:
                if self.get_maze_distance(my_pos, nearest_point(enemy.get_position())) <= 3:
                    nearby_ghosts.append(i)

        if not nearby_ghosts:
            return super().choose_action(game_state)

        agents = [self.index] + nearby_ghosts
        max_score = float('-inf')
        move = None
        acciones = [a for a in game_state.get_legal_actions(self.index) if a != Directions.STOP]
        if not acciones:
            acciones = game_state.get_legal_actions(self.index)

        for a in acciones:
            juego = game_state.generate_successor(self.index, a)
            score = self.minimax(juego, piso=0, agent=1, agents=agents)

            if score > max_score:
                max_score = score
                move = a

        return move

    def minimax(self, game_state, piso, agent, agents):
        if game_state.is_over() or piso == self.depth:
            return self.evaluation_function(game_state)

        curr_agent = agents[agent]
        if game_state.get_agent_state(curr_agent).get_position() is None:
            return self.evaluation_function(game_state)

        acciones = game_state.get_legal_actions(curr_agent)
        if not acciones:
            return self.evaluation_function(game_state)

        num_agents = len(agents)

        if curr_agent == self.index:    # Pacman (MAX turn)
            final_value = float('-inf')
            for i in acciones:
                juego = game_state.generate_successor(curr_agent, i)
                if agent + 1 == num_agents:
                    value = self.minimax(juego, piso + 1, 0, agents)
                else:
                    value = self.minimax(juego, piso, agent + 1, agents)
                final_value = max(final_value, value)
        else:   # Ghosts (MIN turn)
            final_value = float('inf')
            for a in acciones:
                juego = game_state.generate_successor(curr_agent, a)
                if agent + 1 == num_agents:
                    value = self.minimax(juego, piso + 1, 0, agents)
                else:
                    value = self.minimax(juego, piso, agent + 1, agents)
                final_value = min(final_value, value)

        return final_value

    def evaluation_function(self, game_state):
        my_state = game_state.get_agent_state(self.index)
        new_pos = nearest_point(my_state.get_position())
        new_food = self.get_food(game_state).as_list()

        if new_pos == self.start:
            return -9999

        score = self.get_score(game_state) * 200 + my_state.num_carrying * 50

        if my_state.num_carrying >= 3 or len(new_food) <= 2:
            min_home = min(self.get_maze_distance(new_pos, b) for b in self.home_border)
            score += 20.0 / (min_home + 1)
        elif new_food:
            min_food = min(self.get_maze_distance(new_pos, f) for f in new_food)
            score += 10.0 / (min_food + 1)

        # Panic if ghost is close
        for i in self.get_opponents(game_state):
            enemy = game_state.get_agent_state(i)
            ghost_pos = enemy.get_position()
            if ghost_pos is not None and not enemy.is_pacman and enemy.scared_timer <= 1:
                ghost_dist = self.get_maze_distance(new_pos, nearest_point(ghost_pos))
                if ghost_dist <= 1:
                    return -9999
                elif ghost_dist == 2:
                    score -= 40
                else:
                    score -= 10.0 / ghost_dist

        return score


class DefensiveAlphaBetaAgent(DefensiveAStarAgent):

    def __init__(self, index, time_for_computing=.1):
        super().__init__(index, time_for_computing)
        self.depth = 2  # 2 full rounds (piso 1 and 2) so it never exceeds the 0.1s move timer

    def choose_action(self, game_state):
        my_pos = nearest_point(game_state.get_agent_position(self.index))

        # Trigger Alpha-Beta for invaders within 5 tiles, or enemies within 3 tiles at the border
        nearby_enemies = []
        for i in self.get_opponents(game_state):
            enemy = game_state.get_agent_state(i)
            if enemy.get_position() is not None:
                dist = self.get_maze_distance(my_pos, nearest_point(enemy.get_position()))
                if (enemy.is_pacman and dist <= 5) or dist <= 3:
                    nearby_enemies.append(i)

        if not nearby_enemies:
            return super().choose_action(game_state)

        agents = [self.index] + nearby_enemies
        maximum = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        maxmove = None
        acciones = [a for a in game_state.get_legal_actions(self.index) if a != Directions.STOP]
        if not acciones:
            acciones = game_state.get_legal_actions(self.index)

        for a in acciones:
            juego = game_state.generate_successor(self.index, a)
            value = self.min_value(juego, 1, alpha, beta, 1, agents)

            if value > maximum:
                maximum = value
                maxmove = a

            if maximum > beta:
                return maxmove

            alpha = max(alpha, maximum)

        return maxmove

    def max_value(self, game_state, piso, alpha, beta, agents):
        if game_state.is_over() or piso > self.depth:
            return self.evaluation_function(game_state)

        finalvalue = float('-inf')
        acciones = game_state.get_legal_actions(self.index)
        if not acciones:
            return self.evaluation_function(game_state)

        for a in acciones:
            juego = game_state.generate_successor(self.index, a)
            value = self.min_value(juego, piso, alpha, beta, 1, agents)
            finalvalue = max(finalvalue, value)

            if finalvalue > beta:
                return finalvalue

            alpha = max(alpha, finalvalue)

        return finalvalue

    def min_value(self, game_state, piso, alpha, beta, fantasma, agents):
        if game_state.is_over() or piso > self.depth:
            return self.evaluation_function(game_state)

        curr_agent = agents[fantasma]
        if game_state.get_agent_state(curr_agent).get_position() is None:
            return self.evaluation_function(game_state)

        finalvalue = float('inf')
        acciones = game_state.get_legal_actions(curr_agent)
        if not acciones:
            return self.evaluation_function(game_state)

        for a in acciones:
            juego = game_state.generate_successor(curr_agent, a)

            if fantasma + 1 == len(agents):
                value = self.max_value(juego, piso + 1, alpha, beta, agents)
            else:
                value = self.min_value(juego, piso, alpha, beta, fantasma + 1, agents)

            finalvalue = min(finalvalue, value)

            if finalvalue < alpha:
                return finalvalue

            beta = min(beta, finalvalue)

        return finalvalue

    def evaluation_function(self, game_state):
        my_state = game_state.get_agent_state(self.index)
        my_pos = nearest_point(my_state.get_position())

        if my_pos in self.enemy_territory or my_state.is_pacman:
            return -9999

        score = self.get_score(game_state) * 200

        enemies = [game_state.get_agent_state(i) for i in self.get_opponents(game_state)]
        invaders = [e for e in enemies if e.is_pacman and e.get_position() is not None]

        score -= len(invaders) * 1000

        if invaders:
            min_invader_dist = min(
                self.get_maze_distance(my_pos, nearest_point(e.get_position()))
                for e in invaders
            )
            if my_state.scared_timer > 0:
                score -= abs(min_invader_dist - 2) * 25
            else:
                score -= min_invader_dist * 15
        else:
            border_enemies = [e for e in enemies if e.get_position() is not None]
            if border_enemies:
                min_border_dist = min(
                    self.get_maze_distance(my_pos, nearest_point(e.get_position()))
                    for e in border_enemies
                )
                score -= min_border_dist * 5

        return score

    