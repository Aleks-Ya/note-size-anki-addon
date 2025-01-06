import time

def wait_until(predicate, timeout=10, interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if predicate():
            return True
        time.sleep(interval)
    return False