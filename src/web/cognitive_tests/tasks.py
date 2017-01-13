import logging
import multiprocessing
import runpy
import threading
from functools import wraps

logger = logging.getLogger(__name__)
result_queue = multiprocessing.Queue()


def run_processor(path, arguments, keys, *args, **kwargs):
    logger.info('Running %s' % path)
    res_globals = runpy.run_path(path, init_globals=arguments)
    result = {}
    for key in keys:
        if key not in res_globals:
            raise LookupError('Key %s was nit found in result globals' % key)
        result[key] = {
            'value': res_globals[key],
            'comment': res_globals.get(key, None)
        }
    return result


def run_async(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        process = threading.Thread(target=func, args=args, kwargs=kwargs)
        process.start()
    return __wrapper
