# a_star.py

import heapq
import math
from .graph_map import MARKER_COORDS

def heuristic(a, b):
    """Euclidean distance heuristic"""
    x1, y1, z1 = MARKER_COORDS[a]
    x2, y2, z2 = MARKER_COORDS[b]
    return math.sqrt(
        (x2 - x1)**2 +
        (y2 - y1)**2 +
        (z2 - z1)**2
    )

def a_star(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        
        for neighbor, cost in graph[current]:
            tentative_g = g_score[current] + cost
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                
                # A* improvement: use f_score = g_score + heuristic
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    
    return []