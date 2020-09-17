# Orbital Ring Population Calculator

![North America](/images/north_america.png)

An orbital ring is a space mega-structure similar to a space elevator.  Orbital rings are active support structures where a metal 'ring' is spinning around the earth at orbital speeds while platforms are magnetically supported above the ring and are not in orbit, they are stationary to the ground.  Cables can be dropped to the ground for moving people and goods up into low orbit.  [See the video that inspired this project.](https://www.youtube.com/watch?v=LMbI6sk-62E)

This program can display a specified ring on a globe, calculate the population under a ring, and calculate all possible rings to determine which ring would maximize the population under it.

The program was tuned to maximize parallel computation and the resolution of the population raster was tested to calculate the most accurate population in the least amount of time.

## Installation

This program uses [GeographicLib](https://geographiclib.sourceforge.io/html/install.html) which has several install options.

This installation works on macOS Catalina 10.15.6 and a conda enviornment.

```bash
brew install geographiclib
pip install -r requirements.txt
```
![North America](/images/world_top.png)

## Usage

orbital_ring.py can run two types of files:
* -f : latitude, longitude, azimuth files, starts on equator to specify ring
* -F : lat1, lon1, lat2, lon2 files, specify ring from two points

Below are quickstart examples make with ring_files created by the author.

```bash
python3 orbital_ring.py -f ./ring_files/usa_top_1.txt -g
python3 orbital_ring.py -f ./ring_files/usa_top_10.txt -g

python3 orbital_ring.py -f ./ring_files/world_top_1.txt -g
python3 orbital_ring.py -f ./ring_files/world_top_10.txt -g
python3 orbital_ring.py -f ./ring_files/world_top_100.txt -g

python3 orbital_ring.py -f ./ring_files/world_worst_30.txt -g
```

Below is a ring_file that specifies a ring from two points and calculates the population underneath.  The -L flag limits the ring to between the two points, not around the globe, and the -p flag calculates the population.  This file was used to test the accuracy of the population calculator by calculating the population of a line segment over New Zealand.

```bash
python3 orbital_ring.py -F ./ring_files/new_zealand_line.txt -g -L -p
```
![North America](/images/middle_east_width.png)

# More Program Commands
    -f file.txt  : calculate rings with start lat/lon and azim
    -F file.txt  : calculate rings with start lat/lon and end lat/lon
    -c file.txt  : calculate rings with a city's lat/lon **
    default      : if no file is specified, the default will calculate longitudes 0-179
                   by 1 degree increments, with azimuths 90 to -90 by -1 degree increments 
                   default excludes showing rings on a globe

# Showing Rings on a Globe
    -g           : show globe containing rings in specified file
    -w           : show perpendicular width hashes on globe rings

# Special commands
    -l length    : calculate for a line of specified length, not a ring, only works with -f
    -L           : calculate for a line, only works with -F

    -p           : calculate the population of the specified rings or lines
    -s out.txt   : save results of a simulation, will prompt to save
                   if calculation time is longer than 10 minutes

![North America](/images/south_america.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
