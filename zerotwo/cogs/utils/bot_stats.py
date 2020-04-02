import os
import time

import psutil


async def memory_usage():
    """Returns process' memory usage."""

    p = psutil.Process(os.getpid())
    usage = p.memory_info()[0] / 2.0 ** 20  # RAM usage in MB
    return str(f"{usage:.1f}MB")


async def uptime():
    """Bot uptime derived from the process age."""

    p = psutil.Process(os.getpid())
    delta_uptime = time.time() - p.create_time()
    hours, remainder = divmod(int(delta_uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return str(f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
