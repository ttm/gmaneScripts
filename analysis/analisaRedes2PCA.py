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
caminho="./lau/"
#caminho="./lad/" # este jah foi o primeiro
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

janelas=(5000,1000,500,250,100,50)
#janelas=(5000,)
if "ee" in dir(__builtin__):
    ee=__builtin__.ee
else:
    ee=[]
    #janelas=(100,50)
    for j in [janelas[1]]:
        print("janela: %i"%(j,))
        if j < 500:
            #passo = int(j/2)
            passo = int(j*2)
        else:
            passo = int(j)
        e=EvoluiRede(0,20001,j,passo,m, caminho)
        ee.append(e)
        e.drawSections2()
    __builtin__.ee=ee

md=[]
countEv=0
for e in ee: # for each evolution (each window size)
    print(countEv)
    countPr=0
    md.append([])
    eig_vecs=[]
    eigs=[]
    for pr in e.prs: # for each partition
        if e.janela > 100:
            per  =[]
            inter=[]
            hubs =[]
            forcas=pr.g.degree(weight="weight")
            for node in forcas.keys():
                if forcas[node] < pr.f1:
                    per.append(node)
                elif forcas[node] >= pr.f2:
                    hubs.append(node)
                else:
                    inter.append(node)
            #per  =pr.C.cas_exc[0]
            #inter=pr.C.cas_exc[1]
            #hubs =pr.C.cas_exc[2]
        else:
            per=pr.C.cas_exc[0]
            inter=pr.C.cas_exc[1]
            hubs=pr.C.cas_exc[2]
            
        everyone=per+inter+hubs
        tclass=[0]*len(per)+[1]*len(inter)+[2]*len(hubs)
        print("entrando nas primeiras medidas")
        degree=pr.g.degree()
        strengh=pr.g.degree(weight="weight")
        print("clustering")
        cc=x.clustering(pr.g.to_undirected())
        #print("closenes vitality")
        #cv=x.vitality.closeness_vitality(pr.g,weight="weight")
        print("betweeness")
        bc=x.betweenness_centrality(pr.g,weight="weight")

        print("primeira batelada foi, agora entrada e saida")
        degree_=[degree[ev1] for ev1 in everyone]
        id_=pr.g.in_degree()
        id_=[id_[ev1] for ev1 in everyone]
        od= pr.g.out_degree()
        od_= [od[ev1] for ev1 in everyone]

        strengh_=[strengh[ev1] for ev1 in everyone]
        is_= pr.g.in_degree(weight="weight")
        is_=[is_[ev1] for ev1 in everyone]
        os=  pr.g.out_degree(weight="weight")
        os_=[os[ev1] for ev1 in everyone]
        print("segunda batelada de medidas")

        cc_=[cc[ev1] for ev1 in everyone]
        #cv_=[cv[ev1] for ev1 in everyone]
        bc_=[bc[ev1] for ev1 in everyone]
        #md[-1].append(n.vstack((degree_,id_,od_,strengh_,is_,os_,cc_,cv_,bc_,tclass)))


        #  medidas compostas
        # media e desvio das assimetrias e desequlibrios de cada ligacao
        assimetrias=[]
        desequilibrios=[]
        assimArestaM=[]
        assimArestaDP=[]
        deseqArestaM=[]
        deseqArestaDP=[]
        for ev in everyone:
            # calculo de assimetria para ev
            pre=pr.g.predecessors(ev)
            suc=pr.g.successors(ev)
            assimetrias.append(len(pre)-len(suc))

            entrada=pr.g.in_degree(ev,weight="weight")
            saida=pr.g.out_degree(ev,weight="weight")
            desequilibrios.append(entrada-saida)

            as_=[]
            de_=[]
            for node in pre:
                if node in suc:
                    as_.append(0.)
                    de_.append((pr.g[node][ev]['weight']-pr.g[ev][node]['weight'])/strengh[node])
                else:
                    as_.append(1.)
                    de_.append(pr.g[node][ev]['weight']/strengh[node])
            for node in suc:
                if node in pre:
                    pass
                else:
                    as_.append(-1.)
                    de_.append(-pr.g[ev][node]['weight']/strengh[node])

            if len(as_)>0:
                assimArestaM.append(n.mean(as_))
                assimArestaDP.append(n.std(as_))
                deseqArestaM.append(n.mean(de_))
                deseqArestaDP.append(n.std(de_))
            else:
                assimArestaM.append(0.)
                assimArestaDP.append(0.)    
                deseqArestaM.append(0.)
                deseqArestaDP.append(0.)

        md[-1].append(n.vstack((degree_,id_,od_,strengh_,is_,os_,cc_,bc_,assimetrias,desequilibrios,assimArestaM,assimArestaDP,deseqArestaM,deseqArestaDP,tclass)))
        print("arrumacao e fazecao de vetor")

        r=[(cl==0) for cl in tclass]
        g=[(cl==1) for cl in tclass]
        b=[(cl==2) for cl in tclass]
        rgb=n.vstack((r,g,b)).T
        #p.plot(degree_,strengh_,marker="o",color=tclass)
        tcolor=[tuple(rrr) for rrr in rgb]
        p.plot(degree_[:len(per)],strengh_[:len(per)],"bo", ms=3.9,label="peripheral")
        p.plot(degree_[len(per):len(per)+len(inter)],strengh_[len(per):len(per)+len(inter)],"go", ms=3.9,label="intermediary")
        p.plot(degree_[-len(hubs):],strengh_[-len(hubs):],"ro", ms=3.9,label="hubs")
        p.legend(loc="upper left")
        p.xlabel(r"degree $\rightarrow$")
        p.ylabel(r"strengh $\rightarrow$")
        p.ylim(min(strengh_)-1,max(strengh_)+1)
        p.xlim(min(degree_)-1,max(degree_)+1)
        #p.plot(degree_,strengh_,marker="o")
        p.savefig("tempoLAU/ev%ipr%i.png" % (countEv,countPr))
        p.clf()

        p.plot(degree_[:len(per)],cc_[:len(per)],"bo", ms=3.9,label="peripheral")
        p.plot(degree_[len(per):len(per)+len(inter)],cc_[len(per):len(per)+len(inter)],"go", ms=3.9,label="intermediary")
        p.plot(degree_[-len(hubs):],cc_[-len(hubs):],"ro", ms=3.9,label="hubs")
        p.legend(loc="upper right")
        p.xlabel(r"degree $\rightarrow$")
        p.ylabel(r"clustering coefficient $\rightarrow$")
        p.ylim(-0.1,1.1)
        p.title("Clustering coefficient versus degree of vertex")
        p.xlim(min(degree_)-1,max(degree_)+1)
        p.savefig("tempoLAU/ev%ipr%iCC.png" % (countEv,countPr))
        p.clf()
        ###############
        # Se foi feito com a matriz certinha (i,j)
        #M=md[-1][-1][:-1].T # tudo menos a classe

        ## tratamento, z-score
        #M[:,0]=(M[:,0]-M[:,0].mean())/M[:,0].std()

        #c_m=n.cov(M) # matriz de covariancia
        #eig_values, eig_vectors = n.linalg.eig(c_m)

        ## Ordering eigenvalues and eigenvectors
        #args=n.argsort(eig_values)[::-1]
        #eig_values=eig_values[args]
        #eig_vectors=eig_vectors[:,args]

        ## retaining only a selected number of eigenvectors
        #feature_vec=eig_vectors[:,:2]

        #final_data=n.dot(feature_vec.T,M.T)

        ###############
        # Se foi feito com a matriz invertida (j,i)
        #M=md[-1][-1][:-1] # tudo menos a classe
        #M=md[-1][-1][:-1] # tudo menos a classe
        #M=md[-1][-1][:-7] # tudo menos a classe e medidas de sym
        M=md[-1][-1][[0,6,7]] # apenas grau, cc e btness

        # tratamento, z-score
        for i in xrange(M.shape[0]):
            M[i]=(M[i]-M[i].mean())/M[i].std()

        c_m=n.cov(M) # matriz de covariancia
        if not n.isnan(c_m).sum():
            eig_values, eig_vectors = n.linalg.eig(c_m)

            # Ordering eigenvalues and eigenvectors
            args=n.argsort(eig_values)[::-1]
            eig_values=eig_values[args]
            eig_vectors=eig_vectors[:,args]

            # retaining only a selected number of eigenvectors
            feature_vec=eig_vectors[:,:2]
            #print(eig_vectors[:,3])

            final_data=n.dot(M.T,feature_vec)
            xx=final_data[:,0]
            yy=final_data[:,1]
            print eig_vectors[:,:4], eig_values
            eig_vecs.append(eig_vectors[:,:3])
            eigs.append(eig_values)
            p.plot(xx[:len(per)],yy[:len(per)],"bo", ms=3.9,label="peripheral")
            p.plot(xx[len(per):len(per)+len(inter)],yy[len(per):len(per)+len(inter)],"go", ms=3.9,label="intermediary")
            p.plot(xx[-len(hubs):],yy[-len(hubs):],"ro", ms=3.9,label="hubs")
            foo=feature_vec[:,0]
            foo_=("%.2f, "*len(foo)) % tuple(foo)
            #p.xlabel(foo_, fontsize=10)
            p.xlabel("PC1", fontsize=10)
            foo=feature_vec[:,1]
            foo_=("%.2f, "*len(foo)) % tuple(foo)
            #p.ylabel(foo_, fontsize=10)
            p.ylabel("PC2", fontsize=10)
            foo=(eig_values[:4]/eig_values.sum())*100
            foo_=r"$\lambda = $"+("%.3f, "*len(foo) % tuple(foo))
            #p.title(foo_)
            p.title("Vertex position in principal components (PCA)")

            p.legend(loc="upper right")
            p.ylim(min(yy)-1,max(yy)+1)
            p.xlim(min(xx)-1,max(xx)+1)
            p.savefig("PCACHU/ev%ipr%iPCA.png" % (countEv,countPr))
            p.clf()
        else:
            print("degenerou-se")
        countPr+=1
        print(countPr,countEv,e.janela)
    countEv+=1

fv=n.real(eig_vecs)
eigs=n.real(eigs)

#eigs.mean(0) # media dos auto-valores
#abs(fv[:,:,0]).mean(0) # media da composicao dos autovetores

totais=eigs.sum(1)
foo=0
for i in eigs:
    eigs[foo]=(eigs[foo]/eigs[foo].sum())*100
    foo+=1

foo=0
bar=0    
for i in fv:
    bar=0
    for j in xrange(i.shape[1]):
        fv[foo,:,bar]=(n.abs(fv[foo,:,bar])/n.abs(fv[foo,:,bar]).sum())*100
        bar+=1
    foo+=1
    
#
#In [169]: fv[:,:,0].mean(0)
#Out[169]: 
#array([ 11.51575004,  11.45344434,  10.67880313,  11.37672484,
#        11.33302886,  10.74652016,   0.90582107,  10.87527092,
#         3.9887245 ,   4.15070248,   1.21117739,   5.7845798 ,
#         0.79451924,   5.18493323])
# para ler media e desvioA
# normalizandos os eigs e fv.
# eigs deve estar como percentagem

# cada vetor de fv deve ter composicao em percentagem



       
    # PCA

# md[-1][-1][:,-1] eh um individuo
# md[-1][-1][:,-1][-1] == 2 eh hub
# md[-1][-1][:,-1][-1] == 1 eh intermediario 
# md[-1][-1][:,-1][-1] == 0 eh periferico
# md[-1][-1][:,-1][0] eh o grau do vértice

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


