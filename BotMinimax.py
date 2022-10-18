from BotWithObjFunc import BotWithObjFunc
from GameAction import GameAction
from GameState import GameState
from StateManager import StateManager


class BotMinimax(BotWithObjFunc):
    def __init__(self) -> None:
        super().__init__()
    
    def get_action(self, state: GameState) -> GameAction:
        return self.minimax(state, True, state.player1_turn)

    def print_info(self, state: GameState):
        curr_score = self._calculate_objective_func(state)

        print("=====================")
        print("BOARD STATUS")
        print(state.board_status)
        print(f"CURRENT SCORE: {curr_score}")
        print(f"PLAYER 1 TURN: {state.player1_turn}")
        print("=====================")

    def minimax(self, state: GameState, isMax: bool, pov_player1: bool) -> GameAction:
        # print("MINIMAX")
        max_depth = 4
        if (isMax):
            best_action, val = self.maximum(state, max_depth, pov_player1)
        else:
            best_action, val = self.minimum(state, max_depth, pov_player1)
        
        return best_action

    
    def minimum(self, state: GameState, depth: int, pov_player1: bool):
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        # base max value
        val = 1000000
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                temp_action, temp_val = self.minimum(newState, depth - 1, pov_player1)
            else:
                temp_action, temp_val = self.maximum(newState, depth - 1, pov_player1)

            if (temp_val < val):
                val = temp_val
                best_action = action

        # print("BEST VALUE: ", val)
        return best_action, val
        
    
    def maximum(self, state: GameState, depth: int, pov_player1: bool) -> int:
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state, pov_player1)
        
        # base min value
        val = -1000000
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                temp_action, temp_val = self.maximum(newState, depth - 1, pov_player1)
            else:
                temp_action, temp_val = self.minimum(newState, depth - 1, pov_player1)

            if (temp_val > val):
                val = temp_val
                best_action = action
        
        # print("BEST VALUE: ", val)
        return best_action, val
