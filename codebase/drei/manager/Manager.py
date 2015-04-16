import multiprocessing
import numpy as np

from lib.database.Database import MockDatabase
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

        current_addresses = np.array([])

        while True:
            # Update users
            users = self.db.retrieve_users()

            changes = np.array(self.crawler_queue.get())

            for i in range(0, changes.size-1):
                if changes[0] == "1":
                    current_addresses = np.append(current_addresses, changes[1])
                    for user in users:
                        if user.mac == changes[1]:
                            light_id = user.light_id
                            light_color = user.light_color
                            sound = user.sound
                            print("user " + changes[1] + " added")
                            self.per.light_on(light_id)
                            self.per.play_sound(sound)
                            break
                else:
                    del_index = np.where(current_addresses == changes[1])[0][0]
                    current_addresses = np.delete(current_addresses, del_index)
                    for user in users:
                        if user.mac == changes[1]:
                            light_id = user.light_id
                            print("user " + changes[1] + " deleted")
                            self.per.light_off(light_id)

            self.webserver_queue.put(current_addresses)