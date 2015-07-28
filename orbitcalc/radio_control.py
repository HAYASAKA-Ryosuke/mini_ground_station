#!coding:utf-8
import requests
from time import sleep
from orbitcalc import Orbitcalc


class RadioControl:
    def __init__(self, gslat, gslon, gselev):
        self.orbit_calc = Orbitcalc(gslat, gslon, gselev)
        tle1 = "1 07530U 74089B   15207.90021439 -.00000041  00000-0  17621-4 0  9993"
        tle2 = "2 07530 101.5250 182.2818 0011540 224.6195 190.1591 12.53615505862231"
        freq = "145.972"
        self.orbit_calc.SatInfo(
            'NOAA18',
            tle1,
            tle2,
            freq
        )

    def aos_los_display(self):
        sataz, satalt, satfreq, risetime, settime, mel = self.orbit_calc.CalcObserve()
        print(str(risetime))
        print(str(settime))

    def start(self):
        sataz, satalt, satfreq, risetime, settime, mel = self.orbit_calc.CalcObserve()
        requests.get("http://localhost:10100/frequency/human/" + str(satfreq) + 'M')


if __name__ == '__main__':
    lat = '35.642923'
    lon = '139.748864'
    radio_control = RadioControl(gslat=lat, gslon=lon, gselev=30)
    radio_control.aos_los_display()
    while True:
        radio_control.start()
        sleep(1)
