"""Symbolic Differentiation."""
from node import Node

symbols_in_order_of_precedence = ["+", "-", "*", "/"]
numbers = "0,1,2,3,4,5,6,7,8,9".split(",")


def derivative_of_single_term(string):
    """Take string of form: 123x^1234 and return derivative as string."""
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

        if letter not in numbers and variable_started is True:
            variable += letter
            continue

    if variable == "":
        return "0"

    power_as_num = int(power) if power != "" else 1
    multiplier_as_num = int(multiplier) if multiplier != "" else 1

    new_power = str(power_as_num - 1)
    new_multiplier = str(multiplier_as_num * power_as_num)

    if new_power == "0":
        return new_multiplier

    if new_power == "1":
        return new_multiplier + variable

    return new_multiplier + variable + "^" + new_power


def addition_rule(symbol_node):
    return "+".join([x.derivative for x in symbol_node.children])


def subtraction_rule(symbol_node):
    return "-".join([x.derivative for x in symbol_node.children])


def product_rule(symbol_node):
    derivatives = []

    for i in range(0, len(symbol_node.children)):
        terms = [
            symbol_node.children[j].derivative if i == j
            else symbol_node.children[j].contents
            for j in range(0, len(symbol_node.children))
        ]
        derivatives.append("*".join(terms))

    return "+".join(derivatives)


def quotient_rule(symbol_node):
    if len(symbol_node.children) != 2:
        raise Exception("can't apply quotient rule")

    f = symbol_node.children[0]
    g = symbol_node.children[1]

    numerator = "(" + f.derivative + "*" + g.contents + "+" + f.contents + "*" + g.derivative + ")"
    denominator = "(" + g.contents + ")^2"

    return numerator + "/" + denominator


def recursive_parse(current_symbol_index, node):
    """
    Recursive Parse and Differentiate.

    Recursively parse into tree.
    Then traverse back up to form derivatives.
    """
    if current_symbol_index >= len(symbols_in_order_of_precedence):
        node.derivative = derivative_of_single_term(node.contents)
        return node

    symbol = symbols_in_order_of_precedence[current_symbol_index]
    layers = [Node(x) for x in node.contents.split(symbol)]

    # Didn't do anything so pass node on unchanged
    if len(layers) == 1:
        return recursive_parse(current_symbol_index + 1, node)

    symbol_node = Node(symbol)

    for layer in layers:
        child = recursive_parse(current_symbol_index + 1, layer)
        symbol_node.add_child(child)

    if symbol == "+":
        symbol_node.derivative = addition_rule(symbol_node)

    if symbol == "-":
        symbol_node.derivative = subtraction_rule(symbol_node)

    if symbol == "*":
        symbol_node.derivative = product_rule(symbol_node)

    if symbol == "/":
        symbol_node.derivative = quotient_rule(symbol_node)

    return symbol_node


def differniate_expression(expression):
    """Calculate derivative of string."""
    return recursive_parse(0, Node(expression)).derivative
