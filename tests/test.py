def test_pass():
    pass

def test_fail():
    assert 1 == 0

def test_error():
    return  1 / 0

def run_test():
    result = {"pass": 0, "pass_test":[],  "fail": 0 ,"fail_test":[], "error": 0,"error_test":[]}

    for (name, test)  in globals().items():
        if not name.startswith("test_"):
            continue
        try :
            test()
            result["pass"] +=1
            result["pass_test"].append(test.__name__)
        except AssertionError: 
            result["fail"] +=1
            result["fail_test"].append(test.__name__)
        except Exception:
            result["error"] +=1
            result["error_test"].append(test.__name__)
    
    print(f"pass {result['pass']}")
    print(f"pass test :  {result['pass_test']}")
    print(f"fail {result['fail']}")
    print(f"fail test :  {result['fail_test']}")
    print(f"error {result['error']}")
    print(f"error test :  {result['error_test']}")
    return result

if __name__ == '__main__':
    result = run_test()
    # Result is already printed in run_test()