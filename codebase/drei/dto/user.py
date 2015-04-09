__author__ = 's.jahreiss'


""" User DTO.
"""
class User:

    """ Creates  a user.
    """
    def __init__(self, user_mac, user_name, user_sound, user_light):
        self.name = user_name
        self.sound = user_sound
        self.mac = user_mac
        self.light = user_light
