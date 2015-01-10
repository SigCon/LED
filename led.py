import time
import random
from datetime import datetime
import RPi.GPIO as GPIO

# set a score for each player
scores = [0, 0]
listoftimes = []
names = []

# Say who won
def wingame(player):
    """The function wingame accepts the player who won as the only parameter"""
    print names[player] + ' won!'
    scores[player] += 1

# Print date and time
def printdate(repetition):
    '''The function printdate accepts the number
    of repetitions for the '---' string as the only parameter'''
    now = datetime.now()
    print '%s-%s-%s %s:%s:%s' % (now.day, now.month, now.year, now.hour, now.minute, now.second)
    output = '---' * repetition
    return output

def printscore():
    print ""
    print ''
    print "Scores:"
    print "  " + names[0] + ": " + str(scores[0])
    print "  " + names[1] + ": " + str(scores[1])
    print listoftimes

print printdate(10)

# Make sure the GPIO pins are ready
GPIO.setmode(GPIO.BOARD)

# Choose which GPIO pins to use
led = 23
rightButton = 3
leftButton = 5

# Set the buttons as input and the LED as an output
GPIO.setup(led, GPIO.OUT)
GPIO.setup(rightButton, GPIO.IN)
GPIO.setup(leftButton, GPIO.IN)

# Find out the names of the players
leftName = raw_input("What is the left player's name? ")
rightName = raw_input("What is the right player's name? ")
games = int(raw_input("How many games do you want to play? "))

# Put the names in a list
names = [leftName, rightName]


# Play all the games
for game in range(0, games):
    # Turn the LED on
    GPIO.output(led, 1)

    # Generate a random time the led will be on
    randnumber = int(random.uniform(1, 10))
    # randnumber = random.uniform(1, 10)
    listoftimes.append(randnumber)
    print randnumber
    print ''

    # Wait for a random length of time, between 1 and 10 seconds
    time.sleep(randnumber)

    '''One odd thing is that the buttons are on if they are not pressed and off when they are. This is why
    the code says 'Left button pressed' when it finds that 'leftButton' is 'False'.
    '''

    # Check to see if a button is pressed
    # If so, the other player wins
    if GPIO.input(leftButton) == False:
        print names[0] + " cheated!!!"
        wingame(1)
    elif GPIO.input(rightButton) == False:
        print names[1] + " cheated!!!"
        wingame(0)
    else:
        # Turn the led off
        GPIO.output(led, 0)
        # Wait until a button has been pressed
        while GPIO.input(leftButton) and GPIO.input(rightButton):
            pass # Do nothing!
        # See if the left button has been pressed
        if GPIO.input(leftButton) == False:
            wingame(0)
        # See if the right button has been pressed
        if GPIO.input(rightButton) == False:
            wingame(1)

printscore()

# Cleanup
GPIO.cleanup()