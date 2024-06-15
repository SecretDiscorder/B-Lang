import json
from django.shortcuts import render
from django.http import JsonResponse
from .shell import run# Import interpreter Anda di sini
from . import shell
from bs4 import BeautifulSoup
from io import StringIO
import sys
sys.setrecursionlimit(10000)
from decimal import Decimal, getcontext
import mpmath
import roman
import math
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def calculate_result(expression):
    
    try:
        
        expression = expression
        result = Decimal(eval(expression))
        return str(result)
    except Exception as e:
        return "Error"
@csrf_exempt
def kalkulator(request):
    result = ""

    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        result = calculate_result(expression)
        if 'log' in request.POST :
            try:
                angka = expression.split()
                a = int(angka[0])
                b = int(angka[1])
                if b == '':
                    
                    result = math.log(a)
                elif b == '10':
                    result = math.log10(a)
                else :
                    result = math.log(a, b)
            except ValueError:
                result = "Gunakan 2 angka dipisah spasi"
        if 'to_roman' in request.POST:
            try:
                result = roman.toRoman(int(expression))
            except ValueError or IndexError:
                result = "Invalid number must be 0 - 4999"
            except Exception:
                result = "Invalid number must be 0 - 4999"
        elif 'from_roman' in request.POST:
            roman_number = expression
            try:
                result = roman.fromRoman(roman_number)
            except roman.InvalidRomanNumeralError:
                result = "Invalid Roman numeral"
        elif 'sin' in request.POST:
            sin = expression
            try:
                result = math.sin(float(sin))
            except ValueError:
                result = "error"
        elif 'cos' in request.POST:
            cos = expression
            try:
                result = math.cos(float(cos))
            except ValueError:
                result = "error"
        elif 'tan' in request.POST:
            tan = expression
            try:
                result = math.tan(float(tan))
            except ValueError:
                result = "error"
        elif 'asin' in request.POST:
            asin = expression
            try:
                result = math.asin(float(asin))
            except ValueError:
                result = "error"
        elif 'acos' in request.POST:
            acos = expression
            try:
                result = math.acos(float(acos))
            except ValueError:
                result = "error"
        elif 'atan' in request.POST:
            atan = expression
            try:
                result = math.atan(float(atan))
            except ValueError:
                result = "error"
        elif 'factorial' in request.POST:
            fact = expression
            try:
                result = math.factorial(int(fact))
            except ValueError:
                result = "Dont use comma"
        elif 'c_to_f' in request.POST:
            celcius = float(expression)
            try:
                result = ((celcius * 9/5) + 32)
            except ValueError:
                result = "error"
        elif 'f_to_c' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit - 32) * 5/9)
            except ValueError:
                result = "error"
        elif 'c_to_k' in request.POST:
            celcius = expression
            try:
                result = (float(celcius) + 273.15)
            except ValueError:
                result = "error"
        elif 'k_to_c' in request.POST:
            kelvin = float(expression)
            try:
                result = (kelvin - 273.15)
            except ValueError:
                result = "error"
        elif 'c_to_r' in request.POST:
            celcius = float(expression)
            try:
                result = (celcius * 4/5)
            except ValueError:
                result = "error"
        elif 'r_to_c' in request.POST:
            reamur = float(expression)
            try:
                result = (reamur * 5/4)
            except ValueError:
                result = "error"
        elif 'r_to_c' in request.POST:
            reamur = float(expression)
            try:
                result = (float(reamur) * 5/4)
            except ValueError:
                result = "error"
        elif 'f_to_r' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit - 32) * 4/9)
            except ValueError:
                result = "error"
        elif 'f_to_k' in request.POST:
            fahrenheit = float(expression)
            try:
                result = ((fahrenheit + 459.67)* 5/9)
            except ValueError:
                result = "error"
        elif 'r_to_f' in request.POST:
            reamur = float(expression)
            try:
                result = ((reamur * 9/4) + 32)
            except ValueError:
                result = "error"
        elif 'r_to_k' in request.POST:
            reamur = float(expression)
            try:
                result = ((reamur * 5/4) + 273.15)
            except ValueError:
                result = "error"
        elif 'k_to_r' in request.POST:
            kelvin = float(expression)
            try:
                result = ((kelvin - 273.15) * 4/5)
            except ValueError:
                result = "error"
        elif 'k_to_f' in request.POST:
            kelvin = float(expression)
            try:
                result = ((kelvin * 9/5) - 459.67)
            except ValueError:
                result = "error"
        elif 'binary' in request.POST:
            n = int(expression)
            try:
                result = format(n ,"b")
            except ValueError:
                result = "Don't use comma"
        elif 'num' in request.POST:
            n = expression
            try:
                result = int(n, 2)
            except ValueError:
                result = "Not Binary"
                
        elif 'sqrt' in request.POST:
            n = int(expression)
            try:
                result = math.sqrt(n)
            except ValueError:
                result = "Invalid Number"

            
    return render(request, 'kalkulator.html', {'result': result})
    
def index(request):
    try:
        output_result = ""
        selisih = 0.0
        output = ""
        if request.method == 'POST':
            input_code = request.POST.get('input_code', '')
            html_string = input_code
            soup = BeautifulSoup(html_string, 'html.parser')
            text = soup.get_text()

            if text.strip() != "":
                old_stdout = sys.stdout
                new_stdout = StringIO()
                sys.stdout = new_stdout

                # Execute the custom language interpreter function
                result, error = run('<stdin>', text)

                # Restore stdout to its original value
                sys.stdout = old_stdout

                # Get the output from StringIO
                output = new_stdout.getvalue()
                
                # Check if result is a list=
                if error:
                    output_result = repr(error.as_string())  # Ubah error menjadi string
                elif result:
                    if hasattr(result, 'elements') and len(result.elements) == 1:
                        output_result = repr(result.elements[0])
                        output = output_result
                    else:
                        # Check if result is a list
                        if isinstance(result, list):
                            output_result = json.dumps(result)  # Convert list to JSON string

                        else:
                            output_result = repr(result)

    except Exception as e:
        # Handle specific exceptions if needed
        print(f"An error occurred: {e}")
        output_result = f"An error occurred: {e}"

    return render(request, 'index.html', {'output_result': output_result, 'output': output})
