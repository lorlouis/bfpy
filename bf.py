#!/usr/bin/python3
import sys

if len(sys.argv) != 2:
    print("Usage bfpy file.b")
    sys.exit()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

pointer = 0
mem = [0]
program = ""
pc = 0
try:
    with open(sys.argv[1]) as f:
        program = f.read().replace('\n', '')

except IOError:
    print(sys.argv[1] + " could not be opened")

def dec_p():
    global mem
    global pointer
    pointer -= 1
    if pointer < 0:
        raise Exception("pointer smaller than 0")

def inc_p():
    global mem
    global pointer
    pointer += 1
    if pointer == len(mem):
        mem.append(0)

def dec_v():
    global mem
    global pointer
    mem[pointer] -= 1

def inc_v():
    global mem
    global pointer
    mem[pointer] += 1

def print_v():
    global mem
    global pointer
    print(mem[pointer])

def read_v():
    global mem
    global pointer
    mem[pointer] = _GetchUnix()

def jf():
    global mem
    global pointer
    global program
    global pc
    if mem[pointer] != 0:
        loop_counter = 0
        initial_position = pc
        while loop_counter != 0 and program[pc] != ']':
            print('hello')
            if program[pc] == '[':
                loop_counter += 1
            elif program[pc] == ']':
                loop_couter -= 1
            pc += 1
            if pc >= len(program):
                raise Exception('no matching ] {}').format(initial_position)

def jb():
    global mem
    global pointer
    global program
    global pc
    if mem[pointer] != 0:
        loop_counter = 0
        initial_position = pc
        while loop_counter != 0 and program[pc] != ']':
            if program[pc] == '[':
                loop_counter -= 1
            elif program[pc] == ']':
                loop_couter += 1
            pc -= 1
            if pc < 0:
                raise Exception('no matching [ {}').format(initial_position)

mapper = {
    '>': inc_p,
    '<': dec_p,
    '+': inc_v,
    '-': dec_v,
    '.': print_v,
    ',': read_v,
    '[': jf,
    ']': jb
}


# execution
while 0 <= pc < len(program):
    func = mapper.get(program[pc], lambda: None)
    func()
    pc += 1
