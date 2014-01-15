"""
Cronometro usado en el programa de colisiones.

Created by: Jassael Ruiz
Version: 1.0
"""

import simplegui as sg

class stopwatch:
    # define member variables
    A = 0
    B = 0
    C = 0
    tenths_seconds = 0
    
    def timer_handler(self):
        # define event handler for timer with 0.1 sec interval
        # increments tenths_seconds 0.1 per second
        self.tenths_seconds += 1

    def formato(self, t):
        # define helper function format that converts time
        # in tenths of seconds into formatted string A:BC.tenths_seconds
        # member variales A, B, C
        # local varible tenths_seconds
        tenths_seconds = 0
        tenths_seconds = t % 10
        self.C = t // 10
        if(self.C >= 60):
            self.A = self.C // 60
            self.C = self.C % 60
        if(self.C < 10):
            return str(self.A)+":"+str(self.B)+str(self.C)+"."+str(tenths_seconds)
        else:
            return str(self.A)+":"+str(self.C)+"."+str(tenths_seconds)
    
    def start_handler(self):
        # start the timer
        self.timer.start()

    def stop_handler(self):
        # stop the timer
        self.timer.stop()

    def reset_handler(self):
        # reset the timer to 0
        # member variables A, B, C, tenths_seconds
        self.A = 0
        self.B = 0
        self.C = 0
        self.tenths_seconds = 0
   
    def get_time(self):
        # return the formatted time A:BC.tenths_seconds
        return self.formato(self.tenths_seconds)

    def crear_timer(self):
        # create new timer
        self.timer = sg.create_timer(100, self.timer_handler)
