import matplotlib.pyplot as plt


def pace(point):
    """
    Calculate pace (min/km) from speed (m/s)
    """
    speed = point.get("speed", 0.0)
    return 60.0 / speed if speed > 0.0 else None


def plot_all(workouts):
    handles, speed_avg_sum, distance_sum, distance_max, workouts_len = [], 0.0, 0.0, 0.0, 0

    for workout in workouts:
        points = workout["points"]["points"]
        x = list(map(lambda p: p["distance"], points))
        y = list(map(pace, points))

        label = "{0} {1:.2f}km".format(workout["local_start_time"][:16].replace("T", " "), workout["distance"])

        handle, = plt.plot(x, y, lw=1.4, label=label)
        handles.append(handle)

        speed_avg_sum += workout["speed_avg"]
        distance_sum += workout["distance"]
        distance_max = max(distance_max, workout["distance"])

        workouts_len += 1

    # plot average
    handle, = plt.plot([0, distance_max], [60 * workouts_len / speed_avg_sum] * 2, lw=2,
                       label="average {0:.2f}km".format(distance_sum / workouts_len))
    handles.append(handle)

    plt.legend(handles=handles)
    plt.grid()

    return plt
