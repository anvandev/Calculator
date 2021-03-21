from django.shortcuts import render
from .utils import calculate_expression


def home(request):
    return render(request, 'calculator/main.html')


def calculate(request):
    error = True
    answer = False
    expression = request.GET['expression']
    message = None
    try:
        answer = calculate_expression(expression)
        error = False
    except ValueError as err:
        message = err
    except Exception as ex:
        message = f'Unexpected error: {ex}.'
    finally:
        return render(request, 'calculator/main.html', {'error': error,
                                                        'answer': answer,
                                                        'message': message,
                                                        'expression': expression})
