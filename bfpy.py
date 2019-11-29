#!/usr/bin/python3
import sys
import readchar

if len(sys.argv) != 2:
    print("Usage bfpy file.b")
    sys.exit()

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
    if pointer == 0:
        raise Exception('Attempting to go below address 0')
    pointer -= 1

def inc_p():
    global mem
    global pointer
    print(pointer)
    if pointer == sys.maxsize:
        pointer = 0
    else:
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
    if mem[pointer] == 10:
        print()
    print(chr(mem[pointer] & 0xffffffffffffffff), end="")

def print_vl():
    global mem
    global pointer
    if mem[pointer] == 10:
        print()
    print(mem[pointer], end="")

def read_v():
    global mem
    global pointer
    c = ord(readchar.readchar())
    if c == 4:
        c = -1
    mem[pointer] = c

def jf():
    global mem
    global pointer
    global program
    global pc
    if mem[pointer] == 0:
        loop_counter = 0
        initial_position = pc
        pc += 1
        while loop_counter != 0 or program[pc] != ']':
            if program[pc] == '[':
                loop_counter += 1
            elif program[pc] == ']':
                loop_counter -= 1
            pc += 1
            if pc >= len(program):
                raise Exception('no matching ] {}'.format(initial_position))

def jb():
    global mem
    global pointer
    global program
    global pc
    if mem[pointer] != 0:
        loop_counter = 0
        initial_position = pc
        pc -= 1
        while loop_counter != 0 or program[pc] != '[':
            if program[pc] == '[':
                loop_counter -= 1
            elif program[pc] == ']':
                loop_counter += 1
            pc -= 1
            if pc < 0:
                raise Exception('no matching [ {}'.format(initial_position))

mapper = {
    '>': inc_p,
    '<': dec_p,
    '+': inc_v,
    '-': dec_v,
    '.': print_v,
    ',': read_v,
    '|': print_vl,
    '[': jf,
    ']': jb
}


# execution
while 0 <= pc < len(program):
    func = mapper.get(program[pc], lambda: None)
    func()
    pc += 1
