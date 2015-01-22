#-*- coding: utf8 -*-
from __future__ import division
import time, sys, __builtin__
import utilsRedes
reload(utilsRedes)
from utilsRedes import *
t=time.time()


de=0
ate=20001
#caminho="./cpp/"
#caminho="./lau/"
caminho="./lad/"
#caminho="./metarec/"
if sum([i in dir(__builtin__) for i in ("m","de","ate")])==3:
    print(__builtin__.m)
    if __builtin__.m and __builtin__.de==de and __builtin__.ate==ate:
        print("reutilizando mensagens")
        mensagens=m=__builtin__.m
    else:
        print("lendo mensagens")
        mensagens=m=Mensagens(caminho,de,ate)
        __builtin__.m=m
        __builtin__.de=de
        __builtin__.ate=ate
else:
    print("lendo mensagens")
    mensagens=m=Mensagens(caminho,de,ate)
    __builtin__.m=m
    __builtin__.de=de
    __builtin__.ate=ate

print("lidas as mensagens", time.time()-t); t=time.time()

janelas=(10000,5000,1000,500,250,100,50)
#janelas=(100,50)
for j in janelas:
    if j < 500:
        passo = int(j/2)
    else:
        passo = int(j/10)
    e=EvoluiRede(0,20001,j,passo,m, caminho)
    e.drawSections()

sys.exit()
#medidas_mensagens=mm=MedidasMensagens( mensagens, 0,200 )
#rede=Rede( mensagens, 0, 501 )
#mr=MedidasRede( rede )
#pr=ParticionaRede( mr )
#
D=5000 # tamanho da janela em mensagens (D=0 => g crescente; D<0 movimento começa do final da rede)
passo=500 # mensagens adiantadas em cada passo
# iniciando loop de observacao:

class L:
    N=[]
    dist=[]
    dist_f=[]
    dist_i=[]
    dist_o=[]
    dist_fi=[]
    dist_fo=[]
    dist_exc=[]
    dist_inc=[]
    dist_cas_exc=[]
    dist_cas_inc=[]
    dist_ext_exc=[]
    dist_ext_inc=[]
    quebras=[]

de=0
ate_=ate-D
contador=0
for pos in xrange(de,ate_,passo):
    print("criando rede"); t=time.time()
    rede=Rede(mensagens, pos, pos+D)
    print("rede criada: ", t-time.time()); t= time.time()
    #mr=MedidasRede( rede )
    #print("medidas obtidas da rede: ", t-time.time()); t= time.time()
    pr=ParticionaRede( rede )
    print("rede particionada: ", t-time.time()); t= time.time()
    L.dist.append(pr.dist)
    L.dist_f.append(pr.dist_f)
    L.dist_i.append(pr.dist_i)
    L.dist_o.append(pr.dist_o)
    L.dist_fi.append(pr.dist_fi)
    L.dist_fo.append(pr.dist_fo)
    L.dist_exc.append(pr.C.dist_exc)
    L.dist_inc.append(pr.C.dist_inc)
    L.dist_cas_exc.append(pr.C.dist_cas_exc)
    L.dist_cas_inc.append(pr.C.dist_cas_inc)
    L.dist_ext_exc.append(pr.C.dist_ext_exc)
    L.dist_ext_inc.append(pr.C.dist_ext_inc)
    L.quebras.append(pr.quebras)
    L.N.append(pr.g.number_of_nodes())
    print(u"registradas as distribuições: ", t-time.time()); t= time.time()
    contador+=1
    print(contador)

L.s_exc=[]
L.s_inc=[]
for i in xrange(contador):
    L.s_exc.append(sum(L.dist_exc[i]))
    L.s_inc.append(sum(L.dist_inc[i]))

    

arq="%i.txt"%(D,)
f=open(arq,"wb")

#f.write)
f.close()

p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist]
intermediarios=[d[1]/sum(d) for d in L.dist]
hubs=[d[2]/sum(d) for d in           L.dist]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering degree")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_f]
intermediarios=[d[1]/sum(d) for d in L.dist_f]
hubs=[d[2]/sum(d) for d in           L.dist_f]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering strength")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes.png")

p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist_i]
intermediarios=[d[1]/sum(d) for d in L.dist_i]
hubs=[d[2]/sum(d) for d in           L.dist_i]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering in-degree")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_o]
intermediarios=[d[1]/sum(d) for d in L.dist_o]
hubs=[d[2]/sum(d) for d in           L.dist_o]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering out-degree")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_io.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist_fi]
intermediarios=[d[1]/sum(d) for d in L.dist_fi]
hubs=[d[2]/sum(d) for d in           L.dist_fi]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering in-strengh")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_fo]
intermediarios=[d[1]/sum(d) for d in L.dist_fo]
hubs=[d[2]/sum(d) for d in           L.dist_fo]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering out-strengh")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_fio.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist_exc]
intermediarios=[d[1]/sum(d) for d in L.dist_exc]
hubs=[d[2]/sum(d) for d in           L.dist_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification unanimous in all measures")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_inc]
intermediarios=[d[1]/sum(d) for d in L.dist_inc]
hubs=[d[2]/sum(d) for d in           L.dist_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification considering incidences in any measure")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_C_incexc.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist_cas_exc]
intermediarios=[d[1]/sum(d) for d in L.dist_cas_exc]
hubs=[d[2]/sum(d) for d in           L.dist_cas_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification unanimous cascade frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_cas_inc]
intermediarios=[d[1]/sum(d) for d in L.dist_cas_inc]
hubs=[d[2]/sum(d) for d in           L.dist_cas_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification inclusive frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_C_cas_incexc.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    L.dist_ext_exc]
intermediarios=[d[1]/sum(d) for d in L.dist_ext_exc]
hubs=[d[2]/sum(d) for d in           L.dist_ext_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification unanimous cascade frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    L.dist_ext_inc]
intermediarios=[d[1]/sum(d) for d in L.dist_ext_inc]
hubs=[d[2]/sum(d) for d in           L.dist_ext_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("Classification inclusive frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_C_ext_incexc.png")


