#******************************************************************************************************************************
# Given an input file containing flight paths, this script calculates the optimal sequence of jet streams the swallow should fly  
# on to minimize his energy consumption throughout the entire flight. 
#
# > python optimal_path.py -f flight_paths.txt
#
# Output: a list of tuples denoting the jet streams' endpoints and mininum total energy
#*******************************************************************************************************************************

import argparse
from operator import itemgetter

# Read command line args
parser = argparse.ArgumentParser(description='Calculate flight plan and total energy from flight path provided in text file.')
parser.add_argument('-f','--file', help='Tab-delimited text file',required=True)
args = parser.parse_args()
#get file names from command line
file_name = args.file

flight_paths = []
energy_per_mile = 0

with open(file_name, "r") as f:
    for index, line in enumerate(f):   
        
        if index == 0:
            #first line in the file is the constant energy it takes to fly 1 mile WITHOUT jet streams
            energy_per_mile = int(line)
        else:
            #convert each subsequent line to integer array and append to flight_paths array
            flight_paths.append(map(int, line.strip().split(' ')))

#sort flight_paths by start mile marker (first item in each inner array)
flight_paths_sorted = sorted(flight_paths, key=itemgetter(0))


#*************************************
# calculate flight plan and minimun total energy needed to travel the distance
# (assuming that two jet streams cannot start at the same mile marker)
#
# start mile marker = path[0]
# end mile marker = path[1]
# energy to travel the distance = path[2]
#*************************************
end_mile = 0
flight_plan = [] #list of flight paths that use the least amount of energy 
total_energy = 0

for i, path in enumerate(flight_paths_sorted):

    start_mile = path[0]
     
    #append the first flight path in the list and set end mile marker for the path
    if i == 0:
        flight_plan.append(path)
        end_mile = path[1]
        #if start_mile is not 0, calculate energy to get to the start mile without jet stream
        #then add the distance energy
        total_energy = start_mile*energy_per_mile + path[2]
 
    #note: end_mile was set in previous path
    if start_mile >= end_mile:
        flight_plan.append(path)
        #miles without jet stream
        no_stream_distance = start_mile - end_mile
        #add to total energy without jet stream
        total_energy = total_energy + energy_per_mile * no_stream_distance
        
        #now set end_mile to current path's end mile marker
        end_mile = path[1]

        distance_energy = path[2]
        total_energy = total_energy + distance_energy

    
    

print "Flight Plan: ", flight_plan
print "Total Energy: ", total_energy
