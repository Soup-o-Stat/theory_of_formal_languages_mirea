def create_state(current_state):
    state = current_state
    current_state += 1
    return state, current_state

def add_transition(transitions, from_state, to_state, symbol):
    transitions.append((from_state, to_state, symbol))

def connect_nfa(stack, transitions):
    nfa2_start, nfa2_end = stack.pop()
    nfa1_start, nfa1_end = stack.pop()
    add_transition(transitions, nfa1_end, nfa2_start, None)
    stack.append((nfa1_start, nfa2_end))

def union_nfa(stack, transitions, current_state):
    nfa2_start, nfa2_end = stack.pop()
    nfa1_start, nfa1_end = stack.pop()
    new_start, current_state = create_state(current_state)
    new_end, current_state = create_state(current_state)
    add_transition(transitions, new_start, nfa1_start, None)
    add_transition(transitions, new_start, nfa2_start, None)
    add_transition(transitions, nfa1_end, new_end, None)
    add_transition(transitions, nfa2_end, new_end, None)
    stack.append((new_start, new_end))
    return current_state

def closure_nfa(stack, transitions, current_state):
    start, end = stack.pop()
    new_start, current_state = create_state(current_state)
    new_end, current_state = create_state(current_state)
    add_transition(transitions, new_start, start, None)
    add_transition(transitions, end, start, None)
    add_transition(transitions, end, new_end, None)
    add_transition(transitions, new_start, new_end, None)
    stack.append((new_start, new_end))
    return current_state

def process_operator(operators, stack, transitions, current_state):
    operator = operators.pop()
    if operator == '|':
        current_state = union_nfa(stack, transitions, current_state)
    elif operator == '.':
        connect_nfa(stack, transitions)
    return current_state

def compile_nfa(pattern):
    stack = []
    operators = []
    current_state = 0
    transitions = []

    precedence = {'|': 1, '.': 2}

    i = 0
    while i < len(pattern):
        char = pattern[i]

        if char == '(':
            operators.append(char)

        elif char == ')':
            while operators and operators[-1] != '(':
                current_state = process_operator(operators, stack, transitions, current_state)
            operators.pop()

        elif char == '*':
            current_state = closure_nfa(stack, transitions, current_state)

        elif char in precedence:
            while (operators and operators[-1] != '(' and
                   precedence[operators[-1]] >= precedence[char]):
                current_state = process_operator(operators, stack, transitions, current_state)
            operators.append(char)

        else:
            start, current_state = create_state(current_state)
            end, current_state = create_state(current_state)
            add_transition(transitions, start, end, char)
            stack.append((start, end))

            if i + 1 < len(pattern) and pattern[i + 1] not in '|*)':
                operators.append('.')

        i += 1

    while operators:
        current_state = process_operator(operators, stack, transitions, current_state)

    start_state, end_state = stack.pop()
    return start_state, end_state, transitions

def print_nfa(start_state, end_state, transitions):
    print(f"Начальное состояние: {start_state}")
    print(f"Конечное состояние: {end_state}")
    print("Переходы:")
    for (from_state, to_state, symbol) in transitions:
        symbol_str = symbol if symbol is not None else ''
        print(f"  {from_state} --({symbol_str})--> {to_state}")

if __name__ == "__main__":
    pattern = input("Введите регулярное выражение: ")
    start, end, transitions = compile_nfa(pattern)
    print("\nСконструированный НКА:")
    print_nfa(start, end, transitions)
