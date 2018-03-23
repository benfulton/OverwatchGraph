import tarfile
import sys
import json
import dateutil.parser
import matplotlib.pyplot as plt
import argparse

def main(datafile, hero):
    tar = tarfile.open(datafile)

    graph = dict()
    for tarinfo in tar:
        t = tar.extractfile(tarinfo)
        try:
            d = json.load(t)
            general = d['us']['heroes']['stats']['quickplay'][hero]['general_stats']
            damage = general['hero_damage_done']
            deaths = general['deaths']
            ten_minutes = general['time_played'] * 6
            dt = dateutil.parser.parse(tarinfo.name[19:27])
            graph[dt] = damage/ten_minutes
            # graph[dt] = deaths/ten_minutes
            # print(date.date(), damage/ten_minutes, deaths/ten_minutes)
        except (AttributeError, TypeError):
            pass

    dates = sorted(graph.keys())
    values = [graph[dt] for dt in dates]
#    plt.ylim(0,20)
    plt.suptitle(hero + " damage")
    plt.plot_date(dates, values, linestyle='solid', marker='None')
    plt.grid(True)
    plt.show()

    tar.close()

#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hero', help='hero to display')
    parser.add_argument('datafile', help='data file')
    args = parser.parse_args()
    main(args.datafile, args.hero)

