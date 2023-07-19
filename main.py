symbols_in_order_of_precedence = ["+", "-", "*", "/"]

class Node:
    def __init__(self, contents):
        self.contents = contents
        self.children = []
        
    def add_child(self, node):
        self.children.append(node)
        
    def __str__(self):
        return self.contents
    
    def __repr__(self):
        return self.contents
    
numbers = "0,1,2,3,4,5,6,7,8,9".split(",")

def derivative_of_polynomial(string):
    # Take string of form: 123x^1234
    multiplier = ""
    variable = ""
    power = ""
    
    variable_started = False
    variable_ended = False
    
    for letter in string:
        if letter == "^":
            variable_ended = True
            continue
        
        if variable_ended:
            power += letter
            continue
            
        if letter in numbers and variable_started is False:
            multiplier += letter
            continue
        
        if letter not in numbers and variable_started is False:
            variable_started = True
            variable += letter
            continue
        
        if letter not in numbers and variable_started is True and variable_ended is False:
            variable += letter
            continue
    
    if variable == "":
        return "0"        

    
    power_as_num =  int(power) if power != "" else 1
    
    multiplier_as_num = int(multiplier) if multiplier != "" else 1
    

    new_power = str(power_as_num-1)
    new_multiplier = str(multiplier_as_num*power_as_num)
    
    if new_power == "0":
        return new_multiplier
    
    return new_multiplier + variable + "^"+ new_power
    

def recursive_parse(current_symbol_index, node):
    if current_symbol_index >= len(symbols_in_order_of_precedence):
        node.derivative = derivative_of_polynomial(node.contents)
        return node
    
    symbol = symbols_in_order_of_precedence[current_symbol_index]
    layers = [Node(x) for x in node.contents.split(symbol)]    
    
    # Didn't do anything so pass node on unchanged
    if len(layers) == 1:
        return recursive_parse(current_symbol_index+1, node)
    
    symbol_node = Node(symbol)
    
    for layer in layers:
        child = recursive_parse(current_symbol_index+1, layer)
        symbol_node.add_child(child)
    
    if symbol == "+":
        symbol_node.derivative = "+".join([x.derivative for x in symbol_node.children])
    
    if symbol == "-":
        symbol_node.derivative = "+".join([x.derivative for x in symbol_node.children])
         
    if symbol == "*":
        # Take first two
        index = 0
        derivative = ""
        
        while index < len(symbol_node.children)-1:
            f = symbol_node.children[index]
            g = symbol_node.children[index+1]
            
            print(f.contents, g.contents)
            print(f.derivative, g.derivative)
            
            derivative += (f.derivative + "*" + g.contents + "+" + f.contents +"*" + g.derivative)
            index += 1
        symbol_node.derivative = derivative
    
    return symbol_node
