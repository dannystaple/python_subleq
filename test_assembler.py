from assembler import assemble
from nose.tools import assert_equal

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


def test_it_should_ignore_comments():
    code = """
    ;a comment
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