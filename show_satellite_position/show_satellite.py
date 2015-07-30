from mpl_toolkits.basemap import Basemap
from math import acos
from ephem import earth_radius
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from orbitcalc import Orbitcalc

map = Basemap(projection='cyl', resolution='l', lat_0=35, lon_0=139)
map.drawcoastlines()
map.drawcountries()
map.drawmapboundary()
#map.drawmeridians(np.arange(0, 360, 30))
#map.drawparallels(np.arange(-90, 90, 30))

x, y = map(0, 0)
point = map.plot(x, y, 'ro', markersize=5)[0]


def init():
    point.set_data([], [])
    return point,


# animation function.  This is called sequentially
def animate(i):
    orbitcalc = Orbitcalc(gslat=35.642923, gslon=139.748864, gselev=10)
    orbitcalc.SatInfo(
        'noaa',
        '1 25544U 98067A   15211.20457631 -.00000889  00000-0 -59643-5 0  9997',
        '2 25544  51.6434 229.2321 0001100  14.6538  72.7124 15.54918601954736',
        '437.458'
    )
    sataz, satalt, satfreq, risetime, settime, transit_alt, lat, lon  = orbitcalc.CalcObserve()
    #if lon < 0:
    #    lon = 360 + lon
    #if lat < 0:
    #    lat = -1 * lat
    print(lon, lat)
    x, y = map(lon, lat)
    point.set_data(x, y)
    return point,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=20, interval=500, blit=True)

plt.show()
