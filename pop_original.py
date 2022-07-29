"""
File: pop_original.py
Author: Boyana Norris

Shoot arrows at balloons! A (mostly) peaceful game.
This is best run on your machine, in PyCharm or VSCode, or on a terminal:
   python pop_original.py
(The CONSOLE and SHELL in Coding Rooms don't work well with curses.)
"""
import curses
from curses import wrapper
import random


def draw_person(screen, y: int, x: int):
    """Draw a "person" centered at the y, x coordinates"""
    screen.addstr(y, x, ':D')

def draw_arrow(screen, y: int, x: int): 
    """Draw an arrow the y, x coordinates."""
    screen.addstr(y, x, '->')

def main(screen):
    """The main program, which is run through the curses wrapper."""

    # Clear the screen
    curses.cbreak()
    curses.curs_set(0)    # Make cursor invisible

    #screen.keypad(True)
    screen.clear()
    screen.nodelay(True)  # allows input while arrow moving

    dimensions = screen.getmaxyx()   # (height, width) of screen

    # Generate 5 random balloon positions (min 2 points from edges)
    balloons = [(random.randint(1,dimensions[0]-2), 
                random.randint(10,dimensions[1]-2)) for i in range(5)]

    y = dimensions[0]//2   # halfway down the screen 

    # Store in-flight arrows in dictionary with keys being an int counter
    # and values as (y, x) positions
    arrows = {}
    arrow_id = 0
    total_arrows = 6 # number of arrows to shoot
    
    # Game loop
    while True:
        # Draw the (surviving) balloons
        for y_balloon, x_balloon in balloons:
            screen.addstr(y_balloon, x_balloon, '0')
            
        # Get the user's input (up or down arrow)
        key = screen.getch()
        if key == curses.KEY_UP:  # up arrow
            y = max(2, y - 1) # only go up to the second line of the screen
        elif key == curses.KEY_DOWN: # down arrow
            y = min(dimensions[0]-1, y+1) # only go down to the last line of the screen
        elif key == 32: # 32 is the ASCII code for the spacebar
            # "Shoot" an arrow (add it to the dictionary)
            if arrow_id < total_arrows:
                arrows[arrow_id] = (y, 3)
                arrow_id += 1

        # Show arrows left in upper left corner (we reseve the first line for status)
        screen.addstr(0, 0, 'Arrows left: ' + str(total_arrows - arrow_id))
        
        # Draw the person
        draw_person(screen, y, 2)
        
        # Draw all arrows currently in flight
        for arrow in arrows.values():
            draw_arrow(screen, arrow[0], arrow[1])

        screen.refresh()     # refresh the screen (draw everything)
        curses.napms(100)    # wait 100 milliseconds
        screen.clear()       # clear the screen

        # Check if balloon is hit
        for y_arrow, x_arrow in arrows.values():
            if (y_arrow, x_arrow) in balloons:
                balloons.remove((y_arrow, x_arrow))   # Pop the balloon
        
        # Check if game over (no balloons left!)
        if len(balloons) == 0:
            screen.addstr(dimensions[0] // 2, dimensions[1]//2 - 5, '😃 You win! 😃')
            screen.refresh()
            curses.napms(3000)   # pause for 3 seconds
            break
        
        # Check if game over (no arrows!)
        if len(arrows) == 0 and arrow_id >= total_arrows:
            screen.addstr(dimensions[0]//2, dimensions[1]//2 - 6, '😞 You lose! 😞')
            screen.refresh()
            curses.napms(3000)   # pause for 3 seconds
            break

        # Move the arrows forward
        for id in list(arrows):
            pos = arrows[id]
            if pos[1] >= dimensions[1] - 3: 
                # Arrow reached right end of screen
                del arrows[id] 
            else:
                arrows[id] = (pos[0], pos[1]+1)

if __name__ == "__main__":
    # This will call main and pass it the curses window as the screen argument
    wrapper(main)
