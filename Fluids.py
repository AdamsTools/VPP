import numpy as np
import tools as ts


class Fluid():
    def __init__(self):

        self.std_temperature = ts.celsius2kelvin(25)
        self.std_pressure = 101.325

    class Water():
        def __init__(self, temperature, salinity, density, dynamic_visc, kinematic_visc):
            '''  Standard values calculated at sea level '''

            if temperature:
                self.temperature = ts.celsius2kelvin(temperature)
            else:
                self.temperature = Fluid().std_temperature

            if salinity:
                self.salinity = salinity
            else:
                self.salinity = 0

            if density:
                self.density = density
            else:
                self.density = 1.1839

            if dynamic_visc:
                self.dynamic_visc = dynamic_visc
            else:
                self.dynamic_visc = 1.8372 * 10 ** -5

            if kinematic_visc:
                self.kinematic_visc = kinematic_visc
            else:
                self.kinematic_visc = 1.5518 * 10 ** -5

    class Air():
        def __init__(self, temperature, density, dynamic_visc, kinematic_visc, PA=101.325, rel_humidity=80):
            '''
             Standard values calculated at sea level
            :param temperature: [°C]
            :param humidity: []
            :param density: [kg/m3]
            :param RA: [J/K/kg]
            :param RV: [J/K/kg]
            '''

            if temperature:
                self.temperature = ts.celsius2kelvin(temperature)
            else:
                self.temperature = Fluid().std_temperature

            if density:
                self.density = density
            else:
                self.density = self.density_humid(PA, rel_humidity)

            if dynamic_visc:
                self.dynamic_visc = dynamic_visc
            else:
                self.dynamic_visc = 1.8372 * 10 ** -5

            if kinematic_visc:
                self.kinematic_visc = kinematic_visc
            else:
                self.kinematic_visc = 1.5518 * 10 ** -5

        def density_humid(self, PA, rel_humidity):
            # Gas Constants
            RA = 287.05287  # Specific gas constant for dry air
            RV = 461.495  # Specific gas constant for water vapour
            T = ts.kelvin2celsius(self.temperature)
            PV_sat = 611.21 * np.e ** (
                        (18.678 - T / 234.5) * (T / (257.14 + T)))  # Saturated water pressure (Buck(1981,1996))

            PV = (rel_humidity / 100) * PV_sat  # Partial pressure of water vapour [Pa]
            return (PA / RA + PV / RV) * (1 / self.temperature)

        def dynamic_visc_humid(self):
            '''TO BE IMPLEMENTED
            The Science of Sailing Part 1 pg 57 (2.8.7) '''
            None
