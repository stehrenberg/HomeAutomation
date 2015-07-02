import multiprocessing
import numpy as np
from lib.led.led import LED

from lib.logger.Logger import Logger
from lib.database.SQLiteWrapper import SQLiteWrapper
from lib.periphery.Periphery import Periphery

__author__ = 'm.hornung'


class Manager(multiprocessing.Process):
    def __init__(self, crawler_queue, webserver_queue):
        multiprocessing.Process.__init__(self)
        # Create queue for crawler
        self.crawler_queue = crawler_queue
        # Create queue for webserver
        self.webserver_queue = webserver_queue
        # Create controller for status LED
        self.led = LED(LED.MANAGER)
        # Create logger
        self.logger = Logger()

    def run(self):
        self.logger.log(Logger.INFO, 'Running')
        print("Manager running")
        self.led.on()

        # Control for sound and light
        self.per = Periphery()

        # Create the database connection
        self.db = SQLiteWrapper()

        current_users = np.array([])

        # Boolean if the list was altered
        altered = False

        while True:
            # Update users
            users = self.db.retrieve_users()

            # Receive new changes from crawler
            changes = np.array(self.crawler_queue.get())

            old_users = current_users

            # Iterate over changes
            for i in range(0, changes.size - 1):
                # New user connected
                if changes[0] == "1":
                    for user in users:
                        if user.mac.lower() == changes[1].lower():
                            # Signalise changes in user list for webserver
                            altered = True
                            # Add new user to user list
                            old_users = np.append(current_users, changes[1])
                            # Remove duplicates
                            current_users = np.unique(old_users)
                            # Get light and sound information for user
                            light_id = user.light_id
                            light_color = user.light_color
                            sound = user.sound
                            self.logger.log(Logger.INFO, "user " + changes[1] + " added")
                            # Turn on users light and play users sound
                            self.per.light_on(int(light_id), light_color)
                            self.per.play_sound(sound)
                            break
                # User disconnected
                elif changes[0] == "0":
                    for user in users:
                        if user.mac.lower() == changes[1].lower():
                            # Catch deletion of just added users
                            try:
                                del_index = np.where(current_users == changes[1])[0][0]
                            except IndexError:
                                break
                            # Signalise changes in user list for webserver
                            altered = True
                            # Delete user from user list
                            current_users = np.delete(current_users, del_index)
                            # Get light information for user
                            light_id = user.light_id
                            self.logger.log(Logger.INFO, "user " + changes[1] + " deleted")
                            # Turn off users light
                            self.per.light_off(int(light_id))
                # Change in status light
                elif changes[0] == "2":
                    # Set new colour of status light
                    self.per.set_status_light(changes[1])

            # User list was altered
            if altered:
                altered = False
                # Send new user list to webserver
                self.webserver_queue.put(current_users.tolist())

        # Turn off status LED
        self.led.off()
