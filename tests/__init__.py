import time


def wait_until(predicate, timeout=10, interval=0.1) -> None:
    start_time: float = time.time()
    while time.time() - start_time < timeout:
        if predicate():
            return
        time.sleep(interval)


def wait_until_exception(predicate, exception_type: type[BaseException], timeout=10, interval=0.1) -> None:
    start_time: float = time.time()
    while time.time() - start_time < timeout:
        try:
            predicate()
        except exception_type:
            return
        time.sleep(interval)
