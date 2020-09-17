#!/usr/bin/env python3

import csv
import multiprocessing
import os
import sys
import time

import pandas as pd

sys.path.insert(1, os.getcwd() + "/code/")
import settings
from objs import Point, Ring
from pathgen import generate_gc, ring_check
from pathplot import create_gc_globe, create_path
from rasterpop import calculate_shadow


def main():
    settings.init()

    start_time = time.time()

    print("================== Orbital Ring Population Counter ==================")
    print("Processes count: " + str(settings.num_procs))

    finished_rings = []
    lines = []

    proc_cmd_args()

    # 0 = run all permutations, lat lon azim
    # 1 = run experiment file, lat lon azim
    # 2 = run experiment file, lat1 lon1 to lat2 lon2
    # 3 = run city file, city azim
    if settings.experiment_type != 0:
        file = open(settings.experiment_file_name, "r")
        lines = file.readlines()
        file.close()

    if settings.experiment_type == 0:
        print("Run Full Experiment")
        settings.calculate_population = 1
        finished_rings = []
        run_full_experiment()
        # results are saved in the run function
        settings.save_results = 1

    elif settings.experiment_type == 1:
        print("Run Lat-Lon-Azim File")
        finished_rings = run_azim_file(lines)

        if settings.save_results == 1:
            save_results(finished_rings)

    elif settings.experiment_type == 2:
        print("Run Lat1/Lon1-Lat2/Lon2 File")
        finished_rings = run_lat2_file(lines)

        if settings.save_results == 1:
            save_results(finished_rings)

    elif settings.experiment_type == 3:
        print("Run City File")
        finished_rings = run_city_file(lines)

        if settings.save_results == 1:
            save_results(finished_rings)

    if settings.show_globe == 1:
        for ring in finished_rings:
            create_path(ring)

        create_gc_globe(finished_rings)

    if settings.analyze_results == 1:
        analyze_results(finished_rings)

    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print("Total Time: %.2f min\n" % (elapsed_time))

    if settings.save_results != 1 and elapsed_time > 10:
        answer = input("Would you like to save the results? yes/no: ")

        if answer != "no":
            save_results(finished_rings)


def save_results(rings):
    index_pops = []

    df = pd.DataFrame(columns=settings.headers_with_countries)

    for ring in rings:
        # save the general parameters of particular ring
        next_row = [
            ring.start_point.lat,
            ring.start_point.lon,
            ring.azim,
            ring.end_point.lat,
            ring.end_point.lon,
            ring.resolution,
            ring.width,
            ring.path_calculation_time,
            ring.population_calculation_time,
            (ring.path_calculation_time + ring.population_calculation_time),
            ring.population,
        ]

        # save the populations in each country under the ring
        for country in settings.country_codes:
            if country in ring.country_pop:
                next_row.append(ring.country_pop[country])
            else:
                next_row.append(0)

        df.loc[len(df)] = next_row

        pops_list = []

        pops_list.extend(
            [ring.start_point.lat, ring.start_point.lon, ring.azim, ring.width]
        )

        for pop in ring.index_pops:
            pops_list.append(pop[1])

        index_pops.append(pops_list)

    popcount_name = "popcount_" + str(int(rings[0].width / 1000)) + "km"

    f = open("./results/" + popcount_name + ".csv", "a")
    df.to_csv(f, mode="a", header=f.tell() == 0)
    f.close()

    poplines_name = (
        str(rings[0].start_point.lon)
        + "_lon_poplines_"
        + str(int(rings[0].width / 1000))
        + "km"
    )

    print("Results Saved\n")


def analyze_results(rings):
    print("Analyzing Results")

    df = pd.DataFrame(
        columns=[
            "Start_Lat",
            "Start_Lon",
            "Azim",
            "End_Lat",
            "End_Lon",
            "Resolution",
            "Width",
            "Population",
            "Path_Time",
            "Pop_Time",
            "Total_Time",
        ]
    )

    for ring in rings:

        df.loc[len(df)] = [
            ring.start_point.lat,
            ring.start_point.lon,
            ring.azim,
            ring.end_point.lat,
            ring.end_point.lon,
            ring.resolution,
            ring.width,
            ring.population,
            ring.path_calculation_time,
            ring.population_calculation_time,
            (ring.path_calculation_time + ring.population_calculation_time),
        ]


def processes_ring(line):
    ring = Ring(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])

    ring_check(ring)

    if settings.calculate_population == 1:
        generate_gc(ring)
        calculate_shadow(ring)
        ring.points = []

    return ring


def run_full_experiment():
    resolution = 4000
    interval = 100000
    width = 50000

    for lon in range(0, 180):
        finished_rings = []
        proc_args = []

        for azim in range(90, -90, -1):
            proc_args.append([0, lon, azim, 0, 0, resolution, width, interval])

        pool = multiprocessing.Pool(processes=settings.num_procs)

        finished_rings = pool.map(processes_ring, proc_args)

        pool.close()

        save_results(finished_rings)


def run_city_file(lines):
    finished_rings = []
    proc_args = []

    for line in lines:
        if line == "\n":
            continue
        if line[0] == "#":
            continue

        words = line.split(" ")

        # lat long azim resolution width interval
        start_lat = float(words[0])
        start_lon = float(words[1])
        resolution = int(words[2])
        width = int(words[3])
        interval = int(words[4])

        for azim in range(90, -90, -1):
            proc_args.append(
                [start_lat, start_lon, azim, 0, 0, resolution, width, interval]
            )

    pool = multiprocessing.Pool(processes=settings.num_procs)

    finished_rings = pool.map(processes_ring, proc_args)

    return finished_rings


def run_azim_file(lines):
    finished_rings = []
    proc_args = []

    for line in lines:
        if line == "\n":
            continue
        elif line[0] == "#":
            continue

        words = line.split(" ")

        # lat long azim resolution width interval
        start_lat = float(words[0])
        start_lon = float(words[1])
        azim = float(words[2])
        resolution = int(words[3])
        width = int(words[4])
        interval = int(words[5])

        proc_args.append(
            [start_lat, start_lon, azim, 0, 0, resolution, width, interval]
        )

    pool = multiprocessing.Pool(processes=settings.num_procs)

    finished_rings = pool.map(processes_ring, proc_args)

    return finished_rings


def run_lat2_file(lines):
    proc_args = []
    finished_rings = []

    for line in lines:
        if line == "\n":
            continue
        elif line[0] == "#":
            continue

        words = line.split(" ")

        # lat1 long1 lat2 long2 resolution width interval
        start_lat = float(words[0])
        start_lon = float(words[1])
        end_lat = float(words[2])
        end_lon = float(words[3])
        resolution = int(words[4])
        width = int(words[5])
        interval = int(words[6])

        proc_args.append(
            [start_lat, start_lon, -99, end_lat, end_lon, resolution, width, interval]
        )

    pool = multiprocessing.Pool(processes=settings.num_procs)

    finished_rings = pool.map(processes_ring, proc_args)

    return finished_rings


def proc_cmd_args():
    # process command line args

    # command line arguments

    # Specifying Rings in a File
    # -f file.txt  : calculate rings with start lat/lon and azim
    # -F file.txt  : calculate rings with start lat/lon and end lat/lon
    # -c file.txt  : calculate rings with a city's lat/lon **
    # default 	   : if no file is specified, the default will calculate
    # 				 longitudes 0-179 by 1 degree increments, with azimuths
    # 			     90 to -90 by -1 degree increments, default excludes
    # 				 showing rings on a globe

    # Showing Rings on a Globe
    # User must specify rings in a file to show on globe
    # -g           : show globe containing rings in specified file
    # -w 		   : show perpendicular width hashes on globe rings

    # Special commands
    # -l length    : calulate for a line of specified length, not a ring,
    # 				 only works with -f
    # -L 		   : calculate for a line, only works with -F

    # -p 		   : calculate the population of the specified rings or lines
    # -a 		   : analyze results of a simulation
    # -s out.txt   : save results of a simulation, will prompt to save
    # 			     if calculation time is longer than 10 minutes

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-f":
            if len(sys.argv) == i + 1 or sys.argv[i + 1][0] == "-":
                print("Command line error: -f ringfile.txt")
                sys.exit()
            settings.experiment_file_name = sys.argv[i + 1]

            # 1 = run experiment file, lat lon azim
            settings.experiment_type = 1

        if sys.argv[i] == "-F":
            if len(sys.argv) == i + 1 or sys.argv[i + 1][0] == "-":
                print("Command line error: -F ringfile.txt")
                sys.exit()
            settings.experiment_file_name = sys.argv[i + 1]

            # 2 = run experiment file, lat1 lon1 to lat2 lon2
            settings.experiment_type = 2

        if sys.argv[i] == "-c":
            if len(sys.argv) == i + 1 or sys.argv[i + 1][0] == "-":
                print("Command line error: -c cityfile.txt")
                sys.exit()
            settings.experiment_file_name = sys.argv[i + 1]

            # 3 = run all permutations, city file
            settings.experiment_type = 3

        if sys.argv[i] == "-l":
            if len(sys.argv) == i + 1 or sys.argv[i + 1][0] == "-":
                print("Command line error: -l length")
                sys.exit()
            if settings.experiment_type != 1:
                print("Command line error: -l length only works with -f ringfile.txt")
            settings.earth_circ = int(sys.argv[i + 1])

            # 1 == create line with length
            settings.line = 1

        if sys.argv[i] == "-L":
            if settings.experiment_type != 2:
                print("Command line error: -L length only works with -F ringfile.txt")

            # earth_circ is calculated after opening the file

            # 2 == create line with 2 lats/lons
            settings.line = 2

        if sys.argv[i] == "-g":
            settings.show_globe = 1

        if sys.argv[i] == "-w":
            settings.calculate_population = 1
            settings.show_width = 1

        if sys.argv[i] == "-p":
            settings.calculate_population = 1

        if sys.argv[i] == "-a":
            settings.analyze_results = 1

        if sys.argv[i] == "-s":
            settings.save_results = 1
            settings.calculate_population = 1


main()
