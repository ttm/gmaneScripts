#-*- coding: utf8 -*-
from __future__ import division
import numpy as n, pylab as p, networkx as x, random as r

AMBITOX=100
AMBITOY=100
X,Y=n.meshgrid(range(AMBITOX),range(AMBITOY))

# escolhendo circulo do meio:
rx=AMBITOX/2
ry=AMBITOY/2
centro=(AMBITOX/2,AMBITOY/2)
circ=((X-centro[0])**2+(Y-centro[1])**2)< (rx*.9)**2

p.imshow(  circ)
p.show()


# posição do primeiro vértice= topo do circulo

xn,yn=circ.nonzero()
# xn vem sempre crescente.
# pegando yn mais alto:
ind=yn.argmax()
P0=(xn[ind],yn[ind])

p.plot(xn,yn); p.plot(xn,yn,"ro")
p.plot(P0[0],P0[1],"bo")
p.show()

# calculando matrix de distância do P0:
DX=X-P0[0]
DY=Y-P0[1]
D=(DX**2+DY**2)**.5
p.imshow(D); p.colorbar(); p.show()

# cores
cm=p.colormaps()[0]

import pygraphviz as v
A=v.AGraph(directed=True)

A.add_nodes_from(range(150),weight=1.)

A.node_attr['style']='filled'
A.node_attr['fillcolor']='green'

nodes=A.nodes()
# conseguir colocar cada um em uma posicao e escrever em cada 
G=x.DiGraph(A)
cc=x.clustering(G.to_undirected())
cc=[float(i) for i in A.nodes()]
cc=[float(i)/max(cc) for i in cc] # sempre no intervalo [0,1]
TTABELACORES=2**10
cm=p.cm.Reds(range(TTABELACORES))
# http://www.graphviz.org/content/color-names#brewer
A.graph_attr["bgcolor"]="black"
A.graph_attr["bgcolor"]="red"
A.graph_attr["bgcolor"]="forestgreen"
A.graph_attr["page"]="11.5,17"
A.graph_attr["size"]="9.5,12"
A.graph_attr["center"]=1
#A.graph_attr["ratio"]="fill"
A.layout()
ii=0
for node in nodes:
    # http://www.graphviz.org/doc/info/attrs.html 
    n_=A.get_node(node)
    n_.attr['penwidth']=3
    #n_.attr['shape']="box"
    #n_.attr['shape']="diamond"
    n_.attr['shape']="pentagon"
    n_.attr['shape']="point"
    n_.attr['shape']="triangle"
    n_.attr['shape']="doublecircle"
    n_.attr['shape']="invtriangle" # http://www.graphviz.org/doc/info/shapes.html
    n_.attr['orientation']="30" # http://www.graphviz.org/doc/info/shapes.html
    n_.attr['fixedsize']=True
    #n_.attr['style']="rounded,filled,diagonals,dashed,bold"
    n_.attr['fillcolor']= '#%02x%02x%02x' % tuple([255*i for i in cm[int(cc[int(node)]*(TTABELACORES-1))][:-1]])
    pos="%f,%f"%(100* int(ii/20.)+100,40*(ii%20)+60)
    n_.attr['pos']=pos
    n_.attr['label']="Q%i"%(ii+1,)
    #n_.attr['height']=0.15
    #n_.attr['width']=0.15
    #n_.attr['size']="0.15!"

    print ii, pos
    ii+=1
# controlar o que fica escrito em cada vertice.
# a altura e a largura de cada
# cor de borda
# formato
# colocar figura
A.draw("aqui.png")
