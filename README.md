# Orbital_Ring_Population_Calulator
Display maps of orbital rings, calculate populations under a ring, calculate the ring with max population underneath.  Update.

Update 2.

brew install geographiclib

python3 orbital_ring.py -F ./ring_files/new_zealand_line.txt -g -L

% python3 orbital_ring.py -f ./ring_files/usa_top_1.txt -g
% python3 orbital_ring.py -f ./ring_files/usa_top_10.txt -g

% python3 orbital_ring.py -f ./ring_files/world_top_1.txt -g
% python3 orbital_ring.py -f ./ring_files/world_top_10.txt -g
% python3 orbital_ring.py -f ./ring_files/world_top_100.txt -g

% python3 orbital_ring.py -f ./ring_files/world_worst_30.txt -g


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