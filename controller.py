

class Controller:
    def __init__(self, view_obj: object, model_obj: object):
        """the constructor method for the Controller class
        :param: view: an object, the view to be used
        :param: model: an object, the model to be used
        """
        self.__view_obj = view_obj
        self.__model_obj = model_obj
        self.__projectile_list = []
        self.__screen_width = self.__view_obj.get_display_width()
        self.__screen_height = self.__view_obj.get_display_height()




    def game_loop(self):
        """
        The main loop to run the game
        :return: None
        """
        while True:
            # 1. Set status in the view
            num_proj = self.__model_obj.get_num_remaining_projectiles()
            self.__view_obj.set_status_message(str(num_proj) + " projectiles remaining")

            # 2. Update the view (print or redraw everything)
            self.__view_obj.update(self.__model_obj.get_target_list(), self.__model_obj.get_launcher_pos(), self.__model_obj.get_projectile_dict())

            # 3. handle user input
            self.handle_user_input()

            # 3.5 Move the projectiles
            self.__model_obj.move_projectiles()

            # 4. Check if things have collided
            for target in self.__model_obj.get_target_list():
                for projectile in self.__model_obj.get_projectile_dict().values():
                    # if there is a hit
                    if self.__model_obj.check_if_collided(projectile, target):
                        self.__model_obj.delete_target(target)

            # 5. Determine if the game is over
            # there are no targets left (win)
            if len(self.__model_obj.get_target_list()) == 0:
                self.__view_obj.end_game_screen(True)
                break

            # no projectiles left but there are targets left (loss)
            elif num_proj == 0 and len(self.__model_obj.get_projectile_dict()) == 0:
                self.__view_obj.end_game_screen(False)
                break

    def handle_user_input(self):
        """
        Takes the user input from the view and passes the correct action name to the model
        """
        # user_input will be a string, either "up", "down", or "shoot"
        user_input = self.__view_obj.get_user_input()
        self.__model_obj.handle_user_input(user_input)


































