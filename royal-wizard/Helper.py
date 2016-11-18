def get_nearest_visiable_enemy(me, minions, wizards, include_neutral=False):
    nearest_enemy = None
    shortest_dist = 100000

    enemy_faction = [1 - me.faction]
    if include_neutral:
        enemy_faction.append[Faction.NEUTRAL]

    for minion in minions:
        if minion.faction in enemy_faction:
            if me.get_distance_to(minion.x, minion.y) < shortest_dist:
                shortest_dist = me.get_distance_to(minion.x, minion.y)
                nearest_enemy = minion
    for wizard in wizards:
        if wizard.faction in enemy_faction:
            if me.get_distance_to(wizard.x, wizard.y) < shortest_dist:
                shortest_dist = me.get_distance_to(wizard.x, wizard.y)
                nearest_enemy = wizard
    return nearest_enemy