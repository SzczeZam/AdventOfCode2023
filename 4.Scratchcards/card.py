import re
import sys

data = sys.argv[1]
#flag = sys.argv[2] 

input_lines = [ line for line in open(data, "r")]
value_list = [[filter(str.strip, res[0].split(' ')), filter(str.strip, res[1].split(' '))] for li in input_lines for res in re.findall(r'\d:\s(.*)\s\|\s(.*)', li)]
    
t_list = [ set(card[0]) & set(card[1]) for card in value_list]
win_amount_list = [ len(i) for i in t_list ]

#    points = []
#    for wins in win_amount_list:
#        value = 1 if wins > 0 else 0 
#        for win in range(0,wins-1):
#            print(value)
#            value=value*2
#        points.append(value)


cards = [1 for card in input_lines]
for card in range(0, len(cards)):
    print(f"card {card + 1}:{win_amount_list[card]} wins")
    winwin = win_amount_list[card]
    for won_cards in range(0,cards[card]):
        for i in range(1,win_amount_list[card]+1):
            ind = card+i
            print(f"adding one to card {ind+1} : {cards[ind]} +1 ")
            cards[ind] = cards[ind] + 1

print(cards)
print(len(win_amount_list))
#print(len(points))
#print(sum(points))
print(sum(cards))
