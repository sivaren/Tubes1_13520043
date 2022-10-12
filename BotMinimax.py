import sys

from BotWithObjFunc import BotWithObjFunc
from GameAction import GameAction
from GameState import GameState


class BotMinimax(BotWithObjFunc):
    def __init__(self) -> None:
        super().__init__()
    
    def get_action(self, state: GameState) -> GameAction:
        return self.minimax(state, state.player1_turn)

    def minimax(self, state: GameState, isMax: bool) -> GameAction:
        actions = self.get_all_possible_action(state)
        best_action = None

        if (isMax):
            val = sys.maxsize * -1
            for action in actions:
                temp_val = self.minimum(state, 5)
                if (val < temp_val):
                    best_action = action
                    val = temp_val

        else:
            val = sys.maxsize
            for action in actions:
                temp_val = self.maximum(state, 5)
                if (val > temp_val):
                    best_action = action
                    val = temp_val
        
        return best_action

    
    def minimum(self, state: GameState, depth: int) -> int:
        actions = self.get_all_possible_action(state)

        if (len(actions) == 0) or (depth == 0):
            return self._calculate_objective_func(state)

        val = sys.maxsize
        for action in actions:
            newState = self.transform(state, action)
            
            if (state.player1_turn == newState.player1_turn):
                val = min(val, self.minimum(newState, depth - 1))
                    
            else:
                val = min(val, self.maximum(newState, depth - 1))
        
        return val
        
    
    def maximum(self, state: GameState, depth: int) -> int:
        actions = self.get_all_possible_action(state)

        if (len(actions) == 0) or (depth == 0):
            return self._calculate_objective_func(state)

        val = sys.maxsize * -1
        for action in actions:
            newState = self.transform(state, action)
            
            if (state.player1_turn == newState.player1_turn):
                val = max(val, self.maximum(newState, depth - 1))
                    
            else:
                val = max(val, self.minimum(newState, depth - 1))
        
        return val
