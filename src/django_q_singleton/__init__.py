# SPDX-FileCopyrightText: 2024-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT


# https://github.com/steinitzu/celery-singleton
# https://github.com/boxed/urd

def singleton_background_task(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_running = cache.get(BACKGROUND_TASK_REDIS_KEY, 0)
        if is_running:
            logger.info(f"Task {func.__name__} already running")
            return

        logger.info(f"Task {func.__name__} not running, starting it")
        try:
            cache.set(BACKGROUND_TASK_REDIS_KEY, 1)
            func(*args, **kwargs)
        finally:
            cache.set(BACKGROUND_TASK_REDIS_KEY, 0)
            logger.info(f"Task {func.__name__} finished")

    return wrapper
