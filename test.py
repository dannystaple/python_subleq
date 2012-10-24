from SubLeq import   Memory, Cpu
from nose.tools import assert_equal
from assembler import assemble

__author__ = 'danny'


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