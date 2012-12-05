#!/usr/bin/env python
from __future__ import division
from itertools import permutations,combinations

"""
This module contains code for the calculation of the Shapley value in cooperative games.
"""

def power_set(List):
    """
    function to return the powerset of a list
    """
    subs = [list(j) for i in range(len(List)) for j in combinations(List, i+1)]
    return subs


def characteristic_function_check(player_list,characteristic_function):
    """
    A function to check if a characteristic_function is valid
    """
    r=True
    for e in power_set(player_list):
        if ",".join(e) not in characteristic_function:
            return False
    #Need include check that dictionary is superadditive
    return r

def predecessors(player,player_permutation):
    """
    A function to return the predecessors of a player
    """
    r=[]
    for e in player_permutation:
        if e!=player:
            r.append(e)
        else:
            break
    return r

def Marginal_Contribution(player,player_permutation,characteristic_function):
    """
    A function to return the marginal contribution of a player for a given permutation
    """
    pred=predecessors(player,player_permutation)
    predecessor_contribution=0
    for e in permutations(pred):
        e=",".join(e)
        if e in characteristic_function:
            predecessor_contribution=characteristic_function[e]
    pred.append(player)
    for e in permutations(pred):
        e=",".join(e)
        if e in characteristic_function:
            return characteristic_function[e]-predecessor_contribution

#print "Say wha?", Marginal_Contribution("B",pi,cf)
#print "Say wha?", Marginal_Contribution("C",pi,cf)
#print "Say wha?", Marginal_Contribution("A",pi,cf)

def Shapley_calculation(player_list,characteristic_function):
    """
    A function to return the shapley value of a game
    """
    Marginal_Contribution_dict={}
    for e in player_list:
        Marginal_Contribution_dict[e]=0
    k=0
    for pi in permutations(player_list):
        k+=1
        for e in player_list:
            Marginal_Contribution_dict[e]+=Marginal_Contribution(e,pi,characteristic_function)
    for e in Marginal_Contribution_dict:
        Marginal_Contribution_dict[e]/=k
    return Marginal_Contribution_dict

#pl=["A","B","C"]
#cf={"A":1,"B":3,"C":4,"A,B":3,"B,C":4,"A,C":4,"A,B,C":5}
#pi=("C","A","B")
#pl=["A","B"]
#cf={"A":5,"B":12,"A,B":12}
#print Shapley_calculation(pl,cf)

class Coop_Game():
    def __init__(self,player_list,characteristic_function):
        self.player_list=player_list
        self.valid=False
        if type(characteristic_function) is dict:
            if characteristic_function_check(self.player_list,characteristic_function):
                self.characteristic_function=characteristic_function
                self.valid=True
            else:
                print ""
                print "Characteristic function is not valid."
                print ""
        else:
                print ""
                print "The characteristic function must be a dictionary."
                print ""

     def shapley(self):
        self.shapley=Shapley_calculation(self.player_list,self.characteristic_function)
        return self.shapley

#pl=["A","B","C"]
#cf={"A":1,"B":3,"A,B":3,"B,C":2,"A,B,C":5,"A,C":2,"C":4}
#print Shapley_calculation(pl,cf)
#a=Coop_Game(pl,cf)
#print a.valid
#print a.characteristic_function
