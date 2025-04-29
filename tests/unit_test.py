from test import run_test

# Add test functions to test our test framework
def not_a_test_function():
    pass

def test_pass_dummy():
    pass

def test_fail_dummy():
    assert 1 == 0

def test_error_dummy():
    return 1 / 0


def test_framework_identifies_test_functions():
    import test
    original_globals = test.__dict__.copy()
    
    test.__dict__['not_a_test_function'] = not_a_test_function
    test.__dict__['test_dummy'] = lambda: None
    
    result = run_test()
    
    test.__dict__.clear()
    test.__dict__.update(original_globals)
    
    assert 'test_dummy' in result["pass_test"]
    assert 'not_a_test_function' not in result["pass_test"]

def test_framework_counts_correctly():
    import test
    original_globals = test.__dict__.copy()
    
    test.__dict__.clear()
    test.__dict__['test_pass'] = test_pass_dummy
    test.__dict__['test_fail'] = test_fail_dummy
    test.__dict__['test_error'] = test_error_dummy
    
    result = run_test()
    
    test.__dict__.clear()
    test.__dict__.update(original_globals)
    
    assert result["pass"] == 1
    assert result["fail"] == 1
    assert result["error"] == 1
    
    assert "test_pass" in result["pass_test"]
    assert "test_fail" in result["fail_test"]
    assert "test_error" in result["error_test"]

if __name__ == "__main__":

    try:
        test_framework_identifies_test_functions()
        print("test_framework_identifies_test_functions: PASS")
    except Exception as e:
        print(f"test_framework_identifies_test_functions: FAIL - {e}")
    
    try:
        test_framework_counts_correctly()
        print("test_framework_counts_correctly: PASS")
    except Exception as e:
        print(f"test_framework_counts_correctly: FAIL - {e}") 
