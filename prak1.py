#created by Soup-o-Stat

white_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              '*', "+", "-", "/", "(", ")"]
operators = ['*', "+", "-", "/"]

def to_the_list(data):
    input_data = list(data)
    input_data = [item for item in input_data if item.strip()]
    new_input_data = []
    number_sequence = ''
    for token in input_data:
        if token.isdigit():
            number_sequence += token
        elif token in white_list:
            if number_sequence:
                new_input_data.append(number_sequence)
                number_sequence = ''
            new_input_data.append(token)
    if number_sequence:
        new_input_data.append(number_sequence)
    if len(new_input_data) > 0:
        poliz_result = poliz(new_input_data)
        find_answer(poliz_result)
    else:
        print("Error")

def weight_checker(weight):
    if weight in ('+', '-'):
        return 1
    if weight in ('*', '/'):
        return 2
    return 0

def poliz(data):
    output = []
    stack = []
    for token in data:
        if token.isdigit():
            output.append(token)
        elif token in operators:
            while (stack and weight_checker(stack[-1]) >= weight_checker(token)):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
    while stack:
        output.append(stack.pop())
    print("ПОЛИЗ = ", output)
    return output

def operation(operand1, operand2, operation):
    if operation == '+':
        return str(float(operand1) + float(operand2))
    elif operation == '-':
        return str(float(operand1) - float(operand2))
    elif operation == '*':
        return str(float(operand1) * float(operand2))
    elif operation == '/':
        return str(float(operand1) / float(operand2))

def find_answer(poliz_result):
    stack = []
    for fucking_data in poliz_result:
        if fucking_data.isdigit():
            stack.append(fucking_data)
        elif fucking_data in operators:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = operation(operand1, operand2, fucking_data)
            stack.append(result)
    print("Результат:", stack.pop())

def main():
    print("Введите выражение")
    input_data = str(input())
    to_the_list(input_data)

main()
