import time

def elapsed(since):
    return time.time() - since

def mock_time():
    return 200

def test_elapsed():
    time.time = mock_time
    assert elapsed(50) ==150


def warp(func:callable)-> callable: 
    def _inner(value:str):
        print("decorate it ")
        func(value)
    return _inner

@warp
def originale(value:str):
    print(f"from original {value}")

def decorator_withparam(label):
    def actual_decorator(func):
        def __inner(args):
            print(label)
            func(args)
        return __inner
    return actual_decorator

@decorator_withparam("this a lable")
def double(x):
    print(f"result is {x*2}")


if __name__ == '__main__':
    originale("value")
    double("test") 

    
