from datetime import datetime, time

def is_time_between_nine_to_five(check_time):
    """Check if time is between 9-5(working hours)

    Args:
        check_time (time object)

    Returns:
        Boolean
    """
    begin_time = time(9,00)
    end_time = time(17, 00)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    return False
    # else: # crosses midnight
    #     return check_time >= begin_time or check_time <= end_time