from mpl_toolkits.basemap import Basemap
from math import acos, pi, cos, sin
from datetime import datetime
from ephem import earth_radius
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import matplotlib.animation as animation
from orbitcalc import Orbitcalc

base_map = Basemap(projection='cyl', resolution='c', lat_0=35, lon_0=139)
base_map.drawcoastlines()
base_map.drawcountries()
base_map.drawmapboundary(fill_color='aqua')
base_map.fillcontinents(color="coral", lake_color="aqua")
base_map.nightshade(datetime.utcnow())
base_map.drawcoastlines(linewidth=0.5)
#map.drawmeridians(np.arange(0, 360, 30))
#map.drawparallels(np.arange(-90, 90, 30))

x, y = base_map(0, 0)
point = base_map.plot(x, y, 'ro', markersize=5)[0]
point2 = base_map.plot(x, y, 'ro', markersize=5)[0]
ax = plt.gca()


def init():
    point.set_data([], [])
    return point,

def init2():
    point2.set_data([], [])
    return point2,

def VisibilityDistance(elev):
    er = earth_radius / 1000
    xd = acos(er / (elev + er))
    return er * xd

def distance_to_lon(distance):
    return 0.00027778 * distance / 31.0

def distance_to_lat(distance):
    return acos(distance /(2 * 6378150 * pi / (360 * 60 * 60)))


def Circle(lon, lat, r):
    T = 100
    x, y = [0] * T, [0] * T
    print(VisibilityDistance(r))
    for i, theta in enumerate(np.linspace(0, 2 * np.pi, T)):
        visibility_distance = VisibilityDistance(r)
        # x[i] = lon + distance_to_lon(visibility_distance) / 1000 * np.cos(theta) / earth_radius
        y[i] = lat + (VisibilityDistance(r) * cos(theta) /earth_radius)
        x[i] = lon + (VisibilityDistance(r) * sin(theta) / (earth_radius * cos(y[i])))
        # y[i] = lat + distance_to_lat(visibility_distance) / 1000 * np.sin(theta)
    return x, y


# animation function.  This is called sequentially
def animate(i):
    orbitcalc = Orbitcalc(gslat=35.642923, gslon=139.748864, gselev=10)
    orbitcalc.SatInfo(
        'iss',
        '1 25544U 98067A   15217.18521942  .00005825  00000-0  92225-4 0  9992',
        '2 25544  51.6435 199.3767 0001224  47.2704  61.2586 15.55004724955663',
        '437.458'
    )
    sataz, satalt, satfreq, risetime, settime, transit_alt, lat, lon  = orbitcalc.CalcObserve()
    #if lon < 0:
    #    lon = 360 + lon
    #if lat < 0:
    #    lat = -1 * lat
    x, y = base_map(lon, lat)
    print(lon, lat)
    point.set_data(x, y)
    cx, cy = Circle(x, y, 30)
    point2.set_data(cx, cy)
    return point2,

def animate2(i):
    orbitcalc = Orbitcalc(gslat=35.642923, gslon=139.748864, gselev=10)
    orbitcalc.SatInfo(
        'iss',
        '1 25544U 98067A   15217.18521942  .00005825  00000-0  92225-4 0  9992',
        '2 25544  51.6435 199.3767 0001224  47.2704  61.2586 15.55004724955663',
        '437.458'
    )
    sataz, satalt, satfreq, risetime, settime, transit_alt, lat, lon  = orbitcalc.CalcObserve()
    if lat < 0:
        lat = 360 - lat
    x, y = base_map(lon, lat)
    cx, cy = Circle(x, y, 20)
    point2.set_data(cx, cy)
    return point2,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=20, interval=500, blit=False)
anim = animation.FuncAnimation(plt.gcf(), animate2, init_func=init2,
                               frames=20, interval=500, blit=False)
plt.show()
