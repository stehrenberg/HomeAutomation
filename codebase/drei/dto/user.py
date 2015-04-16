__author__ = 's.jahreiss'


class User:
    """ User DTO.
    """

    def __init__(self, user_mac, user_name, user_sound, user_light_id, user_light_color):
        self.name = user_name
        self.sound = user_sound
        self.mac = user_mac
        self.light_id = user_light_id
        self.light_color = user_light_color
