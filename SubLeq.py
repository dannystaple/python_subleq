import itertools
__author__ = 'danny'

#Human helper - cheats
NO_JUMP = -1

class SubLeqInterpreter(object):
    def __init__(self, memory, pc):
        """Memory should be an array. Which is writable/readable is up to implementation.
        pc should be an offset into that memory. Memory word size, a, b and pc should be the same."""
        self.memory = memory
        self.pc = pc

    def run(self):
        while True:
            a, b, j = self.fetch()
            self.execute(a, b, j)
            yield

    def fetch(self):
        """Fetch the instruction"""
        return self.memory[self.pc:self.pc + 3]

    def execute(self, a, b, jump_to):
        """Execute the instruction"""
        if a < 0 or b < 0 or (jump_to != NO_JUMP and jump_to < 0):
            raise StopIteration
        self.memory[b] -= self.memory[a]
        if jump_to != NO_JUMP and self.memory[b] <= 0:
            self.pc = jump_to
        else:
            self.pc += 3

class Memory(object):
    highest_mark =0

    def __init__(self):
        self.memory_sections = []

    def add_section(self, address, data):
        """Add a section of addressable memory.
        address - the location in the memory map,
        data -  an addressable object. Addresses used with that object will
                be relative to the start of the object, not the absolute address.
                It must implement len, and getitem. To be writeable, it must implement setitem too.
        """
        if address < self.highest_mark:
            raise RuntimeError("Sections must be added in order")
        self.memory_sections.append((address, data))
        self.highest_mark = address + len(data)

    def _getsection(self, address):
        """Get a section for a an address.
        Returns the section, and the new address relative to the section start"""
        for section_start, section in self.memory_sections:
            if address >= section_start:
                if address < section_start + len(section):
                    real_addr = address - section_start
                    return section, real_addr
        return None, None

    def __getitem__(self, item):
        """Get item at item"""
        if type(item) is slice:
            return [self[i] for i in range(item.start, item.stop, item.step or 1)]
        else:
            section, real_addr = self._getsection(item)
            if section:
                return section[real_addr]
            return 0


    def __setitem__(self, key, value):
        """Set items if possible"""
        section, real_addr = self._getsection(key)
        if section:
            try:
                section[real_addr] = value
            except TypeError:
                pass

    def __len__(self):
        return self.highest_mark

    def __iter__(self):
        for n in range(self.highest_mark):
            n = yield(self[n])

def MOV(in_addr, out_addr):
    return [
        0, 0, NO_JUMP,
        out_addr, out_addr, NO_JUMP,
        in_addr, 0, NO_JUMP,
        0, out_addr, NO_JUMP,
    ]

def HALT():
    return [
        -1, -1, -1
    ]

def ADD(a, b):
    """Synthesize b += a for subleq"""
    return [
        0, 0, NO_JUMP,
        a, 0, NO_JUMP,
        0, b, NO_JUMP,
    ]

def JMP(j):
    return [0, 0, j]


#Get into git
#Create a simple assembler
#Add labels to assembler
#Add macros to it

class SubLeqAssembler(object):
    """Simple subleq assembler
    """



def hello():
    #hello
    registers_start = 0
    registers = [0]
    rom_start = len(registers)
    rom= tuple([ord(c) for c in "Hello"])
    # 128 bytes of output
    ram_start = rom_start + len(rom)
    ram=([0] * 6)


    prog_start = ram_start + len(ram)
    #Start code at 0xff
    program = (
        MOV(rom_start, ram_start) +
        MOV(rom_start + 1, ram_start + 1) +
        MOV(rom_start + 2, ram_start + 2) +
        MOV(rom_start + 3, ram_start + 3) +
        MOV(rom_start + 4, ram_start + 4) +
        HALT()
    )

    mem = Memory()
    mem.add_section(registers_start, registers)
    mem.add_section(rom_start, rom)
    mem.add_section(ram_start, ram)
    mem.add_section(prog_start, program)

    cpu = SubLeqInterpreter(mem, prog_start)
    r = cpu.run()
    _ = [n for n in r]
    print [chr(n) for n in ram[0:5]]

def add12and13():
    registers_start = 0
    registers = [0]
    rom_start = len(registers)
    rom= (12, 13)
    # 128 bytes of output
    ram_start = rom_start + len(rom)
    ram=[0]

    prog_start = ram_start + len(ram)
    program = (
        MOV(rom_start, ram_start) +
        ADD(rom_start + 1, ram_start) +
        HALT()
    )

    mem = Memory()
    mem.add_section(registers_start, registers)
    mem.add_section(rom_start, rom)
    mem.add_section(ram_start, ram)
    mem.add_section(prog_start, program)

    cpu = SubLeqInterpreter(mem, prog_start)
    r = cpu.run()
    try:
        while True:
            r.next()
    except StopIteration:
        pass

    print "Result is ", mem[ram_start]

hello()
add12and13()