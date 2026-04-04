from dateutil import parser
from gps_helpers import gpsDistance


class Workout(object):
    """A class to keep track of workouts"""

    # Class variable to compute calories burned from workout time
    cal_per_hr = 200
   
    def __init__(self, start, end, calories=None):
        """Creates a workout class"""
        self.icon = '😓'
        self.start = parser.parse(start)
        self.end = parser.parse(end)
        self.calories = calories

    def get_duration(self):
        return self.end - self.start

    def get_calories(self):
        if self.calories is not None:
            return self.calories
        hours = self.get_duration().total_seconds() / 3600
        return hours * self.cal_per_hr

    def __str__(self):
        return f"{self.icon} {self.get_duration()} {round(self.get_calories(),1)} Calories"


class RunWorkout(Workout):
   
    # new class variable
    cals_per_km = 100
   
    def __init__(self, start, end, elev=0, calories=None, route_gps_points=None):
        self.icon = '🏃'
        super().__init__(start, end, calories)
        self.elev = elev
        self.route_gps_points = route_gps_points

    def get_elevation(self):
        return self.elev

    def get_distance(self):
        if not self.route_gps_points:
            return 0
        dist = 0
        for i in range(len(self.route_gps_points) - 1):
            dist += gpsDistance(
                self.route_gps_points[i],
                self.route_gps_points[i + 1]
            )
        return dist

    def get_calories(self):
        if self.calories is not None:
            return self.calories
        dist_km = self.get_distance()
        if dist_km > 0:
            return dist_km * self.cals_per_km
        return super().get_calories()


class SwimWorkout(Workout):
    """Subclass of workout representing swimming"""
   
    cal_per_hr = 400
   
    def __init__(self, start, end, pace, calories=None):
        self.icon = '🏊'
        super().__init__(start, end, calories)
        self._pace = pace

    # getter for pace
    @property
    def pace(self):
        return self._pace

    # overloaded method
    def get_calories(self):
        if self.calories is not None:
            return self.calories
        hours = self.get_duration().total_seconds() / 3600
        return hours * self.cal_per_hr

    def __str__(self):
        duration = self.get_duration()
        cal = round(self.get_calories(), 1)
        return (
            "|––––––––––––––––|\n"
            "|                |\n"
            "| 🏊‍             |\n"
            "| Swimming       |\n"
            "|                |\n"
            f"| {duration}        |\n"
            f"| {cal} Calories |\n"
            "|                |\n"
            "|________________|\n"
        )


def total_calories(workouts):
    return sum(w.get_calories() for w in workouts)


def total_elevation(run_workouts):
    return sum(rw.get_elevation() for rw in run_workouts)