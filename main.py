import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LESS', 'MORE', 'EQUAL', 'LESS_EQUAL', 'MORE_EQUAL', 'NOT_EQUAL',
    'WHILE', 'IF', 'STR', 'CHAR', 'PRINT', 'PRINTCHAR', 'PRINTINT', 'INPUT', 'INPUTCHAR', 'INPUTINT', 'END'
)

# Tokens
t_END: str = "};"
t_LBRACE: str = "{"
t_RBRACE: str = "}"
t_PLUS: str = r'\+'
t_MINUS: str = "-"
t_TIMES: str = r'\*'
t_DIVIDE: str = "//"
t_MOD: str = "%"
t_EQUALS: str = "="
t_LPAREN: str = r'\('
t_RPAREN: str = r'\)'
t_LESS: str = "<"
t_MORE: str = ">"
t_LESS_EQUAL: str = "<="
t_MORE_EQUAL: str = ">="
t_EQUAL: str = "=="
t_NOT_EQUAL: str = "!="
t_WHILE: str = "While"
t_IF: str = "If"
t_STR: str = r'\"[a-zA-Z0-9_!? ,.]*\"'
t_CHAR: str = r'\'[a-zA-Z0-9_!? ,.]\''
t_PRINT: str = "Print"
t_PRINTCHAR: str = "PrintC"
t_PRINTINT: str = "PrintI"
t_INPUT: str = "Input"
t_INPUTCHAR: str = "InputC"
t_INPUTINT: str = "InputI"
t_NAME: str = r'[a-z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r"""\d+"""
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t\n"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

names = {}


def p_program(p):
    """program : statements END"""
    p[0] = ('program', p[1])


def p_statements_multiple(p):
    """statements : statements statement"""
    if p[1] is None:
        p[0] = ('statements', p[2])
    else:
        p[0] = ('statements', p[1], p[2])


def p_statements_simple(p):
    """statements : """
    pass


def p_statement(p):
    """statement : assignment
    | while
    | if
    | input
    | output"""
    p[0] = ('statement', p[1])


def p_operation(p):
    """operation : NAME operand NAME
    | NAME operand NUMBER
    | NUMBER operand NAME
    | NUMBER operand NUMBER"""
    p[0] = ('operation', p[2], p[1], p[3])


def p_operand(p):
    """operand : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MOD"""
    p[0] = ('operand', p[1])


def p_assignment(p):
    """assignment : NAME EQUALS NUMBER
    | NAME EQUALS operation
    | NAME EQUALS NAME
    | NAME EQUALS STR
    | NAME EQUALS CHAR"""
    p[0] = ('assignment', p[1], p[3])


def p_while(p):
    """while : WHILE LPAREN condition RPAREN LBRACE statements RBRACE"""
    p[0] = ('while', p[3], p[6])


def p_if(p):
    """if : IF LPAREN condition RPAREN LBRACE statements RBRACE"""
    p[0] = ('if', p[3], p[6])


def p_condition(p):
    """condition : NAME comparison NUMBER
    | NUMBER comparison NAME
    | NUMBER comparison NUMBER
    | NAME comparison NAME"""
    p[0] = ('condition', p[2], p[1], p[3])


def p_comparison(p):
    """comparison : LESS
    | MORE
    | EQUAL
    | NOT_EQUAL
    | LESS_EQUAL
    | MORE_EQUAL"""
    p[0] = ('comparison', p[1])


def p_input(p):
    """input : INPUTCHAR LPAREN NAME RPAREN
    | INPUT LPAREN NAME RPAREN
    | INPUTINT LPAREN NAME RPAREN"""
    p[0] = ('input', p[3], p[1])


def p_output(p):
    """output : PRINT LPAREN NAME RPAREN
    | PRINTINT LPAREN NAME RPAREN
    | PRINTCHAR LPAREN NAME RPAREN"""
    p[0] = ('output', p[3], p[1])


def p_error(p):
    print("Syntax error at '%s'" % p.value)


parser = yacc.yacc()
command_format = 3
memory_format = 1024
memory = [0] * memory_format * 2
variables = {}
variable_pointer = 512
instruction_pointer = 0
label_array = []


def t_assignment(assignment):
    global memory_format, memory, variables, instruction_pointer, variable_pointer
    if isinstance(assignment[2], tuple):
        if assignment[2][0] == "operation":
            if type(assignment[2][3]) is int:
                memory[instruction_pointer] = 20
                memory[instruction_pointer + 1] = assignment[2][3]
            elif type(assignment[2][3]) is str:
                memory[instruction_pointer] = 1
                if not assignment[2][3] in variables:
                    raise SyntaxError("Variable '%s' is not defined" % assignment[2][3])
                memory[instruction_pointer + 1] = variables[assignment[2][3]]
            instruction_pointer += command_format
            if type(assignment[2][2]) is int:
                memory[instruction_pointer] = 20
                memory[instruction_pointer + 1] = assignment[2][2]
            elif type(assignment[2][2]) is str:
                memory[instruction_pointer] = 1
                if not assignment[2][2] in variables:
                    raise SyntaxError("Variable '%s' is not defined" % assignment[2][2])
                memory[instruction_pointer + 1] = variables[assignment[2][2]]
            instruction_pointer += command_format

            match assignment[2][1][1]:
                case '+':
                    memory[instruction_pointer] = 3
                case '-':
                    memory[instruction_pointer] = 4
                case '*':
                    memory[instruction_pointer] = 5
                case '//':
                    memory[instruction_pointer] = 6
                case '%':
                    memory[instruction_pointer] = 7

    elif type(assignment[2]) is int:
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = assignment[2]
    elif type(assignment[2]) is str and '"' not in assignment[2] and '\'' not in assignment[2]:
        memory[instruction_pointer] = 1
        if not assignment[2] in variables:
            memory[instruction_pointer + 1] = variable_pointer
            variables[assignment[2]] = variable_pointer
            variable_pointer += 1
        else:
            memory[instruction_pointer + 1] = variables[assignment[2]]
    elif '\'' in assignment[2] and len(assignment[2]) == 3:
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = ord(assignment[2][1:-1])
    elif '"' in assignment[2]:
        form_string = assignment[2][1:-1][::-1]
        for char in form_string:
            memory[instruction_pointer] = 20
            memory[instruction_pointer + 1] = ord(char)
            instruction_pointer += command_format
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = len(form_string)
        instruction_pointer += command_format

        if not assignment[1] in variables:
            variables[assignment[1]] = variable_pointer
            for j in range(len(form_string) + 1):
                memory[instruction_pointer] = 2
                memory[instruction_pointer + 1] = variable_pointer
                instruction_pointer += command_format
                variable_pointer += 1
        else:
            raise SyntaxError("String variable '%s' can not be changed" % assignment[1])
        return

    instruction_pointer += command_format
    if not assignment[1] in variables:
        variables[assignment[1]] = variable_pointer
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variable_pointer
        variable_pointer += 1
    else:
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variables[assignment[1]]
    instruction_pointer += command_format


def t_condition(condition_statement):
    global memory_format, memory, variables, instruction_pointer, variable_pointer, label_array
    if type(condition_statement[1][3]) is int:
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = condition_statement[1][3]
    elif type(condition_statement[1][3]) is str:
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variables[condition_statement[1][3]]
    else:
        raise SyntaxError("Unexpected variable type at '%s'" % condition_statement[1][3])
    instruction_pointer += command_format
    if type(condition_statement[1][2]) is int:
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = condition_statement[1][2]
    elif type(condition_statement[1][2]) is str:
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variables[condition_statement[1][2]]
    else:
        raise SyntaxError("Unexpected variable type at '%s'" % condition_statement[1][2])
    instruction_pointer += command_format
    match condition_statement[1][1][1]:
        case '>':
            memory[instruction_pointer] = 11
        case '<':
            memory[instruction_pointer] = 12
        case '==':
            memory[instruction_pointer] = 13
        case '!=':
            memory[instruction_pointer] = 14
        case '>=':
            memory[instruction_pointer] = 15
        case '<=':
            memory[instruction_pointer] = 16
        case _:
            raise SyntaxError("Unexpected condition statement at '%s'" % condition_statement[1])
    current_label = instruction_pointer + 1
    instruction_pointer += command_format
    t_statements(condition_statement[2])
    return current_label


def t_while(while_statement):
    global memory_format, memory, variables, instruction_pointer, variable_pointer, label_array
    return_address = instruction_pointer
    current_label = t_condition(while_statement)
    memory[current_label] = instruction_pointer + command_format
    memory[instruction_pointer] = 10
    memory[instruction_pointer + 1] = return_address
    instruction_pointer += command_format


def t_if(if_statement):
    global memory_format, memory, variables, instruction_pointer, variable_pointer, label_array
    current_label = t_condition(if_statement)
    memory[current_label] = instruction_pointer


def t_input(input_statement):
    global memory_format, memory, variables, instruction_pointer, variable_pointer, label_array
    if input_statement[2] == "InputC":
        memory[instruction_pointer] = 31
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        if not input_statement[1] in variables:
            variables[input_statement[1]] = variable_pointer
            variable_pointer += 1
        memory[instruction_pointer + 1] = variables[input_statement[1]]
        instruction_pointer += command_format
    elif input_statement[2] == "InputI":
        memory[instruction_pointer] = 30
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        if not input_statement[1] in variables:
            variables[input_statement[1]] = variable_pointer
            variable_pointer += 1
        memory[instruction_pointer + 1] = variables[input_statement[1]]
        instruction_pointer += command_format
    elif input_statement[2] == "Input":
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = 10
        instruction_pointer += command_format

        memory[instruction_pointer] = 31
        instruction_pointer += command_format

        memory[instruction_pointer] = 14
        memory[instruction_pointer + 1] = instruction_pointer + 11 * command_format
        instruction_pointer += command_format

        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variable_pointer
        instruction_pointer += command_format
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = 1
        instruction_pointer += command_format
        memory[instruction_pointer] = 3
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variable_pointer
        instruction_pointer += command_format
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variable_pointer
        instruction_pointer += command_format
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = variable_pointer
        instruction_pointer += command_format
        memory[instruction_pointer] = 3
        instruction_pointer += command_format

        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = instruction_pointer + command_format + 1
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        instruction_pointer += command_format

        memory[instruction_pointer] = 10
        memory[instruction_pointer + 1] = instruction_pointer - 11 * command_format
        instruction_pointer += command_format

        memory[instruction_pointer] = 21
        instruction_pointer += command_format
        if not input_statement[1] in variables:
            variables[input_statement[1]] = variable_pointer
        variable_pointer += 32
    else:
        raise SyntaxError("Unexpected command '%s'" % input_statement[2])


def t_output(output_statement):
    global memory_format, memory, variables, instruction_pointer, variable_pointer, label_array
    memory[instruction_pointer] = 1
    if not output_statement[1] in variables:
        raise SyntaxError("Undefined variable at '%s'" % output_statement[1])
    memory[instruction_pointer + 1] = variables[output_statement[1]]
    instruction_pointer += command_format
    if output_statement[2] == "PrintC":
        memory[instruction_pointer] = 32
    elif output_statement[2] == "PrintI":
        memory[instruction_pointer] = 33
    elif output_statement[2] == "Print":
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = 1
        instruction_pointer += command_format

        memory[instruction_pointer] = 16
        memory[instruction_pointer + 1] = instruction_pointer + 14 * command_format
        instruction_pointer += command_format

        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format
        memory[instruction_pointer] = 3
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = instruction_pointer + command_format + 1
        instruction_pointer += command_format

        memory[instruction_pointer] = 1
        instruction_pointer += command_format
        memory[instruction_pointer] = 32
        instruction_pointer += command_format
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format
        memory[instruction_pointer] = 20
        memory[instruction_pointer + 1] = 1
        instruction_pointer += command_format
        memory[instruction_pointer] = 3
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format
        memory[instruction_pointer] = 1
        memory[instruction_pointer + 1] = variables[output_statement[1]]
        instruction_pointer += command_format

        memory[instruction_pointer] = 10
        memory[instruction_pointer + 1] = instruction_pointer - 13 * command_format
        instruction_pointer += command_format
        memory[instruction_pointer] = 21
        instruction_pointer += command_format
        memory[instruction_pointer] = 2
        memory[instruction_pointer + 1] = variables[output_statement[1]]

    else:
        raise SyntaxError("Unknown command '%s'" % output_statement[2])
    instruction_pointer += command_format


def t_statement(statement):
    match statement[1][0]:
        case "assignment":
            t_assignment(statement[1])
        case "while":
            t_while(statement[1])
        case "if":
            t_if(statement[1])
        case "input":
            t_input(statement[1])
        case "output":
            t_output(statement[1])


def t_statements(statements):
    if statements[1][0] == "statements":
        t_statements(statements[1])
        t_statement(statements[2])
    else:
        t_statement(statements[1])


def t_program(program):
    t_statements(program[1])


s = ""
while True:
    s += input('> ') + "\n"
    if "};" in s:
        break

p = parser.parse(s)
t_program(p)

with open("program.o", 'wb') as f:
    for i in range(len(memory)):
        f.write((memory[i]).to_bytes(4, 'big'))
