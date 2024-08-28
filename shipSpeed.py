import math

'''
h  ---> wave height; 
q ---> angle between the ship's heading and the coming direction of the waves; 
D ---> actual displacement of the ship; 
V0 ---> speed of the ship in still water; 
Vw ---> speed of the wind;
k1, k2, k3, k4 ---> parameters determined by the performance of the ship itself.

'''



class shipSpeed:
    def __init__(self, ship_speed, wave_height, displacement, k1, k2, k3, k4, wind_speed, angle):
        self.V0 = ship_speed
        self.h = wave_height
        self.D = displacement
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4
        self.Vw = wind_speed
        self.q = angle
        self.speed = self.calculate_speed()

    def getSpeed(self):
        return self.speed


    def calculate_speed(self):
        wave_impact = (self.k1 - self.k2) * self.h
        wind_impact = self.k3 * 10**-3 * self.Vw * math.cos(math.radians(self.q))
        environmental_impact = wave_impact + wind_impact
        displacement_impact = 1 - (self.k4 * 10**-7 * self.D * self.V0)
        speed = self.V0 - (environmental_impact * displacement_impact)
        return speed