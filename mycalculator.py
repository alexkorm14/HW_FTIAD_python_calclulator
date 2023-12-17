class MyCalculator:
    def __init__(self):
        self.operations = {
            '+' : (1, lambda x, y: x + y, 'left'), '-' : (1, lambda x, y: x - y, 'left'),
            '*' : (2, lambda x, y: x * y, 'left'), '/' : (2, lambda x, y: x / y, 'left'),
            '^' : (3, lambda x, y: x ** y, 'right'), '--' : (3, lambda x: -x,'right'),
        }
        
    def check(self,expression):
        print(list(self.parse_expression(expression)))
        print(list(self.sort_station(self.parse_expression(expression))))
        print(eval(expression.replace('^',"**")))
        return self.calculate(expression) , eval(expression.replace('^',"**"))
    
    def parse_expression(self,expression):
        expression = expression.replace('**','^')
        num = ''
        for s in expression:
            if s in '1234567890.':
                num += s
            elif num:
                yield float(num)
                num = ''
            if s in self.operations or s in "()":
                yield s    
        if num:
            yield float(num)
            
    def sort_station(self,parsed_expression):
        parsed_expression = list(parsed_expression)
        for i in range(1,len(parsed_expression)):
            if i == 1 and parsed_expression[i-1] == '-' and isinstance(parsed_expression[i],float):
                parsed_expression[i-1] = '--'   
            elif (parsed_expression[i-1] == '-' 
            	and (isinstance(parsed_expression[i-2],float) == False and parsed_expression[i-2] != ')') 
                and isinstance(parsed_expression[i],float)):
                parsed_expression[i-1] = '--' 
        stack = []
        for token in parsed_expression:
            if isinstance(token,float):
                yield token
            elif token in self.operations:
                if len(stack):
                    while (stack 
                    and (self.operations.get(token,(0,0,0))[0] < self.operations.get(stack[-1],(0,0,0))[0] 
                     or (self.operations.get(token,(0,0,0))[0] == self.operations.get(stack[-1],(0,0,0))[0] 
                             and self.operations[stack[-1]][-1] == 'left')) 
                    and token != '('):
                        yield stack.pop()   
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack:
                    if stack[-1] != '(':
                        yield stack.pop()
                    else:
                        stack.pop()
                        break
        while stack:
            yield stack.pop()
            
    def calculate(self,expression):
        stack = []
        for token in self.sort_station(self.parse_expression(expression)):
            if token in self.operations:
                if token != '--':
                    y, x = stack.pop(), stack.pop()
                    oper = self.operations[token][1](x, y)
                    stack.append(oper)
                else:
                    x = stack.pop()
                    oper = self.operations[token][1](x)
                    stack.append(oper)
            else:
                stack.append(token)
        
        return stack[0]

    def result(self,expression):
        try:
            my = self.calculate(expression)
            return my
        except Exception as e:
            return str(e)
