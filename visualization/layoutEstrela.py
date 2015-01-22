#-*- coding: utf8 -*-
from __future__ import division
import networkx as x, pylab as p, numpy as n
import random as r

# Dígrafo randômico com 10 nós
g=x.DiGraph()
NV=150 # número de vértices
NA=3000 # número de arestas
g.add_nodes_from(range(NV), weight=1) # Numero de nohs, peso de inicializacao
nodes=g.nodes()
for A in range(NA):
    de=r.sample(nodes,1)[0]
    para=r.sample(nodes,1)[0]
    while (de,para) in g.edges():
        de=r.sample(nodes,1)[0]
        para=r.sample(nodes,1)[0]
    g.add_edge(de,para,weight=1.) # numero de ligacoes de antemao, distribuicao de grau


peso_total=2000 # atividade social forma aresta
ATIVIDADE=peso_total/2 # metade do peso total são as mensagens que geraram interação
es=g.edges()
for i in xrange(int(ATIVIDADE-len(es))): # o que falta de peso nas arestas
    de,para=r.sample(es,1)[0]
    g[de][para]["weight"]+=1.

print(u"atividade: %i, peso total: %i, grau total: %i, peso entrada: %i, grau entrada: %i, peso saída: %i, grau saída: %i"\
        % ( sum([d for d in g.degree(weight="weight").values()])/2,\
            sum(g.degree(weight="weight").values()), sum(g.degree().values()),\
            sum(g.in_degree(weight="weight").values()), sum(g.in_degree().values()),\
            sum(g.out_degree(weight="weight").values()), sum(g.out_degree().values()) )   ) 
print("número de vértices: %i, de arestas: %i"%(g.number_of_nodes(),g.number_of_edges()))

OVER=2000 # adiciona aresta ou peso, indistintamente
for o in xrange(OVER):
    de=r.sample(nodes,1)[0]
    para=r.sample(nodes,1)[0]
    if (de,para) in g.edges():
        g[de][para]["weight"]+=1.
    else:
        g.add_edge(de,para,weight=1.)


print(u"==OVER: %i==\natividade: %i, peso total: %i, grau total: %i, peso entrada: %i, grau entrada: %i, peso saída: %i, grau saída: %i"\
        % ( OVER, sum([d for d in g.degree(weight="weight").values()])/2,\
            sum(g.degree(weight="weight").values()), sum(g.degree().values()),\
            sum(g.in_degree(weight="weight").values()), sum(g.in_degree().values()),\
            sum(g.out_degree(weight="weight").values()), sum(g.out_degree().values()) )   ) 

print("número de vértices: %i, de arestas: %i"%(g.number_of_nodes(),g.number_of_edges()))


######################
### Rede livre de escala
# Reutilitando NV NA peso_total e OVER

import collections as c
gl=x.DiGraph()

gl.add_nodes_from(range(NV), weight=1.) # Numero de nohs, peso de inicializacao
nodes=g.nodes()
for A in xrange(NA):
    ordenacao= c.OrderedDict(sorted(g.degree().items(), key=lambda x: x[1]))
    for o in ordenacao:
        ordenacao[o]+=.5
    total=sum(ordenacao.values())
    dist=[o/total for o in ordenacao.values()]
    cumdist=n.cumsum(dist)
    de=ordenacao.keys()[-sum(n.cumsum(dist)>n.random.random())]

    # nova roleta sem quem jah tah ligado
    ordenacao_=ordenacao.copy()
    for node in g[de].keys():
        ordenacao_.pop(node)
    if de in ordenacao_.keys():
        ordenacao_.pop(de)

    for o in ordenacao:
        ordenacao[o]+=.5
    total=sum(ordenacao_.values())
    dist=[o/total for o in ordenacao_.values()]
    para=ordenacao_.keys()[-sum(n.cumsum(dist)>n.random.random())]
    while (de,para) in gl.edges():
        para=ordenacao_.keys()[-sum(n.cumsum(dist)>n.random.random())]
        print(de,para,"AA")
    gl.add_edge(de,para,weight=1.) # numero de ligacoes de antemao, distribuicao de grau






############3
# obtendo medida e ordenação dos vértices:

param="grau"

ordenacao= c.OrderedDict(sorted(g.degree().items(), key=lambda x: x[1]))

# padrao reta:
i=0
ordenacao_=c.OrderedDict()
for o in ordenacao.keys():
    ordenacao_[o]=(i,i)
    i+=1
x.draw(g,pos=ordenacao_)
p.show()

R=100
FATOR=0.8
PASSO=n.pi*n.sqrt(2)
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO*2*n.pi)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*FATOR,Y*FATOR)
    i+=1

x.draw(g,pos=ordenacao__)
p.show()



R=100
FATOR=0.8
PASSO=n.pi*n.sqrt(2)
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO*2*n.pi)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(angulo)
    ordenacao__[o]=(X*FATOR,Y*FATOR)
    i+=1

x.draw(g,pos=ordenacao__)
p.show()




R=100
FATOR=0.99
PASSO=n.pi*n.sqrt(2)
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO*2*n.pi)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()



R=100
FATOR=0.99
PASSO=n.pi*n.sqrt(2)/14
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO*2*n.pi)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()




R=100
FATOR=0.99
PASSO=n.pi*n.sqrt(2)/44
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO*2*n.pi)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()




R=100
FATOR=0.99
PASSO=n.pi*n.sqrt(2)/44
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()





R=100
FATOR=1.01
PASSO=n.pi*n.sqrt(2)/44
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()





R=100
FATOR=1.01
PASSO=n.pi*n.sqrt(2)
PI0=n.pi

ordenacao__=c.OrderedDict()
i=0
for o in ordenacao.keys():
    angulo=n.complex(0,PI0 -i*PASSO)
    X,Y=R*n.real(n.e**(angulo)),R*n.imag(n.e**angulo)
    ordenacao__[o]=(X*(FATOR**i),Y*(FATOR**i))
    i+=1

x.draw(g,pos=ordenacao__)
p.show()






def spiral(X, Y):
    """Espiral de dentro para fora"""
    x = y = 0
    xx=[x]; yy=[y]
    dx = 0
    dy = -1
    for i in range(max(X, Y)**2):
        if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
            xx+=[x]; yy+=[y]
            # DO STUFF...
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy
    return xx,yy

aresta=n.int(n.ceil(g.number_of_nodes()**.5))
aa=spiral(aresta,aresta)
p.plot(aa[0],aa[1]); p.plot(aa[0],aa[1],"ro");  p.show()
aa=zip(*aa)


ordenacao__=c.OrderedDict()
i=1 # espiral retorna elemento repetido
for o in ordenacao.keys():
    ordenacao__[o]=aa[i]
    i+=1

x.draw(g,pos=ordenacao__)
p.show()
