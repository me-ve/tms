# TMS

This is a simple program for simulation of the Turing machine.\
The user can create the program for it by creating state table file with .stt extension (or any other), which should look like this:
```
<empty symbol>
<start state name>
<first state>
<second state>
...
<last state>
```
where
```
<empty symbol> - a symbol which is considered by simulator as 'empty' (whitespaces don't work yet)
<start state name> - the state that is called in the beginning of processing the tape

<nth state> - the tuple in format (%name,%symbol_in,%symbol_out,%next_state,%direction):
%name - the string which is used to call this state
%symbol_in - input symbol read from the tape
%symbol_out - output symbol written to the tape
%next_state - the name of state that should be called after this state
%direction - the first letter of direction in which the tape should be shifted (Left or Right)
```

The tape should be stored as text file with .tape extension (but don't has to).
Its format is plain simple - it's just two lines:
```
<tape>
<head position>
```
where
```
<tape> - the string containing symbols which are stored on the tape
<head position> - the index of symbol which is set as start point in the program
```

The program launching:
```
$ python main.py <state-file> <tape-file>
```
# Example

As example we will use the program flipping all the bits in `?`-terminated binary number:\
`invert.stt`
```
?
start
(start,0,0,start,L)
(start,1,1,start,L)
(start,?,?,invert,R)
(invert,0,1,invert,R)
(invert,1,0,invert,R)
```
We can see two states: `start` and `invert`.\
The first one finds the `?` symbol and goes to the second state.\
The second one flips each bit from first one after the `?` symbol until it reaches the second `?`.\
We can see there is no `invert` state with `?` input what causes the simulator to stop.
\
`example.tape`
```
1101011?1010
3
```
After running we can see the result in the screen:
```
$ python main.py programs/invert.stt tapes/example.tape
Null character: ?
Head: 3
Available states:
start -> {'0': {'out': '0', 'next': 'start', 'direction': 'L'}, '1': {'out': '1', 'next': 'start', 'direction': 'L'}, '?': {'out': '?', 'next': 'invert', 'direction': 'R'}}
invert -> {'0': {'out': '1', 'next': 'invert', 'direction': 'R'}, '1': {'out': '0', 'next': 'invert', 'direction': 'R'}}
Current state: start
| ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 | ? | 1 | 0 | 1 |
                              ^                              
Current state: start
| ? | ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 | ? | 1 | 0 |
                              ^                              
Current state: start
| ? | ? | ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 | ? | 1 |
                              ^                              
Current state: start
| ? | ? | ? | ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 | ? |
                              ^                              
Current state: start
| ? | ? | ? | ? | ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
                              ^                              
Current state: invert
| ? | ? | ? | ? | ? | ? | ? | 1 | 1 | 0 | 1 | 0 | 1 | 1 | ? |
                              ^                              
Current state: invert
| ? | ? | ? | ? | ? | ? | 0 | 1 | 0 | 1 | 0 | 1 | 1 | ? | 1 |
                              ^                              
Current state: invert
| ? | ? | ? | ? | ? | 0 | 0 | 0 | 1 | 0 | 1 | 1 | ? | 1 | 0 |
                              ^                              
Current state: invert
| ? | ? | ? | ? | 0 | 0 | 1 | 1 | 0 | 1 | 1 | ? | 1 | 0 | 1 |
                              ^                              
Current state: invert
| ? | ? | ? | 0 | 0 | 1 | 0 | 0 | 1 | 1 | ? | 1 | 0 | 1 | 0 |
                              ^                              
Current state: invert
| ? | ? | 0 | 0 | 1 | 0 | 1 | 1 | 1 | ? | 1 | 0 | 1 | 0 | ? |
                              ^                              
Current state: invert
| ? | 0 | 0 | 1 | 0 | 1 | 0 | 1 | ? | 1 | 0 | 1 | 0 | ? | ? |
                              ^                              
Current state: invert
| 0 | 0 | 1 | 0 | 1 | 0 | 0 | ? | 1 | 0 | 1 | 0 | ? | ? | ? |
                              ^                              
Execution ended in 13 ticks
New tape saved into file tapes/example.tape.new
```
as well as in file\
`example.tape.new`
```
?0010100?1010
8
```
