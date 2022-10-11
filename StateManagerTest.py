from GameState import GameState
from GameAction import GameAction
from StateManager import StateManager

import unittest


class StateManagerTest(unittest.TestCase):
    def test_one_step_transform(self):
        state = StateManager.create_new_state()
        action = GameAction("row", (0, 0))
        newState = StateManager.transform(state, action)

        self.assertEqual(newState.row_status[0][0], 1)
        self.assertEqual(newState.board_status[0][0], -1)
        self.assertEqual(newState.player1_turn, False)

    def test_turn_after_scoring(self):
        state = StateManager.create_new_state()
        action1 = GameAction("row", (1, 1))
        action2 = GameAction("row", (1, 2))
        action3 = GameAction("col", (1, 1))
        action4 = GameAction("col", (2, 1))

        for action in [action1, action2, action3, action4]:
            state = StateManager.transform(state, action)
        
        self.assertEqual(state.player1_turn, False)
        self.assertEqual(state.board_status[1][1], 4)
        self.assertEqual(state.board_status[1][2], 1)
        self.assertEqual(state.board_status[2][1], 1)
        self.assertEqual(state.board_status[0][1], -1)
        self.assertEqual(state.board_status[1][0], -1)

    def test_invalid_action(self):
        state = StateManager.create_new_state()
        invalid_action1 = GameAction("invalid", (0, 0))
        invalid_action2 = GameAction("row", (-1, 0))
        invalid_action3 = GameAction("col", (0, -1))
        invalid_action4 = GameAction("row", (4, 0))
        invalid_action5 = GameAction("col", (0, 4))
        invalid_action6 = GameAction("invalid", (-1, 4))

        for action in [invalid_action1, invalid_action2, invalid_action3, invalid_action4, invalid_action5, invalid_action6]:
            self.assertRaises(Exception, StateManager.transform, state, action)


unittest.main()
