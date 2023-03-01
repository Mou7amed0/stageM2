
import sys
import os
import time
import select

import graphe as gr


import random

class Prog : 

  def __init__(self):
    self.graphe = chargerGrapheSemantique("inventaire.csv", "concepts.csv")
    self.graphe.calculNiveau()

    # Sélection de 5 objets du patrimoine faite au hasard
    l = [n.nom for n in self.graphe.consulterObjets()]
    random.shuffle(l)
    self.objetsCandidats = l[0:4]

    self.nouvelAffichage = True
        
    self.nouveauxCandidatsACalculer = False
    

  def run(self):
    while True : 
      self.show()
      self.interact()
      self.update()


  def update(self):
    time.sleep(0.2)

  def interact(self):
    if self.isDataReady():
         # On lit ce caractère
        c = sys.stdin.read(1)
        # On test et compare ce caractère
        if c == '\x1b':         # x1b is ESC
            self.quit()
        elif c=='0' :
            n = int(c)
            print(c)
        elif c=='q' :
            exit(0)   
        print(c)   

  def isDataReady(self):
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []) 

  def show(self):
    if self.nouvelAffichage :
      for i in range(len(self.objetsCandidats)) : 
        s = "%i ) %s" % (i, self.objetsCandidats[i])
        print(s)
      print("\n\n saisissez le numéro de votre choix puis <ENTER>\n\n")
      
      self.nouvelAffichage = False
    
  def quit(self):
    exit(0)


def chargerGrapheSemantique(inventaire, concepts):
  graphe = gr.Graphe()
  
  Ec = set()
  Et = set()
  Eo = {}
  
  # Création des objets
  
  with open(inventaire,"r") as f : 
    for ligne in f : 
      mots = ligne.split(",")
      nom      = (mots[2]).rstrip().lstrip()
      _position = mots[3].split(":")
      position  = (float(_position[0]), float(_position[1])) 
      _tags     = mots[4].split(":")
      tags     = [(t[:-1]).rstrip().lstrip() for t in _tags]
      data = (nom, position,tags)
      Eo[nom] = data
    
  for (nom, position, tags) in Eo.values() :
    objet = gr.Objet(nom, data, graphe)
    graphe.ajouterNoeud(objet)  
    
  # Création de la taxonomie   
  
  with open(concepts,"r") as f : 
    for ligne in f :
      mots = ligne.split(",")
      x = (mots[0]).rstrip().lstrip()
      y = (mots[1]).rstrip().lstrip()
      Ec.add(x)
      Ec.add(y)

      
  for x in Ec : 
    graphe.ajouterNoeud(gr.Noeud(x,None,graphe))
    
  graphe.root = graphe.noeuds["tout"]


  with open(concepts,"r") as f : 
    for ligne in f :
      mots = ligne.split(",")
      x = (mots[0]).rstrip().lstrip()
      y = (mots[1]).rstrip().lstrip()
      z = float(mots[2])

      graphe.ajouterArc(graphe.noeuds[x],graphe.noeuds[y],z)
      
  with open(inventaire,"r") as f : 
    for ligne in f : 
      mots = ligne.split(",")
      nom      = (mots[2]).rstrip().lstrip()
      _tags     = mots[4].split(":")
      tags     = [(t[:-1]).rstrip().lstrip() for t in _tags]
      for tag in tags:
        graphe.ajouterArc(graphe.noeuds[nom], graphe.noeuds[tag],1.0)
      
  return graphe
  

prog = Prog()
prog.run()
