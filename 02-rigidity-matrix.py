from sympy import *
import networkx as nx

def graph_to_matrix(G):
    M = Matrix()
    for edge in G.edges:
        row = []
        for vertex in G.nodes:
            if vertex == edge[0]:
                row.extend([edge[0].x-edge[1].x,edge[0].y-edge[1].y])
            elif vertex == edge[1]:
                row.extend([edge[1].x-edge[0].x,edge[1].y-edge[0].y])
            else:
                row.extend([0,0])
        M=Matrix([M,row])
    return M
def set_pinning(pins, M):
    if type(M) is Matrix:
        M = M.nullspace()
    if type(pins) is int:
        pins = {pins}
    for p in pins:
        for vector in M:
            if vector[2*(p-1)] != 0 or vector[2*(p-1)+1] != 0:
                for i in Range(vector.rows):
                    vector[i] =0;
    return M
def getMotions(M):
    if type(M) is Matrix:
        M = M.nullspace()
    motions = list()
    i = 0
    for vector in M:
        j =0
        set = list()
        for val in vector:
            if val != 0:
                set.append(str(val) + "*v" + str(floor(j/2)+1) + ("x" if (j%2 == 0) else "y"))
            j+=1
        motions.append(set)
    return motions
def motions_to_string(motions):
    string = ""
    for v in motions:
        if len(v) !=0:
            for val in v:
                if val == v[0] and len(v)>1:
                    word = " depends on "
                elif val != v[len(v)-1]:
                    word = ", and "
                elif len(v) == 1:
                    word = " is free\n"
                else:
                    word ="\n"
                string += val + word
    return string
def check_rigidity(M):
    return M.rank() == M.cols-3

graph = nx.DiGraph()
p1 = Point(0,0)
p2 = Point(5,0)
p3 = Point(5,5)
p4 = Point(0,5)
graph.add_edges_from([(p1,p2),(p2,p3),(p3,p4),(p4,p1),(p2,p4)])
A = graph_to_matrix(graph)
pprint(A)
if check_rigidity(A):
    print("the linkage is infinitesimally rigid!")
A = set_pinning({3},A)
print(motions_to_string((getMotions(A))))
