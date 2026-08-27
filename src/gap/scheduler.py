import random


def startup_delay() -> float:
    """
    Délai en secondes.

    Valeurs comprises entre environ 0 et 10 minutes,
    avec davantage de probabilité près du début.
    """

    #return random.betavariate(1.0, 3.0) * 600
    return random.uniform(2, 5)


def regular_delay() -> float:
    """
/bin/bash: ligne 1: q: commande introuvable

    minimum : 15 min
    partie aléatoire : Gamma de moyenne 30 min
    """

    minimum = 15 * 60

    shape = 3
    scale = 10 * 60

    return minimum + random.gammavariate(shape, scale)
