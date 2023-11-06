"""Utility module"""


def Unofficial(method):
    """
    Utility wrapper to classfiy methods as unofficial

    Arguments
    ---------
    method : Reference to method that should be wrapped
    """

    def wrapper(*args, with_unofficial=False, **kwargs):
        """
        Wrapper function
        """

        if with_unofficial:
            method(*args, **kwargs)

        else:
            raise ValueError(
                f"{method} is classified as Unofficial. Use with_unofficial=True in the arguments to use it"
            )

    return wrapper
