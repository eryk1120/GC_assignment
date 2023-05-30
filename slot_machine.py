from itertools import groupby

from number_generators import RandomIntGenerator, SecretRandomIntGenerator

DEFAULT_COST = 5
DEFAULT_REELS = (
    # default proposition for reels
    (1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1),
    (1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1),
    (1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
)


class SlotMachine:
    SING_MAP = {
        0: "J",
        1: "Q",
    }

    VALUE_MAP = {
        0: {3: 30, 4: 45, 5: 100},
        1: {3: 10, 4: 20, 5: 50},
    }

    def __init__(
        self,
        cost: int = DEFAULT_COST,
        reels: tuple[tuple[int, ...], ...] = DEFAULT_REELS,
        reels_positions: tuple[int, ...] = (0, 0, 0, 0, 0),
        rng: RandomIntGenerator = SecretRandomIntGenerator,
        balance: int = 50,
    ) -> None:
        self.cost = cost
        self.reels = reels
        self.rng = rng()
        self.balance = balance
        self.reels_positions = reels_positions

        # check if reels are the same length and if they are not empty
        if not all(len(reel) == len(reels[0]) for reel in reels):
            msg = "Reels must be the same length"
            raise ValueError(msg)
        self.reel_length = len(reels[0])

        self.screen = self._update_rows()

    def _update_rows(self) -> tuple[tuple[int], tuple[int], tuple[int]]:
        row1 = tuple(
            reel[(index - 1) % self.reel_length]
            for index, reel in zip(self.reels_positions, self.reels)
        )
        row2 = tuple(
            reel[index % self.reel_length]
            for index, reel in zip(self.reels_positions, self.reels)
        )
        row3 = tuple(
            reel[(index + 1) % self.reel_length]
            for index, reel in zip(self.reels_positions, self.reels)
        )

        self.screen = (row1, row2, row3)

        return row1, row2, row3

    def _evaluate_points(self):
        points = []

        for row in self.screen:
            # map number of consecutive occurrences to sign
            # 0 - count of occurrences
            # 1 - sign
            groups = [(len(list(i[1])), i[0]) for i in groupby(row)]
            for group in groups:
                if group[0] > 2:
                    points.append(self.VALUE_MAP[group[1]][group[0]])
                    # break for, because cant be more than one group with more than 2 consecutive occurrences in row
                    break

        self.balance += sum(points)
        return points

    def get_screen(self) -> str:
        screen = ""
        for row in self.screen:
            screen += (
                " ".join([self.SING_MAP.get(element, element) for element in row])
                + "\n"
            )

        return screen

    def play(self):
        self.balance -= self.cost
        self.reels_positions = tuple(
            self.rng.generate_random_int(beginning=0, ending=self.reel_length)
            for _ in range(len(self.reels))
        )

        _, _, _ = self._update_rows()
        return self._evaluate_points()
