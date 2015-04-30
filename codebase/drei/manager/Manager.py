import multiprocessing
import numpy as np

from lib.database.MockDatabase import MockDatabase
from lib.periphery.Periphery import Periphery

__author__ = 'm.hornung'


class Manager(multiprocessing.Process):
    def __init__(self, crawler_queue, webserver_queue):
        multiprocessing.Process.__init__(self)
        self.crawler_queue = crawler_queue
        self.webserver_queue = webserver_queue

        # Control for sound and light
        self.per = Periphery()

        # Create the database connection
        self.db = MockDatabase()

    def run(self):
        print("Manager: Running")

        current_users = np.array([])

        # Boolean if the list was altered
        altered = False

        while True:
            # Update users
            users = self.db.retrieve_users()

            changes = np.array(self.crawler_queue.get())

            old_users = current_users

            for i in range(0, changes.size - 1):
                if changes[0] == "1":
                    for user in users:
                        if user.mac == changes[1]:
                            altered = True
                            current_users = np.append(current_users, user)
                            light_id = user.light_id
                            light_color = user.light_color
                            sound = user.sound
                            print("user " + changes[1] + " added")
                            self.per.light_on(int(light_id), light_color)
                            self.per.play_sound(sound)
                            break
                else:
                    for user in users:
                        if user.mac == changes[1]:
                            # Catch deletion of just added users
                            try:
                                del_index = np.where(current_users == user)[0][0]
                            except IndexError:
                                break
                            altered = True
                            current_users = np.delete(current_users, del_index)
                            light_id = user.light_id
                            print("user " + changes[1] + " deleted")
                            self.per.light_off(int(light_id))

            if altered:
                altered = False
                self.webserver_queue.put(current_users.tolist())