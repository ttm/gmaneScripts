#-*- coding: utf8 -*-
from __future__ import division
import time, string, sys, __builtin__, cPickle as pickle
import nltk as k, time as T
#import utilsRedes
import utilsRedes
reload(utilsRedes)
from utilsRedes import *

# abrir arquivos de medidas

if "Mmr" in dir(__builtin__):
    Mmr=__builtin__.Mmr
else:
    f=open("/home/r/repos/pickleDir/Mmr","rb")
    Mmr=pickle.load(f)
    f.close()
    __builtin__.Mmr=Mmr

if "Mml" in dir(__builtin__):
    Mml=__builtin__.Mml
else:
    f=open("/home/r/repos/pickleDir/Mml","rb")
    Mml=pickle.load(f)
    f.close()
    __builtin__.Mml=Mml
# acrescentar setor nas medidas topologicas
if "pr" in dir(__builtin__):
    pr=__builtin__.pr
else:
    f=open("./cpickleDIR/pr2","rb")
    pr=pickle.load(f)
    f.close()
    __builtin__.pr=pr

tagsN=["NN","NNS","NNP","NNPS"]
tagsA=["JJ","JJR","JJS","RB","RBR","RBS","RP"]
tagsV=["VB","VBZ","VBP","VBN","VBD","VBG","MD"]
tagsP=["IN","DT","PRP","PRP\$","PDT","TO","CC","WRB","WDT","WP","WP\$"]
tagsC=["CD","EX","UH","FW",]
tags_=[tagsN,tagsA,tagsV,tagsP,tagsC]
tags__=tagsN+tagsA+tagsV+tagsP+tagsC
ML=["ncont","nc","ne/nc","nl/(nc-ne)","nm/nl","nv/nl","np/(nc-ne)","nd/(nc-ne)","nt","ntd","ntd/nt","nt/(nc-ne)","ntp/nt","Nkw/nt","Nwss/Nkw","Nwss\\_/Nkw\\_","Nwsw/Nkw","Nukwsw/Nukw","Nwsssw/Nwss","Nwnsssw/Nwnss","Nkwnssnsw/Nkw","Nkwssnsw/Nkw","mtkw","dtkw","mtkw\\_","dtkw\\_","mtkwnsw","dtkwnsw","mtkwnsw\\_","dtkwnsw\\_","mtams","dtams","mtams\\_","dtams\\_","mtsw","dtsw","mtsw\\_","dtsw\\_","mtsw2","dtsw2","mtsw2\\_","dtsw2\\_","mtTS","dtTS","mtsTS","dtsTS","mtsTSkw","dtsTSkw","mtsTSpv","dtsTSpv","mtmT","dtmT","mttmT","dttmT","mtsmT","dtsmT"]+tags__+["mlwss","dlwss","mtamH","dtamH","mprof","dprof"]

# fazer histogramas 
vp=[[],[],[],[]]
vi=[[],[],[],[]]
vh=[[],[],[],[]]
for i in xrange(4):
    for mm in Mml[i]:
        val=mm[ML.index('mtkw')]
        val=mm[ML.index('ntp/nt')]
        val=mm[ML.index('np/(nc-ne)')]
        val=mm[ML.index('Nwsw/Nkw')]
        val=mm[ML.index('JJ')]
        val=mm[ML.index('NN')]
        if mm[0] in pr[i].perifericosf:
            vp[i]+=[val]
        if mm[0] in pr[i].intermediariosf:
            vi[i]+=[val]
        if mm[0] in pr[i].hubsf:
            vh[i]+=[val]
            

espacamento=0.001
bins=n.arange(0,100,espacamento)
#bins=n.arange(0,100,1)
## teste de kolmogorov
names=["CPP","LAD","LAU","ELE"]
for i in xrange(4):
    hp=n.histogram(vp[i],bins=bins,density=True)
    hi=n.histogram(vi[i],bins=bins,density=True)
    hh=n.histogram(vh[i],bins=bins,density=True)
    chp=n.cumsum(hp[0]*espacamento)
    chi=n.cumsum(hi[0]*espacamento)
    chh=n.cumsum(hh[0]*espacamento)

    dc=n.abs(chh-chp)
    Dnn=max(dc)
    n1=len(vp[i])
    n2=len(vh[i])
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_HP=Dnn/fact

    dc=n.abs(chh-chi)
    Dnn=max(dc)
    n1=len(vh[i])
    n2=len(vi[i])
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_HI=Dnn/fact

    dc=n.abs(chp-chi)
    Dnn=max(dc)
    n1=len(vp[i])
    n2=len(vi[i])
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_PI=Dnn/fact
    print "%s & %.2f & %.2f & %.2f \\\\\\hline"% (names[i],calpha_HP, calpha_HI, calpha_PI)

# para cada setor
v=[vp,vi,vh]
R=["CPP-LAD","CPP-LAU","CPP-ELE","LAD-LAU","LAD-ELE","LAU-ELE"]
R_=["P","I","H"]
for i in xrange(3):
    h1=n.histogram(v[i][0],bins=bins,density=True); np1=v[i][0]
    h2=n.histogram(v[i][1],bins=bins,density=True); np2=v[i][1]
    h3=n.histogram(v[i][2],bins=bins,density=True); np3=v[i][2]
    h4=n.histogram(v[i][3],bins=bins,density=True); np4=v[i][3]

    ch1=n.cumsum(h1[0]*espacamento)
    ch2=n.cumsum(h2[0]*espacamento)
    ch3=n.cumsum(h3[0]*espacamento)
    ch4=n.cumsum(h4[0]*espacamento)
    
    dc=n.abs(ch1-ch2)
    Dnn=max(dc)
    n1=len(np1)
    n2=len(np2)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_12=Dnn/fact
    
    dc=n.abs(ch1-ch3)
    Dnn=max(dc)
    n1=len(np1)
    n2=len(np3)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_13=Dnn/fact
   
    dc=n.abs(ch1-ch4)
    Dnn=max(dc)
    n1=len(np1)
    n2=len(np4)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_14=Dnn/fact
 
    dc=n.abs(ch2-ch3)
    Dnn=max(dc)
    n1=len(np2)
    n2=len(np3)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_23=Dnn/fact
 
    dc=n.abs(ch2-ch4)
    Dnn=max(dc)
    n1=len(np2)
    n2=len(np4)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_24=Dnn/fact
 
    dc=n.abs(ch3-ch4)
    Dnn=max(dc)
    n1=len(np3)
    n2=len(np4)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_34=Dnn/fact
 
    print "%s & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f \\\\\\hline"%(R_[i],calpha_12,calpha_13,calpha_14,calpha_23,calpha_24,calpha_34)



sys.exit()
i=0
for prr in pr: # para cada lista
    mmr=Mmr[i]; i+=1
    for aut in prr.perifericosf:
        jj=0
        while mmr[jj][0]!=aut:
            jj+=1
        mmr[jj].append(0.)
    for aut in prr.intermediariosf:
        jj=0
        while mmr[jj][0]!=aut:
            jj+=1
        mmr[jj].append(1.)
    for aut in prr.hubsf:
        jj=0
        while mmr[jj][0]!=aut:
            jj+=1
        mmr[jj].append(2.)
# fazer correlacao de cada um
# medidas de rede
#i=0
#COV=[]; EVA=[];EVE=[];ARGS=[];EVA_=[];EVE_=[];FVEC=[];FINAL=[];V=[]; V_=[]
#NUM=2
#for mmr in Mmr:
#    mmr_=[i[1:] for i in mmr] # jogando ids fora
#    v=n.array(mmr_).T;V+=[v]
#    v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_+=[v_]
#    cov=n.cov(v_); COV.append(cov)
#    eva,eve=n.linalg.eig(cov); EVA+=[eva]; EVE+=[eve]
#    args=n.argsort(eva)[::-1]; ARGS+=[args]
#    eva_=eva[args]; EVA_+=[eva_]
#    eve_=eve[:,args]; EVE_+=[eve_]
#    fvec=eve[:,:NUM]; FVEC+=[fvec]
#    final=n.dot(fvec.T,v_); FINAL+=[final]

def covPca(Mmr,pr,autores=None):
    ii=0
    COV=[]; EVA=[];EVE=[];ARGS=[];EVA_=[];EVE_=[];FVEC=[];FINAL=[];V=[]; V_=[]
    NUM=2
    for mmr in Mmr:
        if autores ==None:
            mmr_=[i[1:] for i in mmr] # jogando ids fora
        else:
            #au=exec("Mmr."+autores)
            mmr_=[i[1:] for i in mmr if i[0] in getattr(pr[ii],autores)] # jogando ids fora
        v=n.array(mmr_).T;V+=[v]
        v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_+=[v_]
        cov=n.cov(v_); COV.append(cov)
        eva,eve=n.linalg.eig(cov); EVA+=[eva]; EVE+=[eve]
        args=n.argsort(eva)[::-1]; ARGS+=[args]
        eva_=eva[args]; EVA_+=[eva_]
        eve_=eve[:,args]; EVE_+=[eve_]
        fvec=eve[:,:NUM]; FVEC+=[fvec]
        final=n.dot(fvec.T,v_); FINAL+=[final]
        ii+=1
    return COV, EVA, EVE, ARGS, EVA_, EVE_, FVEC, FINAL, V, V_


MR_FIX=["$diameter$","$ncc$","$nwc$","$nsc$","$radius$","$sl$","$trans$","$wi$"]
MR=["$d$","$d_i$","$d_o$","$s$","$s_i$","$s_o$","$bc$","$c$","$tri$","$cv$","$in\;cent$","$in\;comp$","$in\;per$","$in\;per\_$"]
MR2=["$d$","$d_i$","$d_o$","$s$","$s_i$","$s_o$","$bc$","$c$","$triangles$","$cv$","$in\;center$","$in\;component$","$in\;periphery$","$in\;periphery_$"]
MR_=MR+MR_FIX+["sector"]
MR2_=MR2+MR_FIX+["sector"]

COV,COVP,COVI,COVH=covPca(Mmr,pr)[0],covPca(Mmr,pr,"perifericosf")[0],covPca(Mmr,pr,"intermediariosf")[0],covPca(Mmr,pr,"hubsf")[0]
os_cor=((n.abs(COV[0])>=0.8)*(n.abs(COV[1])>=0.8)*(n.abs(COV[2])>=0.8)*(n.abs(COV[3])>=0.8)).nonzero()
#os_cor=((cov>0.0)*(cov<0.5)).nonzero()

os_corp=((n.abs(COVP[0])>=0.8)*(n.abs(COVP[1])>=0.8)*(n.abs(COVP[2])>=0.8)*(n.abs(COVP[3])>=0.8)).nonzero()

os_cori=((n.abs(COVI[0])>=0.8)*(n.abs(COVI[1])>=0.8)*(n.abs(COVI[2])>=0.8)*(n.abs(COVI[3])>=0.8)).nonzero()

os_corh=((n.abs(COVH[0])>=0.8)*(n.abs(COVH[1])>=0.8)*(n.abs(COVH[2])>=0.8)*(n.abs(COVH[3])>=0.8)).nonzero()


jj=0
for i in os_cor[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_cor[1][jj]:
        print ("%s - %s "+("& %.4f "*4)*4+"\\\\ \\hline")%(MR2_[i],MR2_[os_cor[1][jj]], 
               COV[0][i,os_cor[1][jj]],COVP[0][i,os_cor[1][jj]],COVI[0][i,os_cor[1][jj]],COVH[0][i,os_cor[1][jj]],
               COV[1][i,os_cor[1][jj]],COVP[1][i,os_cor[1][jj]],COVI[1][i,os_cor[1][jj]],COVH[1][i,os_cor[1][jj]],
               COV[2][i,os_cor[1][jj]],COVP[2][i,os_cor[1][jj]],COVI[2][i,os_cor[1][jj]],COVH[2][i,os_cor[1][jj]],
               COV[3][i,os_cor[1][jj]],COVP[3][i,os_cor[1][jj]],COVI[3][i,os_cor[1][jj]],COVH[3][i,os_cor[1][jj]])
    jj+=1

#
#ii=0
#COVP=[]; EVA=[];EVE=[];ARGS=[];EVA_=[];EVE_=[];FVEC=[];FINAL=[];V=[]; V_=[]
#NUM=2
#for mmr in Mmr:
#    mmr_=[i[1:] for i in mmr if i[0] in pr[ii].perifericosf] # jogando ids fora
#    v=n.array(mmr_).T;V+=[v]
#    v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_+=[v_]
#    cov=n.cov(v_); COVP.append(cov)
#    eva,eve=n.linalg.eig(cov); EVA+=[eva]; EVE+=[eve]
#    args=n.argsort(eva)[::-1]; ARGS+=[args]
#    eva_=eva[args]; EVA_+=[eva_]
#    eve_=eve[:,args]; EVE_+=[eve_]
#    fvec=eve[:,:NUM]; FVEC+=[fvec]
#    final=n.dot(fvec.T,v_); FINAL+=[final]
#    ii+=1
#

#ii=0
#COVI=[]; EVA=[];EVE=[];ARGS=[];EVA_=[];EVE_=[];FVEC=[];FINAL=[];V=[]; V_=[]
#NUM=2
#for mmr in Mmr:
#    mmr_=[i[1:] for i in mmr if i[0] in pr[ii].intermediariosf] # jogando ids fora
#    v=n.array(mmr_).T;V+=[v]
#    v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_+=[v_]
#    cov=n.cov(v_); COVI.append(cov)
#    eva,eve=n.linalg.eig(cov); EVA+=[eva]; EVE+=[eve]
#    args=n.argsort(eva)[::-1]; ARGS+=[args]
#    eva_=eva[args]; EVA_+=[eva_]
#    eve_=eve[:,args]; EVE_+=[eve_]
#    fvec=eve[:,:NUM]; FVEC+=[fvec]
#    final=n.dot(fvec.T,v_); FINAL+=[final]
#    ii+=1
#


#ii=0
#COVH=[]; EVA=[];EVE=[];ARGS=[];EVA_=[];EVE_=[];FVEC=[];FINAL=[];V=[]; V_=[]
#NUM=2
#for mmr in Mmr:
#    mmr_=[i[1:] for i in mmr if i[0] in pr[ii].hubsf] # jogando ids fora
#    v=n.array(mmr_).T;V+=[v]
#    v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_+=[v_]
#    cov=n.cov(v_); COVH.append(cov)
#    eva,eve=n.linalg.eig(cov); EVA+=[eva]; EVE+=[eve]
#    args=n.argsort(eva)[::-1]; ARGS+=[args]
#    eva_=eva[args]; EVA_+=[eva_]
#    eve_=eve[:,args]; EVE_+=[eve_]
#    fvec=eve[:,:NUM]; FVEC+=[fvec]
#    final=n.dot(fvec.T,v_); FINAL+=[final]
#    ii+=1




jj=0
for i in os_cor[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_cor[1][jj]:
        print ("%s - %s "+"& %.4f "*4+"\\\\ \\hline")%(MR2_[i],MR2_[os_cor[1][jj]], COV[0][i,os_cor[1][jj]],COV[1][i,os_cor[1][jj]], COV[2][i,os_cor[1][jj]],COV[3][i,os_cor[1][jj]])
    jj+=1

print "\n\n\n"
jj=0
for i in os_corp[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_corp[1][jj]:
        print ("%s - %s "+"& %.4f "*4+"\\\\ \\hline")%(MR2_[i],MR2_[os_corp[1][jj]], COVP[0][i,os_corp[1][jj]],COVP[1][i,os_corp[1][jj]], COVP[2][i,os_corp[1][jj]],COVP[3][i,os_corp[1][jj]])
    jj+=1

print "\n\n\n"
jj=0
for i in os_cori[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_cori[1][jj]:
        print ("%s - %s "+"& %.4f "*4+"\\\\ \\hline")%(MR2_[i],MR2_[os_cori[1][jj]], COVI[0][i,os_cori[1][jj]],COVI[1][i,os_cori[1][jj]], COVI[2][i,os_cori[1][jj]],COVI[3][i,os_cori[1][jj]])
    jj+=1

print "\n\n\n"
jj=0
for i in os_corh[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_corh[1][jj]:
        print ("%s - %s "+"& %.4f "*4+"\\\\ \\hline")%(MR2_[i],MR2_[os_corh[1][jj]], COVH[0][i,os_corh[1][jj]],COVH[1][i,os_corh[1][jj]], COVH[2][i,os_corh[1][jj]],COVH[3][i,os_corh[1][jj]])
    jj+=1


#sys.exit()
#################################
# medidas de texto
def covPcaL(Mml,pr,autores=None):
    ii=0
    COVl=[]; EVAl=[];EVEl=[];ARGSl=[];EVA_l=[];EVE_l=[];FVECl=[];FINALl=[];Vl=[]; V_l=[]
    NUM=2
    for mml in Mml:
        if autores==None:
            mml_=[i[1:] for i in mml] # jogando ids fora
        else:
            mml_=[i[1:] for i in mml if i[0] in getattr(pr[ii],autores)] # jogando ids fora
        mml__=[]
        for foo in mml_:
            tags=foo[-39:-6]
            stags=sum(tags)
            if stags:
                tags_=[tag/stags for tag in tags]
                bar=[foo[0]/foo[8]]+foo[1:-39]+tags_+foo[-6:]
                mml__+=[bar]
            else:
                mml__+=[foo]
        v=n.array(mml__).T;Vl+=[v]
        for vv in v:
            nz=n.isnan(vv).nonzero()[0]
            #print "nz", nz
            vv[nz]=n.median(vv)
        # v[-7] até v[-39] incluso
        #for vv in v.T:
        #    vv[-39:-6]=vv[-39:-6]/vv[-39:-6].sum()
        v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_l+=[v_]
        cov=n.cov(v_); COVl.append(cov)
        eva,eve=n.linalg.eig(cov); EVAl+=[eva]; EVEl+=[eve]
        args=n.argsort(eva)[::-1]; ARGSl+=[args]
        eva_=eva[args]; EVA_l+=[eva_]
        eve_=eve[:,args]; EVE_l+=[eve_]
        fvec=eve[:,:NUM]; FVECl+=[fvec]
        final=n.dot(fvec.T,v_); FINALl+=[final]
        ii+=1
    return COVl, EVAl,EVEl,ARGSl,EVA_l,EVE_l,FVECl,FINALl,Vl,V_l
#i=0
#COVl=[]; EVAl=[];EVEl=[];ARGSl=[];EVA_l=[];EVE_l=[];FVECl=[];FINALl=[];Vl=[]; V_l=[]
#NUM=2
#for mml in Mml:
#    mml_=[i[1:] for i in mml] # jogando ids fora
#    mml__=[]
#    for foo in mml_:
#        tags=foo[-39:-6]
#        stags=sum(tags)
#        if stags:
#            tags_=[tag/stags for tag in tags]
#            bar=[foo[0]/foo[8]]+foo[1:-39]+tags_+foo[-6:]
#            mml__+=[bar]
#        else:
#            mml__+=[foo]
#    v=n.array(mml__).T;Vl+=[v]
#    for vv in v:
#        nz=n.isnan(vv).nonzero()[0]
#        print "nz", nz
#        vv[nz]=n.median(vv)
#    # v[-7] até v[-39] incluso
#    #for vv in v.T:
#    #    vv[-39:-6]=vv[-39:-6]/vv[-39:-6].sum()
#    v_=n.array([(((vv-vv.mean())/vv.std()) if vv.std() else n.zeros(len(vv))) for vv in v]); V_l+=[v_]
#    cov=n.cov(v_); COVl.append(cov)
#    eva,eve=n.linalg.eig(cov); EVAl+=[eva]; EVEl+=[eve]
#    args=n.argsort(eva)[::-1]; ARGSl+=[args]
#    eva_=eva[args]; EVA_l+=[eva_]
#    eve_=eve[:,args]; EVE_l+=[eve_]
#    fvec=eve[:,:NUM]; FVECl+=[fvec]
#    final=n.dot(fvec.T,v_); FINALl+=[final]
tagsN=["NN","NNS","NNP","NNPS"]
tagsA=["JJ","JJR","JJS","RB","RBR","RBS","RP"]
tagsV=["VB","VBZ","VBP","VBN","VBD","VBG","MD"]
tagsP=["IN","DT","PRP","PRP\$","PDT","TO","CC","WRB","WDT","WP","WP\$"]
tagsC=["CD","EX","UH","FW",]
tags_=[tagsN,tagsA,tagsV,tagsP,tagsC]
tags__=tagsN+tagsA+tagsV+tagsP+tagsC

ML=["ncont","nc","ne/nc","nl/(nc-ne)","nm/nl","nv/nl","np/(nc-ne)","nd/(nc-ne)","nt","ntd","ntd/nt","nt/(nc-ne)","ntp/nt","Nkw/nt","Nwss/Nkw","Nwss\\_/Nkw\\_","Nwsw/Nkw","Nukwsw/Nukw","Nwsssw/Nwss","Nwnsssw/Nwnss","Nkwnssnsw/Nkw","Nkwssnsw/Nkw","mtkw","dtkw","mtkw\\_","dtkw\\_","mtkwnsw","dtkwnsw","mtkwnsw\\_","dtkwnsw\\_","mtams","dtams","mtams\\_","dtams\\_","mtsw","dtsw","mtsw\\_","dtsw\\_","mtsw2","dtsw2","mtsw2\\_","dtsw2\\_","mtTS","dtTS","mtsTS","dtsTS","mtsTSkw","dtsTSkw","mtsTSpv","dtsTSpv","mtmT","dtmT","mttmT","dttmT","mtsmT","dtsmT"]+tags__+["mlwss","dlwss","mtamH","dtamH","mprof","dprof"]

COV,COVP,COVI,COVH=covPcaL(Mml,pr)[0],covPcaL(Mml,pr,"perifericosf")[0],covPcaL(Mml,pr,"intermediariosf")[0],covPcaL(Mml,pr,"hubsf")[0]

os_cor=((n.abs(COV[0])>=0.8)*(n.abs(COV[1])>=0.8)*(n.abs(COV[2])>=0.8)*(n.abs(COV[3])>=0.8)).nonzero()
#os_cor=((cov>0.0)*(cov<0.5)).nonzero()

os_corp=((n.abs(COVP[0])>=0.8)*(n.abs(COVP[1])>=0.8)*(n.abs(COVP[2])>=0.8)*(n.abs(COVP[3])>=0.8)).nonzero()

os_cori=((n.abs(COVI[0])>=0.8)*(n.abs(COVI[1])>=0.8)*(n.abs(COVI[2])>=0.8)*(n.abs(COVI[3])>=0.8)).nonzero()

os_corh=((n.abs(COVH[0])>=0.8)*(n.abs(COVH[1])>=0.8)*(n.abs(COVH[2])>=0.8)*(n.abs(COVH[3])>=0.8)).nonzero()


jj=0
for i in os_cor[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_cor[1][jj]:
        print ("%s-%s "+("& %.3f "*4)*4+"\\\\ \\hline")%(ML[i],ML[os_cor[1][jj]], 
               COV[0][i,os_cor[1][jj]],COVP[0][i,os_cor[1][jj]],COVI[0][i,os_cor[1][jj]],COVH[0][i,os_cor[1][jj]],
               COV[1][i,os_cor[1][jj]],COVP[1][i,os_cor[1][jj]],COVI[1][i,os_cor[1][jj]],COVH[1][i,os_cor[1][jj]],
               COV[2][i,os_cor[1][jj]],COVP[2][i,os_cor[1][jj]],COVI[2][i,os_cor[1][jj]],COVH[2][i,os_cor[1][jj]],
               COV[3][i,os_cor[1][jj]],COVP[3][i,os_cor[1][jj]],COVI[3][i,os_cor[1][jj]],COVH[3][i,os_cor[1][jj]])
    jj+=1


print "\n=====\n"
#os_corl=(n.abs(cov)<0.07).nonzero()
#os_corl=(n.abs(cov)>.9).nonzero()

#os_corl=((cov>0.0)*(cov<0.5)).nonzero()
#os_corl=((cov>0.99)*(cov<1.5)).nonzero()
#os_corl=((n.abs(cov)>0.960)*(n.abs(cov)<=0.99)).nonzero()
#os_corl=((cov>0.6)*(cov<0.7)).nonzero()
#os_corl=(n.abs(cov)<0.1).nonzero()
#os_corl=(cov<-0.29).nonzero()

#jj=0
#for i in os_corl[0]:
#    #if MR_[i]!=MR_[os_cor[1][jj]]:
#    if i<os_corl[1][jj]:
#        print ML[i],ML[os_corl[1][jj]], cov[i,os_corl[1][jj]]
#    jj+=1


print 'ok'
    
# fazer correlacao da matriz conjunta
def covPcaC(Mml,Mmr,pr,autores=None):
    NUM=2
    ii=0
    MM_=[]
    MM__=[]
    V_c=[]
    COVc=[]
    EVAc=[]
    EVEc=[]
    ARGSc=[]
    EVA_c=[]
    EVE_c=[]
    FVECc=[]
    FINALc=[]
    time=T.time()
    for mmr in Mmr: # para cada lista
        mml=Mml[ii]
        ar=[i[0] for i in mmr]
        al=[i[0] for i in mml]
        # as posições dos elementos de ar em al:
        perm=[al.index(i) for i in ar] 
        mml2=[mml[i] for i in perm] 
        ############
        if autores==None:
            mml_=[i[1:] for i in mml2] # jogando ids fora
        else:
            mml_=[i[1:] for i in mml2 if i[0] in getattr(pr[ii],autores)] # jogando ids fora
            mmr=[i for i in mmr if i[0] in getattr(pr[ii],autores)] # jogando ids fora
            
        mml__=[]
        for foo in mml_:
            tags=foo[-39:-6]
            stags=sum(tags)
            if stags:
                tags_=[tag/stags for tag in tags]
                bar=foo[:-39]+tags_+foo[-6:]
                mml__+=[bar]
            else:
                mml__+=[foo]
        ##########
        #MM=n.hstack(([i[1:] for i in mml__],[i[1:] for i in mmr])); MM_+=[MM]
        print T.time()-time; time=T.time()
        MM=n.hstack((mml__,[i[1:] for i in mmr])).T; MM_+=[MM]
        count=0
        for MMM in MM:
            nz=n.isnan(MMM).nonzero()[0]
            count+=len(nz)
            #print "nz", nz
            MMM[nz]=n.median(MMM)
        print ii,count
        print T.time()-time; time=T.time()

        v_=n.array([(((MMM-MMM.mean())/MMM.std()) if MMM.std() else n.zeros(len(MMM))) for MMM in MM]); V_c+=[v_]
        cov=n.cov(v_); COVc.append(cov)
        eva,eve=n.linalg.eig(cov); EVAc+=[eva]; EVEc+=[eve]
        args=n.argsort(eva)[::-1]; ARGSc+=[args]
        eva_=eva[args]; EVA_c+=[eva_]
        eve_=eve[:,args]; EVE_c+=[eve_]
        fvec=eve[:,:NUM]; FVECc+=[fvec]
        final=n.dot(fvec.T,v_); FINALc+=[final]
        print T.time()-time; time=T.time()
        ii+=1
    return COVc,EVAc,EVEc,ARGSc,EVA_c,EVE_c,FVECc,FINALc,V_c,MM
MC=ML+MR_

#os_corc=((n.abs(cov)>0.960)*(n.abs(cov)<=0.99)).nonzero()
#os_corc=((n.abs(cov)>=0.6)).nonzero()
#os_corc=((n.abs(cov)>0.960)*(n.abs(cov)<=0.99)).nonzero()

COV,COVP,COVI,COVH=covPcaC(Mml,Mmr,pr)[0],covPcaC(Mml,Mmr,pr,"perifericosf")[0],covPcaC(Mml,Mmr,pr,"intermediariosf")[0],covPcaC(Mml,Mmr,pr,"hubsf")[0]

os_cor=((n.abs(COV[0])>=0.5)*(n.abs(COV[1])>=0.5)*(n.abs(COV[2])>=0.5)*(n.abs(COV[3])>=0.5)).nonzero()
#os_cor=((cov>0.0)*(cov<0.5)).nonzero()

os_corp=((n.abs(COVP[0])>=0.5)*(n.abs(COVP[1])>=0.5)*(n.abs(COVP[2])>=0.5)*(n.abs(COVP[3])>=0.5)).nonzero()

os_cori=((n.abs(COVI[0])>=0.5)*(n.abs(COVI[1])>=0.5)*(n.abs(COVI[2])>=0.5)*(n.abs(COVI[3])>=0.5)).nonzero()

os_corh=((n.abs(COVH[0])>=0.5)*(n.abs(COVH[1])>=0.5)*(n.abs(COVH[2])>=0.5)*(n.abs(COVH[3])>=0.5)).nonzero()

jj=0
for i in os_cor[0]:
    #if MR_[i]!=MR_[os_cor[1][jj]]:
    if i<os_cor[1][jj] and i<=94 and os_cor[1][jj]>=95:
        print ("%s-%s "+("& %.3f "*4)*4+"\\\\ \\hline")%(MC[i],MC[os_cor[1][jj]], 
               COV[0][i,os_cor[1][jj]],COVP[0][i,os_cor[1][jj]],COVI[0][i,os_cor[1][jj]],COVH[0][i,os_cor[1][jj]],
               COV[1][i,os_cor[1][jj]],COVP[1][i,os_cor[1][jj]],COVI[1][i,os_cor[1][jj]],COVH[1][i,os_cor[1][jj]],
               COV[2][i,os_cor[1][jj]],COVP[2][i,os_cor[1][jj]],COVI[2][i,os_cor[1][jj]],COVH[2][i,os_cor[1][jj]],
               COV[3][i,os_cor[1][jj]],COVP[3][i,os_cor[1][jj]],COVI[3][i,os_cor[1][jj]],COVH[3][i,os_cor[1][jj]])
    jj+=1

############################
#G,P,I,H=covPca(Mmr,pr),covPca(Mmr,pr,"perifericosf"),covPca(Mmr,pr,"intermediariosf"),covPca(Mmr,pr,"hubsf")


# analisando PCA
EVA,EVE  =covPcaC(Mml,Mmr,pr)[4:6]
EVAP,EVEP=covPcaC(Mml,Mmr,pr,"perifericosf")[4:6]
EVAI,EVEI=covPcaC(Mml,Mmr,pr,"intermediariosf")[4:6]
EVAH,EVEH=covPcaC(Mml,Mmr,pr,"hubsf")[4:6]

EVA,EVE=n.real(EVA),n.real(EVE)
EVA[0]=EVA[0]/EVA[0].sum()
EVA[1]=EVA[1]/EVA[1].sum()
EVA[2]=EVA[2]/EVA[2].sum()
EVA[3]=EVA[3]/EVA[3].sum()
EVAP,EVEP=n.real(EVAP),n.real(EVEP)
EVAP[0]=EVAP[0]/EVAP[0].sum()
EVAP[1]=EVAP[1]/EVAP[1].sum()
EVAP[2]=EVAP[2]/EVAP[2].sum()
EVAP[3]=EVAP[3]/EVAP[3].sum()
EVAI,EVEI=n.real(EVAI),n.real(EVEI)
EVAI[0]=EVAI[0]/EVAI[0].sum()
EVAI[1]=EVAI[1]/EVAI[1].sum()
EVAI[2]=EVAI[2]/EVAI[2].sum()
EVAI[3]=EVAI[3]/EVAI[3].sum()
EVAH,EVEH=n.real(EVAH),n.real(EVEH)
EVAH[0]=EVAH[0]/EVAH[0].sum()
EVAH[1]=EVAH[1]/EVAH[1].sum()
EVAH[2]=EVAH[2]/EVAH[2].sum()
EVAH[3]=EVAH[3]/EVAH[3].sum()

# fazendo print dos primeirs autovalores para as 4 listas e 4 conjuntos de vértices
print ("$\lambda$ & "+("%.3f & "*4)*4+"\\\\\\hline")%(EVA[0][0],EVAP[0][0],EVAI[0][0],EVAH[0][0],
                                                    EVA[1][0],EVAP[1][0],EVAI[1][0],EVAH[1][0],
                                                    EVA[2][0],EVAP[2][0],EVAI[2][0],EVAH[2][0],
                                                    EVA[3][0],EVAP[3][0],EVAI[3][0],EVAH[3][0])
print "=======================\n\n\n\n"
# uma tabela para cada autovetor
for i in xrange(4,5):
    l=[]
    NZ=n.array([],dtype=n.int)
    E=[]
    EP=[]
    EI=[]
    EH=[]
    for j in xrange(4):
        #print EVA[j][i],EVAP[j][i],EVAI[j][i],EVAH[j][i]
        l+=[100*EVA[j][i],100*EVAP[j][i],100*EVAI[j][i],100*EVAH[j][i]]
        EVE_=EVE[j][i]/n.sum(n.abs(EVE[j][i])); E+=[EVE_]
        EVEP_=EVEP[j][i]/n.sum(n.abs(EVEP[j][i])); EP+=[EVEP_]
        EVEI_=EVEI[j][i]/n.sum(n.abs(EVEI[j][i])); EI+=[EVEI_]
        EVEH_=EVEH[j][i]/n.sum(n.abs(EVEH[j][i])); EH+=[EVEH_]

        nz=  (n.abs(EVE_)>0.05).nonzero()[0]
        nzp=(n.abs(EVEP_)>0.05).nonzero()[0]
        nzi=(n.abs(EVEI_)>0.05).nonzero()[0]
        nzh=(n.abs(EVEH_)>0.05).nonzero()[0]
        NZ=n.union1d(NZ,nz)
        NZ=n.union1d(NZ,nzp)
        NZ=n.union1d(NZ,nzi)
        NZ=n.union1d(NZ,nzh)

    print ("$\lambda$ "+("& %.2f "*4)*4+"\\\\\\hline")%tuple(l)
    for nn in NZ:
        l=[]
        for j in xrange(4):
            l+=[100*E[j][nn],100*EP[j][nn],100*EI[j][nn],100*EH[j][nn]]
        print ("%s "+("& %.2f "*4)*4+"\\\\\\hline")%tuple([MC[nn]]+l)


#jj=0
#for i in os_corc[0]:
#    #if MR_[i]!=MR_[os_cor[1][jj]]:
#    if i<os_corc[1][jj] and i<=94 and os_corc[1][jj]>=95:
#        print MC[i],MC[os_corc[1][jj]], cov[i,os_corc[1][jj]]
#    jj+=1

# fazer pca conjunto
# fazer pca de cada
