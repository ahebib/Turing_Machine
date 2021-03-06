#Programmer: Ammar Hebib
#utm.py
#Universal Turing Machine

from time import clock, time
#without this python exceeds recurrsion depth
import sys
sys.setrecursionlimit(100000)
#create tape object
from tape import Tape
tape = Tape()

def main():
    #menu chose which example to run by entering number
    print 'Choose test: '
    print '1. Non-Terminating TM '
    print '2. Subtraction '
    print '3. Busy Beaver 3 '
    print '4. Busy Beaver 4 '
    
    choice = input('Which test would you like? ')
    if(choice == 1):
        nonTerminating()
    elif(choice == 2):
        subtraction()
    elif(choice == 3):
        busyBeaver3()
    elif(choice == 4):
        busyBeaver4()

def nonTerminating():
    userInput = raw_input('Please input a combination of 1, 0, and b: ')

    tape.stringToArray(userInput)
    
    state = initState()
    position = start()
    cntTransitionFunction(tape, state, position)
    

def subtraction():
    firstInput = raw_input("First number: ")
    secondInput = raw_input("Second number: ")
    while(int(firstInput) <= int(secondInput)):
        print "Please input a first number that is larger than the second."
        firstInput = firstInput = raw_input("First number: ")
        secondInput = raw_input("Second number: ")

    #combines the two inputs with a 1 in between them
    tapeString = ''
    for i in range(int(firstInput)):
        tapeString = tapeString + '0'
 
    tapeString = tapeString + '1'

    for i in range(int(secondInput)):
        tapeString = tapeString + '0'
        
    tape.stringToArray(tapeString)
    
    state = initState()
    position = start()
    subtractionTransition(tape, state, position)

def busyBeaver3():
    userInput = raw_input('Please input a combination of 1, 0, and b: ')

    tape.stringToArray(userInput)
    
    state = initState()
    position = start()

    busyBeaver3Transition(tape, state, position)
    

def busyBeaver4():
    userInput = raw_input('Please input a combination of 1, 0, and b: ')

    tape.stringToArray(userInput)
    
    state = initState()
    position = start()

    busyBeaver4Transition(tape, state, position)

def initState():
    #initiates state
    state = 'q0'

    return state

def start():
    #select the start location on tape
    position = 0

    return position

def halt(tape, position, state):
    #stops the program
    print 'Final Result: ' + tape.arrayToString()
    print 'Runtime: ' + str(time()) + ' ms'

def moveL(position, tape):
    #move position 1 to the left
    #check to see if index exists
    if(position == 0):
        tape.extendLeft()
    else:
        position = position - 1
    
    return position, tape

def moveR(position, tape):
    #move position 1 to the right
    #check to see if index exists
    if(position == tape.getTapeLength()-1):
        tape.extendRight()
    position = position + 1

    return position, tape

def read(tape, position):
    #reads value at position on tape
    value = tape.getValue(position)

    return value

def write(tape, position, replacement):
    #replaces value at position with replacement
    tape.setValue(position, replacement)

    return tape

def cntTransitionFunction(tape, state, position):
    #used a try statement because if exceeded recursion then an error occurs
    try:
    #Transition Function for counting
        value = read(tape, position)

        print tape.arrayToString()
        #q0 state
        if(value == '0' and state == 'q0'):
            position, tape = moveR(position, tape)
            #recursion
            cntTransitionFunction(tape, state, position)
        elif(value == '1' and state == 'q0'):
            position, tape = moveR(position, tape)
            cntTransitionFunction(tape, state, position)
        elif(value == 'b' and state == 'q0'):
            position, tape = moveL(position, tape)
            state = 'q1'
            #recursion with new state and positin
            cntTransitionFunction(tape, state, position)
        #q1 state
        elif(value == '0' and state == 'q1'):
            replacement = '1'
            tape = write(tape, position, replacement)
            position, tape = moveR(position, tape)
            state = 'q0'
            cntTransitionFunction(tape, state, position)
        elif(value == '1' and state == 'q1'):
            replacement = '0'
            tape = write(tape, position, replacement)
            position, tape = moveL(position, tape)
            cntTransitionFunction(tape, state, position)
        elif(value == 'b' and state == 'q1'):
            replacement = '1'
            tape = write(tape, position, replacement)
            position, tape = moveR(position, tape)
            state = 'q0'
            cntTransitionFunction(tape, state, position)
    except Exception, e:
        print 'Max object calling in Python'
        print 'Last possible count: ' + tape.arrayToString()
        
def subtractionTransition(tape, state, position):
    #changes state and determines what to do next for subtraction
    value = read(tape, position)

    print tape.arrayToString()
    
    #q0 state -----------------------------------------------
    if(value == '0' and state == 'q0'):
        replacement = 'b'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        #change state
        state = 'q1'
        #recall function with new state
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q0'):
        replacement = 'b'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        state = 'q5'
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q0'):
        halt(tape, position, state)
    #q1 state -----------------------------------------------
    elif(value == '0' and state == 'q1'):
        position, tape = moveR(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q1'):
        position, tape = moveR(position, tape)
        state = 'q2'
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q1'):
        halt(tape, position, state)
    #q2 state -----------------------------------------------
    elif(value == '0' and state == 'q2'):
        replacement = '1'
        tape = write(tape, position, replacement)
        position, tape = moveL(position, tape)
        state = 'q3'
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q2'):
        position, tape = moveR(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q2'):
        position, tape = moveL(position, tape)
        state = 'q4'
        subtractionTransition(tape, state, position)
        
    #q3 state -----------------------------------------------
    elif(value == '0' and state == 'q3'):
        position, tape = moveL(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q3'):
        position, tape = moveL(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q3'):
        position, tape = moveR(position, tape)
        state = 'q0'
        subtractionTransition(tape, state, position)
        
    #q4 state -----------------------------------------------
    elif(value == '0' and state == 'q4'):
        position, tape = moveL(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q4'):
        replacement = 'b'
        tape = write(tape, position, replacement)
        position, tape = moveL(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q4'):
        replacement = '0'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        state = 'q6'
        subtractionTransition(tape, state, position)
        
    #q5 state -----------------------------------------------
    elif(value == '0' and state == 'q5'):
        replacement = 'b'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == '1' and state == 'q5'):
        replacement = 'b'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        subtractionTransition(tape, state, position)
        
    elif(value == 'b' and state == 'q5'):
        position, tape = moveR(position, tape)
        state = 'q6'
        subtractionTransition(tape, state, position)
        
    #q6 state -----------------------------------------------
    elif(value == '0' and state == 'q6'):
        halt(tape, position, state)
    elif(value == '1' and state == 'q6'):
        halt(tape, position, state)
    elif(value == 'b' and state == 'q6'):
        halt(tape, position, state)

def busyBeaver3Transition(tape, state, position):
    #Transition Function for beaver 3
    value = read(tape, position)

    print tape.arrayToString()
    #state q0 checks if needs to write, where to move, and then recalls function
    if(value == '0' and state == 'q0'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q1'
        position, tape = moveR(position, tape)
        busyBeaver3Transition(tape, state, position)
    elif(value == '1' and state == 'q0'):
        halt(tape, position, state)
    elif(value == 'b' and state == 'q0'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q1'
        position, tape = moveR(position, tape)
        busyBeaver3Transition(tape, state, position)
    #state q1
    elif(value == '0' and state == 'q1'):
        position, tape = moveR(position, tape)
        state = 'q2'
        busyBeaver3Transition(tape, state, position)
    elif(value == '1' and state == 'q1'):
        position, tape = moveR(position, tape)
        busyBeaver3Transition(tape, state, position)
    elif(value == 'b' and state == 'q1'):
        replacement = '0'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        state = 'q2'
        busyBeaver3Transition(tape, state, position)
    #state q2
    elif(value == '0' and state == 'q2'):
        replacement = '1'
        tape = write(tape, position, replacement)
        position, tape = moveL(position, tape)
        busyBeaver3Transition(tape, state, position)
    elif(value == '1' and state == 'q2'):
        state = 'q0'
        position, tape = moveL(position, tape)
        busyBeaver3Transition(tape, state, position)
    elif(value == 'b' and state == 'q2'):
        replacement = '1'
        tape = write(tape, position, replacement)
        position, tape = moveL(position, tape)
        busyBeaver3Transition(tape, state, position)

def busyBeaver4Transition(tape, state, position):
    #Transition Function for beaver 4
    value = read(tape, position)

    print tape.arrayToString()
    
    #state q0 checks if needs to write, where to move, and then recalls function
    if(value == '0' and state == 'q0'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q1'
        position, tape = moveR(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == '1' and state == 'q0'):
        state = 'q1'
        position, tape = moveL(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == 'b' and state == 'q0'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q1'
        position, tape = moveR(position, tape)
        busyBeaver4Transition(tape, state, position)
    #state q1
    elif(value == '0' and state == 'q1'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q0'
        position, tape = moveL(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == '1' and state == 'q1'):
        replacement = '0'
        tape = write(tape, position, replacement)
        state = 'q2'
        position, tape = moveL(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == 'b' and state == 'q1'):
        replacement = '1'
        tape = write(tape, position, replacement)
        state = 'q0'
        position, tape = moveL(position, tape)
        busyBeaver4Transition(tape, state, position)
    #state q2
    elif(value == '0' and state == 'q2'):
        replacement = '1'
        tape = write(tape, position, replacement)
        halt(tape, position, state)
    elif(value == '1' and state == 'q2'):
        state = 'q3'
        position, tape = moveL(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == 'b' and state == 'q2'):
        replacement = '1'
        tape = write(tape, position, replacement)
        halt(tape, position, state)
    #state q3
    elif(value == '0' and state == 'q3'):
        replacement = '1'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == '1' and state == 'q3'):
        replacement = '0'
        tape = write(tape, position, replacement)
        state = 'q0'
        position, tape = moveR(position, tape)
        busyBeaver4Transition(tape, state, position)
    elif(value == 'b' and state == 'q3'):
        replacement = '1'
        tape = write(tape, position, replacement)
        position, tape = moveR(position, tape)
        busyBeaver4Transition(tape, state, position)
        
main()
