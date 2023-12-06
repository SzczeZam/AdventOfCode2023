import re
import sys

data = sys.argv[1]
#flag = sys.argv[2] 

input_lines = [ line for line in open(data, "r")]
value_list = [[filter(str.strip, res[0].split(' ')), filter(str.strip, res[1].split(' '))] for li in input_lines for res in re.findall(r'\d:\s(.*)\s\|\s(.*)', li)]
    
t_list = [ set(card[0]) & set(card[1]) for card in value_list]
win_amount_list = [ len(i) for i in t_list ]

points = []
for wins in win_amount_list:
    value = 1 if wins > 0 else 0 
    for win in range(0,wins-1):
        print(value)
        value=value*2
    points.append(value)

print(win_amount_list)
print(points)

print(sum(points))
