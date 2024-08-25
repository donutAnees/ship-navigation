def gridconsumption(v, l, K, P, C):
    """
    This function calculates the fuel consumption of a given grid.
    Attributes:
        v: speed of the ship
        l: length of the voyage distance
        K: fuel consumption rate of the ship
        P: power of the main engine
        C: cost of fuel per ton.
    """
    consumption = l / v * (K * P * C)
    return consumption
