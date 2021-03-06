"""Calculator is built using "ping pong" algorithm, without eval() etc.
Main final function: calculate_expression().
calculate_expression() uses two functions in utils.py: clear_and_convert() and calculator_without_parentheses().
calculator_without_parentheses() uses two remaining functions:
math_operation() -> ping_calculate_pong() -> calculator_without_parentheses().

Allowed operations: +, -, *, /, **, use of parentheses.  Spaces don't matter.
Negative numbers should be written as: (-34), float numbers: 3.4
Expression example: ((-2.3) + 3 ** (2 - 2)) * 2.2 + (6/(3 + 3)* (-2)) ** 2
"""


def math_operation(expression):
    """Simple calculator for two numbers in expression like 3 + 3."""
    if not str(expression[0]).isdigit() or not str(expression[2]).isdigit():
        # eliminates the error call for float and negative numbers
        if not str(expression[0]).replace('.', '1').replace('-', '1').isdigit() or \
                not str(expression[2]).replace('.', '1').replace('-', '1').isdigit():
            raise ValueError(f'{expression} - check this fragment, something wrong.')
    if expression[2] == 0 and expression[1] == '/':
        raise ValueError(f'{expression} - division by zero.')
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
    """The function takes two arguments.
    Argument 1: an expression from which we will extract one subexpression.
    Argument 2: the index of the mathematical operator around which function takes the subexpression to extract.
    The function:
    1. takes the expression and extract one subexpression around math operator (like 2 + 2) - ping;
    2. calculates subexpression result using function math_operation();
    3. replaces in expression: subexpression to subexpression result - pong.
    """
    if len(expression) < 3 or operator_index == len(expression)-1 or operator_index == 0:
        raise ValueError(f'{expression} - check this fragment, something wrong.')
    sub_expression = expression[operator_index - 1:operator_index + 2]
    sub_result = math_operation(sub_expression)
    expression[operator_index+1] = sub_result
    del expression[operator_index-1:operator_index+1]


def calculator_without_parentheses(expression):
    """The function:
     1. prioritizes mathematical operations in expression without any parentheses;
     2. transfers expression and indexes of math operators to the function ping_calculate_pong();
     3. returns result of calculations.
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
            j += 1    # protection against a possible eternal loop when an incorrect expression is entered
    return expression


def clear_and_convert(string_math_expression):
    """This function takes string expression and converts it to list with int, float, and 'math signs'."""
    # clear the expression of spaces and convert it to the list
    cleared_expression = list(filter(lambda x: x != ' ', string_math_expression))
    # check characters in the expression for correctness
    check_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')', '.']
    for element in cleared_expression:
        if element not in check_list:
            raise ValueError(f'Houston, we have a problem. Element "{element}" in expression is not correct.')
    # find multi-digit numbers and create new list num_exp with int
    num_exp = []
    number = ''
    len_cleared_expression = len(cleared_expression)
    for i, element in enumerate(cleared_expression):
        if element.isdigit():
            number += element
            if i == len_cleared_expression - 1 or not cleared_expression[i+1].isdigit():
                num_exp.append(int(number))
                number = ''
        else:
            num_exp.append(element)
    # find float numbers and update list num_exp
    while '.' in num_exp:
        i = num_exp.index('.')
        if (i != 0 and i != len(num_exp) - 1
                and isinstance(num_exp[i-1], int)
                and isinstance(num_exp[i+1], int)):
            float_number = float(str(num_exp[i-1]) + num_exp[i] + str(num_exp[i+1]))
            num_exp[i+1] = float_number
            del num_exp[i-1:i+1]
        else:
            raise ValueError('Something wrong with ".".')
    # find negative numbers and create new list with negative numbers
    neg_exp = []
    excluded_index = None
    neg_check_list = ['+', '-', '*', '/', '(']
    len_num_exp = len(num_exp)
    for i, element in enumerate(num_exp):
        if element == '-':
            if i == len_num_exp - 1:
                raise ValueError('Something wrong with "-".')
            elif isinstance(num_exp[i+1], int) and (i == 0 or num_exp[i-1] in neg_check_list):
                n_number = int('-' + str(num_exp[i+1]))
                neg_exp.append(n_number)
                excluded_index = i + 1
            elif isinstance(num_exp[i+1], float) and (i == 0 or num_exp[i-1] in neg_check_list):
                n_number = float('-' + str(num_exp[i+1]))
                neg_exp.append(n_number)
                excluded_index = i + 1
            else:
                neg_exp.append(element)
        elif i != excluded_index:
            neg_exp.append(element)
    # find exponent operator and create new list with final converted expression
    converted_expression = []
    i = 0
    len_neg_exp = len(neg_exp)
    while i < len_neg_exp:
        if (i == 0 or i == len_neg_exp - 1) and neg_exp[i] == '*':
            raise ValueError('Something wrong with "*".')
        elif neg_exp[i] == '*' and neg_exp[i+1] == '*':
            converted_expression.append('**')
            i += 2
        else:
            converted_expression.append(neg_exp[i])
            i += 1
    return converted_expression


def calculate_expression(str_math_expression):
    """This function:
     1. uses clear_and_convert() to prepare the string math expression for further calculations;
     2. finds all subexpressions inside parentheses (if there are such);
     3. transfers subexpression to calculator_without_parentheses() for further calculations;
     4. replaces subexpression with the result;
     5. returns final result of all calculations.
    """
    expression = clear_and_convert(str_math_expression)
    for element in expression.copy():
        if ')' in expression:
            if '(' in expression:
                if expression.index(')') > expression.index('('):
                    z = expression.index(')')
                    a = z
                    while expression[a] != '(':
                        a -= 1
                    fragment = expression[a+1:z]
                    fr_result = calculator_without_parentheses(fragment)
                    if len(fr_result) != 1:    # checking for an input error in a fragment of the expression like ((()))
                        raise ValueError(f'{fr_result} - check this fragment, something wrong.')
                    expression[z] = fr_result[0]
                    del expression[a:z]
                else:
                    raise ValueError('Something wrong with parentheses.')
            else:
                raise ValueError('Something wrong with parentheses.')
        else:
            expression = calculator_without_parentheses(expression)
    if len(expression) != 1:
        raise ValueError('Something wrong in your expression.')
    if len(expression) == 1:
        return str(round(expression[0], 5))
