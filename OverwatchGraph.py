import tarfile
import json
import dateutil.parser
import matplotlib.pyplot as plt
import argparse
from operator import attrgetter

def average(general, datapoint):
    try:
        damage = general[datapoint]
        ten_minutes = general['time_played'] * 6
        return damage/ten_minutes
    except KeyError:
        return 0

def damage(general):
    return average(general, 'hero_damage_done')


def deaths(general):
    return average(general, 'deaths')


def eliminations(general):
    return average(general, 'eliminations')


def wins(general):
    return average(general, 'games_won')

def main(datafile):
    tar = tarfile.open(datafile)

    heroes = ['pharah', 'bastion', "reinhardt", "tracer", "symmetra", "roadhog", "moira", "zarya"]
    files = sorted((t for t in tar if t.name.endswith('json')), key=attrgetter('name'))

    days = []
    for tarinfo in files:
        t = tar.extractfile(tarinfo)
        try:
            dt = dateutil.parser.parse(tarinfo.name[19:27])
            d = json.load(t)
            hero_dict = [d['us']['heroes']['stats']['quickplay'][hero]['general_stats'] for hero in heroes]
            days.append((dt, hero_dict))
        except (AttributeError, TypeError, KeyError):
            pass

#    plt.ylim(0,20)
    plt.suptitle("wins")
    for i in range(len(heroes)):
        plt.plot_date([d[0] for d in days], [wins(d[1][i]) for d in days], label=heroes[i], linestyle='solid', marker='None')
    plt.grid(True)
    plt.legend()
    plt.show()

    tar.close()

#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help='data file')
    args = parser.parse_args()
    main(args.datafile)
