# spots.py

class Spot:

    def __init__(self, center: tuple[float, float], redius: float):
        self._center = center
        self._radius = radius

    def center(self) -> tuple[float,float]:
        return self._center

    def radius(self) -> float:
        return self._radius

    def move_right(self) -> None:
        center_x, center_y = self._center
        self._center = (center_x + 0.001, center_y)


class SpotsState:

    def __init__(self):
        self._spots = [
            Spot((0.5,0.5), 0.05),
            Spot((0.25,0.75), 0.05),
            Spot((0.5,0.5), 0.05),
            Spot((0.5,0.5), 0.05),]


    def all_spots(self) -> None:
        return self._spots

    def move_spots()
