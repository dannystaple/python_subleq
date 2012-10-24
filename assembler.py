__author__ = 'danny'

#Add labels to assembler
#Add macros to it

def number_or_label(param):
    if param.isdigit() or param.startswith('-'):
        return int(param)
    else:
        return param


def instructions_to_numbers(code):
    """Given the code,
    output numbers representing the instructions.
    Leave label refs as label strings"""
    output = []
    for line in code.splitlines():
        label = None
        if ':' in line:
            label, _, line = line.partition(':')
            label = label.strip()
        line = line.strip()

        operation, _, parameters = line.partition(' ')
        operation = operation.lower()
        instruction = None
        if operation == "subleq":
            parameters = [param.strip() for param in parameters.split(',')]
            params = [number_or_label(param) for param in parameters]
            if len(params) == 2:
                params.append(-1)
            elif len(params) != 3:
                raise TypeError('Incorrect number of parameters')
            instruction =params
        elif operation == "halt":
            instruction = [-1, -1, -1]

        if instruction:
            output.append((label, instruction))

    return output

def calculate_labels(first_pass):
    """Given the first pass code, generate any labels"""
    address = 0
    labels = {}
    for label, instruction in first_pass:
        if label:
            labels[label] = address
        address += len(instruction)
    return labels

def render_code(first_pass, labels):
    output = []
    for _, instruction in first_pass:
        instruction = [type(param) is str and labels[param] or param for param in instruction]
        output.extend(instruction)
    return output

def assemble(code):
    """Given a string of code lines and the starting address (all labels relative to this),
    will output the list of assembled code"""
    #Multi stage assembly:
    # 0 Macro expansion - including "placeholder" labels.
    # 1 Instructions/constants to numbers. Leave labels as strings
    # 2 Calculate address values
    # 3 Place address values in references, render to number code only
    first_pass = instructions_to_numbers(code)
    labels = calculate_labels(first_pass)
    output = render_code(first_pass, labels)
    return output

sample_hello_world = """
; Example code: (inserted labels - ram_start.)

#def begin CLR a:
    subleq a, a
#def end

#def begin MOV in,out
    CLR 0
    CLR out
    subleq in, 0
    subleq 0, out
#def end

    MOV hello, ram_start
    MOV hello + 1, ram_start + 1
    MOV hello + 2, ram_start + 2
    MOV hello + 3, ram_start + 3
    MOV hello + 4, ram_start + 4
    halt

hello: dc.c "Hello"
"""