#!coding:utf-8
import requests
from time import sleep
from orbitcalc import Orbitcalc
from ast import literal_eval


class RadioControl:
    def __init__(self, sat_name, gslat, gslon, gselev, tle1, tle2, freq):
        self.orbit_calc = Orbitcalc(gslat, gslon, gselev)
        self.orbit_calc.SatInfo(
            sat_name,
            tle1,
            tle2,
            freq
        )

    def aos_los_display(self):
        sataz, satalt, satfreq, risetime, settime, mel, lat, lon = self.orbit_calc.CalcObserve()
        print('AOS:' + str(risetime) + ' LOS:' + str(settime))

    def set_gain(self):
        content = requests.get("http://localhost:10100/gain/list").content
        requests.get("http://localhost:10100/gain/" + str(literal_eval(content.decode())['gains'][-1]))

    def start(self):
        sataz, satalt, satfreq, risetime, settime, mel, lat, lon = self.orbit_calc.CalcObserve()
        print('AZ:' + str(sataz) + ' EL:' + str(satalt))
        print(satfreq)
        requests.get("http://localhost:10100/frequency/human/" + str(satfreq) + 'M')
        print(requests.get("http://localhost:10100/state").content)


if __name__ == '__main__':
    sat_name = 'PRISM'
    lat = '35.642923'
    lon = '139.748864'
    elev = 5
    tle1 = "1 28895U 05043F   15227.77024120  .00000352  00000-0  77356-4 0  9996"
    tle2 = "2 28895  97.8220  52.4330 0018449 107.0638 253.2587 14.62865866522306"
    #freq = "437.345"
    freq = "80"
    radio_control = RadioControl(sat_name, lat, lon, elev, tle1, tle2, freq)
    radio_control.aos_los_display()
    radio_control.set_gain()
    while True:
        radio_control.start()
        sleep(1)
