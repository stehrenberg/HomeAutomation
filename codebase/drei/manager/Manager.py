import multiprocessing
import numpy as np
from lib.led.led import LED
import logging


from lib.database.SQLiteWrapper import SQLiteWrapper
from lib.periphery.Periphery import Periphery

__author__ = 'm.hornung'


class Manager(multiprocessing.Process):
    def __init__(self, crawler_queue, webserver_queue):
        multiprocessing.Process.__init__(self)
        self.crawler_queue = crawler_queue
        self.webserver_queue = webserver_queue
        self.led = LED(LED.MANAGER)
        logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

    def run(self):
        logging.info('Manager: Running')
        print("Manager: Running")
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

            changes = np.array(self.crawler_queue.get())

            old_users = current_users

            for i in range(0, changes.size - 1):
                if changes[0] == "1":
                    for user in users:
                        if user.mac.lower() == changes[1].lower():
                            altered = True
                            current_users = np.append(current_users, changes[1])
                            light_id = user.light_id
                            light_color = user.light_color
                            sound = user.sound
                            logging.info("user " + changes[1] + " added")
                            print("user " + changes[1] + " added")
                            self.per.light_on(int(light_id), light_color)
                            self.per.play_sound(sound)
                            break
                else:
                    for user in users:
                        if user.mac.lower() == changes[1].lower():
                            # Catch deletion of just added users
                            try:
                                del_index = np.where(current_users == changes[1])[0][0]
                            except IndexError:
                                break
                            altered = True
                            current_users = np.delete(current_users, del_index)
                            light_id = user.light_id
                            logging.info("user " + changes[1] + " deleted")
                            print("user " + changes[1] + " deleted")
                            self.per.light_off(int(light_id))

            if altered:
                altered = False
                self.webserver_queue.put(current_users.tolist())

        self.led.off()
