from BotWithObjFunc import BotWithObjFunc
from GameAction import GameAction
from GameState import GameState
from StateManager import StateManager


class BotMinimax(BotWithObjFunc):
    def __init__(self) -> None:
        super().__init__()
    
    def get_action(self, state: GameState) -> GameAction:
        return self.minimax(state, True)

    def print_info(self, state: GameState):
        curr_score = self._calculate_objective_func(state)

        print("=====================")
        print("BOARD STATUS")
        print(state.board_status)
        print(f"CURRENT SCORE: {curr_score}")
        print(f"PLAYER 1 TURN: {state.player1_turn}")
        print("=====================")

    def minimax(self, state: GameState, isMax: bool) -> GameAction:
        # print("MINIMAX")
        if (isMax):
            best_action, val = self.maximum(state, 3)
        else:
            best_action, val = self.minimum(state, 3)
        
        return best_action

    
    def minimum(self, state: GameState, depth: int):
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state)
        
        # base max value
        val = 1000000
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                temp_action, temp_val = self.minimum(newState, depth - 1)
            else:
                temp_action, temp_val = self.maximum(newState, depth - 1)

            if (temp_val < val):
                val = temp_val
                best_action = action

        # print("BEST VALUE: ", val)
        return best_action, val
        
    
    def maximum(self, state: GameState, depth: int) -> int:
        best_action = None

        if (depth == 0):
            return best_action, self._calculate_objective_func(state)
        
        actions = self.get_all_possible_action(state)
        if (len(actions) == 0):
            return best_action, self._calculate_objective_func(state)
        
        # base min value
        val = -1000000
        for action in actions:
            # create new state according to action
            newState = StateManager.transform(state, action)

            temp_val = 0
            if (state.player1_turn == newState.player1_turn):
                # completing 1 block
                temp_action, temp_val = self.maximum(newState, depth - 1)
            else:
                temp_action, temp_val = self.minimum(newState, depth - 1)

            if (temp_val > val):
                val = temp_val
                best_action = action
        
        # print("BEST VALUE: ", val)
        return best_action, val
