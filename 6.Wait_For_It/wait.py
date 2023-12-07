import re
import sys
from functools import reduce

data = sys.argv[1]
#flag = sys.argv[2] 

input_lines = [ re.findall(r'(\d+)', line) for line in open(data, "r")]

times = input_lines[0]
dists = input_lines[1]

ww = [len([s for s in range(0,int(times[t])) if (s*(int(times[t])-s)>int(dists[t]))]) for t in range(0,len(times))]
product = reduce(lambda x,y : x*y, ww)
print(ww)
print(product)
