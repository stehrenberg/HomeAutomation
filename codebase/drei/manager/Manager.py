import multiprocessing
import numpy as np

from lib.database.database import MockDatabase

__author__ = 'm.hornung'


class Manager(multiprocessing.Process):
    def __init__(self, crawler_queue, webserver_queue):
        multiprocessing.Process.__init__(self)
        self.crawler_queue = crawler_queue
        self.webserver_queue = webserver_queue

        # Create the database connection
        self.db = MockDatabase()

    def run(self):
        print("Manager: Running")

        users = self.db.retrieve_users()
        current_addresses = np.array(self.crawler_queue.get())

        # Initialise users
        for add_address in current_addresses:
            for user in users:
                if user.mac == add_address:
                    user_sound = user.sound
                    user_light = user.light
                    print("user " + add_address + " added")
                    print("sound " + user_sound + " played")
                    print("light " + user_light + " on")
                    #TODO: lichter an, sound abspielen
                    break

        self.webserver_queue.put(current_addresses)

        while True:
            new_addresses = np.array(self.crawler_queue.get())

            # Any changes?
            if not np.array_equal(current_addresses, new_addresses):
                # Update users
                users = self.db.retrieve_users()

                # Which addresses are new?
                add_addresses = np.setdiff1d(new_addresses, current_addresses)
                # Which addresses are gone?
                del_addresses = np.setdiff1d(current_addresses, new_addresses)

                # Delete gone addresses and turn off corresponding lights
                del_indexes = np.searchsorted(current_addresses, del_addresses)
                current_addresses = np.delete(current_addresses, del_indexes)
                for del_address in del_addresses:
                    for user in users:
                        if user.mac == del_address:
                            user_light = user.light
                            print("user " + del_address + " deleted")
                            print("light " + user_light + " off")
                            #TODO: lichter aus
                            break

                # Add new addresses, turn on corresponding lights and play sound if in db
                current_addresses = np.append(current_addresses, add_addresses)
                for add_address in add_addresses:
                    for user in users:
                        if user.mac == add_address:
                            user_sound = user.sound
                            user_light = user.light
                            print("user " + add_address + " added")
                            print("sound " + user_sound + " played")
                            print("light " + user_light + " on")
                            #TODO: lichter an, sound abspielen
                            break

            self.webserver_queue.put(current_addresses)

            print("Manager: Retrieved addresses")