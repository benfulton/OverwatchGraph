import json
import OverwatchGraph
import numpy
from math import exp
import MySQLdb

conn = MySQLdb.connect(host = '127.0.0.1',user = 'overwatch', passwd = 'pharmercy',db = 'overwatch')
cursor = conn.cursor()

cursor.execute("""select json from statistics""")
players = cursor.fetchall()
quickplay = (json.loads(p[0])['heroes']['stats']['quickplay'] for p in players)
syms = [q['symmetra']['general_stats'] for q in quickplay if 'symmetra' in q]


#print("Wins,Damage/10m,Eliminations/10m,Wins/10m")
#for s in syms:
#    print(s['games_won'], OverwatchGraph.damage(s), OverwatchGraph.eliminations(s), OverwatchGraph.wins(s))

dd = (OverwatchGraph.damage(s) for s in syms)
d = sorted((x for x in dd if x > 100), reverse=True )
rank = numpy.array(range(1,len(d)+1))
damage = numpy.array(d)
f = numpy.polyfit(numpy.log(rank), damage, 1)
print("y ≈ %s log(x) + %s" % tuple(f))
y = 4515
x = exp((y - f[1])/f[0])
print("Estimated rank for %s damage is %s" % (y,x))
for d in damage:
    print(d)


