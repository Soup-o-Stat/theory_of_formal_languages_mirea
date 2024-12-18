from collections import defaultdict as dd

class FiniteStateMachine:
    def __init__(self):
        self.available_states = {0, 1, 2, 3}
        self.start_state = 0
        self.accepted_states = {1, 2, 3}
        self.current = self.start_state

        self.transitions = dd(lambda: None, {
            (0, 'alpha'): 1,
            (1, 'alpha'): 1,
            (1, 'num'): 2,
            (1, 'underscore'): 3,
            (2, 'num'): 2,
            (2, 'alpha'): 1,
            (2, 'underscore'): 3,
            (3, 'underscore'): 3,
            (3, 'alpha'): 1,
            (3, 'num'): 2,})

    def restart(self):
        self.current = self.start_state

    def classify_char(self, character: str) -> str:
        if character.isalpha():
            return 'alpha'
        elif character.isdigit():
            return 'num'
        elif character == '_':
            return 'underscore'
        return None

    def is_accepted(self) -> bool:
        return self.current in self.accepted_states

    def evaluate_input(self, input_seq: str) -> bool:
        self.restart()

        for char in input_seq:
            char_type = self.classify_char(char)
            if char_type is None:
                return False
            next_state = self.transitions[(self.current, char_type)]
            if next_state is None:
                return False
            self.current = next_state
        else:
            return self.is_accepted()

if __name__ == "__main__":
    fsm = FiniteStateMachine()
    while True:
        user_input = input("Введите строку для анализа: ")
        if fsm.evaluate_input(user_input):
            print("Строка принята")
        else:
            print("Строка не принята")
