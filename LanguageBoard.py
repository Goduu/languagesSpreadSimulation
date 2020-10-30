#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from random import random, randrange, uniform

# Couleur associée à l'état
STATE = {
    "SUSCEPTIBLE": 0,
    "LEARNING": 1,
    "LEARNED": 2
}

NAT_ZONE = True

ZONE_X = [20,30]
ZONE_Y = [15,20]
xs = [30, 8, 23]
ys = [30, 22, 8]
RED_ZONE = [[19,40],[19, 40]]
GREEN_ZONE = [[0,15],[15,40]]
BLUE_ZONE = [[15,35],[0,20]]

class LanguageBoard:
    def __init__(self, size, round_nbr, cluster_nbr):

        self._length = size
        self._width = size

        self._cluster_nbr = cluster_nbr

        self._language_status = 0

        self._spread_rate = 0.2

        self._learning_rate = uniform(0.1,0.5)

        self._learning_rejection = np.zeros((self._length, self._width), dtype=float)


        self._language_vec = []

        self._max_level = np.zeros((self._length, self._width), dtype=int)

        self._counter = [],[],[]
        self.reset()

    #########################
    # Gestion des attributs #
    #########################

    @property
    def spreadRate(self):
        return self._contagion_rate

    @spreadRate.setter
    def spreadRate(self, proba_learn):
        self._spread_rate = proba_learn

    @property
    def clusterNbr(self):
        return self._cluster_nbr

    @clusterNbr.setter
    def clusterNbr(self, nb_clusters):
        self._cluster_nbr = nb_clusters
    
    @property
    def population(self):
        return self._width * self._length

    @property
    def counter_points(self):
    
        self._counter[0].append(self._language_vec[-1][0].sum())
        self._counter[1].append(self._language_vec[-1][1].sum())
        self._counter[2].append(self._language_vec[-1][2].sum())

        return self._counter
    @property
    def R0(self):
        return (self._spread_rate * 0.1)

    @property
    def currentRound(self):
        return self._current_round

    ###################################
    # Fin de la gestion des attributs #
    ###################################

    def initBoard(self):
        etat0 = np.zeros((self._length, self._width), dtype=int)
        rgb = np.zeros((self._length, self._width), dtype=int), np.zeros((self._length, self._width), dtype=int), np.zeros((self._length, self._width), dtype=int)
        etat0[0:self._length, 0:self._width] = STATE["SUSCEPTIBLE"]

        for x in range(self._length):
            for y in range(self._width):
                self._max_level[x,y] = randrange(300,600)
                self._learning_rejection[x,y] = uniform(0.05,0.5)
        
        
        xs = [30, 8, 23]
        ys = [30, 22, 8]
        # Creation de la population immunisée
        for i in range(self._cluster_nbr):
            # x0 = randrange(self._length)
            # y0 = randrange(self._width)
            # print(x0,y0)
            x0 = xs[i]
            y0 = ys[i]
            etat0[x0, y0] = STATE["LEARNED"]
            rgb[0][x0, y0] = 0
            rgb[1][x0, y0] = 0
            rgb[2][x0, y0] = 0
            rgb[i][x0, y0] = 255
            self._contamination_dates[x0, y0] = -1
            self._counter[STATE["LEARNED"]][0] += 1

        self._state_db.append(etat0)
        self._language_vec.append(rgb)
    def reset(self):
        self._state_db = []
        self._language_vec = []
        self._contamination_dates = np.zeros((self._length, self._width), dtype=int)
        self._current_round = 0

        self._counter = []
        for n in range(len(STATE.items())):
            self._counter.append([])
            self._counter[n].append(0)

        self.initBoard()

    def nextRound(self):
        """
        Create next round state
        :return: next round state
        """
        neighbours = []
        current_state = self._state_db[-1]
        state = current_state.copy()
        language_vec = self._language_vec[-1]
        max_levels = self._max_level
        # We init the next round data with the same data as previous round
        for n in range(len(STATE.items())):
            self._counter[n].append(self._counter[n][-1])

        for x in range(self._length):
            for y in range(self._width):

                #-----------------------------
                # Making the Nationalist zone
                #-----------------------------
                if NAT_ZONE:
                    if(random() < 0.8):
                        if x > ZONE_X[0] and x < ZONE_X[1]:
                            if y > ZONE_Y[0] and y < ZONE_Y[1]:
                                state[x, y] = STATE["LEARNING"]
                                language_vec[0][x,y] /= 2
                                if language_vec[0][x,y] > 0:
                                    language_vec[0][x,y] -= 1
                                language_vec[1][x,y] /= 2
                                if language_vec[1][x,y] > 0:
                                    language_vec[1][x,y] -= 1
                                language_vec[2][x,y] /= 2
                                if language_vec[2][x,y] > 0:
                                    language_vec[2][x,y] -= 1
                        # if x > RED_ZONE[0][0] and x < RED_ZONE[0][1]:
                        #     if y > RED_ZONE[1][0] and y < RED_ZONE[1][1]:
                        #         state[x, y] = STATE["LEARNING"]
                        #         if language_vec[0][x,y] > 0  and language_vec[0][x,y] < 255 - 5:
                        #             language_vec[0][x,y] += 5
                        #         language_vec[1][x,y] /= 1.25
                        #         language_vec[2][x,y] /= 1.25
                        # if x > GREEN_ZONE[0][0] and x < GREEN_ZONE[0][1]:
                        #     if y > GREEN_ZONE[1][0] and y < GREEN_ZONE[1][1]:
                        #         state[x, y] = STATE["LEARNING"]
                        #         language_vec[0][x,y] /= 1.25
                        #         if language_vec[1][x,y] > 0 and language_vec[1][x,y] < 255 - 5:
                        #             language_vec[1][x,y] += 5
                        #         language_vec[2][x,y] /= 1.25
                        # if x > BLUE_ZONE[0][0] and x < BLUE_ZONE[0][1]:
                        #     if y > BLUE_ZONE[1][0] and y < BLUE_ZONE[1][1]:
                        #         state[x, y] = STATE["LEARNING"]
                        #         language_vec[0][x,y] /= 1.25
                        #         language_vec[1][x,y] /= 1.25
                        #         if language_vec[2][x,y] > 0 and language_vec[2][x,y] < 255 - 25:
                        #             language_vec[2][x,y] += 5



                if current_state[x,y] == STATE["LEARNING"]:
                    if max(language_vec[0][x,y],language_vec[1][x,y],language_vec[2][x,y]) == 255:
                        state[x, y] = STATE["LEARNED"]
                    continue
                if current_state[x, y] == STATE["LEARNED"]:

                    #
                    # Contamination des voisins
                    #

                    # Case "coin", où l'on a 3 voisins
                    if x == 0 and y == 0:
                        neighbours = [[0, 1], [1, 1], [1, 0]]
                    if x == (self._length - 1) and y == 0:
                        neighbours = [[x - 1, 0], [x - 1, 1], [x, 1]]
                    if x == 0 and y == (self._width - 1):
                        neighbours = [[0, y - 1], [1, y - 1], [1, y]]
                    if x == (self._length - 1) and y == (self._width - 1):
                        neighbours = [[x - 1, y], [x - 1, y - 1], [x, y - 1]]

                    # Case "bord" mais pas coin, où l'on 5 voisins
                    if x == 0 and not (y == 0 or y == (self._width - 1)):
                        neighbours = [[0, y - 1], [0, y + 1], [1, y - 1], [1, y], [1, y + 1]]
                    if x == (self._length - 1) and not (y == 0 or y == (self._width - 1)):
                        neighbours = [[x, y - 1], [x, y + 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
                    if not (x == 0 or x == (self._length - 1)) and y == 0:
                        neighbours = [[x - 1, 0], [x + 1, 0], [x - 1, 1], [x, 1], [x + 1, 1]]
                    if not (x == 0 or x == (self._length - 1)) and y == (self._width - 1):
                        neighbours = [[x - 1, y], [x + 1, y], [x - 1, y - 1], [x, y - 1], [x + 1, y - 1]]

                    # Autres cas : 8 cases
                    if 0 < x < (self._length - 1) and 0 < y < (self._width - 1):
                        neighbours = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1],
                                      [x, y - 1], [x, y + 1],
                                      [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]]

                    for nb in neighbours:
                        if current_state[nb[0], nb[1]] == STATE["SUSCEPTIBLE"] or current_state[nb[0], nb[1]] == STATE["LEARNING"]:
                            if random() > self._learning_rejection[nb[0],nb[1]]:
                                if sum((language_vec[0][nb[0], nb[1]],
                                       language_vec[1][nb[0], nb[1]],
                                       language_vec[2][nb[0], nb[1]])) <= max_levels[nb[0],nb[1]]:
                                    self._contamination_dates[nb[0], nb[1]] = self._current_round
                                    # Same person might have been infected at the same round by another person : the
                                    # tests avoids double counting
                                    language_vec[0][nb[0], nb[1]] += self._spread_rate * self._language_vec[-1][0][x,y]
                                    language_vec[0][nb[0], nb[1]] = min(language_vec[0][nb[0], nb[1]],255)
                                    language_vec[1][nb[0], nb[1]] += self._spread_rate * self._language_vec[-1][1][x,y]
                                    language_vec[1][nb[0], nb[1]] = min(language_vec[1][nb[0], nb[1]],255)
                                    language_vec[2][nb[0], nb[1]] += self._spread_rate * self._language_vec[-1][2][x,y]
                                    language_vec[2][nb[0], nb[1]] = min(language_vec[2][nb[0], nb[1]],255)
                                        
                                    
                                    if not state[nb[0], nb[1]] == STATE["LEARNING"]:
                                        state[nb[0], nb[1]] = STATE["LEARNING"]

                                        self._counter[STATE["LEARNING"]][-1] += 1
                        else:
                            if random() > 1.5*self._learning_rejection[nb[0],nb[1]]:
                                if sum((language_vec[0][nb[0], nb[1]],
                                       language_vec[1][nb[0], nb[1]],
                                       language_vec[2][nb[0], nb[1]])) <= max_levels[nb[0],nb[1]]:

                                    self._contamination_dates[nb[0], nb[1]] = self._current_round
                                    # Same person might have been infected at the same round by another person : the
                                    # tests avoids double counting
                                    language_vec[0][nb[0], nb[1]] += self._spread_rate/3 * self._language_vec[-1][0][x,y]
                                    language_vec[0][nb[0], nb[1]] = min(language_vec[0][nb[0], nb[1]],255)
                                    language_vec[1][nb[0], nb[1]] += self._spread_rate/3 * self._language_vec[-1][1][x,y]
                                    language_vec[1][nb[0], nb[1]] = min(language_vec[1][nb[0], nb[1]],255)
                                    language_vec[2][nb[0], nb[1]] += self._spread_rate/3 * self._language_vec[-1][2][x,y]
                                    language_vec[2][nb[0], nb[1]] = min(language_vec[2][nb[0], nb[1]],255)
                                        
                                    
                                    if not state[nb[0], nb[1]] == STATE["LEARNING"]:
                                        state[nb[0], nb[1]] = STATE["LEARNING"]

                                        self._counter[STATE["LEARNING"]][-1] += 1

        self._state_db.append(state)
        self._language_vec.append(language_vec)
        self._current_round += 1

        return state,language_vec

    def lastBoard(self):
        return self._state_db[-1],self._language_vec[-1]