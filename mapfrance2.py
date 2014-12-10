import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from mpl_toolkits.basemap import Basemap
from pandas import Series, DataFrame

from matplotlib.collections import LineCollection
from matplotlib import cm
import shapefile

plt.ion() #enable figure interactive mode
plt.close('all')

treattype = 1
if(treattype == 1):    #full
    nmax = 16
    shorten = 1
    shortenstep = 5
    inc_deps = 1
    inc_roads = 1
    informative = 1  #marker size and color are variable
    map_res = 'h'
elif(treattype == 2):   #medium
    nmax = 8
    shorten = 1
    shortenstep = 5
    inc_deps = 1
    inc_roads = 1
    informative = 1  #marker size and color are variable
    map_res = 'h'
else:                  #short
    nmax = 3
    shorten = 1
    shortenstep = 10
    inc_deps = 0
    inc_roads = 0
    informative = 1  #marker size and color are variable
    map_res = 'l'

ac_data = DataFrame()
for i in range(1,nmax+1):
    print "Reading out_short_ok_%i" % i
    ac_data_part = pd.read_csv('out_short_ok_'+ str(i) +'.csv')
    ac_data = pd.concat([ac_data, pd.DataFrame(ac_data_part)])
    [n1,n2]=ac_data.shape
    print ("Full array has %i lines %i columns\n" %(n1,n2))

#raise SystemExit


if(shorten):
    arr_len = ac_data.shape[0]
    ac_data = ac_data[0:arr_len:shortenstep]

lats = ac_data.latG
lons = ac_data.longG
gravs = ac_data.grav
lums = ac_data.lum
atms = ac_data.atm

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.

lllat = 40.0
urlat = 52.5
lllon = -10.0
urlon = 12.0
lat0 = (lllat+urlat)*0.5
lon0 = (lllon+urlon)*0.5

parsec1 = 44.0 #for lambert projection (Lambert93)
parsec2 = 49.0
lat0 = 46.5
lon0 = 3.0

# Lambert cc proj
m = Basemap(width=1200000,height=1200000,
            rsphere=(6378137.00,6356752.3142),\
            resolution=map_res,area_thresh=1000.,projection='lcc',\
            lat_1=parsec1,lat_2=parsec2,lat_0=lat0,lon_0=lon0)

#m.fillcontinents(color='coral',lake_color='aqua')
# m.fillcontinents(color='khaki',lake_color='aqua')
m.fillcontinents(color='#f4a460',lake_color='aqua')

plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)

#Let's create a basemap of Europe
x1 = lllon
x2 = urlon
y1 = lllat
y2 = urlat
m.drawcountries(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(y1,y2,2.5),labels=[1,0,0,0],color='black',dashes=[1,0],labelstyle='+/-',linewidth=0.2) # draw parallels
m.drawmeridians(np.arange(x1,x2,5.),labels=[0,0,0,1],color='black',dashes=[1,0],labelstyle='+/-',linewidth=0.2) # draw meridians

m.drawmapboundary(fill_color='aqua')


x, y = m(lons.values,lats.values)

if(informative):
    color_vec1 = ['k', 'b', 'g', 'y', 'r', 'm', 'c', 'w', 'c']
    color_vec2 = ['#fff5eb','#fee6ce','#fdd0a2','#fdae6b','#fd8d3c',
                     '#f16913','#d94801','#a63603','#7f2704'] #sequential, single hue orange
    color_vec3 = ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6',
                     '#4292c6','#2171b5','#08519c','#08306b'] #sequential, single hue blue
    color_vec4 = ['#d73027','#f46d43','#fdae61','#fee090','#ffffbf',
                     '#e0f3f8','#abd9e9','#74add1','#4575b4']  #diverging, colorb safe, use flipud
    color_vec5 = ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4',
                    '#1d91c0','#225ea8','#253494','#081d58']
    color_vec4 =  np.flipud(color_vec4)
    
    #colorvar = gravs; coltype = 1; color_vec  = color_vec2
    #colorvar = lums-1; coltype = 2; color_vec  = color_vec4
    colorvar = atms-1; coltype = 3; color_vec  = color_vec5
    g_max = colorvar.max()
    g_ave = colorvar.mean()
    g_std = colorvar.std()
    if(coltype==1):
        #grav
        sizfact = g_max/10
        sizfact = g_ave/1
        alpha_scl = 0.1 #grav
    elif(coltype==2):
        sizfact = g_ave/3
        alpha_scl = 0.1 #atm
    else:
        #lum
        sizfact = g_max/10
        sizfact = g_ave/2
        alpha_scl = 0.1 #atm

    pCnt = 0
    for x, y, g in zip(x,y,colorvar):
        
        if(not(pCnt%1000)): print pCnt

        if(coltype==1):
            ## grav
            if g > g_ave + 3*g_std:
                mark_col = 'r'
            else:
                mark_col = 'b'
        elif(coltype==2):
            mark_col = color_vec[g]  #atm or lum
        else:
            try:
                mark_col = color_vec[int(g)]  #atm or lum
            except TypeError as e:
                print "I/O error({0}) ".format(e.message)
                mark_col = 'w'
            except:
                print "Unexpected error:", sys.exc_info()[0]
                mark_col = 'w'
                #raise
        pCnt += 1
        m.plot(x, y, marker='.', markersize=g/sizfact, markerfacecolor=mark_col, linestyle='', alpha=0.1)
else:
    m.plot(x, y, 'k.', alpha=alpha_scl)

plt.show(block=False)



#### include department borders from shapefile -  http://www.gadm.org/ ####

def traceShape(file_shapefile):
    r = shapefile.Reader(file_shapefile)
    shapes = r.shapes()
    records = r.records()
    #sc_fac = 100000
    for record, shape in zip(records,shapes):
        #print shape.points
        lonsh,latsh = zip(*shape.points)
        # lonsh = [x/sc_fac for x in lonsh]
        # latsh = [x/sc_fac for x in latsh]
        data = np.array(m(lonsh, latsh)).T
     
        if len(shape.parts) == 1:
            segs = [data,]
        else:
            segs = []
            for i in range(1,len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])
     
        lines = LineCollection(segs,antialiaseds=(1,))
        # lines.set_facecolors(cm.jet(np.random.rand(1)))
        lines.set_edgecolors('k')
        lines.set_linewidth(0.1)
        ax.add_collection(lines)

    return None

dir_shapefile = 'SHP/'
if(inc_deps):
    file_shapefile = dir_shapefile + r"FRA_adm2.shp"
    traceShape(file_shapefile)

if(inc_roads):    
    file_shapefile = dir_shapefile + r"RoadL.shp"  #good
    ##too many roads - mapcruzin.com -OpenStreetMap data as of 2014-09-03T20:22:02Z courtesy of http://download.geofabrik.de
    #file_shapefile = dir_shapefile + r"roads.shp"  
    traceShape(file_shapefile)

filename = 'carteFrance_' + colorvar.name + '.png'
plt.savefig(filename,dpi=300)
plt.show()



