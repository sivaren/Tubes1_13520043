from Bot import Bot
from GameState import GameState

class BotWithObjFunc(Bot):
    def __init__(self):
        super().__init__()
        self.__table_score = {
            0: 0,
            1: 5,
            2: -10,
            3: 20,
            4: 0,
        }
    
    def __get_score(self, count_stick: int):
        return self.__table_score[count_stick]

    def _calculate_objective_func(self, state: GameState):
        score = 0
        for i in range(len(state.board_status)):
            for j in range(len(state.board_status[i])):
                abs_val = abs(state.board_status[i][j])
                if (abs_val == 4):
                    flip = (1 if state.player1_turn else -1) * \
                        (1 if state.board_status[i][j] == -4 else -1)
                    score += 100 * flip
                else:
                    score += self.__get_score(abs_val)

        return score

    def _display_state(self, state: GameState):        
        score = self._calculate_objective_func(state)
        
        print("GAME STATE")
        print("Board Status")
        print(state.board_status)
        print("Row Status")
        print(state.row_status)
        print("Col Status")
        print(state.col_status)
        print(f"Player 1 Turn: {state.player1_turn}")
        print(f"Score: {score}")
        print("=====================================")
        
