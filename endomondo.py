import datetime
import json
import urllib.request


def get(url, headers=None):
    if headers is None:
        headers = {}

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)

    return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))


def get_as_chrome(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'}

    return get(url, headers=headers)


class EndomondoUser:
    workout_url = "https://www.endomondo.com/rest/v1/users/{0}/workouts/{1}"
    workouts_list_url = "https://www.endomondo.com/rest/v1/users/{0}/workouts?before={1}Z&after={2}Z"

    def __init__(self, user_id):
        self.id = user_id
        self.workouts_map = {}

    def workouts(self, before=datetime.datetime.utcnow(),
                 after=datetime.datetime.utcnow() - datetime.timedelta(3 * 365 / 12)):
        return list(map(self.get_workout, self.get_workouts_ids(before, after)))

    def get_workout(self, workout_id):
        if workout_id not in self.workouts_map:
            workout = get_as_chrome(EndomondoUser.workout_url.format(self.id, workout_id))
            self.workouts_map[workout_id] = workout

        return self.workouts_map[workout_id]

    def get_workouts_ids(self, before, after):
        workouts = get_as_chrome(
            EndomondoUser.workouts_list_url.format(self.id, before.isoformat('T'), after.isoformat('T')))

        return map(lambda w: w["id"], workouts)
