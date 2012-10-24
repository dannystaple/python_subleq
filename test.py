from SubLeq import  HALT, Memory, Cpu
from nose.tools import assert_equal
from assembler import assemble

__author__ = 'danny'

def test_assembling_simple_program():
    program = assemble("subleq 1, 0, 5")
    assert_equal(program, [1, 0, 5])

def test_assembling_halt():
    program = assemble("halt")
    assert_equal(program, [-1, -1, -1])

def test_assembling_nojump():
    program = assemble("subleq 1, 0")
    assert_equal(program, [1, 0, -1])

def test_incorrect_params():
    try:
        program = assemble("subleq 1,2,3,4")
        assert False, "Should have raised a type error"
    except TypeError:
        pass

def test_assembling_multilines():
    program = assemble("""
        subleq 2, 5, 7
        halt""")
    assert_equal(program, [2, 5, 7, -1, -1, -1])

def test_it_should_allow_label_declarations():
    program = assemble("""
    start:    subleq 2, 5, 7
        halt""")
    assert_equal(program, [2, 5, 7, -1, -1, -1])

def test_it_should_follow_label_refs():
    code = """
        subleq 0, 0
    start: subleq 1, 1
        subleq 0, 1, start
        halt"""
    program = assemble(code)
    assert_equal(program, [
        0, 0, -1,
        1, 1, -1,
        0, 1, 3,
        -1, -1, -1
    ])


def test_running():
    ram_start = 0
    ram = [12, 8]
    prog_start = ram_start + len(ram)
    program = assemble("""
        subleq 1,0,-1
        halt""")
    mem = Memory()
    mem.add_section(ram_start, ram)
    mem.add_section(prog_start, program)
    c = Cpu(mem, prog_start)
    r = c.run()
    _ = [n for n in r]
    assert(ram[0] == 4)