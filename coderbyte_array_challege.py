"""
Have the function ArrayChallenge(strArr) read the strArr parameter being passed
which will represent a full day and will be filled with events that span from
time X to time Y in the day. The format of each event will be hh:mmAM/PM-hh:mmAM/PM.
For example, strArr may be ["10:00AM-12:30PM”,"02:00PM-02:45PM”,"09:10AM-09:50AM”].

Your program will have to output the longest amount of free time available between
the start of your first event and the end of your last event in the format: hh:mm.
The start event should be the earliest event in the day and the latest event should
be the latest event in the day. The output for the previous input would therefore
be 01:30 (with the earliest event in the day starting at 09:10AM and the latest
event ending at 02:45PM). The input will contain at least 3 events and the events 
may be out of order.

Examples
Input: {"12:15PM-02:00PM”,"09:00AM-10:00AM”,"10:30AM-12:00PM”}
Output: 00:30
Input: {"12:15PM-02:00PM”,"09:00AM-12:11PM”,"02:02PM-04:00PM”}
Output: 00:04
"""

list = [
    "10:10AM-10:20AM",
    "12:05PM-12:07PM",
    "12:15PM-02:00PM",
    "09:00AM-10:00AM",
    "11:30AM-12:00PM",
    "09:15PM-09:20PM",
    "09:05PM-09:07PM",
    "09:01PM-09:02PM",
]
# list = ["10:00AM-12:30PM","02:00PM-02:45PM","09:10AM-09:50AM"]
# list = ["10:00AM-12:30PM","09:10AM-09:50AM"]
# list = ["02:00PM-02:45PM","03:45PM-04:00PM"]
# list = ["10:00AM-11:00AM","11:45AM-12:00PM"]

to_hour_military = lambda num: 12 if (num == 12) else num + 12


def sort_by_schedule(list, schedule):
    if schedule.lower() == "am":
        return sorted(
            [e for e in list if e.split("-")[0][-2:].lower() == "am"],
            key=lambda ev: int(ev.split("-")[0][:2] * 60) + int(ev.split("-")[0][3:5]),
        )
    return sorted(
        [e for e in list if e.split("-")[0][-2:].lower() == "pm"],
        key=lambda ev: (
            to_hour_military(int(ev.split("-")[0][:2])),
            int(ev.split("-")[0][3:5]),
        ),
    )


def hhmm_to_minutes(hh, mm):
    return int((int(hh) * 60) + int(mm))


def diff_between_last_am_first_pm(last_time, current_hour, current_min):
    # Diff between last am and first pm
    hour_last_time = int(last_time / 60)
    min_last_time = last_time - hour_last_time * 60
    """
    Diff formula:
    (Current hour in military - last hours *to minutes) - (current mins - last mins)
    Result: Free time between last am event to first pm event
    """
    return (int(to_hour_military(current_hour) - hour_last_time) * 60) - abs(
        current_min - min_last_time
    )


def calculate_max_free_time(list):

    max_free_time = 0
    last_time_control = 0
    current_free_time = 0
    # Time AM
    if sort_by_schedule(list, "am") != []:
        """
        In AM the calculation is in hours to minutes
        for example:
            first event end in 10:00AM
            second event start in 11:AM
            Result: (10*60) - (11*60) -> abs(600 - 660)
            = 60 (60 mins of difference)
        """
        for index, ev in enumerate(sort_by_schedule(list, "am")):
            event = ev.split("-")
            # Hour to minutes for more control
            ev_mins_start = hhmm_to_minutes(event[0][:2], event[0][3:5])
            ev_mins_end = hhmm_to_minutes(event[1][:2], event[1][3:5])
            # If the first event
            if index == 0:
                last_time_control = ev_mins_end
                continue

            # Free time between last event to current event
            current_free_time = abs((last_time_control - ev_mins_start))
            # Assigning max free time
            if max_free_time < current_free_time:
                max_free_time = current_free_time
            # Last time control
            last_time_control = ev_mins_end

    # Time PM
    if sort_by_schedule(list, "pm") != []:
        """
        In PM the calculation is in 12 hour format,
        to 24 hour format to minutes
        for example:
            First event end in 02:00PM
            Second event start in 03:00PM
            Result = abs( (14-15)*60 ) = 60 (60 mins of difference)
        """
        for index, ev in enumerate(sort_by_schedule(list, "pm")):
            event = ev.split("-")
            hour_start = int(event[0][:2])
            mins_start = int(event[0][3:5])
            hour_end = int(event[1][:2])
            mins_end = int(event[1][3:5])

            # If it exists max free time from the am schedule
            if index == 0 and max_free_time != 0:
                current_free_time = diff_between_last_am_first_pm(
                    last_time=last_time_control,
                    current_hour=hour_start,
                    current_min=mins_start,
                )
                if max_free_time < current_free_time:
                    max_free_time = current_free_time
                last_time_control = [hour_end, mins_end]
                continue
            elif index == 0:
                last_time_control = [hour_end, mins_end]
                continue

            # Diff formula:
            # (Current hour - Last hour in military time to minutes)
            # + (Current minutes - last minutes)
            # Result = total diff in minutes
            current_free_time = (
                to_hour_military(hour_start) - to_hour_military(last_time_control[0])
            ) * 60 + (mins_start - last_time_control[1])
            # Check max free time
            if max_free_time < current_free_time:
                max_free_time = current_free_time
            # Last time control
            last_time_control = [hour_end, mins_end]

    return max_free_time


def ArrayChallenge(strArr):
    free_time = calculate_max_free_time(strArr)
    hour = int(free_time / 60)
    min = free_time - hour * 60
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(min)) == 1:
        min = "0" + str(min)
    return print(hour, ":", min, sep="")


ArrayChallenge(list)
