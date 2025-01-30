"""This program can be used as a calculator for lambda calculus"""
class LambdaTerm:
    """This class is used as the base for all lambda terms."""
    
    @classmethod
    def fromstring(cls, string):
        """Convert the input to a lambda term"""
        string = string.strip()

        while string.startswith('(') and string.endswith(')'):
            string = string[1:-1].strip()

        if len(string) == 1 and string.isalpha():
            return Variable(string)
        
        if string.isdigit():
            return NumericLiteral(int(string))
        
        if string.startswith("λ") or string.startswith("\\"):
            if "." in string:
                variable, body = string[1:].split(".", 1)
                variables = variable.strip()
                abstractions = body.strip()
                for var in reversed(variables.split()):
                    abstractions = Abstraction(Variable(var.strip()), cls.fromstring(abstractions))
                return abstractions
            raise ValueError(f"Invalid abstraction: {string}")
        
        # Deal with arithmetic operations 
        for operator in ["+", "-", "*", "/", "^"]:
            parenthesis_level = 0
            
            for i, character in enumerate(string):
                if character == "(":
                    parenthesis_level += 1
                elif character == ")":
                    parenthesis_level -= 1
                elif character == operator and parenthesis_level == 0:
                    left = cls.fromstring(string[:i].strip())
                    right = cls.fromstring(string[i+1:].strip())
                    if operator == "^":
                        operator = "**"
                    return ArithmeticOperation(left, operator, right)
                    
        symbols = cls.split_symbols(string)
        if len(symbols) > 1:
            current_value = cls.fromstring(symbols[0])
            for token in symbols[1:]:
                current_value = Application(current_value, cls.fromstring(token))
            return current_value
        
        raise ValueError(f"Invalid lambda term: {string}")
    
    @classmethod
    def split_symbols(cls, string):
        """Split the string into symbols, paying attention to parentheses"""
        symbols = []
        current_value = []
        parenthesis_level = 0

        for character in string:
            if character == " " and parenthesis_level == 0:
                if current_value:
                    symbols.append("".join(current_value).strip())
                    current_value = []

            else:
                if character == "(":
                    parenthesis_level += 1
                elif character == ")":
                    parenthesis_level -= 1
                current_value.append(character)

        if current_value:
            symbols.append("".join(current_value).strip())
        return symbols        

    def __call__(self, argument):
        """If the object is an Abstraction, then apply substitution method on the body"""
        if isinstance(self, Abstraction):
            return self.body.substitute({self.variable.symbol: argument}).reduce()
        raise TypeError("Only Abstraction can be called")
    
    def __eq__(self, other):
        """Check the equivalence of the two lambda terms"""
        if type(self) != type(other):
            return False
        return str(self.reduce()) == str(other.reduce())   
    
    def substitue(self, rules):
        """Override in subclasses"""
        pass

    def reduce(self):
        """Override in subclasses"""
        pass

    def free_variables(self):
        """Override in subclasses"""
        pass

class ArithmeticOperation(LambdaTerm):
    """This class represents the arithmetic operations"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator 
        self.right = right

    def __repr__(self):
        return f"ArithmeticOperation({repr(self.left)}, '{self.operator}', {repr(self.right)})"
    
    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
    
    def substitute(self, rules):
        left = self.left.substitute(rules)
        right = self.right.substitute(rules)
        return ArithmeticOperation(left, self.operator, right)
    
    def reduce(self):
        left = self.left.reduce()
        right = self.right.reduce()
            
        # Evaluate if both sides are numeric literals
        if isinstance(left, NumericLiteral) and isinstance(right, NumericLiteral):
            if self.operator == '+':
                return NumericLiteral(left.value + right.value)
            elif self.operator == '-':
                return NumericLiteral(left.value - right.value)
            elif self.operator == '*':
                return NumericLiteral(left.value * right.value)
            elif self.operator == '/' and right.value != 0:
                return NumericLiteral(left.value // right.value)
            elif self.operator == '/' and right.value == 0:
                raise ValueError("Cannot divide by zero")
            elif self.operator == '**':
                return NumericLiteral(left.value ** right.value)

        if self.operator == "*" and isinstance(left, Variable) and isinstance(right, ArithmeticOperation):
            if right.operator == "**" and isinstance(right.left, Variable) and right.left.symbol == left.symbol:
                return ArithmeticOperation(left, "**", NumericLiteral(right.right.value + 1))

        if self.operator == "*":
            if isinstance(right, ArithmeticOperation) and right.operator == "+":
                return ArithmeticOperation(
                    ArithmeticOperation(left, "*", right.left).reduce(),
                    "+",
                    ArithmeticOperation(left, "*", right.right).reduce()
                ).reduce()
            
        if isinstance(left, ArithmeticOperation) and left.operator == "+":
            return ArithmeticOperation(
                ArithmeticOperation(left.left, "*", right).reduce(),
                "+",
                ArithmeticOperation(left.right, "*", right).reduce()
            ).reduce()
        
        return ArithmeticOperation(left, self.operator, right)

class Variable(LambdaTerm):
    """This class represents the variables."""
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f"Variable('{self.symbol}')"
    
    def __str__(self):
        return self.symbol
    
    def substitute(self, rules):
        return rules.get(self.symbol, self)
    
    def reduce(self):
        return self
    
    def free_variables(self):
        """A variable is always free."""
        return {self.symbol}
    
class NumericLiteral(LambdaTerm):
    """This class represents a numeric literal"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumericLiteral({self.value})"
    
    def __str__(self):
        return str(self.value)
    
    def substitute(self, rules):
        return self
    
    def reduce(self):
        return self
    
    def free_variables(self):
        return set()
    
class Abstraction(LambdaTerm):
    """This class represents a lambda term of the form (λx.M)"""

    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __repr__(self):
        return f"Abstraction({repr(self.variable)}, {repr(self.body)})"
    
    def __str__(self):
        return f"λ{self.variable}.{self.body}"
    
    def substitute(self, rules):
        """Avoid substitution of bound variables"""
        if self.variable.symbol in rules:
            rules = rules.copy()
            del rules[self.variable.symbol]
        return Abstraction(self.variable, self.body.substitute(rules))
    
    def reduce(self):
        return Abstraction(self.variable, self.body.reduce())
    
    def free_variables(self):
        """Return the free variables in the body, excluding the bound variable."""
        return self.body.free_variables() - {self.variable.symbol}

class Application(LambdaTerm):
    """This class represents a lambda term in the form of (M N)"""
    def __init__(self, function, argument):
        self.function = function
        self.argument = argument

    def __repr__(self):
        return f"Application({repr(self.function)}, {repr(self.argument)})"
    
    def __str__(self):
        return f"({self.function} {self.argument})"
    
    def substitute(self, rules):
        return Application(self.function.substitute(rules), self.argument.substitute(rules))
    
    def reduce(self):
        reduced_function = self.function.reduce()
        reduced_argument = self.argument.reduce()

        # Apply beta reduction when the function is an abstraction
        if isinstance(reduced_function, Abstraction):
            return reduced_function.body.substitute({reduced_function.variable.symbol: reduced_argument}).reduce()
        return Application(reduced_function, reduced_argument)
    
    def free_variables(self):
        return self.function.free_variables().union(self.argument.free_variables())

def evaluate(term, max_steps=50):
    """Evaluate a lambda term to its normal form."""
    current = term
    for step in range(max_steps):
        next_term = current.reduce()
        if str(next_term) == str(current):  
            return next_term  
        current = next_term
    raise RecursionError("Evaluation did not converge within max_steps.")

def main():
    """Interactive Lambda Calculus interpreter."""
    print("   ")
    print("Lambda Calculus Interpreter")
    print("Enter lambda terms in form of '(λx.x) y, use for exponentiation '^'")
    print("Type 'exit' to quit")

    while True:
        try:
            user_input = input("\nEnter lambda term: ")
            if user_input.lower() == 'exit':
                print("\nExiting...")
                break

            if not user_input:
                continue
            
            term = LambdaTerm.fromstring(user_input)
            result = evaluate(term)
            if isinstance(result, NumericLiteral):
                print("Solution:", result.value)
            else:
                print("Solution:", result)

            second_input = input("\nEnter another lambda term to check equivalence (or press Enter to skip): ")
            if second_input:
                second_term = LambdaTerm.fromstring(second_input)
                if term == second_term:
                    print("The two terms are equivalent.")
                else:
                    print("The two terms are not equivalent.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
