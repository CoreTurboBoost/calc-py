#!/bin/env python3

import math
import decimal
import sys
import typing

APP_VERSION_MAJOR = 0
APP_VERSION_MINOR = 3

def log10(x):
    return math.log(x, 10)
def log2(x):
    return math.log(x, 2)
def cosec(x):
    return 1/math.sin(x)
def sec(x):
    return 1/math.cos(x)
def cot(x):
    return 1/math.tan(x)

KNOWN_CONSTS = {"pi": math.pi, "e": math.e, "deg2rad": (math.pi/180), "rad2deg": (180/math.pi)}
KNOWN_FUNCTIONS = {"sqrt": math.sqrt, "log10": log10, "log2": log2, "cos": math.cos, "sin": math.sin, "tan": math.tan, "cosec": cosec, "sec": sec, "cot": cot, "acos": math.acos, "asin": math.asin, "atan": math.atan}

def console_output_debug_msg(message : str, end = "\n"):
    print(f"[debug]: {message}", end = end)

class Token:
    TYPE_BAD = -1
    TYPE_NONE = 0
    TYPE_IDENTIFIER = 1
    TYPE_CONST = 2
    TYPE_NUMBER = 3
    TYPE_ADDITION = 4
    TYPE_SUBTRACTION = 5
    TYPE_MULTIPLICATION = 6
    TYPE_DIVISION = 7
    TYPE_EXPONENT = 8
    TYPE_OPEN_BRACKET = 9
    TYPE_CLOSE_BRACKET = 10
    TYPE_FUNCTION = 11
    def get_str_from_type_enum(enum_type: TYPE_NONE):
        if (enum_type == Token.TYPE_BAD):
            return "Bad"
        elif (enum_type == Token.TYPE_NONE):
            return "None"
        elif (enum_type == Token.TYPE_IDENTIFIER):
            return "Identifier"
        elif (enum_type == Token.TYPE_CONST):
            return "Const"
        elif (enum_type == Token.TYPE_NUMBER):
            return "Number"
        elif (enum_type == Token.TYPE_ADDITION):
            return "Addition"
        elif (enum_type == Token.TYPE_SUBTRACTION):
            return "Subtraction"
        elif (enum_type == Token.TYPE_MULTIPLICATION):
            return "MultiplicatioN"
        elif (enum_type == Token.TYPE_DIVISION):
            return "Division"
        elif (enum_type == Token.TYPE_EXPONENT):
            return "Exponent"
        elif (enum_type == Token.TYPE_OPEN_BRACKET):
            return "Open bracket"
        elif (enum_type == Token.TYPE_CLOSE_BRACKET):
            return "Close bracket"
        elif (enum_type == Token.TYPE_FUNCTION):
            return "Function"
        else:
            return "Unknown"

    # Object specific methods
    def __init__(self):
        self.lexeame = ""
        self.type = Token.TYPE_NONE
        self.char_index = 0
        self.error_object = None
    def get_type_str(self):
        return Token.get_str_from_type_enum(self.type)

class TokenError:
    TYPE_NONE = 0
    TYPE_UNKNOWN_CHAR = 1
    TYPE_UNKNOWN_IDENTIFIER = 2
    TYPE_DECIMAL_POINT_COUNT = 3
    def __init__(self):
        self.string = ""
        self.type = TokenError.TYPE_NONE

def lex(expression : str):
    skip_char_count = 0
    tokens = []
    for char_index, char in enumerate(expression):
        if (skip_char_count > 0):
            skip_char_count -= 1
            continue
        if (char.isspace()):
            continue
        if (char.isdigit() or char == '.'):
            decimal_count = 0
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_NUMBER
            cur_token.lexeame = ""
            skip_char_count = -1
            for char_index in range(char_index, len(expression)):
                char = expression[char_index]
                if (char == '.'):
                    decimal_count += 1
                    if (decimal_count > 1):
                        cur_token.type = Token.TYPE_BAD
                        cur_token.error_object = TokenError()
                        cur_token.error_object.type = TokenError.TYPE_DECIMAL_POINT_COUNT
                        cur_token.error_object.string = f"Number cannot have more than one decimal point"
                        break
                    cur_token.lexeame += char
                    skip_char_count += 1
                elif (char.isdigit()):
                    cur_token.lexeame += char
                    skip_char_count += 1
                else:
                    break
            tokens.append(cur_token)
        elif (char.isalpha() or char == '_'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_IDENTIFIER
            cur_token.lexeame = ""
            skip_char_count -= 1
            for char_index in range(char_index, len(expression)):
                char = expression[char_index]
                if (char.isalnum() or char == '_'):
                    cur_token.lexeame += char
                    skip_char_count += 1
                else:
                    break
            if (cur_token.lexeame in KNOWN_CONSTS.keys()):
                cur_token.type = Token.TYPE_CONST
            elif (cur_token.lexeame in KNOWN_FUNCTIONS.keys()):
                cur_token.type = Token.TYPE_FUNCTION
            else:
                cur_token.type = Token.TYPE_BAD
                cur_token.error_object = TokenError()
                cur_token.error_object.type = TokenError.TYPE_UNKNOWN_IDENTIFIER
                cur_token.error_object.string = f"Unknown constant or function \'{cur_token.lexeame}\'"
            tokens.append(cur_token)
        elif (char == '+'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_ADDITION
            cur_token.lexeame = '+'
            tokens.append(cur_token)
        elif (char == '-'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_SUBTRACTION
            cur_token.lexeame = '-'
            tokens.append(cur_token)
        elif (char == '*'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_MULTIPLICATION
            cur_token.lexeame = '*'
            tokens.append(cur_token)
        elif (char == '/'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_DIVISION
            cur_token.lexeame = '/'
            tokens.append(cur_token)
        elif (char == '^'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_EXPONENT
            cur_token.lexeame = '^'
            tokens.append(cur_token)
        elif (char == '('):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_OPEN_BRACKET
            cur_token.lexeame = '('
            tokens.append(cur_token)
        elif (char == ')'):
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_CLOSE_BRACKET
            cur_token.lexeame = ')'
            tokens.append(cur_token)
        else:
            cur_token = Token()
            cur_token.char_index = char_index
            cur_token.type = Token.TYPE_BAD
            cur_token.lexeame = ""
            cur_token.error_object = TokenError()
            cur_token.error_object.type = TokenError.TYPE_UNKNOWN_CHAR
            if (char.isprintable()):
                print_char = f"\'{char}\'"
            else:
                print_char = f"{ord(char)}"
            cur_token.error_object.string = f"Unknown char {print_char}"
            tokens.append(cur_token)
    return tokens

def get_lex_error_count(tokens : typing.List[Token]):
    error_count = 0
    for token in tokens:
        if (token.type == Token.TYPE_BAD):
            error_count += 1
    return error_count

def print_lex_errors(tokens : typing.List[Token]):
    error_count = 0
    for token in tokens:
        if (token.type == Token.TYPE_BAD):
            print(f"TOKEN ERROR: char {token.char_index+1}. {token.error_object.string}.")
            error_count += 1
    return error_count

def eval_lex_tokens(tokens : typing.List[Token]):
    # returns (evaluated_value, errors)
    # evaluated_value : Decimal() or None on error
    # errors : list[str]
    tokens = tokens.copy()
    def get_op_precedence(token_type : Token):
        # larget number greater precedence
        if (token_type == Token.TYPE_NONE or token_type == Token.TYPE_OPEN_BRACKET):
            return 0
        if (token_type == Token.TYPE_ADDITION or token_type == Token.TYPE_SUBTRACTION):
            return 1
        if (token_type == Token.TYPE_MULTIPLICATION or token_type == Token.TYPE_DIVISION):
            return 2
        if (token_type == Token.TYPE_EXPONENT):
            return 3
        if (token_type == Token.TYPE_FUNCTION):
            return 1 # NOTE: Not sure where functions appear here. Assuming they are like * and /
        # add functions here
        console_output_debug_msg(f"get_precedence fn param not recognised token_type:{token_type}")
        return -1
    def is_operator(token_type : Token):
        if (token_type == Token.TYPE_ADDITION or token_type == Token.TYPE_SUBTRACTION):
            return True
        if (token_type == Token.TYPE_MULTIPLICATION or token_type == Token.TYPE_DIVISION):
            return True
        if (token_type == Token.TYPE_EXPONENT):
            return True
        if (token_type == Token.TYPE_FUNCTION):
            return True
        return False

    errors = []
    evaluated_value = 0
    operators_stack = []
    numbers_stack = []
    post_fix_token_list = []

    open_bracket_token = Token()
    open_bracket_token.char_index = -1
    open_bracket_token.type = Token.TYPE_OPEN_BRACKET
    open_bracket_token.lexeame = "("
    close_bracket_token = Token()
    close_bracket_token.char_index = -1
    close_bracket_token.type = Token.TYPE_CLOSE_BRACKET
    close_bracket_token.lexeame = ")"
    zero_token = Token()
    zero_token.char_index = -1
    zero_token.type = Token.TYPE_NUMBER
    zero_token.lexeame = "0"

    # handled minus signs and convert constants
    cur_token_index = 0
    cur_token = None
    for cur_token_index in range(len(tokens)):
        cur_token = tokens[cur_token_index]
        if (cur_token.type == Token.TYPE_CONST):
            tokens[cur_token_index].lexeame = str(KNOWN_CONSTS[tokens[cur_token_index].lexeame])
            tokens[cur_token_index].type = Token.TYPE_NUMBER
    cur_token_index = 0
    cur_token = None
    while (cur_token_index < len(tokens)):
        cur_token = tokens[cur_token_index]
        if (cur_token.type == Token.TYPE_SUBTRACTION):
            if (cur_token_index == 0):
                if (len(tokens) > 1):
                    console_output_debug_msg(f"cur_token_index:{cur_token_index} next token type:\'{Token.get_str_from_type_enum(tokens[cur_token_index+1].type)}\'")
                    if (tokens[cur_token_index+1].type == Token.TYPE_NUMBER or tokens[cur_token_index+1].type == Token.TYPE_CONST or tokens[cur_token_index+1].type == Token.TYPE_IDENTIFIER):
                        console_output_debug_msg("     Added tokens: (0<token>))")
                        tokens.insert(0, open_bracket_token)
                        tokens.insert(1, zero_token)
                        tokens.insert(cur_token_index+4, close_bracket_token)
                        cur_token_index += 3
            else:
                if (cur_token_index+1 < len(tokens)):
                    console_output_debug_msg(f"cur_token_index:{cur_token_index} last token type:\'{Token.get_str_from_type_enum(tokens[cur_token_index-1].type)}\', next token type:\'{Token.get_str_from_type_enum(tokens[cur_token_index+1].type)}\'")
                    if ((tokens[cur_token_index-1].type != Token.TYPE_NUMBER and tokens[cur_token_index-1].type != Token.TYPE_CONST and tokens[cur_token_index-1].type != Token.TYPE_IDENTIFIER and tokens[cur_token_index-1].type != Token.TYPE_CLOSE_BRACKET) and (tokens[cur_token_index+1].type == Token.TYPE_NUMBER or tokens[cur_token_index+1].type == Token.TYPE_CONST or tokens[cur_token_index+1].type == Token.TYPE_IDENTIFIER)):
                        console_output_debug_msg(f"((tokens[cur_token_index-1].type != Token.TYPE_NUMBER:{tokens[cur_token_index-1].type != Token.TYPE_NUMBER}")
                        console_output_debug_msg(f"tokens[cur_token_index-1].type != Token.TYPE_CONST:{tokens[cur_token_index-1].type != Token.TYPE_CONST}")
                        console_output_debug_msg(f"tokens[cur_token_index-1] != Token.TYPE_IDENTIFIER:{tokens[cur_token_index-1].type != Token.TYPE_IDENTIFIER}")
                        console_output_debug_msg(f"tokens[cur_token_index-1] != Token.TYPE_CLOSE_BRACKET:{tokens[cur_token_index-1].type != Token.TYPE_CLOSE_BRACKET}")
                        console_output_debug_msg(f"tokens[cur_token_index+1].type == Token.TYPE_NUMBER:{tokens[cur_token_index+1].type == Token.TYPE_NUMBER}")
                        console_output_debug_msg(f"tokens[cur_token_index+1] == Token.TYPE_CONST:{tokens[cur_token_index+1].type == Token.TYPE_CONST}")
                        console_output_debug_msg(f"tokens[cur_token_index+1] == Token.TYPE_IDENTIFIER:{tokens[cur_token_index+1].type == Token.TYPE_IDENTIFIER}")
                        console_output_debug_msg("     Added tokens: (0<token>))")
                        tokens.insert(cur_token_index, zero_token)
                        tokens.insert(cur_token_index, open_bracket_token)
                        tokens.insert(cur_token_index+4, close_bracket_token)
                        cur_token_index += 3
        cur_token_index += 1

    # debug
    console_output_debug_msg(f"Printing partial processed tokens:")
    for token in tokens:
        print(f"{token.lexeame}", end = "")
    print()
    # /debug

    #infix to postfix
    open_bracket_count = 0
    for token_index, token in enumerate(tokens):

        post_fix_str = ""
        for o in post_fix_token_list:
            post_fix_str += str(o.lexeame) + " "
        console_output_debug_msg(f"[{token_index}] post fix expression: \'{post_fix_str}\'")

        if (token.type == Token.TYPE_IDENTIFIER or token.type == Token.TYPE_CONST):
            post_fix_token_list.append(token)
        elif (token.type == Token.TYPE_NUMBER):
            post_fix_token_list.append(token)
        elif (token.type == Token.TYPE_OPEN_BRACKET):
            open_bracket_count += 1
            operators_stack.append(token)
        elif (token.type == Token.TYPE_CLOSE_BRACKET):
            open_bracket_count -= 1
            cur_token = operators_stack[-1]
            while (cur_token.type != Token.TYPE_OPEN_BRACKET):
                if (len(operators_stack) == 0):
                    errors.append("Unmatched brackets, no matching \'(\' found")
                    break
                post_fix_token_list.append(operators_stack.pop())
                cur_token = operators_stack[-1]
            if (len(operators_stack) > 0):
                operators_stack.pop() 
        # NEW -------  Attempts to reverse the order of the functions if they are placed one after the other without brackets
        elif (is_operator(token.type) and token.type == Token.TYPE_FUNCTION):
            cur_func_prec = get_op_precedence(token.type)
            if len(operators_stack) > 0:
                stack_top_op_precedence = get_op_precedence(operators_stack[-1].type)
                while stack_top_op_precedence >= cur_func_prec and operators_stack[-1].type != Token.TYPE_FUNCTION:
                    post_fix_token_list.append(operators_stack.pop())
                    if (len(operators_stack) > 0):
                        stack_top_op_precedence = get_op_precedence(operators_stack[-1].type)
                    else:
                        break
            operators_stack.append(token)
        # /NEW ------

        elif (is_operator(token.type)):
            console_output_debug_msg(f"[{token_index}] Considered token as an operator, {token}")
            cur_op_precedence = get_op_precedence(token.type)
            if (len(operators_stack) > 0):
                stack_top_op_precedence = get_op_precedence(operators_stack[-1].type)
            else:
                stack_top_op_precedence = get_op_precedence(Token.TYPE_NONE)
            console_output_debug_msg(f"[{token_index}] both precedences (cur, stack_top): ({cur_op_precedence}, {stack_top_op_precedence})")
            if (cur_op_precedence > stack_top_op_precedence):
                console_output_debug_msg(f"[{token_index}] Added {token.lexeame} to op stack")
            while (stack_top_op_precedence >= cur_op_precedence):
#                console_output_debug_msg(f"[{token_index}] Adding operator to post-fix list ({operators_stack[-1].lexeame})")
                console_output_debug_msg(f"[{token_index}] Adding operator to post-fix list ({operators_stack[-1].lexeame}) then added another operator to operators_stack ({token.lexeame})")
                post_fix_token_list.append(operators_stack.pop())
                if (len(operators_stack) > 0):
                    stack_top_op_precedence = get_op_precedence(operators_stack[-1].type)
                else:
                    stack_top_op_precedence = get_op_precedence(Token.TYPE_NONE)
            operators_stack.append(token)
#            if (cur_op_precedence == stack_top_op_precedence):
#                console_output_debug_msg(f"[{token_index}] Adding operator to post-fix list ({operators_stack[-1].lexeame}) then added another operator to operators_stack ({token.lexeame})")
#                post_fix_token_list.append(operators_stack.pop())
#                operators_stack.append(token)
        else:
            error_string = f"[char_index:{token.char_index}] Token list contains unknown or bad token type"
            errors.append(error_string)
    
    if (len(operators_stack) > 0):
        console_output_debug_msg(f"Adding remaining operators on stack to post-fix list, len:{len(operators_stack)}")
    for operator_index in range(len(operators_stack)):
        console_output_debug_msg(f" [{operator_index}] adding operator:{operators_stack[-1].lexeame} to post_fix_token_list")
        post_fix_token_list.append(operators_stack.pop())

    if (open_bracket_count > 0):
        errors.append(f"Bracket mismatch. Some brackets dont have \')\', {open_bracket_count} specifically")

    # debug
    post_fix_str = ""
    for o in post_fix_token_list:
        post_fix_str += " " + str(o.lexeame)
    console_output_debug_msg(f"post fix expression: {post_fix_str}")
    # /debug

    if (len(errors) > 0):
        return (None, errors)

    # process post fix list
    for token in post_fix_token_list:
        if (token.type == Token.TYPE_NUMBER):
            numbers_stack.append(decimal.Decimal(token.lexeame))
        elif (is_operator(token.type)):
            if (len(numbers_stack) < 1):
                errors.append("0 Too many operators, for the number of operands")
                break
            operand_a = numbers_stack.pop()
            if (token.type == Token.TYPE_FUNCTION):
                console_output_debug_msg(f"running function {token.lexeame}")
                try:
                    numbers_stack.append(decimal.Decimal(KNOWN_FUNCTIONS[token.lexeame.lower()](operand_a)))
                    continue
                except ZeroDivisionError:
                    errors.append(f"{[token.char_index+1]} Function failure, math domain error")
                    break
                except ValueError:
                    errors.append(f"{[token.char_index+1]} Function failure, math domain error")
                    break
                except:
                    errors.append(f"{[token.char_index+1]} Function failure, {sys.exc_info()[1]}")
                    break

            if (len(numbers_stack) < 1):
                errors.append("1 Too many operators, for the number of operands")
                break
            operand_b = numbers_stack.pop()
            if (token.type == Token.TYPE_ADDITION):
                numbers_stack.append(operand_a + operand_b)
            if (token.type == Token.TYPE_SUBTRACTION):
                numbers_stack.append(operand_b - operand_a)
            if (token.type == Token.TYPE_MULTIPLICATION):
                numbers_stack.append(operand_a * operand_b)
            if (token.type == Token.TYPE_DIVISION):
                if (operand_a == 0):
                    errors.append(f"[{token.char_index+1}] Division by zero")
                    break
                numbers_stack.append(operand_b / operand_a)
            if (token.type == Token.TYPE_EXPONENT):
                console_output_debug_msg(f"exponent operation: {operand_b}^{operand_a}")
                try:
                    numbers_stack.append(decimal.Decimal(math.pow(operand_b, operand_a)))
                except:
                    errors.append(f"[{token.char_index+1}] expression: \'{operand_b}^({operand_a})\' failed, {sys.exc_info()[1]}")

    if (len(numbers_stack) > 1):
        errors.append(f"Too few operators, for the number of operands, {len(numbers_stack)} specifically")
        console_output_debug_msg(f"Error: numbers_stack:{numbers_stack}")

    if (len(errors) > 0):
        return (None, errors)
    return (numbers_stack[0], errors)

is_interactive = False
if (len(sys.argv) == 1):
    is_interactive = True
if len(sys.argv) > 1:
    if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print(f"python3 {sys.argv[0]} [expression]")
        print( "python3 {-v|-h|__VERSION__}")
        print( "  -v, --version    print program version and exit")
        print( "      __VERSION__  output version in specific format")
        print( "  -h, --help       print this help page and exit")
        sys.exit()
    if (sys.argv[1] == "--version" or sys.argv[1] == "-v"):
        print(f"VERSION: {APP_VERSION_MAJOR}.{APP_VERSION_MINOR}")
        sys.exit()
    if (sys.argv[1] == "__VERSION__"):
        print(f"{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}")
        sys.exit()

while is_interactive:
    if is_interactive:
        try:
            expression = input(">> ").strip()
        except EOFError:
            print("\r")
            expression = "q"
        if expression == "q" or expression == "exit":
            sys.exit()
    else:
        expression = sys.argv[1]
    lex_tokens = lex(expression)
    lex_error_count = print_lex_errors(lex_tokens)
    if (lex_error_count > 0):
        print(f"{lex_error_count} error(s) occured in <expression>")
        if is_interactive:
            continue
        else:
            sys.exit()

    console_output_debug_msg("All lex tokens:")
    for token_index, token in enumerate(lex_tokens):
        console_output_debug_msg(f" [{token_index}] {token.lexeame}")
    console_output_debug_msg("End of tokens")
    evaluated_value, errors = eval_lex_tokens(lex_tokens)
    if (len(errors) > 0):
        print("Input had errors, no value returned", file = sys.stderr)
        for error in errors:
            print(f"Error: {error}", file = sys.stderr)
        if is_interactive:
            continue
        else:
            sys.exit(1)
    print(evaluated_value)
