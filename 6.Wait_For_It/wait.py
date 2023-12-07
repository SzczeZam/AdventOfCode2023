import re
import sys
from functools import reduce

data = sys.argv[1]
flag = sys.argv[2] 

input_lines = [ re.findall(r'(\d+)', line) for line in open(data, "r")]

times = input_lines[0] if flag == '1' else ''.join(input_lines[0]) 
dists = input_lines[1] if flag == '1' else ''.join(input_lines[1]) 
print( times, dists )

ww = [len([s for s in range(0,int(times)) if (s*(int(times)-s)>int(dists))])]

#product = reduce(lambda x,y : x*y, ww)
print(ww)
#print(product)
