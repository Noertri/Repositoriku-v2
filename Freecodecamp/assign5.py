import copy
import random
# Consider using the modules imported above.


class Hat:

    def __init__(self, **balls):
        self.contents = []

        for color, ball in balls.items():
            if ball >= 1:
                for n in range(ball):
                    self.contents.append(color)

    def draw(self, m=1):
        n = len(self.contents)

        if m > n:
            return self.contents
        else:
            sample = list()
            for _ in range(m):
                i = random.choice(self.contents)
                sample.append(i)
                self.contents.remove(i)
            return sample


def experiment(hat=None, expected_balls={}, num_balls_drawn=1, num_experiments=1):
    n = 0
    colors = list(expected_balls.keys())
    for _ in range(num_experiments):
        hat_copy = copy.deepcopy(hat)
        sample = hat_copy.draw(num_balls_drawn)
        if sample.count(colors[0]) >= expected_balls[colors[0]] and sample.count(colors[1]) >= expected_balls[colors[1]]:
            n += 1

    prob = n/num_experiments

    return prob


hat = Hat(blue=3, red=2, green=6)
probability = experiment(hat=hat, num_balls_drawn=4, num_experiments=1000, expected_balls={"blue": 2, "green": 1})