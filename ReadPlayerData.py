import pandas as pd
import json
from urllib.request import Request, urlopen
import urllib
import time
import tarfile
import MySQLdb
import argparse
import dateutil
from operator import attrgetter

conn = MySQLdb.connect(host = '127.0.0.1',user = 'overwatch', passwd = 'pharmercy',db = 'overwatch')
cursor = conn.cursor()

cursor.execute("""select battletag from statistics""")
players = [p[0] for p in cursor.fetchall()]

def request_player(battletag):
    q = Request("https://owapi.net/api/v3/u/%s/heroes" % battletag)
    q.add_header('User-Agent', 'Mozilla/5.0')
    return json.loads(urlopen(q).read().decode())


def from_tar(datafile):
    tar = tarfile.open(datafile)
    files = sorted((t for t in tar if t.name.endswith('json')), key=attrgetter('name'))

    for tarinfo in files:
        t = tar.extractfile(tarinfo)
        try:
            dt = dateutil.parser.parse(tarinfo.name[19:27])
            d = json.load(t)
            cursor.execute(
                """INSERT INTO statistics (battletag, json, created_at, updated_at) VALUES (%s,%s, %s, sysdate())""",
            ("Syzygy-11715", json.dumps(d['us']), dt))
        except (AttributeError, TypeError, KeyError):
            pass
    conn.commit()


def from_excel():
    xl = pd.ExcelFile("data/OverwatchTopPlayers.xlsx")
    print(xl.sheet_names)
    df = xl.parse("Symmetra")

    for battletag in df.loc[:, 'Player']:
        print(battletag)
        if battletag in players:
            continue

        try:
            player = request_player(battletag)

            cursor.execute(
                """INSERT INTO statistics (battletag, json, created_at, updated_at) VALUES (%s,%s, sysdate(), sysdate())""",
                (battletag, json.dumps(player['us'])))
            conn.commit()

            time.sleep(10)
        except urllib.error.HTTPError:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help='data file')
    args = parser.parse_args()
    from_tar(args.datafile)
