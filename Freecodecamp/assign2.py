def add_time(start, duration, today=None):
    start_time = start.split()
    time_list = start_time[0].split(':')
    duration_time = duration.split(':')

    start_hour = int(time_list[0])
    start_min = int(time_list[1])
    duration_hour = int(duration_time[0])
    duration_min = int(duration_time[1])

    min_time = start_min + duration_min
    if min_time >= 60:
        hour_time = start_hour + duration_hour + (min_time//60)
        min_time = min_time % 60
    else:
        hour_time = start_hour + duration_hour

    days_val = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thrusday": 4, "friday": 5, "saturday": 6,
                0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thrusday", 5: "Friday", 6: "Saturday"}

    if today is None:
        n, ans1 = time_decision(hour_time, min_time, start_time[1])
        if n == 0:
            ans = ans1
        elif n == 1:
            ans = "{} (next day)".format(ans1)
        else:
            ans = "{} ({} days later)".format(ans1, str(n))
    else:
        n, ans1 = time_decision(hour_time, min_time, start_time[1])
        if n == 0:
            ans = "{}, {}".format(ans1, today)
        elif n == 1:
            m = days_val[today.lower()] + 1
            next_day = days_val[m]
            ans = "{}, {} (next day)".format(ans1, next_day)
        else:
            m = days_val[today.lower()] + n
            if m >= 7:
                m = m % 7
            next_day = days_val[m]
            ans = "{}, {} ({} days later)".format(ans1, next_day, str(n))

    return ans


def time_decision(hour, minute, info):
    if hour < 12:
        ans1 = "{}:{} {}".format(str(hour), str(minute).zfill(2), info)
        n = 0
    elif (hour >= 12) and (hour < 24):
        if hour > 12:
            hour = hour % 12
        if info == 'AM':
            ans1 = "{}:{} PM".format(str(hour), str(minute).zfill(2))
            n = 0
        else:
            ans1 = "{}:{} AM".format(str(hour), str(minute).zfill(2))
            n = 1
    else:
        days = hour // 24
        hour = hour % 24
        n, ans1 = time_decision(hour, minute, info)
        n = n + days

    return n, ans1


t = add_time("6:30 PM", "205:12")
print(t)