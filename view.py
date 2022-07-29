import curses


class ViewBalloonPop:
    def __init__(self, screen=None):
        """the constructor method for the View class"""
        self.__status_message = ""

        self.screen = screen
        self.screen.nodelay(True)

        # the symbols each thing in game appears as
        self.__target_symbol = "O"
        self.__launcher_symbol = ":D"
        self.__projectile_symbol = "->"

        # Clear the screen
        curses.cbreak()
        curses.curs_set(0)  # Make cursor invisible

    def get_display_height(self) -> int:
        """returns the display height in pixels"""
        num_rows, num_cols = self.screen.getmaxyx()
        return num_rows

    def get_display_width(self) -> int:
        """returns the display width in pixels"""
        num_rows, num_cols = self.screen.getmaxyx()
        return num_cols

    def set_status_message(self, input_str: str) -> None:
        """updates the status message that prints at the top (x projectiles remaining)"""
        self.__status_message = input_str

    def update(self, target_list: list, launcher_pos: list, projectile_dict: dict) -> None:
        """
        Prints/displays all the new stuff (more like a rewrite rather than an update)
        :param target_list: the list of target coordinates
        :param launcher_pos: the current coordinates of the launcher
        :param projectile_dict: the dictionary of coordinates for the projectiles
        :return: none
        """
        # draw the status message in the upper left corner
        self.screen.addstr(0, 0, self.__status_message)

        # draw the targets
        # scale up and display the targets on screen

        for coord_pair in target_list:
            self.screen.addstr(coord_pair[0], coord_pair[1], self.__target_symbol)
        # draw the launcher
        self.screen.addstr(launcher_pos[0], launcher_pos[1], self.__launcher_symbol)

        # draw projectiles
        for projectile in projectile_dict.values():
            self.screen.addstr(projectile[0], projectile[1], self.__projectile_symbol)

        self.screen.refresh()     # refresh the screen (draw everything)
        curses.napms(100)    # wait 100 milliseconds
        self.screen.clear()       # clear the screen

        # # debugging outputs
        self.screen.addstr(0, 50, f"launcher: ({launcher_pos[0]}, {launcher_pos[1]})")
        self.screen.addstr(0, 70, str(target_list))
        self.screen.addstr(0, 150, str(projectile_dict))

    def get_user_input(self):
        """
        Takes in user key inputs on the w, s, and space keys
        :return: "up", "down", "shoot", or None depending on the input
        """
        # Get the user's input (up or down arrow)
        key = self.screen.getch()

        # w is up
        # s is down
        # space is shoot
        keystroke_dict = {119: 'up', 115: 'down', 32: 'shoot'}
        if key in keystroke_dict:
            return keystroke_dict[key]
        else:
            pass

    def end_game_screen(self, win_state: bool) -> None:
        """
        Displays the end game screen for 3 seconds
        ":) You win! :)" if win, ":( You lose. :(" if lose
        :param win_state: A boolean, true if user won, false if they lost
        :return: None
        """
        num_rows, num_cols = self.screen.getmaxyx()
        curses.cbreak()
        curses.curs_set(0)
        # win
        if win_state:
            self.screen.addstr(int(num_rows * .5), int(num_cols * .5), ":) You win! :)")
            self.screen.refresh()
            curses.napms(3000)  # pause for 3 seconds

        # lose
        else:
            self.screen.addstr(int(num_rows * .5), int(num_cols * .5), ":( You lose. :(")
            self.screen.refresh()

            curses.napms(3000)  # pause for 3 seconds
