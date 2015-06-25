__author__ = 's.ehrenberg'

import unittest
from dto.user import User
from lib.database.SQLiteWrapper import SQLiteWrapper
from lib.database import InitTables, DropTables

class DBWrapperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DropTables.main()
        InitTables.main()
        cls.db_wrapper = SQLiteWrapper()
        cls.testuser = User(
            user_mac='00:80:41:ae:fd:7f',
            user_name='Steff',
            user_sound='/sounds/bla',
            user_light_id='None',
            user_light_color='#ffffff')
        cls.double_mac_testuser = User(
            user_mac='00:80:41:ae:fd:7f',
            user_name='Hugo',
            user_sound='/sounds/blubb',
            user_light_id='None',
            user_light_color='#ffffff')
        cls.double_sound_testuser = User(
            user_mac='00:80:41:00:fd:7f',
            user_name='Kevin',
            user_sound='/sounds/bla',
            user_light_id='None',
            user_light_color='#ffffff')

    def tearDown(self):
        """
        Ensuring that db is clean after every test
        """
        users = self.db_wrapper.retrieve_users()
        for user in users:
            self.db_wrapper.delete_user(user.mac)

    def test_simple_user_adding(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))

    def test_faulty_user_adding(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertFalse(self.db_wrapper.add_user(self.double_mac_testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))

    def test_list_sounds(self):
        sound_list = self.db_wrapper.list_sounds()
        self.assertTrue(sound_list.__contains__('bla'))

    def test_get_user(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))
        user = self.db_wrapper.get_user('00:80:41:ae:fd:7f')
        self.assertEqual(self.testuser.mac, user.mac)
        self.assertEqual(self.testuser.name, user.name)
        self.assertEqual(self.testuser.sound, user.sound)
        self.assertEqual(self.testuser.light_color, user.light_color)
        # light_id kann nicht verglichen werden, weil testuser-object noch keine id hat

    def test_get_nonexistent_user(self):
        self.assertTrue(self.db_wrapper.get_user(self.testuser) == None)

    def test_retrieve_users(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))
        users = self.db_wrapper.retrieve_users()
        mac_addresses = []
        for user in users:
            mac_addresses.append(user.mac)
        self.assertTrue(mac_addresses.__contains__(self.testuser.mac))
        self.assertTrue(mac_addresses.__contains__(self.double_sound_testuser.mac))

    def test_retrieve_users_from_empty_db(self):
        users = self.db_wrapper.retrieve_users()
        self.assertTrue(len(users) == 0)
        print("users from empty db: ", users)

    def test_update_user(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))
        updated_user = User(
            user_mac='00:80:41:ae:fd:7f',
            user_name='Steff',
            user_sound='/sounds/bla',
            user_light_id='None',
            user_light_color='#ff00ff')
        self.assertTrue(self.db_wrapper.update_user(updated_user.mac, updated_user))

    def test_update_user_with_existing_sound(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))
        updated_sound_user = User(
            user_mac='00:80:41:ae:fd:7f',
            user_name='Steff',
            user_sound='/sounds/blubb',
            user_light_id='None',
            user_light_color='#ff00ff')
        self.assertTrue(self.db_wrapper.update_user(updated_sound_user.mac, updated_sound_user))
        user = self.db_wrapper.get_user('00:80:41:ae:fd:7f')
        self.assertTrue(self.db_wrapper.list_sounds().__contains__('bla'))
        self.assertTrue(self.db_wrapper.list_sounds().__contains__('blubb'))

    def test_delete_user(self):
        self.assertTrue(self.db_wrapper.add_user(self.testuser))
        self.assertTrue(self.db_wrapper.add_user(self.double_sound_testuser))
        kevins_mac = '00:80:41:00:fd:7f'
        self.assertTrue(None != self.db_wrapper.get_user(kevins_mac))
        self.db_wrapper.delete_user(kevins_mac)
        self.assertEquals(None, self.db_wrapper.get_user(kevins_mac))
        print('Users nach delete: ', self.db_wrapper.retrieve_users())

    def test_add_pathless_soundfile(self):
        dieter = User(
            user_mac='00:80:44:ae:fd:7f',
            user_name='Dieter',
            user_sound='bla.wav',
            user_light_id='None',
            user_light_color='#ffffff')
        self.db_wrapper.add_user(dieter)
        users = self.db_wrapper.retrieve_users()
        print("users: ", users)

if __name__ == '__main__':
    unittest.main()
