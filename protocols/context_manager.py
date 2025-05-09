class PytestManagerRaise:
    
    def __init__(self, exception:Exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type:Exception, exc_value:Exception, exc_traceback):
        if exc_type is self.exception:
            return True
        else:
            raise exc_value
        
with PytestManagerRaise(ZeroDivisionError):
    assert (1/0) 



import time

class Timer:
    def __init__(self):
        pass

    def __enter__(self):
        self.since  = time.time()
        return self
        
    def elapsed(self):
        return time.time() - self.since

    def __exit__(self, exce_type, exce_val, tracback):
        pass



with Timer() as start:
    time.sleep(10)
    print(start.elapsed())