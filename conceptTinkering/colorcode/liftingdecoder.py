import numpy as np

class vertex:
    def __init__(self, color) -> None:
        self.coordinates = None
        self.color = color

class edge(vertex):
    def __init__(self, firstvertex, secondvertex) -> None:
        super().__init__()
        self.vertices = set()
        self.vertices.update([firstvertex, secondvertex])
class face(edge):
    def __init__(self, edges) -> None:
        super().__init__()
        self.edges = set()
        self.edges.update(edges)
        self.neighboring_faces = set()

class cCGraph():
    def __init__(self) -> None:
        self.faces = set()

sgraph = cCGraph()

one = vertex()
two = vertex()
three = vertex()
four = vertex()
five = vertex()
six = vertex()
seven = vertex()
onefour = edge(one, four)
threefour = edge(three, four)
oneseven = edge(one, seven)
threeseven = edge(three, seven)
onefive = edge(one, five)
twofive = edge(two, five)
twoseven = edge(two, seven)
twosix = edge(two, six)
threesix = edge(three, six)
r = face()
g = face()
b = face()
r.edges.update([onefour, oneseven, threeseven, threefour])
g.edges.update([oneseven, twoseven, twofive, onefive])
b.edges.update([threeseven, twoseven, twosix, threesix])
sgraph.faces.update([r, g, b])



class chainComplexCode:
    def __init__(self) -> None:
        self.vertices = set()
        self.edges = set()
        self.faces = set()


def genColorCode():
    pass

def projToHyperV(H, c):
    newVerteces = set()
    for face in H.faces:
        for vertex in face.vertices:
            if vertex.color!=c:
                newVerteces.add(vertex)
    construcNewGraphFromVertices(newVerteces)

