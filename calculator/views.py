from django.shortcuts import render
from .utils import clear_and_convert, calculate_expression


def home(request):
    return render(request, 'calculator/main.html')


def calculate(request):
    expression = request.GET['expression']
    try:
        converted_expression = clear_and_convert(expression)
        answer = calculate_expression(converted_expression)
        return render(request, 'calculator/main.html', {'expression': expression,
                                                        'error': False,
                                                        'answer': answer})
    except Exception as e:
        message = e
        return render(request, 'calculator/main.html', {'expression': expression,
                                                        'error': True,
                                                        'message': message})
    except:
        return render(request, 'calculator/main.html', {'expression': expression,
                                                        'error': True})
