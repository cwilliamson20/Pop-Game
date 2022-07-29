"""Main driver for a configuration with arrows shooting at balloon targets."""
import curses

from view import ViewBalloonPop
from model import Model
from controller import Controller


def main():
    # NOTE: this program uses the W and S keys (from the WASD layout) as replacements for the up and down arrows
    screen = curses.initscr()
    view_obj = ViewBalloonPop(screen)
    dimensions = screen.getmaxyx()
    model_obj = Model(dimensions[0], dimensions[1], 5, 6)    # model with 5 targets and 6 projectiles
    controller = Controller(view_obj, model_obj)
    controller.game_loop()


if __name__ == "__main__":
    main()
