# -*- coding: utf-8 -*-

from datetime import datetime

from django.utils.timezone import timedelta

RESULT_CHOICES = (
    (0, 'Game is in process'),
    (1, '0-1'),
    (2, '1-0'),
    (3, '1/2'),
    (4, '+/-'),
    (5, '-/+'),
    (6, '-/-'),
    )

def normalize_email(username):
    """
    Normalize email, User@Mail.com => user@mail.com

    :param username: email
    :returns: normalized user email
    """
    try:
        email_name, domain_part = username.strip().split('@', 1)
    except ValueError:
        return False
    else:
        username = '@'.join([email_name.lower(), domain_part.lower()])
    return username

def get_last_and_group(group):
    last = group.pop()
#    if last.is_self_player and len(group) > 0:
#        new_last = group.pop()
#        group.insert(group[len(group)-1], last)
#        last = new_last
    return last, group

def normalize_group(group, player=None):
    if player:
        group.append(player)
    if (len(group) % 2) != 0:
        player, group = get_last_and_group(group)
    return player, group

def get_couples_and_selfplayer(group):
    couples = []
    self_player = None
    first, second = group[:len(group)/2], group[len(group)/2:]
    if len(first) != len(second):
        self_player, second = get_last_and_group(second)
    for i in xrange(len(first)):
        print 'first', first[i].playername
        couples += [(first[i].playername, second[i].playername)]
    return self_player, couples

def get_total_couples(group):
    couples = []
    for i in xrange(len(group)):
        couples += [(group[i],c[1]) for c in [[group[i],x] for x in group[i:]]]
        couples += [(group[i],c[0]) for c in [[group[i],x] for x in group[i:]]]
    return list(set(couples))

def upload_to_dir(name):
    now = datetime.now()
    return '%s_%s_%s_%s_%s' % (now.year, now.month, now.day, now.hour, name)

def get_limit(dt=None, time_limit=None):
    time_limit = time_limit if time_limit else 2
    min = int(time_limit) * 60
    now = dt if dt else datetime.now()
    end_time = now + timedelta(minutes=min)
    return end_time

def get_waiting_counts(group, rounds_count):
    counts = []
    max_count = float(rounds_count)
    total_count = len(group)*rounds_count
    coefficient = int(round(len(group)/7))
    delimiter = int(round(len(group)/2) + coefficient)
    first, second = group[:delimiter], group[delimiter:]
    counts += [(first[0].playername, max_count)]
    i, count = 0, max_count - 0.5
    for player in first[1:]:
        if i % coefficient == 0:
            count -= 0.5
        counts += [(player.playername, count)]
        i += 1
    i = 0
    for player in second[:len(second)-1]:
        if i % 2 == 0:
            count -= 0.5
        counts += [(player.playername, count)]
        i += 1
    counts += [(second[len(second)].playername, 0.0)]
    return counts

def get_elo_coefficient(rate):
    cK = None
    if (rate > 1000) and (rate < 2400):
        cK=15
    elif rate <= 1000:
        cK = 30
    elif rate >= 2400:
        cK = 10
    return cK

def get_degree(rate, sex):
    degree = 0
    if sex == 0:
        return degree
    elif sex == 1:
        if (rate > 2200) and (rate <= 2299):
            degree=1
        elif (rate > 2300) and (rate <= 2399):
            degree = 2
        elif (rate > 2400) and (rate <= 2499):
            degree = 3
        elif rate >= 2500:
            degree = 4
    elif sex == 2:
        if (rate >= 2000) and (rate <= 2099):
            degree=5
        elif (rate > 2100) and (rate <= 2199):
            degree=6
        elif (rate > 2200) and (rate <= 2299):
            degree=7
        elif rate >= 2300:
            degree = 8
    return degree

def set_player_result(result, type):
    plus = 0.0
    result = int(result)
    if result == 3:
        plus = 0.5
    if type == 'white' and (result in [1,5]):
        plus = 1.0
    elif type == 'black' and (result in [2,4]):
        plus = 1.0
    return plus

