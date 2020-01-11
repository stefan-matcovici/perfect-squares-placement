from functools import wraps
from multiprocessing import Process, Manager
from time import time


def timing(timeout):
    """
    Decorator to call function in subprocess and wait at most `timeout` seconds to finish
    :param timeout: no of seconds to wait for the function to finish
    :return:
    """

    def real_timing(function):
        @wraps(function)
        def wrap(*args, **kw):
            manager = Manager()
            result = manager.Value("result", -1.0)

            args += (result,)
            action_process = Process(target=function, args=args, kwargs=kw)

            ts = time()
            action_process.start()
            action_process.join(timeout=timeout)
            te = time()

            action_process.terminate()

            if action_process.exitcode is None:
                return -1, -1

            return result.value, te - ts

        return wrap

    return real_timing
