import sys

from BotWithObjFunc import BotWithObjFunc
from GameAction import GameAction
from GameState import GameState
from StateManager import StateManager


class BotMinimax(BotWithObjFunc):
    def __init__(self) -> None:
        super().__init__()
    
    def get_action(self, state: GameState) -> GameAction:
        return self.minimax(state, not state.player1_turn)

    def print_info(self, state: GameState):
        curr_score = self._calculate_objective_func(state)

        print("=====================")
        print("BOARD STATUS")
        print(state.board_status)
        print(f"CURRENT SCORE: {curr_score}")
        print(f"PLAYER 1 TURN: {state.player1_turn}")
        print("=====================")


    def minimax(self, state: GameState, isMax: bool) -> GameAction:
        print("MINIMAX")
        actions = self.get_all_possible_action(state)
        best_action = None
        val = 0

        if (isMax):
            val = sys.maxsize * -1
            for action in actions:
                temp_val = self.minimum(state, 1)
                if (val < temp_val):
                    best_action = action
                    val = temp_val

        else:
            val = sys.maxsize
            for action in actions:
                temp_val = self.maximum(state, 1)
                if (val > temp_val):
                    best_action = action
                    val = temp_val
        
        print("Value:", val)
        print("Best state tujuan:", StateManager.transform(state, best_action).board_status)
        return best_action

    
    def minimum(self, state: GameState, depth: int) -> int:
        print("MINIMUM CALLED WITH DEPTH", depth)
        actions = self.get_all_possible_action(state)

        if (len(actions) == 0) or (depth == 0):
            return self._calculate_objective_func(state)

        val = sys.maxsize
        minState = None
        for action in actions:
            newState = StateManager.transform(state, action)
            
            if (state.player1_turn == newState.player1_turn):
                val = min(val, self.minimum(newState, depth - 1))
                    
            else:
                val = min(val, self.maximum(newState, depth - 1))

            if(val == self._calculate_objective_func(newState)):
                minState = newState
    
        print("MINIMUM STATE:", minState.board_status)
        print("MINIMUM VALUE:", val)
        return val
        
    
    def maximum(self, state: GameState, depth: int) -> int:
        print("MAXIMUM CALLED WITH DEPTH", depth)
        actions = self.get_all_possible_action(state)

        if (len(actions) == 0) or (depth == 0):
            return self._calculate_objective_func(state)

        val = sys.maxsize * -1
        maxState = None
        for action in actions:
            newState = StateManager.transform(state, action)
            
            if (state.player1_turn == newState.player1_turn):
                val = max(val, self.maximum(newState, depth - 1))
                    
            else:
                val = max(val, self.minimum(newState, depth - 1))
            
            if(val == self._calculate_objective_func(newState)):
                maxState = newState
    
        print("MAXIMUM STATE:", maxState.board_status)
        print("MAXIMUM VALUE:", val)
        return val
