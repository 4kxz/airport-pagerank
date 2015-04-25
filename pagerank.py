from collections import defaultdict
import csv

airports = defaultdict(set)
cols = 'air,airid,src,srcid,dst,dstid,code,stops,eqp'
with open('data/routes.dat') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=cols.split(','))
    for row in reader:
        airports[row['src']].add(row['dst'])

D = 0.85
pageranks = defaultdict(lambda: 1 / len(airports))
for i in range(100):
    p = 0
    q = defaultdict(float)
    for src, flights in airports.items():
        if len(flights) > 0:
            x = pageranks[src] / len(flights)
            for dst in flights:
                q[dst] += x
        else:
            p += pageranks[src]
    p /= len(airports)
    x = (1 - D) / len(airports)
    for src in airports:
        pageranks[src] = x + (q[src] + p) * D

ranking = sorted(pageranks.items(), key=lambda x: x[1], reverse=True)
line = '{:04},{x[0]},{x[1]:.10f}'
for i, x in enumerate(ranking):
    print(line.format(i, x=x))
