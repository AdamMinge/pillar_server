import functools


def invoke_repeatedly_context(steps: list[dict[str, any]] = None):
    def decorator(func):
        @functools.wraps(func)
        def decorated_method(self, *args, **kwargs):
            for step in steps:
                func(self, *args, **kwargs, **step)

        return decorated_method

    return decorator
