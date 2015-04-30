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

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.name, self.sound, self.mac, self.light_id, self.light_color)

    def __repr__(self):
        return self.__str__()