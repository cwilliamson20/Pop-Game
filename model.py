import random


class Model:
    """
    The model portion of the MVC for the Pop game.

    Represents the screen as a unit square in order to adapt to different screen sizes
    The origin is in the top left corner
    """

    def __init__(self, screen_height: int, screen_width: int, num_targets: int, num_projectiles: int = None, ):
        """
        The constructor method for the model class
        :param num_targets: the number of targets to create
        :param num_projectiles: the maximum number of targets given to the user to fire
        """
        # makes a list of tuples for the random target positions
        self.__target_list = []

        self.__screen_height = screen_height
        self.__screen_width = screen_width

        #
        # all points are formatted (y, x) to work better with curses
        # lessened the range slightly because there was an issue where every few runs a target would spawn out of bounds
        for x in range(num_targets):
            self.__target_list.append((random.randint(3, screen_height-3), random.randint(3, screen_width-3)))

        # sets the launcher position to [y = 0.5 height, x = 0]
        self.__launcher_pos = [int(0.5 * screen_height), 0]

        # initializes the projectile position dictionary to later update when projectiles are fired
        self.__projectiles_dict = {}
        self.__num_projectiles = num_projectiles
        self.__num_projectiles_remaining = num_projectiles
        self.__num_projectiles_hit = 0

    def get_num_remaining_projectiles(self) -> int:
        """
        Returns the number of projectiles remaining
        """
        return self.__num_projectiles_remaining

    def get_target_list(self) -> list:
        """
        returns the targets_list instance variable
        """
        return self.__target_list

    def get_launcher_pos(self) -> list:
        """
        returns the launcher_pos instance variable
        :return: self.__launcher_pos: a list with two items, [y-coord, x-coord]
        """
        return self.__launcher_pos

    def handle_user_input(self, input_str: str) -> None:
        """
        Takes the user input string from the controller and decides what to do based on that
        :param input_str: a string, the input from the user (either shoot, up, or down)
        """
        if input_str == "up" or input_str == "down":
            self.move_launcher(input_str)
        elif input_str == "shoot":
            if self.__num_projectiles_remaining > 0:
                self.add_projectile(self.__launcher_pos[0])

    def move_launcher(self, direction: str):
        """
        alters the launcher's coordinates by 1 in the vertical direction based on direction
        :param direction: the direction to move the launcher
        :return: None
        """
        if direction == "up":
            # make sure it doesn't go out of bounds or onto the status indicator
            if not self.__launcher_pos[0] < 2:
                self.__launcher_pos[0] -= 1
        elif direction == "down":
            # make sure it doesn't go out of bounds
            if not self.__launcher_pos[0] > self.__screen_height - 3:
                self.__launcher_pos[0] += 1

    def add_projectile(self, y_pos) -> None:
        """
        Adds a projectile to the instance variable self.__projectiles_dict
        :return: None
        """
        self.__num_projectiles_remaining -= 1
        # entries are formatted as key = [0 to num projectiles] = [y coord, x coord]
        self.__projectiles_dict[self.__num_projectiles - self.__num_projectiles_remaining] = [y_pos, 0]

    def get_projectile_dict(self) -> dict:
        """
        returns the self.__projectile_dict instance variable
        """
        return self.__projectiles_dict

    def check_if_collided(self, projectile_coords: list, target_coords: list) -> bool:
        """
        Checks if a projectile has collided with the target
        Returns true if there is a collision, false otherwise
        :param projectile_coords: a list, the coordinates of the projectile
        :param target_coords: a list, the coordinates of the target
        :return: True or False
        """
        # y coordinates
        if projectile_coords[0] == target_coords[0]:

            # x coordinates
            if projectile_coords[1] == target_coords[1]:
                return True

        else:
            return False

    def move_projectiles(self) -> None:
        """
        Moves the projectiles along to the right
        """
        for key in list(self.__projectiles_dict.keys()):
            # if it is less than 0.01 away from 1 then it needs to be deleted
            if self.__projectiles_dict[key][1] >= self.__screen_width - 1:
                del self.__projectiles_dict[key]
            else:
                self.__projectiles_dict[key][1] += 1


    def delete_target(self, target_item) -> None:
        """
        Deletes a target from the target list when it is hit
        :param target_item: the item from the list
        :return: None
        """
        self.__target_list.remove(target_item)


































