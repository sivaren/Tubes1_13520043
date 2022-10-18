import random
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

    # print current information
    def print_info(self, state: GameState):
        # action_idx = self.succ_score.index(max(self.succ_score))
        # action = self.succ_table[action_idx]
        curr_score = self._calculate_objective_func(state)
        score_target = max(self.succ_score)
        
        print("SUCCESSORS")
        for i in range (len(self.succ_table)):
            print(i + 1, self.succ_table[i]['action_type'], self.succ_table[i]['position'], self.succ_score[i])
        print("BOARD STATUS")
        print(state.board_status)
        print(f"CURRENT SCORE: {curr_score}")
        print(f"SCORE TARGET: {score_target}".upper())
        print(f"PLAYER 1 TURN: {state.player1_turn}".upper())
        print("=====================")

    # generate all successors
    def generate_successors(self, state: GameState):
        for i in range (len(state.row_status)):
            for j in range (len(state.row_status[i])):
                if(state.row_status[i][j] == 0):
                    action = GameAction("row", (j, i))
                    newState = StateManager.transform(state, action)
                    score = self._calculate_objective_func(newState)

                    self.add_succ_table({
                        'action_type': "row",
                        'position': (j, i),
                    })
                    self.add_succ_score(score)

        for i in range (len(state.col_status)):
            for j in range (len(state.col_status[i])):
                if(state.col_status[i][j] == 0):
                    action = GameAction("col", (j, i))
                    newState = StateManager.transform(state, action)
                    score = self._calculate_objective_func(newState)

                    self.add_succ_table({
                        'action_type': "col",
                        'position': (j, i),
                    })
                    self.add_succ_score(score)
    
    # select arbitrary neighbor from all highest-value successor occurences
    def select_arbitrary_neighbor(self):
        max_val = max(self.succ_score)
        max_val_idx = []

        for i in range (len(self.succ_score)):
            if self.succ_score[i] == max_val:
                max_val_idx.append(i)
        neighbor_idx = random.choice(max_val_idx)
        
        return neighbor_idx

    # make decision and get an action
    def get_action(self, state: GameState) -> GameAction:
        self.generate_successors(state)
        self.print_info(state)
        
        neighbor_idx = self.select_arbitrary_neighbor()
        # use a line of code below to not randomize the neighbor
        # action_idx = self.succ_score.index(max(self.succ_score))
        action = self.succ_table[neighbor_idx]
        action_type = action['action_type']
        position = action['position']

        # attributes clearance
        self.succ_table = []
        self.succ_score = []

        return GameAction(action_type, position)
