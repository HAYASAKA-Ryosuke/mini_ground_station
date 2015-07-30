#!coding:utf-8

import ephem
import math
import datetime

ENCODING = 'utf-8'

degreeconv = 180/math.pi
#
home = ephem.Observer()
#home.lat = '43.134694'
home.lat = '35.646266'
#home.lon = '141.248194'
home.lon = '139.753218'
home.elev = 50
#home.lat='43.066438'
#home.lon='141.300925'

#home.lat='43.579953888889'
#home.lon='141.998324722222'
#1 25544U 98067A   12366.89848378  .00006715  00000-0  11734-3 0  9373
#2 25544  51.6460 219.3718 0016515 109.6991  15.4155 15.51833175808723
#calctime_utc=datetime.datetime(2013,11,23,0,0)
calctime_utc = datetime.datetime.now()
satresult = []


class Orbitcalc(object):
    C = 299792458
    _gslat = ''
    _gslon = ''
    _gselev = ''
    _satname = ''
    _tle1 = ''
    _tle2 = ''
    _frequency = ''

    def __init__(self, gslat, gslon, gselev):
        self._gslat = str(gslat)
        self._gslon = str(gslon)
        self._gselev = str(gselev)

    def SatInfo(self, satname, tle1, tle2, frequency):
        """
            衛星の基本情報を入力
        """
        self._satname = str(satname)
        self._tle1 = str(tle1)
        self._tle2 = str(tle2)
        self._frequency = str(frequency)

    def dopplershift(self, rangerate):
        """
            ドップラシフトの計算
        """
        #return math.sqrt(1-(V/c)**2)/(1-(V/c)*math.cos(theta))
        #http://stackoverflow.com/questions/18763484/wrong-range-rate-with-pyephem
        return (self.C/(self.C + rangerate))

    def CalcObserve(self):
        home = ephem.Observer()
        home.lat = self._gslat
        home.lon = self._gslon
        #home.date='2014/02/25 1:58:25.00'
        home.elev = int(self._gselev)
        sat = ephem.readtle(self._satname, self._tle1, self._tle2)
        sat.compute(home)
        sataz = math.degrees(sat.az)
        satalt = math.degrees(sat.alt)
        satlat = math.degrees(sat.sublat)
        satlon = math.degrees(sat.sublong)
        satfreq = float(self._frequency) * self.dopplershift(sat.range_velocity)
        risetime=ephem.localtime(sat.rise_time)
        settime=ephem.localtime(sat.set_time)
        return sataz, satalt, satfreq, risetime, settime, math.degrees(sat.transit_alt), satlat, satlon
