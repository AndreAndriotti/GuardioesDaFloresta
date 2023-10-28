import time

class Cooldown:
    def __init__(self, cooldown_duration):
        self.cooldown_duration = cooldown_duration
        self.last_used_time = 0

    def IsReady(self):
        current_time = time.time()
        if current_time - self.last_used_time >= self.cooldown_duration:
            return True
        else:
            return False

    def Reset(self):
        self.last_used_time = time.time()


