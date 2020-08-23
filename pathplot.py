from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot

import settings
from objs import Ring


def create_path(ring):
    #get start/end coordinates from ring
    start_lat = ring.start_point.lat
    start_lon = ring.start_point.lon
    
    end_lat = ring.end_point.lat
    end_lon = ring.end_point.lon
    
    #calculate antipodes
    ant1lon=start_lon+180
    if ant1lon>360:
        ant1lon= ant1lon - 360
    ant1lat=-start_lat
    ant2lon=end_lon+180
    if ant2lon>360:
        ant2lon= ant2lon - 360
    ant2lat=-end_lat

    #create path name
    name = str(start_lon) + " " + str(ring.azim)
    
    #create a line not a ring
    if settings.line == 1 or settings.line == 2:
        ring.paths[name]={'lon':[ start_lon, end_lon ], 
                          'lat':[ start_lat, end_lat ], 
                          'clr':'blue', 'dash':None}
    #create a ring
    else:
        #color = colors_main.pop(0)
        ring.paths[name]={'lon':[ start_lon, ant2lon, ant1lon, end_lon, start_lon ], 
                          'lat':[ start_lat, ant2lat, ant1lat, end_lat, start_lat ], 
                          'clr':'blue', 'dash':None}
    ring.num_paths += 1

    #show perpendicular hash marks to indicate width
    if settings.show_width == 1:
        i = 0
        for row in ring.perpendiculars:
            start_point = row[0]
            end_point = row[1]

            name = name + str(i)
            ring.paths[name]={'lon':[ start_point.lon, end_point.lon ], 
                              'lat':[ start_point.lat, end_point.lat ], 
                              'clr':'orange', 'dash':None}
            i += 1


def create_gc_globe(rings):
    DataDict=list()

    #loop through rings
    for ring in rings:
        #loop through paths for each ring
        for path in ring.paths.keys():
            #add path to dictionary for plotting
            DataDict.append(
                dict(
                    type = 'scattergeo',
                    lon = ring.paths[path]['lon'],
                    lat = ring.paths[path]['lat'],
                    name= path,
                    mode = 'lines',
                    line = dict(
                        width = 2.5,
                        color = ring.paths[path]['clr'],
                        dash= ring.paths[path]['dash'],
                    ),
                    opacity = 1.0,
                )
            )

    #set up globe data
    figdata={}
    figdata['data']=DataDict

    projs=['hammer','mercator','azimuthal equal area','orthographic']
    projtype=projs[3]

    figdata['layout'] = dict(
        title = 'Great Circle Segments',
        showlegend = False,
        geo = dict(
            scope='world',
            projection= dict(type=projtype,rotation = dict( lon = -100, lat = 40, roll = 0)),
            showland = True,
            showcountries=True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)'
        ),
    )
    
    plot(figdata)
