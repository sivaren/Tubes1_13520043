import random
import multiprocessing as mp
from GameState import GameState
from StateManager import StateManager
from GameAction import GameAction
from BotWithObjFunc import BotWithObjFunc

class LocalSearchBot(BotWithObjFunc):
    def __init__(self):
        super().__init__()
        self.succ_table = []
        self.succ_score = []

    # append action to successors table
    def add_succ_table(self, action: dict):
        self.succ_table.append(action)
    
    # append score to array of successor score
    def add_succ_score(self, score: int):
        self.succ_score.append(score)

    # generate all successors
    def generate_successors(self, state: GameState, retval: GameAction):
        for i in range (len(state.row_status)):
            for j in range (len(state.row_status[i])):
                if(state.row_status[i][j] == 0):
                    action = GameAction("row", (j, i))
                    newState = StateManager.transform(state, action)
                    score = self._calculate_objective_func(newState, state.player1_turn)

                    self.add_succ_table(action)
                    self.add_succ_score(score)

        for i in range (len(state.col_status)):
            for j in range (len(state.col_status[i])):
                if(state.col_status[i][j] == 0):
                    action = GameAction("col", (j, i))
                    newState = StateManager.transform(state, action)
                    score = self._calculate_objective_func(
                        newState, state.player1_turn)

                    self.add_succ_table(action)
                    self.add_succ_score(score)

        # initiate return value
        retval[0] = self.succ_table[0]
    
    # select arbitrary neighbor from all highest-value successor occurences
    def select_arbitrary_neighbor(self):
        max_val = max(self.succ_score)
        max_val_idx = []

        for i in range (len(self.succ_score)):
            if self.succ_score[i] == max_val:
                max_val_idx.append(i)
        neighbor_idx = random.choice(max_val_idx)
        
        return neighbor_idx
    
    # local search execution
    def local_search(self, state: GameState, retval: GameAction):
        self.generate_successors(state, retval)

        # use a line of code below to not randomize the neighbor
        # neighbor_idx = self.succ_score.index(max(self.succ_score))
        neighbor_idx = self.select_arbitrary_neighbor()
        best_action = self.succ_table[neighbor_idx]

        # get the best action (compare w/ placeholder) - to use timeout
        if self.succ_score[neighbor_idx] >= self.succ_score[0]:
            retval[0] = best_action

        # attributes clearance
        self.succ_table = []
        self.succ_score = []

        return best_action

    # make decision and get an action
    def get_action(self, state: GameState) -> GameAction:
        # use code down below to include timeout (5 secs)
        mgr = mp.Manager()
        retval = mgr.dict()
        timeinst = mp.Process(target=self.local_search, args=(state, retval))
        timeinst.start()
        timeinst.join(5)
        if timeinst.is_alive():
            timeinst.terminate()
            timeinst.join()
        
        return retval.values()[0]
