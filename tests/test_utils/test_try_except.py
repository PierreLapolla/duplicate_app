from utils.try_except import try_except


def test_divide_success_cleanup():
    """Test that successful division returns correct result and cleanup function is executed."""
    cleanup_executed = False

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    @try_except(finally_callable=cleanup)
    def divide(a, b):
        return a / b

    # Successful division test
    cleanup_executed = False  # Reset flag before test
    result = divide(4, 2)
    assert result == 2, "Expected 4 / 2 to equal 2"
    assert cleanup_executed, (
        "Expected cleanup function to be executed after successful division"
    )


def test_divide_exception_cleanup():
    """Test that division by zero returns None and cleanup function is executed."""
    cleanup_executed = False

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    @try_except(finally_callable=cleanup)
    def divide(a, b):
        return a / b

    # Division by zero test
    cleanup_executed = False  # Reset flag before test
    result = divide(1, 0)
    assert result is None, "Expected division by zero to return None"
    assert cleanup_executed, "Expected cleanup function to be executed on exception"


def test_divide_exception_error_callable():
    """Test that error callable is invoked on exception with the correct error message."""
    cleanup_executed = False
    error_called = False
    error_msg = ""

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    def handle_error(e):
        nonlocal error_called, error_msg
        error_called = True
        error_msg = str(e)

    @try_except(finally_callable=cleanup, error_callable=handle_error)
    def divide(a, b):
        return a / b

    # Test for error handling on division by zero
    cleanup_executed = False
    error_called = False  # Reset flags before test
    result = divide(1, 0)
    assert result is None, "Expected divide to return None on exception"
    assert error_called, "Expected error callable to be executed on exception"
    assert cleanup_executed, "Expected cleanup function to be executed on exception"
    assert "division by zero" in error_msg, (
        "Expected 'division by zero' in error message"
    )


def test_multiply_success_with_error_callable():
    """Test that error callable is not invoked on a successful multiplication."""
    cleanup_executed = False
    error_called = False
    error_msg = ""

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    def handle_error(e):
        nonlocal error_called, error_msg
        error_called = True
        error_msg = str(e)

    @try_except(finally_callable=cleanup, error_callable=handle_error)
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    assert result == 12, "Expected 3 * 4 to equal 12"
    assert cleanup_executed, (
        "Expected cleanup function to be executed on successful multiplication"
    )
    assert not error_called, (
        "Expected error callable not to be executed on successful multiplication"
    )


def test_function_with_kwargs():
    """Test a function using keyword arguments for both valid and invalid inputs."""
    cleanup_executed = False
    error_called = False
    error_msg = ""

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    def handle_error(e):
        nonlocal error_called, error_msg
        error_called = True
        error_msg = str(e)

    @try_except(finally_callable=cleanup, error_callable=handle_error)
    def add(a=0, b=0):
        return a + b

    # Valid call using keyword arguments
    cleanup_executed = False
    error_called = False
    result = add(a=7, b=5)
    assert result == 12, "Expected add(a=7, b=5) to equal 12"
    assert cleanup_executed, (
        "Expected cleanup function to be executed on successful addition"
    )
    assert not error_called, (
        "Expected error callable not to be executed on successful addition"
    )

    # Invalid call that triggers an exception (TypeError)
    cleanup_executed = False
    error_called = False
    result = add(a="a", b=5)
    assert result is None, "Expected add(a='a', b=5) to return None due to exception"
    assert cleanup_executed, (
        "Expected cleanup function to be executed on exception in add"
    )
    assert error_called, "Expected error callable to be executed on exception in add"


def test_no_args_function():
    """Test that a no-argument function works correctly with the decorator."""
    cleanup_executed = False
    error_called = False

    def cleanup():
        nonlocal cleanup_executed
        cleanup_executed = True

    def handle_error(e):
        nonlocal error_called
        error_called = True

    @try_except(finally_callable=cleanup, error_callable=handle_error)
    def greet():
        return "hello"

    result = greet()
    assert result == "hello", "Expected greet() to return 'hello'"
    assert cleanup_executed, "Expected cleanup function to be executed for greet()"
    assert not error_called, (
        "Expected error callable not to be executed when no error occurs in greet()"
    )
