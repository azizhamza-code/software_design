import time


test_r= 6

def test_pass():
    pass

def test_fail():
    assert 1 == 0

def test_error():
    return  1 / 0

def run_test(pattern=None):
    result = {
        "pass": 0, "pass_test":[], "pass_times":{},
        "fail": 0, "fail_test":[], "fail_times":{},
        "error": 0, "error_test":[], "error_times":{}
    }
    
    # Check if setup and teardown functions exist
    setup_func = globals().get("setup", None)
    teardown_func = globals().get("teardown", None)

    for (name, test) in globals().items():
        # Skip if not a test or if pattern is provided and not in the name
        if not name.startswith("test_") or (pattern and pattern not in name) or not callable(test):
            continue
        
        start_time = time.time()
        try:
            # Call setup function if it exists
            if setup_func:
                setup_func()
                
            test()
            end_time = time.time()
            duration = end_time - start_time
            result["pass"] +=1
            result["pass_test"].append(test.__name__)
            result["pass_times"][test.__name__] = duration
        except AssertionError: 
            end_time = time.time()
            duration = end_time - start_time
            result["fail"] +=1
            result["fail_test"].append(test.__name__)
            result["fail_times"][test.__name__] = duration
        except Exception:
            end_time = time.time()
            duration = end_time - start_time
            result["error"] +=1
            result["error_test"].append(test.__name__)
            result["error_times"][test.__name__] = duration
        finally:
            # Call teardown function if it exists
            if teardown_func:
                teardown_func()
    
    print(f"pass {result['pass']}")
    for test_name in result["pass_test"]:
        print(f"  {test_name}: {result['pass_times'][test_name]:.6f} seconds")
    
    print(f"fail {result['fail']}")
    for test_name in result["fail_test"]:
        print(f"  {test_name}: {result['fail_times'][test_name]:.6f} seconds")
    
    print(f"error {result['error']}")
    for test_name in result["error_test"]:
        print(f"  {test_name}: {result['error_times'][test_name]:.6f} seconds")
    
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", help="Pattern to filter test names")
    args = parser.parse_args()
    
    result = run_test(args.pattern)
