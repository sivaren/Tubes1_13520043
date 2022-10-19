from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import multiprocessing as mp
from copy import deepcopy
import numpy as np
class LSBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        mgr = mp.Manager()
        rv = mgr.dict()
        timeinst = mp.Process(target=self.thinking, args=(state, rv))
        timeinst.start()
        timeinst.join(5)
        if timeinst.is_alive():
            # Timeout, returning best action so far...
            timeinst.terminate()
            timeinst.join()
        return rv.values()[0]

    def thinking(self, state: GameState, retval: GameAction):
        bestObj = -37
        posibGameActions = []
        for y in range(len(state.col_status)):
            for x in range(len(state.col_status[y])):
                if state.col_status[y][x] == 0:
                    posibGameActions.append(GameAction("col", (x, y)))
        for y in range(len(state.row_status)):
            for x in range(len(state.row_status[y])):
                if state.row_status[y][x] == 0:
                    posibGameActions.append(GameAction("row", (x, y)))
        # placeholder
        retval[0] = posibGameActions[0]
        # Get the best action
        for act in posibGameActions:
            new_state = self.adv_board_status_once(state, act)
            new_obj = self.objective(new_state)
            if new_obj >= bestObj:
                retval[0] = act
                bestObj = new_obj
            else:
                return # END PROCESS
        return