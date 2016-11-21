import heapq
from math import *

from model.Faction import Faction

def get_nearest_visible_enemy(me, minions, wizards, buildings=[], include_neutral=False):
    enemy_faction = [1 - me.faction]
    if include_neutral:
        enemy_faction.append(Faction.NEUTRAL)

    enemies = [minion for minion in minions if minion.faction in enemy_faction]
    enemies.extend([wizard for wizard in wizards if wizard.faction in enemy_faction])
    enemies.extend([building for building in buildings if building.faction in enemy_faction])

    nearest_enemy, _, _ = get_nearest_item(me, enemies)
    return nearest_enemy

def get_distance(point_a, point_b):
    return hypot(point_a.x - point_b.x, point_a.y - point_b.y)

def get_nearest_item(point, item_list):
    shortest_dist = 10000000
    nearest_item = None
    nearest_index = None
    for index in range(len(item_list)):
        dist = get_distance(point, item_list[index])
        if dist < shortest_dist:
            shortest_dist = dist
            nearest_item = item_list[index]
            nearest_index = index

    return nearest_item, nearest_index, shortest_dist

def shortest_path(graph, start, end):
    distances = {}
    previous = {}
    max_int = 100000000000

    for vertex in range(len(graph)):
        if vertex == start:
            distances[vertex] = 0
        else:
            distances[vertex] = max_int
        previous[vertex] = None
    
    while len(distances):
        min_value = min(distances.values())
        smallest = [key for key in distances if distances[key] == min_value][0]
        if smallest == end:
            path = []
            while previous[smallest] is not None:
                path.append(graph[smallest])
                smallest = previous[smallest]
            path.append(graph[smallest])
            path.reverse()
            return path
        if distances[smallest] == max_int:
            break
        
        for edge in graph[smallest].edges:
            alt = distances[smallest] + edge.distance
            if edge.to in distances and alt < distances[edge.to]:
                distances[edge.to] = alt
                previous[edge.to] = smallest

        del distances[smallest]

    return None # can't reach