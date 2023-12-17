from mycalculator import MyCalculator
from flask import Flask, render_template, request

app = Flask(__name__)
calc = MyCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    result = calc.result(expression)
    return render_template('index.html', 
    	result=f'{expression} = {result}')

if __name__ == '__main__':
    app.run(debug=True)