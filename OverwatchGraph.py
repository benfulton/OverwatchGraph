import tarfile
import json
import dateutil.parser
import matplotlib.pyplot as plt
import argparse
from operator import attrgetter
import MySQLdb

def load_players():
    conn = MySQLdb.connect(host = '127.0.0.1',user = 'overwatch', passwd = 'pharmercy',db = 'overwatch')
    cursor = conn.cursor()

    battletag = 'Syzygy-11715'
    cursor.execute("""select json, created_at from statistics where battletag like %s order by created_at""", (battletag, ))
    return cursor.fetchall()

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

def main():
    players = load_players()
    heroes = ['pharah'] # ['pharah', 'bastion', "reinhardt", "tracer", "symmetra", "roadhog", "moira", "zarya"]

    days = []
    for tarinfo in players:
        try:
            hero_dict = [json.loads(tarinfo[0])['heroes']['stats']['quickplay'][hero]['general_stats'] for hero in heroes]
            days.append((tarinfo[1], hero_dict))
        except (AttributeError, TypeError, KeyError):
            pass

#    plt.ylim(0,20)
    plt.suptitle("damage")
    for i in range(len(heroes)):
        plt.plot_date([d[0] for d in days], [damage(d[1][i]) for d in days], label=heroes[i], linestyle='solid', marker='None')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
