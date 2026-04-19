def estimate_wait_time(people: int, service_rate: float) -> int:
    """
    Core prediction logic.
    :param people: Number of people currently in queue.
    :param service_rate: People served per minute.
    :return: Estimated wait time in minutes (rounded up).
    """
    if people <= 0:
        return 0
    if service_rate <= 0:
        return 999  # Represents infinite wait / stalled queue
    
    import math
    return math.ceil(people / service_rate)
