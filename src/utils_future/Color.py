import random


class Color:
    LK_COLOR_LIST = [
        '#ffbe29',
        '#8d153a',
        '#eb7400',
        '#00534e',
    ]

    @staticmethod
    def lk(__**):
        return random.choice(Color.LK_COLOR_LIST)
