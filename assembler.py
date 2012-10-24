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

def render_parameterised_macro(line, name, body, params):
    """Given a line known to contain the macro, and macro info,
    Find the parameters, substitute and return"""
    preamble, _, post = line.partition(name)
    post = post.strip()
    assert(post.startswith('('))
    post = post[1:]
    param_values, _, rest = post.partition(")")

    param_values = [param.strip() for param in param_values.split(',')]
    param_values = zip(params, param_values)

    for param_name, param_value in param_values:
        body = body.replace(param_name, param_value)

    line = preamble + body + rest
    return line

def render_macros(line, macros):
    """Given a line of non-preprocessed code, and a list of macros, process macro expansions until done.
    NOTE: Ignore comments"""
    if line.startswith(";"):
        return line
    else:
        while [macro_name for macro_name in macros.keys() if macro_name in line]:
            for macro_name, macro_info in macros.items():
                macro_body, params = macro_info
                if params and macro_name in line:
                    line = render_parameterised_macro(line, macro_name, macro_body, params)
                else:
                    line = line.replace(macro_name, macro_body)
        return line



def preprocessor(code):
    """Given the lines of code,
    will preprocess it - defining macro's, and then rendering them out."""
    macros = {} # name: expansion
    lines = (line.strip() for line in code.splitlines())
    processed_lines = []
    for line in lines:
        if line.startswith("#def begin"):
            macro_name = line.replace("#def begin", "").strip()
            params = None
            if " " in macro_name:
                macro_name, _, params = macro_name.partition(" ")
                params.split(",")
                params = [param.strip() for param in params]
            macro_body = []
            line = lines.next()
            while not line.startswith("#def end"):
                macro_body.append(line)
                line = lines.next()
            macros[macro_name] = ("\n".join(macro_body), params)
        else:
            processed_lines.append(render_macros(line, macros))
    return "\n".join(processed_lines)


def assemble(code):
    """Given a string of code lines and the starting address (all labels relative to this),
    will output the list of assembled code"""
    #Multi stage assembly:
    # 0 Macro expansion - including "placeholder" labels.
    # 1 Instructions/constants to numbers. Leave labels as strings
    # 2 Calculate address values
    # 3 Place address values in references, render to number code only
    preprocessed = preprocessor(code)
    first_pass = instructions_to_numbers(preprocessed)
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