"""
This calculator is built using "ping pong" algorithm, without eval() etc.
Allowed operations: +, -, *, /, **, use of parentheses. Spaces don't matter.
Negative numbers should be written as: (-34), float numbers: 3.4
Expression example: ((-2.3) + 3 ** (2 - 2)) * 2.2 + (6/(3 + 3)* (-2)) ** 2
"""


def math_operation(expression):
    """ simple calculator for two numbers in expression like 3 + 3 """
    if not str(expression[0]).isdigit() or not str(expression[2]).isdigit():
        # исключает вызов ошибки при дробных и отрицательных числах
        if not str(expression[0]).replace('.', '1').replace('-', '1').isdigit() or \
                not str(expression[2]).replace('.', '1').replace('-', '1').isdigit():
            raise Exception(f'{expression} - check your expression, something wrong')
    if expression[2] == 0 and expression[1] == '/':
        raise Exception(f'{expression} - division by zero in expression')
    operator = expression[1]
    if operator == '**':
        return expression[0]**expression[2]
    elif operator == '*':
        return expression[0]*expression[2]
    elif operator == '/':
        return expression[0]/expression[2]
    elif operator == '+':
        return expression[0]+expression[2]
    elif operator == '-':
        return expression[0]-expression[2]


def ping_calculate_pong(expression, operator_index):
    """
    argument 1: an expression from which we will extract one subexpression
    argument 2: the index of the mathematical operator around which function takes the subexpression to extract
    Function: 1. takes the expression and extract one subexpression around math operator (like 2 + 2) - ping;
      2. calculates subexpression result using "math_operation" function;
      3. replace in expression: subexpression to subexpression result - pong.
    """
    if len(expression) < 3 or operator_index == len(expression)-1 or operator_index == 0:
        raise Exception(f'{expression} - check your expression, something wrong')
    sub_expression = expression[operator_index - 1:operator_index + 2]
    sub_result = math_operation(sub_expression)
    expression[operator_index+1] = sub_result
    del expression[operator_index-1:operator_index+1]


def calculator_without_parentheses(expression):
    """
    argument - expression to count
    function prioritizes mathematical operations and applies function "ping_calculate_pong"
    returns expression with result
    """
    j = 1
    while len(expression) > j:
        if "**" in expression:
            ping_calculate_pong(expression, expression.index('**'))
        elif '*' in expression or '/' in expression:
            if '*' in expression and '/' in expression:
                if expression.index('*') < expression.index('/'):
                    ping_calculate_pong(expression, expression.index('*'))
                else:
                    ping_calculate_pong(expression, expression.index('/'))
            elif '/' not in expression:
                ping_calculate_pong(expression, expression.index('*'))
            elif '*' not in expression:
                ping_calculate_pong(expression, expression.index('/'))
        elif '+' in expression or '-' in expression:
            if '+' in expression and '-' in expression:
                if expression.index('+') < expression.index('-'):
                    ping_calculate_pong(expression, expression.index('+'))
                else:
                    ping_calculate_pong(expression, expression.index('-'))
            elif '-' not in expression:
                ping_calculate_pong(expression, expression.index('+'))
            elif '+' not in expression:
                ping_calculate_pong(expression, expression.index('-'))
        else:
            j += 1  # защита от возможного вечного цикла, при вводе некорректного выражения
    return expression


def calculate_expression(expression):
    for el in expression.copy():
        if ')' in expression:
            if '(' in expression:
                if expression.index(')') > expression.index('('):
                    z = expression.index(')')
                    a = z
                    while expression[a] != '(':
                        a -= 1
                    fragment = expression[a+1:z]
                    fr_result = calculator_without_parentheses(fragment)
                    if len(fr_result) != 1:  # проверка на наличие ошибки ввода в фрагменте выражения ((()))
                        raise Exception(f'{fr_result} - check your expression, something wrong')
                    expression[z] = fr_result[0]
                    del expression[a:z]
                else:
                    raise Exception('check your expression, something wrong with parentheses')
            else:
                raise Exception('check your expression, something wrong with parentheses')
        else:
            expression = calculator_without_parentheses(expression)
    if len(expression) != 1:
        raise Exception(f'{expression} - check your expression, something wrong')
    if len(expression) == 1:
        return f'{expression[0]}'


def clear_and_convert(math_expression):
    # clear the expression of spaces and convert it to the list
    cleared_expression = list(filter(lambda x: x != ' ', math_expression))
    # check characters in the expression for correctness
    check_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')', '.']
    for element in cleared_expression:
        if element not in check_list:
            raise Exception(f'Houston, we have a problem. Element "{element}" in expression is not correct.')
    # find multi-digit numbers and create new list with int
    int_exp = []
    i = 0
    while i < len(cleared_expression):
        number = ''
        while i < len(cleared_expression) and cleared_expression[i].isdigit():
            number += cleared_expression[i]
            if i+1 == len(cleared_expression) or not cleared_expression[i+1].isdigit():
                int_exp.append(int(number))
            i += 1
        if i < len(cleared_expression):
            int_exp.append(cleared_expression[i])
        i += 1
    # find float numbers and update list
    while '.' in int_exp:
        if int_exp.index('.') != len(int_exp)-1 and int_exp.index('.') != 0 \
                and type(int_exp[int_exp.index('.')-1]) == int \
                and type(int_exp[int_exp.index('.')+1]) == int:
            float_number = float(str(int_exp[int_exp.index('.')-1]) + int_exp[int_exp.index('.')] +
                              str(int_exp[int_exp.index('.')+1]))
            int_exp[int_exp.index('.')+1] = float_number
            del int_exp[int_exp.index('.')-1:int_exp.index('.')+1]
        else:
            raise Exception(f'Check your expression, something wrong with "."')
    # find negative numbers and update list
    i = 0
    while '(' in int_exp and i < len(int_exp.copy()):
        if int_exp[i] == '(' and i+3 < len(int_exp) and int_exp[i+1] == '-' and int_exp[i+3] == ')':
            if type(int_exp[i+2]) == int:
                negative_number = int('-' + str(int_exp[i+2]))
                int_exp[i + 3] = negative_number
                del int_exp[i:i + 3]
            elif type(int_exp[i + 2]) == float:
                negative_number = float('-' + str(int_exp[i+2]))
                int_exp[i + 3] = negative_number
                del int_exp[i:i + 3]
            else:
                raise Exception(f'Check your expression, something wrong with "(-number)"')
        i += 1
    # find exponent operator and create new list
    exp = []
    i = 0
    while i < len(int_exp):
        if int_exp[i] == '*' and i != len(int_exp)-1 and int_exp[i+1] == '*':
            exp.append('**')
            i += 2
        else:
            exp.append(int_exp[i])
            i += 1
    return exp
