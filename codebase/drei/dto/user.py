__author__ = 's.jahreiss'


""" User DTO.
"""
class User:

    """ Creates  a user.
    """
    def __init__(self, user_id, user_name, user_sound, user_mac):
        self.user_id = user_id
        self.user_name = user_name
        self.user_sound = user_sound
        self.user_mac = user_mac
