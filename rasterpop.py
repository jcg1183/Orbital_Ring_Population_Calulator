import math
import time

import numpy as np
import rasterio
import reverse_geocoder as rg

import settings


def calculate_shadow(ring):
    start_time = time.time()

    population = 0

    # Open and prepare population raster
    raster = rasterio.open("../pop_data/2020pop2.5min.tif")
    band1 = raster.read(1)

    # remove negative values from population raster
    band1[band1 < 0] = 0

    # shadow raster has 0 in cells which are not under the ring
    # and has a 1 for cells under the ring
    shadow = np.zeros(shape=band1.shape, dtype=int)

    # loop through each list of perpendicular points in ring.points
    for index, perp_points in ring.points:
        index_population = 0

        # loop through points in the list of perpendicular points
        for point in perp_points:
            # calculate raster coordinates from lat/lon
            y, x = raster.index(point.lon, point.lat)

            # check to see if multiple lat/lon points to same raster cell
            if shadow[y, x] == 0:
                coordinates = (point.lat, point.lon)

                # determine which country each coordinate pair is in
                results = rg.search(coordinates, mode=1)

                # add the population to the country population totals
                if results[0]["cc"] in ring.country_pop:
                    ring.country_pop[results[0]["cc"]] += band1[y, x]
                else:
                    ring.country_pop[results[0]["cc"]] = band1[y, x]

                # add the population of each cell to the population under the
                # perpendicular
                index_population += band1[y, x]

            # mark the cell as visited
            shadow[y, x] = 1

        # add the index coordinates and perpendicular population to the
        # list of perpendicular populations
        ring.index_pops.append([index, index_population])

    raster.close()

    # multiply the shadow raster with the population raster.  Shadow raster
    # cells with a 0 will cancel out the population not under the ring
    shadow_pop = np.multiply(band1, shadow)

    # sum the raster to calculate total population under the ring
    population = np.sum(shadow_pop)

    ring.population = population

    print(
        "Lat %.4f Lon %.4f Azim %.4f - %.2f mil pop"
        % (
            ring.start_point.lat,
            ring.start_point.lon,
            ring.azim,
            float(population / 1000000),
        )
    )

    end_time = time.time()

    ring.population_calculation_time = end_time - start_time

