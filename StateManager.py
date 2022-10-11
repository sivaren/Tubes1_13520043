from GameState import GameState
from GameAction import GameAction
import numpy as np


class StateManager:
    NUMBER_OF_DOTS = 4

    @staticmethod
    def __is_grid_occupied(state: GameState, action: GameAction):
        x = action.position[0]
        y = action.position[1]
        occupied = True

        if action.action_type == "row" and state.row_status[y][x] == 0:
            occupied = False
        if action.action_type == "col" and state.col_status[y][x] == 0:
            occupied = False

        return occupied

    @staticmethod
    def __update_state(state: GameState, action: GameAction):
        new_board_status = state.board_status.copy()
        new_row_status = state.row_status.copy()
        new_col_status = state.col_status.copy()

        x = action.position[0]
        y = action.position[1]

        val = 1
        playerModifier = 1
        if state.player1_turn:
            playerModifier = -1

        pointScored = False
        if y < (StateManager.NUMBER_OF_DOTS - 1) and x < (StateManager.NUMBER_OF_DOTS - 1):
            new_board_status[y][x] = (
                abs(new_board_status[y][x]) + val) * playerModifier
            if abs(new_board_status[y][x]) == 4:
                pointScored = True

        if action.action_type == "row":
            new_row_status[y][x] = 1
            if y >= 1:
                new_board_status[y-1][x] = (
                    abs(new_board_status[y-1][x]) + val) * playerModifier
                if abs(new_board_status[y-1][x] == 4):
                    pointScored = True

        elif action.action_type == "col":
            new_col_status[y][x] = 1
            if x >= 1:
                new_board_status[y][x -
                                    1] = (abs(new_board_status[y][x-1]) + val) * playerModifier
                if abs(new_board_status[y][x-1]) == 4:
                    pointScored = True

        new_player1_turn = (
            not state.player1_turn) if not pointScored else state.player1_turn

        return GameState(new_board_status, new_row_status, new_col_status, new_player1_turn)

    @staticmethod
    def __valid_action(action: GameAction):
        if action.action_type in ["row", "col"] and len(action.position) == 2 and action.position[0] >= 0 and action.position[1] >= 0 and action.position[0] < StateManager.NUMBER_OF_DOTS and action.position[1] < StateManager.NUMBER_OF_DOTS:
            return True

        return False

    @staticmethod
    def transform(state: GameState, action: GameAction):
        if StateManager.__valid_action(action) and not StateManager.__is_grid_occupied(state, action):
            return StateManager.__update_state(state, action)
        else:
            raise Exception("Invalid action")

    @staticmethod
    def create_new_state(player1_first=True):
        return GameState(
            np.zeros(shape=(StateManager.NUMBER_OF_DOTS -
                            1, StateManager.NUMBER_OF_DOTS - 1)),
            np.zeros(shape=(StateManager.NUMBER_OF_DOTS,
                            StateManager.NUMBER_OF_DOTS-1)),
            np.zeros(shape=(StateManager.NUMBER_OF_DOTS -
                            1, StateManager.NUMBER_OF_DOTS)),
            player1_first,
        )
