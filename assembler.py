__author__ = 'danny'

#Add labels to assembler
#Add macros to it


def assemble(code):
    """Given a string of code lines and the starting address (all labels relative to this),
    will output the list of assembled code"""
    output = []
    for line in code.splitlines():
        line = line.strip()
        operation, _, parameters = line.partition(' ')
        operation = operation.lower()
        if operation == "subleq":
            params = [int(param) for param in parameters.split(',')]
            if len(params) == 2:
                params.append(-1)
            elif len(params) != 3:
                raise TypeError('Incorrect number of parameters')
            output += params
        elif operation == "halt":
            output += [-1, -1, -1]
    return output