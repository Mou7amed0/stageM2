
class Noeud : 

  def __init__(self, nom, data, graphe):
    self.nom     = nom
    self.gr      = graphe
    self.niveau  = 1
    self.interet = 0.0
    self.parents = []
    self.enfants = []

  def charger(self, concepts, inventaire):
    pass
     
  def ajouterParent(self, noeud):
    self.parents.append(noeud)
    
  def ajouterEnfant(self, noeud):
    self.enfants.append(noeud)
    
  def consulterParents(self):
    return self.parents
    
  def consulterEnfants(self):
    return self.enfants
    
  def modifierInteret(self,interet):
    self.interet = interet
    
  def ajouterInteret(self, dInteret):
    self.interet += dInteret
    
  def consulterInteret(self):
    return self.interet
    
  def arc(self, noeud1, noeud2):
    return self.gr.arcs.get((noeud1.nom, noeud2.nom), None)
    
  def calculNiveau(self):
    if self.enfants == [] :
      return 0
    else:
      l = [noeud.calculNiveau() for noeud in self.enfants]
      self.niveau = 1 + max(l)
     # print(self.niveau)
      return self.niveau
      
  def calculUpDoi(self):
    if self.enfants != [] :
      l = [noeud.interet * self.arc(noeud,self) for noeud in self.enfants]
      self.interet += sum(l)
      
  def calculDownDoi(self):
    if self.parents != [] : 
      l = [noeud.interet * self.arc(self, noeud) for noeud in self.parents]
      self.interet += sum(l)
      
      

class Objet(Noeud):
  def __init__(self, nom, data, gr):
    Noeud.__init__(self,nom, data, gr)
    self.position = data[1]
    self.tags     = data[2]
    self.niveau   = 0

  def calculInteret(self):
    if self.parents != [] : 
      self.interet = sum([p.consulterInteret() for p in self.consulterParent()])    

# ========================================================

class Graphe :

  def __init__(self):
    self.noeuds  = {}
    self.arcs    = {}
    self.root    = None
    self.niveaux = []

  def calculerObjetsLesPlusInteressants(self,n):
    l = [(noeud.interet, noeud) for noeud in self.niveaux[0]]
    l.sort()
    l.reverse()
    resultat = [noeud for (interet,noeud) in l]
    return resultat[0:n-1] 

  def calculerInteretObjet(self ):
    pass

  def obtenirNoeudConnaissantNom(self,nom):
    return self.noeuds.get(nom, None)

  def consulterObjets(self):
    return self.niveaux[0]

  def consulterTags(self):
    return self.niveaux[1]

  def consulterNiveau(self,i):
    return self.niveaux[i]
    
  def montrerDoiNiveau(self,i):
    return dict((n.nom,n.doi) for n in self.niveaux[i])
    
  def ajouterNoeud(self, noeud):
    if not noeud.nom in self.noeuds : 
      self.noeuds[noeud.nom] = noeud
    
  def ajouterArc(self, noeud1, noeud2, w):
    self.arcs[(noeud1.nom, noeud2.nom)] = w 	  
    noeud1.ajouterParent(noeud2)
    noeud2.ajouterEnfant(noeud1)
    
  def calculNiveau(self):
    n = self.root.calculNiveau() + 1
    

    self.niveaux = [[] for i in range(n+1)]
    for noeud in self.noeuds.values() : 
      #print(">>>> ", noeud.nom, " > ", noeud.niveau)
      self.niveaux[noeud.niveau].append(noeud)
    
      
  def calculInteretMax(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    return max(l)
    
  def normalisationInteret(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    interetMax = max(l)
    for noeud in self.noeuds.values():
      noeud.interet = noeud.interet / doiMax
      
  def calculUpInteret(self):
    n = len(self.niveaux)
    for i in range(1,n-1):
      for noeud in self.niveaux[i]:
        noeud.calculUpInteret() 
        
  def calculDownInteret(self):
    n = len(self.niveaux)
    indices = list(range(0,n-2))
    indices.reverse()
    print(indices)
    for i in indices : 
      for noeud in self.niveaux[i] : 
        noeud.calculDownInteret()
