# -*- coding: utf-8 -*- 
import numpy as np

# Element type description
_dico_element = {  0: 'point',
                   1: 'line',
                   2: 'triangle',
                   3: 'quadrangle'}

# Number of nodes for each element
_dico_elemsize = { 0: 1,
                   1: 2,
                   2: 3,
                   3: 4}

class Mesh:
    """
    - dim : dimension du maillage
    - nodes : tableau des coordonnees
    - elements : dictionnaire d'elementType

        elementType:
        - 0: point,
        - 1: line,
        - 2: triangle,
        - 3: quadrangle,

        Dans ce dictionnaire, nous retrouvons un autre 
        dictionnaire. Si il n'y a pas de valeur, il n'y
        a pas d'elements de ce type. Sinon, nous avons 
        une cle par région et les valeurs sont le tableau
        des elements associes.

    """
    def __init__(self):
        self.nodes = None
        self.elements={}
        for k in _dico_element.keys():
            self.elements[k]={}
            
    def fromFreeFem(self, filename):
        """
        Creation d'un maillage a partir d'un maillage FreeFem.

        :Parametres d'entree:

           - filename : fichier FreeFem

        :Parametres de sortie:

           - maillage

        """
        self.ndim = 2
        f = open(filename)

        line = f.read().split()

        # read vertices size, triangles size and lines size
        [nbVertices, nbTria, nbLine] = map(int, line[0:3])

        # read coordinates
        tmp = map(np.double, line[3:nbVertices*3 + 3])
        self.nodes = np.zeros((nbVertices,3))
        self.nodes[:,0] = tmp[0::3]
        self.nodes[:,1] = tmp[1::3]
        self.nodes = np.ascontiguousarray(self.nodes, np.double)

        # read triangles and their region
        ind = nbVertices*3+3
        tmp = np.asarray(map(np.int, line[ind:ind + nbTria*4]))

        region = np.unique(tmp[3::4])
        tmp = tmp.reshape((nbTria, 4))
        for rg in region:
            elem = np.where(tmp[:, 3] == rg)[0]
            self.elements[2][rg] = np.array(tmp[elem, :3]) - 1
            self.elements[2][rg] = np.ascontiguousarray(self.elements[2][rg], np.int32)

        # read lines
        ind = ind + nbTria*4
        tmp = np.array(map(np.int, line[ind:]))
        region = np.unique(tmp[2::3])
        tmp = tmp.reshape((nbLine, 3))
        for rg in region:
            elem = np.where(tmp[:, 2] == rg)[0]
            self.elements[1][rg] = np.array(tmp[elem, :2]) - 1
            self.elements[1][rg] = np.ascontiguousarray(self.elements[1][rg], np.int32)
        
        f.close()        

    def fromCoords(self, x, y):
        """ 
        Creation d'un maillage a partir des intervalles x, y, z.

        :Parametres d'entree:

            - x : points dans la direction x

            - y : points dans la direction y 
                
        :Parametres de sortie:

            - maillage

        :Exemple:

        ::
        
            import mesh
            from numpy import linspace

            m = mesh.Mesh()
            m.fromCoords(np.linspace(0, 1, 10), np.linspace(0, 1, 10))
        

        """
        coords = (np.asarray(x, dtype = np.double),)
        
        coords += (np.asarray(y, dtype = np.double),)
        
        self.ndim = len(coords)

        shape = [c.size for c in coords]
        size = 1
        for i in shape:
            size *= i

        self._setNodes(coords, shape, size)
        self._setElements(shape, size)

    def numberOfNodes(self) :
        """
        Renvoie le nombre de points contenus dans le maillage.

        :Parametres de sortie:

            - nombre de points

        """
        return self.nodes.shape[0]

    def numberOfElements( self, elementType=None) :
        """
        Renvoie le nombre d'elements contenus dans le maillage.
        
        :Parametre d'entree:

            - elementType : si None, renvoie le nombre total d'elements
                            sinon renvoie le nombre d'element ayant le 
                            type elementType
                          
                          - 0: point,
                          - 1: line,
                          - 2: triangle,
                          - 3: quadrangle,

        :Parametres de sortie:

            - nombre d'elements

        """
        s = 0
        if elementType == None:
            for k in self.elements.keys():
                if self.elements[k] != {}:
                    for key, value in self.elements[k].iteritems():
                        s += value.shape[0]
        else:
            for key, value in self.elements[elementType].iteritems():
                s += value.shape[0]
        return s

    def _setNodes(self, coords, shape, size):
        nn = np.indices(shape[-1::-1])
        self.nodes = np.zeros((size, 3), dtype = np.double)

        for i, c in enumerate(coords):
            self.nodes[:, i] = c[nn[-1 - i]].flatten()

    def _setElements(self, shape, size):

        nn = np.arange(size - shape[0])
        nn = nn[(nn + 1) % shape[0] != 0]

        quad = np.empty((nn.size, 4), dtype = np.int)
        quad[:, 0] = nn[:]
        quad[:, 1] = nn[:] + 1
        quad[:, 2] = nn[:] + shape[0] + 1
        quad[:, 3] = nn[:] + shape[0]

        self.elements[3][1] = quad

        line = np.arange(shape[0])
        self.elements[1][1] = np.asarray([line[:-1], line[1:]]).transpose()
        self.elements[1][3] = size - 1 - np.asarray([line[:-1], line[1:]]).transpose()
        
        line = np.arange(shape[0] - 1, size, shape[0])
        self.elements[1][2] = np.asarray([line[:-1], line[1:]]).transpose()
        self.elements[1][4] = size - 1 - np.asarray([line[:-1], line[1:]]).transpose()            

        for k in self.elements.keys():
            for r in self.elements[k].keys():
                self.elements[k][r] = np.ascontiguousarray(self.elements[k][r], np.int32)

    def plot(self):
        import matplotlib.pylab as plt

        plt.hold(True)
        if self.elements[2] != {}:
            for key, value in self.elements[2].iteritems():
                tab = np.vstack((value[:, :-1], value[:, 1:], value[:, 2::-2]))
                for t in tab:
                    plt.plot(self.nodes[t, 0],self.nodes[t, 1], 'r')
        if self.elements[3] != {}:
            for key, value in self.elements[3].iteritems():
                tab = np.vstack((value[:, :-2], value[:, 1:-1], value[:, 2:], value[:, 3::-3]))
                for t in tab:
                    plt.plot(self.nodes[t, 0],self.nodes[t, 1],'r')

        plt.hold(False)
        plt.show()

    def __str__(self):
        s = 'Mesh\n'
        s += '\tNumber of nodes: %d\n'%self.numberOfNodes()
        s += '\tNumber of line elements: %d\n'%self.numberOfElements(1)
        s += '\tNumber of triangle elements: %d\n'%self.numberOfElements(2)
        s += '\tNumber of quadrangle elements: %d\n'%self.numberOfElements(3)
        return s

    def __add__(self, m):
        mnew = Mesh()
        mnew.nodes = np.concatenate((self.nodes, m.nodes))
        for k in self.elements.keys():
            if self.elements[k] != {} or m.elements[k] != {}: 
                for r in np.unique(self.elements[k].keys() + m.elements[k].keys()):
                    if self.elements[k].has_key(r):
                        if m.elements[k].has_key(r):
                            mnew.elements[k][r] = np.concatenate((self.elements[k][r], m.elements[k][r]+self.numberOfNodes()))
                        else:
                            mnew.elements[k][r] = self.elements[k][r].copy()
                    else:
                        mnew.elements[k][r] = m.elements[k][r].copy() + self.numberOfNodes()
        return mnew

if __name__ == '__main__':

    m = Mesh()
    m.fromFreeFem("membrane.msh")
    print m

    m1 = Mesh()
    x = np.linspace(1., 2., 11)
    m1.fromCoords(x, x)
    print m1

    m1 = m + m1
    print m1
    m1.plot()
