import os
from pathlib import Path

def logger(param):
        path_ = os.path.join(Path(__file__).parent, param)
        def decorator(func):
            def _inner(*args):
                try :
                    with open(path_, 'a') as file_logging:   
                        file_logging.write(f"called with {args}\n")
                except NotADirectoryError:
                    with open(path_, 'x') as file_logging:   
                        file_logging.write(f"called with {args}")
                func(*args)
            return _inner
        return decorator

@logger("logger_file.txt")
def double(x:int)->int:
    return 2 * x


if __name__ == '__main__':
    double(4)
    double(5)