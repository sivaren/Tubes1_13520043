from BotWithObjFunc import BotWithObjFunc
from GameAction import GameAction
from GameState import GameState
from StateManager import StateManager
import multiprocessing as mp
import sys

MAX_VAL = sys.maxsize
MIN_VAL = -1 * MAX_VAL

class BotMinimaxPruning(BotWithObjFunc):
    def __init__(self) -> None:
        super().__init__()
    
    def get_action(self, state: GameState) -> GameAction:
        mgr = mp.Manager()
        rv = mgr.dict()
        timeinst = mp.Process(target=self.minimax, args=(state, True, state.player1_turn, rv))
        timeinst.start()
        timeinst.join(5)
        if timeinst.is_alive():
            timeinst.terminate()
            timeinst.join()
        return rv.values()[0]

    def minimax(self, state: GameState, isMax: bool, pov_player1: bool, rv: GameAction):
        max_depth = 5
        if (isMax):
            best_action, _ = self.maximum(state, max_depth, MIN_VAL, MAX_VAL, pov_player1, rv)
        else:
            best_action, _ = self.minimum(state, max_depth, MIN_VAL, MAX_VAL, pov_player1, rv)
        rv[0]= best_action
        return best_action

    
    def minimum(self, state: GameState, depth: int, alpha: int, beta: int, pov_player1: bool, rv : GameAction):
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        # base max value
        val = MAX_VAL
        rv[0]= actions[0]
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                _, temp_val = self.minimum(newState, depth - 1, alpha, beta, pov_player1,rv)
            else:
                _, temp_val = self.maximum(newState, depth - 1, alpha, beta, pov_player1,rv)

            if (temp_val < val):
                val = temp_val
                best_action = action
                rv[0] = best_action
            
            # update beta value
            beta = val if (val < beta) else beta
            # pruning
            if (beta <= alpha):
                break
        return best_action, val
        
    
    def maximum(self, state: GameState, depth: int, alpha: int, beta: int, pov_player1: bool, rv : GameAction) -> int:
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        # base min value
        val = MIN_VAL
        rv[0]= actions[0]
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                _, temp_val = self.maximum(newState, depth - 1, alpha, beta, pov_player1,rv)
            else:
                _, temp_val = self.minimum(newState, depth - 1, alpha, beta, pov_player1,rv)

            if (temp_val > val):
                val = temp_val
                best_action = action
                rv[0]= best_action
            
            # update alpha value
            alpha = val if (val > alpha) else alpha
            # pruning
            if (beta <= alpha):
                break
        return best_action, val
