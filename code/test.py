from tkinter import *
from tkinter.ttk import *
import time
import threading

class Interface:
    def __init__(self, master):
        self.master = master
        self.browse_button= Button (master, text="Browse", command=self.browser)
        self.browse_button.pack()
        # Create an indeterminate progressbar here but don't pack it.
        # Change the maximum to change speed. Smaller == faster.
        self.progressbar = Progressbar(mode="indeterminate", maximum=20)

    def browser (self):
        # set up thread to do work in
        self.thread = threading.Thread(target=self.read_file, args=("filename",))
        # disable the button
        self.browse_button.config(state="disabled")
        # show the progress bar
        self.progressbar.pack()
        # change the cursor
        self.master.config(cursor="wait")
        # force Tk to update
        self.master.update()

        # start the thread and progress bar
        self.thread.start()
        self.progressbar.start()
        # check in 50 milliseconds if the thread has finished
        self.master.after(50, self.check_completed)

    def check_completed(self):
        if self.thread.is_alive():
            # if the thread is still alive check again in 50 milliseconds
            self.master.after(50, self.check_completed)
        else:
            # if thread has finished stop and reset everything
            self.progressbar.stop()
            self.progressbar.pack_forget()
            self.browse_button.config(state="enabled")
            self.master.config(cursor="")
            self.master.update()

            # Call method to do rest of work, like displaying the info.
            self.display_file()

    def read_file (self, filename):
        time.sleep(7)  # actually do the read here

    def display_file(self):
        pass  # actually display the info here

window = Tk()
starter = Interface(window)
window.mainloop()