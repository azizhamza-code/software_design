def test_pass():
    pass

def test_fail():
    assert 1 == 0

def test_error():
    return  1 / 0

def run_test(pattern=None):
    result = {"pass": 0, "pass_test":[],  "fail": 0 ,"fail_test":[], "error": 0,"error_test":[]}
    
    # Check if setup and teardown functions exist
    setup_func = globals().get("setup", None)
    teardown_func = globals().get("teardown", None)

    for (name, test) in globals().items():
        # Skip if not a test or if pattern is provided and not in the name
        if not name.startswith("test_") or (pattern and pattern not in name):
            continue
        try:
            # Call setup function if it exists
            if setup_func:
                setup_func()
                
            test()
            result["pass"] +=1
            result["pass_test"].append(test.__name__)
        except AssertionError: 
            result["fail"] +=1
            result["fail_test"].append(test.__name__)
        except Exception:
            result["error"] +=1
            result["error_test"].append(test.__name__)
        finally:
            # Call teardown function if it exists
            if teardown_func:
                teardown_func()
    
    print(f"pass {result['pass']}")
    print(f"pass test :  {result['pass_test']}")
    print(f"fail {result['fail']}")
    print(f"fail test :  {result['fail_test']}")
    print(f"error {result['error']}")
    print(f"error test :  {result['error_test']}")
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", help="Pattern to filter test names")
    args = parser.parse_args()
    
    result = run_test(args.pattern)
