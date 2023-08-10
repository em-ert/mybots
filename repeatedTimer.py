# Copyright (c) 2021-2025 Tackhyun Jung and Jongsung Yoon.
# This Library is completely free of charge.
__version__ = '0.0.1'

# Slighly modified by Emily Ertle

import time
from time import sleep
from threading import Timer
from typing import Callable


class REPEATED_TIMER(object):
    def __init__(self: object, interval: int, duration: int, function: Callable, *args: tuple, **kwargs: dict) -> object:
        self._timer = None
        self.interval = interval
        self.duration = duration
        self.timer_tick = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.num_ticks = 0


    def _run(self) -> None:
        self.is_running = False
        self.start()
        self.timer_tick(self.num_ticks, *self.args, **self.kwargs)
    
    def start(self) -> None:
        if not self.is_running:
            # If a timer has already been created
            if self._timer is not None:
                self.num_ticks += 1
                if self.duration - self.num_ticks <= 0:
                    return
            
            # Initializes a timer
            self.next_call += self.interval
            self._timer = Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self) -> None:
        self._timer.cancel()
        self.is_running = False