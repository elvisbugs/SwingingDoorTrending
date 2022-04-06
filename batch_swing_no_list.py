import random as rnd
import math

import matplotlib.pyplot as plt


def choose_one(**chances: dict[str, float]) -> str:
    total = sum([val for val in chances.values()])
    chances = {key: val / total for key, val in chances.items()}

    randnum = rnd.random()
    cum = 0
    for key, val in chances.items():
        cum += val
        if randnum < cum:
            return key


def gen_random(points: int, dev: float):
    return [rnd.normalvariate(0, dev) for x in range(points)]


def gen_trend(points: int, type: str, first: float = 0, **params) -> list:
    data = [first]

    dev = params.get("dev", 1)

    if type == "sine":
            amp = params.get("amp", 1)
            freq = params.get("freq", 1)
            data = [amp * math.sin(x * freq) for x in range(points)]

    elif type == "stock":
        temp = gen_random(points + 1, dev)

        # moving sum
        for i in range(1, points):
            data.append(data[i - 1] + temp[i])

    elif type == "smooth":
        window = params.get("window", 2)
        prob = params.get("prob", 0)
        mult = params.get("mult", 10)
        adjust = params.get("adjust", False)

        temp = gen_random(points + window, dev)

        # moving sum with random spikes
        for i in range(1, points + window):
            last = data[i - 1]
            diff = temp[i]
            new = last + diff

            if rnd.random() < prob:
                diff *= mult * (-1 * adjust)

                new = last + diff
                if adjust:
                    if (new > last and diff > 0) or (new < last and diff < 0):
                        diff *= -1
                    new = last + diff

            data.append(new)

        # rounding moving average
        _round = params.get("round", 2)
        for i in range(points):
            data[i] = round(sum(data[i : i + window]) / window, _round)

        data = data[:points]

    else:
        return []

    return data


################################################################################
# Finja que a partir daqui é tudo C
################################################################################
# from dataclasses import dataclass

# INF = float("inf")

# # struct
# @dataclass
# class Point:
#     """Decimal order is 1.000x"""
#     x: int = 0
#     y: int = 0

# @dataclass
# class Slope:
#     """Decimal order is 1.000x"""
#     pivot: int = 0
#     onend: int = 0

# # Python                        # C
# # pivot = Point(1000, 2000)     # Point pivot = { 1000, 2000 };

# # Globals (all ints are 1000x)
# err: int = 0 # error size
# end: int = 0 # maximum time axis size

# # Necessary points
# pivot   = Point(0, 0) # x is always 0
# last    = Point(0, 0) # last point
# current = Point(0, 0) # current point, becomes last

# # Necessary slopes
# top = Slope(pivot.y + err, -INF) # top pivot error point
# bot = Slope(pivot.y - err, INF) # bottom pivot error point

# # Helper functions
# def slope_on_end(height) -> int:
#     pass

# def tanline(x: float, y: float, max: float, pad: float) -> float:
#     """
#     x: current distance in time
#     y: current value
#     max: max time allowed
#     pad: pivot height
#     """
#     return ((max * (y - pad)) / x) + pad

################################################################################

INF = float("inf")


def tanline(x: float, y: float, max: float, pad: float) -> float:
    return ((max * (y - pad)) / x) + pad


class Cwing:
    def __init__(self, error=1, maxtime=25):
        self.count = -1  # genial, permite setup ao inserir o primeiro dado
        self.time = 0
        self.error = error
        self.maxtime = maxtime

        self.last = 0
        self.curr = 0

    def setup(self, pivot):
        self.time = 0
        self.pivot = pivot
        self.last = pivot
        self.top_slope = -INF
        self.bot_slope = INF
        self.calc_pivots()

        return self.count, pivot

    def calc_pivots(self):
        self.top_pivot = self.pivot + self.error / 2
        self.bot_pivot = self.pivot - self.error / 2

    def calc_slopes(self):
        lintop = tanline(self.time, self.curr, self.maxtime, self.top_pivot)
        linbot = tanline(self.time, self.curr, self.maxtime, self.bot_pivot)

        # check and updates each door's angles
        self.top_slope = self.top_slope if self.top_slope > lintop else lintop
        self.bot_slope = self.bot_slope if self.bot_slope < linbot else linbot

    def process(self, data):
        # ah como eu queria ter o ++
        self.time += 1
        self.count += 1

        # The first addition must make setup and return the value
        if self.count == 0:
            return self.setup(data)

        # Shifts values for new data
        self.last = self.curr
        self.curr = data

        if self.time >= self.maxtime or self.check_door():
            return self.setup(data)

        return self.count, None

    def check_door(self) -> bool:
        if self.time:
            self.calc_slopes()
            # if the doors open in the distance
            return self.top_slope > self.bot_slope

        return False


if __name__ == "__main__":
    points = 100
    # datalist = gen_trend(points, "stock", 10)
    datalist = gen_trend(
        points, "smooth", 24, dev=0.8, prob=0.02, mult=10, window=10, round=1
    )  # chunky
    complist = []

    door = Cwing(error=0.2, maxtime=100)

    for x in datalist:
        result = door.process(x)
        if result[1] is not None:
            complist.append(result)

    plt.plot(datalist, color="black", label=f"raw data ({points})")
    plt.plot(*zip(*complist), color="red", label=f"compressed ({len(complist)})")

    comp_rate = int(100 * (1 - len(complist) / points))
    plt.title(f"Compression of {comp_rate}%")
    plt.legend()
    plt.show()
