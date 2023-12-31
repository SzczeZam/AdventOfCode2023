import sys
import re

data = sys.argv[1]
#flag = sys.argv[2] 

input_lines = [ line for line in open(data, "r")]
map_lists = re.split(r'.*?:\n?\s?', "".join(input_lines))[1:]

numeral_list = []
for values in map_lists:
    lines = filter(str.strip, re.split(r'\n', values))
    x = [ re.split(r'\s', line) for line in lines ]
    numeral_list.append(x) 

seeds = numeral_list[0]
seed_to_soil = numeral_list[1]
soil_to_fert = numeral_list[2]
fert_to_water = numeral_list[3]
water_to_ligth = numeral_list[4]
light_to_temp = numeral_list[5]
temp_to_humid = numeral_list[6]
humid_to_loc = numeral_list[7]

def traverse_map(init_val, to_map):
    out_value = int(init_val)
    in_num = int(init_val)
    for row in to_map:
        m = [ int(column) for column in row ]
        if in_num >= m[1] and in_num < m[1]+m[2]:  
            out_value = (in_num - m[1]) + m[0]
    return out_value

def seed_to_loc(seed, map_list):
    cur = int(seed)
    for tmlist in map_list:
        val = traverse_map(cur, tmlist)
        cur = val
    print("SEED: "  + str(seed))
    return cur 

#for item in numeral_list:
#    print(item)

print("seeds: ",seeds)
seed_ranges = [ (seeds[0][i], seeds[0][i+1]) for i in range(0,len(seeds[0]),2) ]

print("searching...")
locations = []
for r_pair in seed_ranges:
    start = int(r_pair[0])
    end = start + int(r_pair[1]) 
    for value in range(start,end):
        out = seed_to_loc(value,numeral_list[1:])
        locations.append(out)

#locations = [ seed_to_loc(seed,numeral_list[1:]) for seed in total_seeds]
print(locations)
print(min(locations))

#print(map_lists)
