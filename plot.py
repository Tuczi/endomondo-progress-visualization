import itertools

import matplotlib.pyplot as plt


def pace(point):
    """
    Calculate pace (min/km) from speed (m/s)
    :param point: dictionary representing Endomondo point
    :return: pace value (float)
    """
    speed = point.get("speed", 0.0)
    return 60.0 / speed if speed > 0.0 else None


def bubble_sort(l, key=lambda e: e):
    """
    Bubble sort algorithm (in-place) - used for mostly sorted data
    :param l: mutable input list
    :param key: sorting key
    :return sorted input list
    """
    changed = True
    size = len(l) - 1
    while size > 0 and changed:
        changed = False
        for i in range(size):
            if key(l[i]) > key(l[i + 1]):
                changed = True
                l[i], l[i + 1] = l[i + 1], l[i]
        size -= 1

    return l


# TODO think about boxplot
def average_pace_approximation_curve(workouts, aggregation_step=None):
    """
    Create points representing curve with average pace (approximation)
    :param workouts: list of workouts
    :param aggregation_step: granulation (default 30)
    :return: points lists (two lists of floats)
    """
    if aggregation_step is None:
        aggregation_step = 30

    group_key = lambda p: int(p[0] * aggregation_step)
    flat_data = itertools.chain.from_iterable(map(distance_pace_pair, workouts))
    sorted_data = bubble_sort(list(filter(lambda e: e[1] is not None, flat_data)), key=group_key)
    grouped_data = itertools.groupby(sorted_data, key=group_key)

    x, y = [], []
    for point in grouped_data:
        x.append((point[0] + 0.5) / aggregation_step)
        tmp = list(point[1])
        y.append(sum(e[1] for e in tmp) / len(tmp))

    return x, y


def distance_pace_pair(workout):
    points = workout["points"]["points"]
    return list(map(lambda p: (p["distance"], pace(p)), points))


def workout_to_plot_points(workout):
    points = workout["points"]["points"]
    x = list(map(lambda p: p["distance"], points))
    y = list(map(pace, points))
    return x, y


def plot_workouts(workouts):
    """
    Plot all workouts
    :param workouts: list of workouts
    :return: list of plot handle
    """
    handles = []

    for workout in workouts:
        x, y = workout_to_plot_points(workout)

        label = "{0} {1:.2f}km".format(workout["local_start_time"][:16].replace("T", " "), workout["distance"])

        handle, = plt.plot(x, y, lw=1, label=label)
        handles.append(handle)

    return handles


def plot_average(workouts, aggregation_step=None):
    """
    Plot average curve and line
    :param workouts: list of workouts
    :param aggregation_step: see average_pace_approximation_curve
    :return:
    """
    handles, speed_avg_sum, distance_sum, distance_max, workouts_len = [], 0.0, 0.0, 0.0, 0

    for workout in workouts:
        speed_avg_sum += workout["speed_avg"]
        distance_sum += workout["distance"]
        distance_max = max(distance_max, workout["distance"])

    handle, = plt.plot([0, distance_max], [60 * len(workouts) / speed_avg_sum] * 2, lw=2,
                       label="average {0:.2f}km".format(distance_sum / len(workouts)))
    handles.append(handle)

    x, y = average_pace_approximation_curve(workouts, aggregation_step)
    handle, = plt.plot(x, y, lw=2, label="average curve")
    handles.append(handle)

    return handles


def plot_all(workouts):
    handles = plot_workouts(workouts)
    handles.extend(plot_average(workouts))
    plt.legend(handles=handles)
    plt.grid()
