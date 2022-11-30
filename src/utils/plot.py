from typing import Callable, Any
from .globals import Globals
from typing import Any
import matplotlib.pyplot as plt
import functools


def plotlive(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    plt.ion()

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        axes = plt.gcf().get_axes()
        for axis in axes:
            axis.cla()
        plt.clf()

        result = func(*args, **kwargs)
        plt.show()
        plt.pause(Globals.DRAW_TIMER)

        return result

    return wrapper
