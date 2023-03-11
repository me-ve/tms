#!/bin/python

import re
import sys
import time

def load_instructions(filename:str) -> tuple[chr, str, dict]:
    states = {}
    with open(filename, "r") as file:
        text = file.read().strip()
    lines = text.split("\n")
    # TODO fix using whitespaces as null_char
    assert len(lines[0]) == 1, f"Error: expected one character in top line ({len(lines[0])} characters != 1)"
    null_char, start_state, states_lines = lines[0], lines[1], lines[2:]
    for state in states_lines:
        if state == "":
            continue
        state = re.sub('[\(\) ]', '', state).split(",")
        assert len(state) == 5, f"Error: wrong state parameters count ({len(state)} != 5)"
        name, symbol_in, symbol_out, next_state, direction = state
        if name not in states:
            states[name] = {} 
        states[name][symbol_in] = {}
        states[name][symbol_in]["out"] = symbol_out
        states[name][symbol_in]["next"] = next_state
        states[name][symbol_in]["direction"] = direction.upper()
    return null_char, start_state, states

def load_tape(filename:str) -> list[chr]:
    tape = []
    with open(filename, "r") as file:
        lines = file.read().split("\n")
    assert len(lines) == 2, f"Error: wrong lines count ({len(lines)} != 2)"
    tape = list(lines[0])
    head_pos = int(lines[1])
    return tape, head_pos

def save_tape(filename:str, tape:list[chr], head:int):
    with open(filename, "w") as file:
        file.write("".join(tape)+"\n"+str(head))

def draw_tape(tape:list[chr], null_char:chr, head:int, width:int) -> None:
    n = len(tape)
    min_cell = head - width // 2
    cell_range = range(min_cell, min_cell+width)
    res = ""
    under_res = ""
    for i in cell_range:
        if i == head:
            under_res += "  ^ "
        else:
            under_res += "    "
        if i not in range(n):
            res += f"| {null_char} "
        else:
            res += f"| {tape[i]} "
    print(res + "|" + "\n" + under_res + " ")

def get_current_symbol(tape:list[chr], head:int, null_char:chr) -> chr:
    return tape[head] if head in range(len(tape)) else null_char

def fetch_state(name:str, states:dict, symbol:chr) -> dict:
    state = states.get(name, {})
    if state is None:
        return {}
    return state.get(symbol, {})

def adjust_tape(tape:list[chr], head:int, null_char:chr) -> list[chr]:
    if head not in range(len(tape)):
        if head < 0:
            for i in range(-head):
                tape.insert(0, null_char)
                head += 1
        else:
            for i in range(head - len(tape) + 1):
                tape.append(null_char)
    return tape, head

def execute_state(tape:list[chr], state_properties:dict, head:int) -> tuple[list, int, str]:
    new_symbol = state_properties["out"]
    direction = state_properties["direction"]
    next_state = state_properties["next"]
    tape_len = len(tape)
    tape[head] = new_symbol
    d_head = 1 if direction == "R" else -1
    head += d_head
    return tape, head, next_state

def process_state(tape:list, states:dict, current_state:str, head:int, null_char:chr) -> bool:
    current_symbol = get_current_symbol(tape, head, null_char)
    state_properties = fetch_state(current_state, states, current_symbol)
    state_exists = bool(state_properties)   # empty dict evaluates to False
    next_state = current_state
    if state_exists:
        tape, head, next_state = execute_state(tape, state_properties, head)
        tape, head = adjust_tape(tape, head, null_char)
    return state_exists, head, next_state

def main_loop(states_file:str, tape_file:str):
    sleep_time = 0
    tape_display_width = 16
    try:
        null_char, start_state_name, states = load_instructions(states_file)
    except Exception as e:
        print(f"Error: could not have read the states from file {states_file}")
        print(f"Details: {e}")
        exit(1)
    current_state = start_state_name
    try:
        tape, head = adjust_tape(*load_tape(tape_file), null_char)
    except Exception as e:
        print(f"Error: there was a problem with reading tape from file {tape_file}")
        print(f"Details: {e}")
        exit(1)
    print(f"Null character: {null_char}")
    print(f"Head: {head}")
    print("Available states:")
    for name in states:
        print(f"{name}:")
        for symbol_in, properties in states[name].items():
            symbol_out, next_state, direction = properties.values()
            print(f"\t{symbol_in}: output: {symbol_out}, next state: {next_state}, direction: {direction}")
    status = True
    ticks = 0
    while status:
        print(f"Current state: {current_state}")
        draw_tape(tape, null_char, head, tape_display_width)
        status, head, current_state = process_state(tape, states, current_state, head, null_char)
        ticks += 1
        time.sleep(sleep_time)
    print(f"Execution ended in {ticks} ticks")
    save_tape(tape_file+".new", tape, head)
    print(f"New tape saved into file {tape_file}.new")

def main():
    if len(sys.argv) != 3:
        print(f"Using: python {sys.argv[0]} <state-file> <tape-file>")
        exit(1)
    main_loop(sys.argv[1], sys.argv[2])

main()