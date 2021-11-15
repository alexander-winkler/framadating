import csv
from itertools import product
from collections import Counter, defaultdict
from statistics import stdev
import numpy as np
from matplotlib import pyplot as plt
import re
import requests


counter = []
var_list = []
avail = {}

poll_id = False
service_url = "https://terminplaner4.dfn.de/exportcsv.php?poll="

if not poll_id:
    poll_id = input("Please insert Poll-ID: \n>>>\t")

# Fetch poll data

res = requests.get(service_url+poll_id)
csv_string = res.text.split('\n')[:-1]
    
reader = csv.reader(csv_string, delimiter=',')

date = next(reader)
time = next(reader)
header = [f"{d}, {t}" for d,t in zip(date,time)]


for r in reader:
    try:
        pers = r[0]
        avail[r[0]] = [header[n] for n,x in enumerate(r) if x.upper() in ["JA", "YES"]]
        print(pers,avail[r[0]])
    except Exception as e:
        print(e)
        

total_combinations = 0

for av in avail.values():
    if total_combinations == 0:
        total_combinations = len(av)
    else:
        total_combinations *= len(av)


# Gauge complete time of calculation

items_per_second = 20000

seconds = total_combinations / items_per_second
minutes = seconds / 60
hours = minutes / 60
days = hours / 24
years = days / 365.25


print(f"""There are about {total_combinations} possible combinations. We'd better reduce complexity, because it will take us around 

* {seconds} seconds
* {minutes} minutes
* {hours} hours
* {days} days
* {years} years

 to calcuate everything."""
 )


    
most_common_dates = Counter([item for sublist in avail.values()
    for item in sublist]).most_common()

most_common_dates = [x[0] for x in most_common_dates[::-1]]

avail = { k : v for k,v in sorted(avail.items(), key = lambda x:len(x[1]), reverse = False) }

for k,v in avail.items():
    avail[k] = [V for V in most_common_dates if V in v]
    
  
grouping = ""

for n,x in enumerate(product(*avail.values())):
    c = Counter(x)
    var = np.var(list(c.values()))
    if not grouping:
        grouping = (x,var)
        print(f"Initial variance: {var}")
        counter.append(n)
        var_list.append(var)
    elif var < grouping[1]:
        grouping = (x,var)
        print(f"new variance: {grouping[1]}")
        with open("teilnehmerliste.tsv","w") as OUT:
            for name,zahl in zip(avail.keys(),grouping[0]):
                print(f"{name}\t{zahl}",file = OUT)
            print("=====", file = OUT)
            for t,z in sorted(Counter(grouping[0]).items()):
                print(f"{t}\t{z}", file = OUT)
        counter.append(n)
        var_list.append(var)
        plt.plot(counter,var_list)



zeitplan = defaultdict(list)

for name,zahl in zip(avail.keys(),grouping[0]):
    zeitplan[zahl].append(name)



for tag,tn in sorted(zeitplan.items(), key = lambda x : (x[0].split('/')[1],x[0].split('/')[0]) ):
    print(f"\n\n# {tag}\n")
    tn = sorted(tn, key = lambda x: re.findall(r'\w+',x)[-1])
    for n,TN in enumerate(tn,1):
        print(f"{n}. {TN}")