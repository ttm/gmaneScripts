#-*- coding: utf8 -*-
from __future__ import division
import time, string, sys, __builtin__, cPickle as pickle
import nltk as k
import utilsRedes
reload(utilsRedes)
from utilsRedes import *

#from ZODB.FileStorage import FileStorage
#from ZODB.DB import DB
#import transaction

atime=time.time()

caminhos={"ele":"./ele/", "cpp":"./cpp/","lau":"./lau/","lad":"./lad/"}
if "m" in dir(__builtin__):
    m=__builtin__.m # m=(cpp, lad, lau, ele), cada um um obj com as 20k msgs
    print("reutilizando mensagens")
else:
    try:
        f=open("cpickleDIR/m","rb")
        m=pickle.load(f)
        f.close()
        __builtin__.m=m
        print("aproveitadas mensagens do pickleDIR")
        print time.time()-atime; atime=time.time()
    except:
        print("lendo mensagens")
        cpp=Mensagens(caminhos["cpp"],0,20001, text="yes")
        print("lido cpp")
        print time.time()-atime; atime=time.time()
        lad=Mensagens(caminhos["lad"],0,20001, text="yes")
        print("lido lad")
        print time.time()-atime; atime=time.time()
        lau=Mensagens(caminhos["lau"],0,20001, text="yes")
        print("lido lau")
        print time.time()-atime; atime=time.time()
        ele=Mensagens(caminhos["ele"],0,20001, text="yes")
        print("lido ele")
        print time.time()-atime; atime=time.time()
        m=(cpp,lad,lau,ele)
        f=open("./cpickleDIR/m", 'wb')
        pickle.dump(m,f,-1)
        f.close()
        __builtin__.m=m
        print("feito dump")
        print time.time()-atime; atime=time.time()

try:
    r=__builtin__.r
except:
    try:
        f=open("cpickleDIR/r","rb")
        r=pickle.load(f)
        f.close()
        print("aproveitadas redes do cpickleDIR")
        __builtin__.r=r
    except:
        rcpp=Rede(m[0],0,20001)
        rlad=Rede(m[1],0,20001)
        rlau=Rede(m[2],0,20001)
        rele=Rede(m[3],0,20001)
        r=[rcpp,rlad,rlau,rele]
        f=open("./cpickleDIR/r", 'wb')
        pickle.dump(r,f,-1)
        f.close()
        print time.time()-atime; atime=time.time()
        __builtin__.r=r

try:
    f=open("cpickleDIR/pr2","rb")
    pr2=pickle.load(f)
    f.close()
    print("aproveitadas particoes do cpickleDIR")
    print time.time()-atime; atime=time.time()
except:
    print("deu pau, precisa fazer as redes para fazer as particoes, tah feito no analisaRedesTexto2.py")
    prcpp=ParticionaRede2(r[0])
    prlad=ParticionaRede2(r[1])
    prlau=ParticionaRede2(r[2])
    prele=ParticionaRede2(r[3])
    pr2=[prcpp,prlad,prlau,prele]
    f=open("./cpickleDIR/pr2", 'wb')
    pickle.dump(pr2,f,-1)
    f.close()
    print time.time()-atime; atime=time.time()

# fazer medidas de rede
if "mr" not in dir(__builtin__):
    try:
        f=open("/disco/mr","rb")
        mr=pickle.load(f)
        f.close()
        __builtin__.mr=mr
        print("aproveitado mr")
    except:
        print("fazendo mr")
        mr=[]
        for rr in r:
            mmr=MedidasRede(rr)
            mr.append(mmr)
        f=open("/disco/mr", 'wb')
        pickle.dump(mr,f,-1)
        f.close()
        __builtin__.mr=mr
        print("feito mr")
else:           
    mr=__builtin__.mr


#
#mr=[]
#for rr in r:
#    mmr=MedidasRede(rr)
#    mr.append(mmr)
# fazer medidas de texto, para cada autor
if "mla" not in dir(__builtin__):
    try:
        f=open("/disco/mla","rb")
        mla= pickle.load(f)
        f.close()
        __builtin__.mla=mla
        print("aproveitado mla")
    except:
        print("fazendo mla")
        mla=[]
        i=0
        for rr in r:
            nodes=rr.g.nodes()
            mla_={}
            for node in nodes:
               foo=MedidasLMensagens(m[i],0,20001,autores=[node])
               mla_[node]=foo
            mla+=[mla_]
            i+=1
        f=open("/disco/mla", 'wb')
        pickle.dump(mla,f,-1)
        f.close()
        __builtin__.mla=mla
        print("feito mla")
else:
    mla=__builtin__.mla


# montar matriz atributo valor para os participantes
# para cada autor, colocar as medidas de rede e de texto
if "Mmr" not in dir(__builtin__):
    try:
        f=open("/disco/Mmr","rb")
        Mmr= pickle.load(f)
        f.close()
        __builtin__.Mmr=Mmr
        print("aproveitado Mmr")
    except:
        print("fazendo Mmr")
        i=0
        Mmr=[]
        for mrr in mr: # para cada lista
            matriz=[] # matriz atributo-valor
            MR_FIX=[mrr.diameter,mrr.ncc,mrr.nwc,mrr.nsc,mrr.radius,mrr.sl,mrr.transitivity,mrr.wi]
            for aut in mrr.g.nodes():
                MR=[mrr.d[aut],mrr.id_[aut],mrr.od[aut],
                   mrr.s[aut],mrr.is_[aut],mrr.os[aut],
                   mrr.bc[aut],mrr.c[aut],mrr.triangles[aut],mrr.cv[aut],
                   aut in mrr.center, aut in mrr.component,aut in mrr.periphery, aut in mrr.periphery_]
                MR_=[aut]+MR+MR_FIX
                matriz+=[MR_]
            Mmr+=[matriz]
        f=open("/disco/Mmr", 'wb')
        pickle.dump(Mmr,f,-1)
        f.close()
        __builtin__.Mmr=Mmr
        print("feito Mmr")
else:
    Mmr=__builtin__.Mmr
        
if "Mml" not in dir(__builtin__):
    try:
        f=open("/disco/Mml","rb")
        Mmr= pickle.load(f)
        f.close()
        __builtin__.Mml=Mml
        print("aproveitado Mml")
    except:
        print("fazendo Mml")
        tagsN=["NN","NNS","NNP","NNPS"]
        tagsA=["JJ","JJR","JJS","RB","RBR","RBS","RP"]
        tagsV=["VB","VBZ","VBP","VBN","VBD","VBG","MD"]
        tagsP=["IN","DT","PRP","PRP$","PDT","TO","CC","WRB","WDT","WP","WP$"]
        tagsC=["CD","EX","UH","FW",]
        tags_=[tagsN,tagsA,tagsV,tagsP,tagsC]
        tags__=tagsN+tagsA+tagsV+tagsP+tagsC
        
        ii=0
        Mml=[]
        for maa in mla: # para cada lista
            matriz=[] # matriz atributo-valor
            jj=0
            for aut in maa.keys():
                mll=maa[aut]
                #foobar
                ML_foobar=[mll.ncontractions]
                # medidas letras
                #ML_ml=[mll.nc,mll.ne,mll.nl,mll.nm,mll.nv,mll.np,mll.nd,]
                if mll.T.strip() and (len(set(mll.T))>1) and len(mll.T) > 20:
                    ML_ml=list(mll.letrasTudo)
                    # medidas tokens
                    ML_tk=[mll.nt,mll.ntd,mll.ntd/mll.nt,mll.nt/(mll.nc-mll.ne),mll.ntp/mll.nt,
                           len(mll.kw)/mll.nt, (len(mll.wss)/len(mll.kw)) if mll.kw else 0,(len(mll.wss_)/len(set(mll.kw))) if mll.kw else 0,(len(mll.wsw)/len(mll.kw)) if mll.kw else 0,(len(mll.ukwsw)/len(mll.ukw)) if mll.ukw else 0,(len(mll.wsssw)/len(mll.wss)) if mll.wss else 0, (len(mll.wnsssw)/len(mll.wnss)) if mll.wnss else 0,(len(mll.kwnssnsw)/len(mll.kw)) if mll.kw else 0,(len(mll.kwssnsw)/len(mll.kw)) if mll.kw else 0]
                    # medidas tamanhos
                    ML_tm=[mll.mtkw,mll.dtkw,mll.mtkw_,mll.dtkw_,n.mean(mll.tkwnsw),n.std(mll.tkwnsw),n.mean(mll.tkwnsw_),n.std(mll.tkwnsw_),
                           n.mean(mll.tams),n.std(mll.tams),n.mean(mll.tams_),n.std(mll.tams_),
                           n.mean(mll.tsw),n.std(mll.tsw),n.mean(mll.tsw_),n.std(mll.tsw_),
                           n.mean(mll.tsw2),n.std(mll.tsw2),n.mean(mll.tsw2_),n.std(mll.tsw2_)]
                    # medidas de tamanhos de sentencas
                    ML_tm2=[mll.mtTS, mll.dtTS, mll.mtsTS, mll.dtsTS,mll.mtsTSkw, mll.dtsTSkw,mll.mtsTSpv,mll.dtsTSpv]
                    # medidas dos tamanhos nas mensagens
                    ML_tm3=[mll.mtmT,mll.dtmT,mll.mttmT,mll.dttmT,mll.mtsmT,mll.dtsmT]
            
                    # medidas POS
                    ML_pos=[]
                    for tag in tags__:
                        if tag in mll.htags.keys():
                           ML_pos+=[mll.htags[tag]]
                        else:
                           ML_pos+=[0.]
            
                    # wordnet
                    tamH=[len(i) for i in mll.sshe]
                    ML_wn=[mll.mlwss,mll.dlwss,n.mean(tamH),n.std(tamH),n.mean(mll.profundidade),n.std(mll.profundidade)]
            
                    ML_=[aut]+ML_foobar+ML_ml+ML_tk+ML_tm+ML_tm2+ML_tm3+ML_pos+ML_wn
                    matriz+=[ML_]
                    jj+=1
                else:
                    matriz+=[[aut]+[0]*(7+14+20+8+6+33+6+1)]
            Mml+=[matriz]
            ii+=1
        f=open("/disco/Mml", 'wb')
        pickle.dump(Mml,f,-1)
        f.close()
        __builtin__.Mml=Mml
        print("feito Mml")
else:
    Mml=__builtin__.Mml




sys.exit()
# fazer parte linguistica seletivamente
if "ml" not in dir(__builtin__):
#    try:
#        # geral
#        print("textos do pickleDIR")
#        f=open("cpickleDIR/ml","rb")
#        ml= pickle.load(f)
#        f.close()
#        __builtin__.ml=ml
#        print("aproveitados textos do pickleDIR")
#        # perifericos
#        print("textos do pickleDIRp")
#        f=open("cpickleDIR/mlp","rb")
#        mlp= pickle.load(f)
#        f.close()
#        __builtin__.mlp=mlp
#        print("aproveitados textos do pickleDIRp")
#        # intermediarios
#        print("textos do pickleDIRi")
#        f=open("cpickleDIR/mli","rb")
#        mli= pickle.load(f)
#        f.close()
#        __builtin__.mli=mli
#        print("aproveitados textos do pickleDIRi")
#        # hubs
#        print("textos do pickleDIRh")
#        f=open("cpickleDIR/mlh","rb")
#        mlh= pickle.load(f)
#        f.close()
#        __builtin__.mlh=mlh
#        print("aproveitados textos do pickleDIRh")
#    except:
#        print("fazendo medidas de texto")
#        # geral

    try:
        f=open("cpickleDIR/ml","rb")
        ml= pickle.load(f)
        f.close()
        __builtin__.ml=ml
        print("aproveitado ml")
        print time.time()-atime; atime=time.time()
    except:
        ml_c=MedidasLMensagens(m[0],0,20001)
        print("processado cpp")
        ml_d=MedidasLMensagens(m[1],0,20001)
        print("processado lad")
        ml_u=MedidasLMensagens(m[2],0,20001)
        print("processado lau")
        ml_e=MedidasLMensagens(m[3],0,20001)
        print("processado ele")
        ml=[ml_c,ml_d,ml_u,ml_e]
        f=open("./cpickleDIR/ml", 'wb')
        pickle.dump(ml,f,-1)
        f.close()
        __builtin__.ml=ml

    # perifericos
    try:
        f=open("cpickleDIR/mlp","rb")
        mlp= pickle.load(f)
        f.close()
        __builtin__.mlp=mlp
        print("aproveitado mlp")
        print time.time()-atime; atime=time.time()
    except:
        ml_cp=MedidasLMensagens(m[0],0,20001,autores=pr2[0].perifericosf)
        print("processado cpp perifericos")
        ml_dp=MedidasLMensagens(m[1],0,20001,autores=pr2[1].perifericosf)
        print("processado lad")
        ml_up=MedidasLMensagens(m[2],0,20001,autores=pr2[2].perifericosf)
        print("processado lau")
        ml_ep=MedidasLMensagens(m[3],0,20001,autores=pr2[3].perifericosf)
        print("processado ele")
        mlp=[ml_cp,ml_dp,ml_up,ml_ep]
        f=open("./cpickleDIR/mlp", 'wb')
        pickle.dump(mlp,f,-1)
        f.close()
        __builtin__.mlp=mlp

    try:
        f=open("cpickleDIR/mli","rb")
        mli= pickle.load(f)
        f.close()
        __builtin__.mli=mli
        print("aproveitado mli")
        print time.time()-atime; atime=time.time()
    except:
        # intermediarios
        ml_ci=MedidasLMensagens(m[0],0,20001,autores=pr2[0].intermediariosf)
        print("processado cpp intermediarios")
        ml_di=MedidasLMensagens(m[1],0,20001,autores=pr2[1].intermediariosf)
        print("processado lad")
        ml_ui=MedidasLMensagens(m[2],0,20001,autores=pr2[2].intermediariosf)
        print("processado lau")
        ml_ei=MedidasLMensagens(m[3],0,20001,autores=pr2[3].intermediariosf)
        print("processado ele")
        mli=[ml_ci,ml_di,ml_ui,ml_ei]
        f=open("./cpickleDIR/mli", 'wb')
        pickle.dump(mli,f,-1)
        f.close()
        __builtin__.mli=mli

    try:
        f=open("cpickleDIR/mlh","rb")
        mlh= pickle.load(f)
        f.close()
        __builtin__.mlh=mlh
        print("aproveitado mlh")
        print time.time()-atime; atime=time.time()
    except:
        # hubs
        ml_ch=MedidasLMensagens(m[0],0,20001,autores=pr2[0].hubsf)
        print("processado cpp hubs")
        ml_dh=MedidasLMensagens(m[1],0,20001,autores=pr2[1].hubsf)
        print("processado lad")
        ml_uh=MedidasLMensagens(m[2],0,20001,autores=pr2[2].hubsf)
        print("processado lau")
        ml_eh=MedidasLMensagens(m[3],0,20001,autores=pr2[3].hubsf)
        print("processado ele")
        mlh=[ml_ch,ml_dh,ml_uh,ml_eh]
        f=open("./cpickleDIR/mlh", 'wb')
        pickle.dump(mlh,f,-1)
        f.close()
        __builtin__.mlh=mlh
else:
    print("aproveitando medidas de texto")
    ml=__builtin__.ml
    mlp=__builtin__.mlp
    mli=__builtin__.mli
    mlh=__builtin__.mlh

#
## teste de kolmogorov
#c1=n.cumsum(ml[0].htkw_[0])
#c2=n.cumsum(ml[1].htkw_[0])
#dc=n.abs(c1-c2)
#Dnn=max(dc)
#n1=len(ml[0].tkw_)
#n2=len(ml[1].tkw_)
#fact=((n1+n2)/(n1*n2))**0.5
#calpha=Dnn/fact
#

##############################
# incidencia das etiquetas morfossintáticas do corpus da Brown
#l=[]
#for k in ml[0].htags__.keys()[::-1]:
#    l.append(tuple([k]+[100*ll.htags__[k] for ll in ml]))
#
#for ll in l:
#    print "%s & %.4f & %.4f & %.4f & %.4f \\\\" % ll
d={}
for k in ml[0].htags__.keys()[::-1]:
    d[k]=[]
for i in xrange(4):
    for k in ml[0].htags__.keys()[::-1]:
        d[k]+=[ml[i].htags__[k],mlp[i].htags__[k],mli[i].htags__[k],mlh[i].htags__[k]]
        #l.append(tuple([k]+[100*ll.htags__[k] for ll in ml]))
tagsN=["NN","NNS","NNP","NNPS"]
tagsA=["JJ","JJR","JJS","RB","RBR","RBS","RP"]
tagsV=["VB","VBZ","VBP","VBN","VBD","VBG","MD"]
tagsP=["IN","DT","PRP","PRP$","PDT","TO","CC","WRB","WDT","WP","WP$"]
tagsC=["CD","EX","UH","FW",]
tags_=[tagsN,tagsA,tagsV,tagsP,tagsC]
ii=0
for tt in tags_:
    jj=0
    for tag in tt:
        sval= ("%s"+(" & %.2f"*4)*4+"\\\\")%tuple([tag]+[100*dd for dd in d[tag]])
        jj+=1
        if jj==len(tt):
            sval+="\\hline"
            print sval
            foo=[d[ttag] for ttag in tt]
            bar=[0]*16
            for stats in foo:
                for i in xrange(len(bar)):
                    bar[i]+=stats[i]

            sval= ("%s"+(" & %.2f"*4)*4+"\\\\\\hline\\hline")%tuple(["+"]+[100*dd for dd in bar])
            print sval
        else:
            print sval



#
#tags=ml[0].htags__.keys()[::-1]
#for k in tags:
#    sval= ("%s"+(" & %.2f"*4)*4+"\\\\")%tuple([k]+[100*dd for dd in d[k]])
#    if k in ("DT","VBG","RBR","LS"):
#        sval+="\\hline"
#    print sval
#
sys.exit()
mtmT=[]
dtmT=[]
mttmT=[]
dttmT=[]
mtsmT=[]
dtsmT=[]
for i in xrange(4):
    # media e desvio de chars/msg
    mtmT+=[ml[i].mtmT,mlp[i].mtmT,mli[i].mtmT,mlh[i].mtmT]
    dtmT+=[ml[i].dtmT,mlp[i].dtmT,mli[i].dtmT,mlh[i].dtmT]
    # media e descio em n de tokens / msg
    mttmT+=[ml[i].mttmT,mlp[i].mttmT,mli[i].mttmT,mlh[i].mttmT]
    dttmT+=[ml[i].dttmT,mlp[i].dttmT,mli[i].dttmT,mlh[i].dttmT]
    # media e descio em sents / msg
    mtsmT+=[ml[i].mtsmT,mlp[i].mtsmT,mli[i].mtsmT,mlh[i].mtsmT]
    dtsmT+=[ml[i].dtsmT,mlp[i].dtsmT,mli[i].dtsmT,mlh[i].dtsmT]

labels=(r"$\mu\left(\frac{|chars|}{msg}\right)$",r"$\sigma\left(\frac{|chars|}{msg}\right)$",r"$\mu\left(\frac{|tokens|}{msg}\right)$",r"$\sigma\left(\frac{|tokens|}{msg}\right)$",r"$\mu\left(\frac{|sents|}{msg}\right)$",r"$\sigma\left(\frac{|sents|}{msg}\right)$")

nnnM=(mtmT,dtmT,
      mttmT, dttmT,
      mtsmT, dtsmT)

i=0
for ll in labels:
    sval= ("%s"+" & %.2f & %.2f & %.2f & %.2f"*4+" \\\\") % tuple([ll]+nnnM[i])
    if i%2==1:
        sval+="\\hline"
    i+=1
    print sval



sys.exit()

#-->############################
# numero de sentencas:
nsents=[]
mtTS=[]
dtTS=[]
mtsTS=[]
dtsTS=[]
mtsTSkw=[]
dtsTSkw=[]
mtsTSpv=[]
dtsTSpv=[]
for i in xrange(4):
	nsents+=[len(ml[i].TS),len(mlp[i].TS),len(mli[i].TS),len(mlh[i].TS)]
	# media e desvio dos tamanhos das sentencas em chars:
	mtTS+=[ml[i].mtTS,mlp[i].mtTS,mli[i].mtTS,mlh[i].mtTS]
	dtTS+=[ml[i].dtTS,mlp[i].dtTS,mli[i].dtTS,mlh[i].dtTS]
	# media e desvio dos tamanhos das sentencas em tokens:
	mtsTS+=[ml[i].mtsTS,mlp[i].mtsTS,mli[i].mtsTS,mlh[i].mtsTS]
	dtsTS+=[ml[i].dtsTS,mlp[i].dtsTS,mli[i].dtsTS,mlh[i].dtsTS]
	# media e desvio do tamanho das sentencas em palavras conhecidas:
	mtsTSkw+=[ml[i].mtsTSkw,mlp[i].mtsTSkw,mli[i].mtsTSkw,mlh[i].mtsTSkw]
	dtsTSkw+=[ml[i].dtsTSkw,mlp[i].dtsTSkw,mli[i].dtsTSkw,mlh[i].dtsTSkw]
	# media e desvio do tamanho das sentencas em palavras conhecidas que retornam synsets e n sao stopwords:
	mtsTSpv+=[ml[i].mtsTSpv,mlp[i].mtsTSpv,mli[i].mtsTSpv,mlh[i].mtsTSpv]
	dtsTSpv+=[ml[i].dtsTSpv,mlp[i].dtsTSpv,mli[i].dtsTSpv,mlh[i].dtsTSpv]

labels=(r"$|sents|$",r"$\mu\left(\frac{chars}{sent}\right)$",r"$\sigma\left(\frac{chars}{sent}\right)$",r"$\mu\left(\frac{tokens}{sent}\right)$",r"$\sigma\left(\frac{tokens}{sent}\right)$",r"$\mu\left(\frac{kw}{sent}\right)$",r"$\sigma\left(\frac{kw}{sent}\right)$",r"$\mu\left(\frac{kwssnsw}{sent}\right)$",r"$\sigma\left(\frac{kwssnsw}{sent}\right)$")
nnnS2=(nsents,mtTS,dtTS,mtsTS,dtsTS,mtsTSkw,dtsTSkw,mtsTSpv,dtsTSpv)
i=0
for ll in labels:
    if i==0:
        sval= ("%s"+" & %i & %i & %i & %i"*4+" \\\\") % tuple([ll]+nnnS2[i]);
    else:
        sval= ("%s"+" & %.2f & %.2f & %.2f & %.2f"*4+" \\\\") % tuple([ll]+nnnS2[i])
    if i%2==0:
        sval+=" \\hline"
    print sval
    i+=1






sys.exit()
labels=(r"$\mu(size\,of\,known\,word=skw)$",r"$\sigma(skw)$",r"$\mu(\neq skw)$",r"$\sigma(\neq skw)$",
        r"$\mu(skwss)$",r"$\sigma(skwss)$",r"$\mu(\neq skwss)$",r"$\sigma(\neq skwss)$",
        r"$\mu(ssw)$",r"$\sigma(ssw)$",r"$\mu(\neq ssw_)$",r"$\sigma(\neq ssw_)$",
        r"$\mu(snsssw)$",r"$\sigma(snsssw)$",r"$\mu(\neq snsssw\)$",r"$\sigma(\neq snsssw)$")
#nnnS=(mtkwO,dtkwO,mtkw_O,dtkw_O,
#      mtpvO,dtpvO,mtpv_O,dtpv_O,
#      mtswO,dtswO,mtsw_O,dtsw_O,
#      mtsw2O,dtsw2O,mtsw2_O,dtsw2_O)

mskw=[]
dskw=[]
mskw_=[]
dskw_=[]

mskwss=[]
dskwss=[]
mskwss_=[]
dskwss_=[]

mssw=[]
dssw=[]
mssw_=[]
dssw_=[]



msssw=[]
dsssw=[]
msssw_=[]
dsssw_=[]

for i in xrange(4):
    mskw+=[n.mean(ml[i].tkw),n.mean(mlp[i].tkw),n.mean(mli[i].tkw),n.mean(mlh[i].tkw)]
    dskw+=[n.std(ml[i].tkw),n.std(mlp[i].tkw),n.std(mli[i].tkw),n.std(mlh[i].tkw)]
    mskw_+=[n.mean(ml[i].tkw_),n.mean(mlp[i].tkw_),n.mean(mli[i].tkw_),n.mean(mlh[i].tkw_)]
    dskw_+=[n.std(ml[i].tkw_),n.std(mlp[i].tkw_),n.std(mli[i].tkw_),n.std(mlh[i].tkw_)]

    mskwss+=[n.mean([len(jj) for jj in ml[i].wss]),n.mean([len(jj) for jj in mlp[i].wss]),n.mean([len(jj) for jj in mli[i].wss]),n.mean([len(jj) for jj in mli[i].wss])]     
    dskwss+=[n.std([len(jj) for jj in ml[i].wss]),n.std([len(jj) for jj in mlp[i].wss]),n.std([len(jj) for jj in mli[i].wss]),n.std([len(jj) for jj in mli[i].wss])]     
    mskwss_+=[n.mean([len(jj) for jj in set(ml[i].wss)]),n.mean([len(jj) for jj in set(mlp[i].wss)]),n.mean([len(jj) for jj in set(mli[i].wss)]),n.mean([len(jj) for jj in set(mli[i].wss)])]     
    dskwss_+=[n.std([len(jj) for jj in set(ml[i].wss)]),n.std([len(jj) for jj in set(mlp[i].wss)]),n.std([len(jj) for jj in set(mli[i].wss)]),n.std([len(jj) for jj in set(mli[i].wss)])]     
    

    mssw+=[n.mean(ml[i].tsw),n.mean(mlp[i].tsw),n.mean(mli[i].tsw),n.mean(mlh[i].tsw)]
    dssw+=[n.std(ml[i].tsw),n.std(mlp[i].tsw),n.std(mli[i].tsw),n.std(mlh[i].tsw)]
    mssw_+=[n.mean(ml[i].tsw_),n.mean(mlp[i].tsw_),n.mean(mli[i].tsw_),n.mean(mlh[i].tsw_)]
    dssw_+=[n.std(ml[i].tsw_),n.std(mlp[i].tsw_),n.std(mli[i].tsw_),n.std(mlh[i].tsw_)]

    msssw+=[ml[i].mtsw2,mlp[i].mtsw2,mli[i].mtsw2,mlh[i].mtsw2]
    dsssw+=[ml[i].dtsw2,mlp[i].dtsw2,mli[i].dtsw2,mlh[i].dtsw2]
    msssw_+=[ml[i].mtsw2_,mlp[i].mtsw2_,mli[i].mtsw2_,mlh[i].mtsw2_]
    dsssw_+=[ml[i].dtsw2_,mlp[i].dtsw2_,mli[i].dtsw2_,mlh[i].dtsw2_]


vals=(mskw,dskw,mskw_,dskw_,
     mskwss,dskwss, mskwss_, dskwss_,
     mssw, dssw, mssw_, dssw_,
     msssw, dsssw, msssw_, dsssw_)


i=0
for l in labels:
    tval=(("%s "+("& %.2f "*4)*4) %((l,)+tuple(vals[i])))+"\\\\"
    if i%4==3: tval+=" \\hline"
    print tval
    i+=1



sys.exit()

############################
# Medidas de texto por autor
if "mtps" not in dir(__builtin__):
    try:
        f=open("cpickleDIR/mtps","rb")
        mtps= pickle.load(f)
        f.close()
        __builtin__.mtps=mtps
    except:
	mtps=[]
	foobar=0
        for pr in pr2:
            autores=pr.perifericosf
            mtp=[]
            for per in autores:
                mtp.append(MedidasLMensagens(m[foobar],0,20001,autores=[per]))
            foobar+=1
            mtps.append(mtp)
        __builtin__.mtps=mtps
        f=open("./cpickleDIR/mtps", 'wb')
        pickle.dump(mtps,f,-1)
        f.close()

if "mtis" not in dir(__builtin__):
    try:
        f=open("cpickleDIR/mtis","rb")
        mtis= pickle.load(f)
        f.close()
        __builtin__.mtis=mtis
    except:
        mtis=[]
	foobar=0
        for pr in pr2:
            autores=pr.intermediariosf
            mti=[]
            for inter in autores:
                mti.append(MedidasLMensagens(m[foobar],0,20001,autores=[inter]))
            foobar+=1
            mtis.append(mti)
        __builtin__.mtis=mtis
        f=open("./cpickleDIR/mtis", 'wb')
        pickle.dump(mtis,f,-1)
        f.close()


if "mths" not in dir(__builtin__):
    try:
        f=open("cpickleDIR/mths","rb")
        mths= pickle.load(f)
        f.close()
        __builtin__.mths=mths
    except:
        mths=[]
	foobar=0
        for pr in pr2:
            autores=pr.hubsf
            mth=[]
            for hub in autores:
                mth.append(MedidasLMensagens(m[foobar],0,20001,autores=[hub]))
            foobar+=1
            mths.append(mth)
        __builtin__.mths=mths
        f=open("./cpickleDIR/mths", 'wb')
        pickle.dump(mths,f,-1)
        f.close()


frac_ptp=[]
nper=0
for mpt in mtps:
    for mt in mpt:
        if mt.T.strip():
            frac_ptp.append(mt.np/(mt.nc -mt.ne))
            nper+=1

frac_pth=[]
nhub=0
for mht in mths:
    for mt in mht:
        if mt.T:
            frac_pth.append(mt.np/(mt.nc -mt.ne))
            nhub+=1

#bins=n.arange(100.)/100
#p.hist(frac_pth, bins=bins,normed=True,alpha=0.5,label="hubs")
#p.xlabel(r"size $\rightarrow$")
#p.ylabel(r"fraction of samples $\rightarrow$")
#
##-->    p.hist(ll.tkw, bins,normed=True,alpha=0.5,label="incident")
#p.hist(frac_ptp, bins=bins,normed=True,alpha=0.5,label="perifericos")
#p.legend(loc="upper right")
##p.legend(loc="upper right")
##p.xlabel(r"size $\rightarrow$")
##p.ylabel(r"fraction of samples $\rightarrow$")
#p.show()

mlm1=[]
pacote=1
if "mlm1" in dir(__builtin__):
    mlm1=__builtin__.mlm1
else:
    count=0
    for mm in m:
        mX=m[count]
        prX=pr2[count]; count+=1
        mp=MensagensPacotes(mX,autores=prX.perifericosf)
        mi=MensagensPacotes(mX,autores=prX.intermediariosf)
        mh=MensagensPacotes(mX,autores=prX.hubsf)
        mlmp=[]
        for i in xrange(0,len(mp.mm)-pacote,pacote):
            mlmp.append(MedidasLMensagens(mp,i,i+pacote))
        mlmi=[]
        for i in xrange(0,len(mi.mm)-pacote,pacote):
            mlmi.append(MedidasLMensagens(mi,i,i+pacote))
        mlmh=[]
        for i in xrange(0,len(mh.mm)-pacote,pacote):
            mlmh.append(MedidasLMensagens(mh,i,i+pacote))
        mlm1.append((mlmp,mlmi,mlmh))
    __builtin__.mlm1=mlm1

for mlm_ in mlm1:
    # substantivos
    npp=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm_[0] if "htags_" in dir(ll)] # punctuation
    npi=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm_[1] if "htags_" in dir(ll)] # punctuation
    nph=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm_[2] if "htags_" in dir(ll)] # punctuation
    # adjectives
    #npp=[100*(ll.htags_["JJ"]+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm_[0]] # punctuation
    #npi=[100*(ll.htags_["JJ"]+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm_[1]] # punctuation
    #nph=[100*(ll.htags_["JJ"]+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm_[2]] # punctuation
    ## stopword por known word
    #npp=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlm_[0]] # punctuation
    #npi=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlm_[1]] # punctuation
    #nph=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlm_[2]] # punctuation
    # punct por token
    #npp=[100*(ll.ntp/(ll.nt)) for ll in mlm_[0]] # punctuation
    #npi=[100*(ll.ntp/(ll.nt)) for ll in mlm_[1]] # punctuation
    #nph=[100*(ll.ntp/(ll.nt)) for ll in mlm_[2]] # punctuation
    # punct por char
    #npp=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[0]] # punctuation
    #npi=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[1]] # punctuation
    #nph=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[2]] # punctuation
    espacamento=0.05
    bins=n.arange(0,100,espacamento)
    #bins=n.arange(0,100,1)
    hp=n.histogram(npp,bins=bins,density=True)
    hi=n.histogram(npi,bins=bins,density=True)
    hh=n.histogram(nph,bins=bins,density=True)
    
    chp=n.cumsum(hp[0]*espacamento)
    chi=n.cumsum(hi[0]*espacamento)
    chh=n.cumsum(hh[0]*espacamento)
    
    dc=n.abs(chh-chp)
    Dnn=max(dc)
    n1=len(npp)
    n2=len(nph)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_HP=Dnn/fact
    
    dc=n.abs(chh-chi)
    Dnn=max(dc)
    n1=len(npi)
    n2=len(nph)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_HI=Dnn/fact
    
    dc=n.abs(chp-chi)
    Dnn=max(dc)
    n1=len(npi)
    n2=len(npp)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha_PI=Dnn/fact
    print calpha_HP, calpha_HI, calpha_PI

    #p.hist(npp, bins=bins,normed=True,alpha=0.5,label=u"periféricos")
    #p.hist(nph, bins=bins,normed=True,alpha=0.5,label="hubs")
    #p.legend(loc="upper right")
    #p.show()

for ii in xrange(3):
    # substantivos
    np1=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm1[0][ii] if "htags_" in dir(ll)] # punctuation
    np2=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm1[1][ii] if "htags_" in dir(ll)] # punctuation
    np3=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm1[2][ii] if "htags_" in dir(ll)] # punctuation
    np4=[100*(ll.htags_.get("NN",0)+ll.htags_.get("NNS",0)+ll.htags_.get("NNP",0)) for ll in mlm1[3][ii] if "htags_" in dir(ll)] # punctuation
    # adjetivos
    np1=[100*(ll.htags_.get("JJ",0)+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm1[0][ii] if "htags_" in dir(ll)] # punctuation
    np2=[100*(ll.htags_.get("JJ",0)+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm1[1][ii] if "htags_" in dir(ll)] # punctuation
    np3=[100*(ll.htags_.get("JJ",0)+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm1[2][ii] if "htags_" in dir(ll)] # punctuation
    np4=[100*(ll.htags_.get("JJ",0)+ll.htags_.get("JJR",0)+ll.htags_.get("JJS",0)) for ll in mlm1[3][ii] if "htags_" in dir(ll)] # punctuation
    # punct por token
    #npp=[100*(ll.ntp/(ll.nt)) for ll in mlm_[0]] # punctuation
    #npi=[100*(ll.ntp/(ll.nt)) for ll in mlm_[1]] # punctuation
    #nph=[100*(ll.ntp/(ll.nt)) for ll in mlm_[2]] # punctuation
    # punct por char
    #npp=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[0]] # punctuation
    #npi=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[1]] # punctuation
    #nph=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlm_[2]] # punctuation
    espacamento=0.05
    bins=n.arange(0,100,espacamento)
    #bins=n.arange(0,100,1)
    h1=n.histogram(np1,bins=bins,density=True)
    h2=n.histogram(np2,bins=bins,density=True)
    h3=n.histogram(np3,bins=bins,density=True)
    h4=n.histogram(np4,bins=bins,density=True)
    
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
 
    print calpha_12,calpha_13,calpha_14,calpha_23,calpha_24,calpha_34


#for ll in labels:
#    mstring=("%s"+" & %.2f & %.2f & %.2f & %.2f"*4 + " \\\\") % tuple([ll]+nnnS[i])
#    if i in (3,7,11,15):
#        mstring+=" \\hline"
#    i+=1
#

#sys.exit()
#######################################
# fazendo por conjunto de mensagens
# de 10 em 10
# o lance aqui parece ser: fazer um novo
# m para fazer um novo MedidasLMensagens

# de entrada, dá-se o conjunto de autores e o conjunto original de mensagens
# aí se realiza o MedidasLMensagens com o numero de mensagens
# que for mais cabível





#############################################
### Por mensagem
#
#if "mmtps" not in dir(__builtin__):
#    try:
#        f=open("cpickleDIR/mmtps","rb")
#        mmtps= pickle.load(f)
#        f.close()
#        __builtin__.mmtps=mmtps
#    except:
#	mmtps=[]
#        foobar=0
#        for pr in pr2:
#            autores=pr.perifericosf
#            mtp=[]
#            for per in autores:
#                mm=m[foobar]
#                id_msgs=[i[0] for i in mm.aa[per]]
#                in_ids=[mm.ids.index(i) for i in id_msgs]
#                for ind in in_ids:
#                    mtp.append(MedidasLMensagens(m[foobar],ind,ind+1,autores=[per]))
#            foobar+=1
#            mmtps.append(mtp)
#        __builtin__.mmtps=mmtps
#        f=open("./cpickleDIR/mmtps", 'wb')
#        pickle.dump(mmtps,f,-1)
#        f.close()
#
#if "mmtis" not in dir(__builtin__):
#    try:
#        f=open("cpickleDIR/mmtis","rb")
#        mmtis= pickle.load(f)
#        f.close()
#        __builtin__.mmtis=mmtis
#    except:
#        mmtis=[]
#        foobar=0
#        for pr in pr2:
#            autores=pr.intermediariosf
#            mti=[]
#            for inter in autores:
#                mm=m[foobar]
#                id_msgs=[i[0] for i in mm.aa[inter]]
#                in_ids=[mm.ids.index(i) for i in id_msgs]
#                for ind in in_ids:
#                    mtp.append(MedidasLMensagens(m[foobar],ind,ind+1,autores=[inter]))
#            foobar+=1
#            mmtis.append(mti)
#        __builtin__.mmtis=mmtis
#        f=open("./cpickleDIR/mmtis", 'wb')
#        pickle.dump(mmtis,f,-1)
#        f.close()
#
#
#if "mmths" not in dir(__builtin__):
#    try:
#        f=open("cpickleDIR/mmths","rb")
#        mmths= pickle.load(f)
#        f.close()
#        __builtin__.mmths=mmths
#    except:
#        mmths=[]
#        foobar=0
#        for pr in pr2:
#            autores=pr.hubsf
#            mth=[]
#            for hub in autores:
#                mm=m[foobar]
#                id_msgs=[i[0] for i in mm.aa[hub]]
#                in_ids=[mm.ids.index(i) for i in id_msgs]
#                for ind in in_ids:
#                    mtp.append(MedidasLMensagens(m[foobar],ind,ind+1,autores=[hub]))
#
#                mth.append(MedidasLMensagens(m[foobar],0,20001,autores=[hub]))
#            foobar+=1
#            mmths.append(mth)
#        __builtin__.mmths=mmths
#        f=open("./cpickleDIR/mmths", 'wb')
#        pickle.dump(mmths,f,-1)
#        f.close()
#
#
#frac_ptp=[]
#nper=0
#for mpt in mtps:
#    for mt in mpt:
#        if mt.T.strip():
#            frac_ptp.append(mt.np/(mt.nc -mt.ne))
#            nper+=1
#
#frac_pth=[]
#nhub=0
#for mht in mths:
#    for mt in mht:
#        if mt.T:
#            frac_pth.append(mt.np/(mt.nc -mt.ne))
#            nhub+=1
#
#bins=n.arange(50.)/50
#p.hist(frac_pth, bins=bins,normed=True,alpha=0.5,label="hubs")
##p.xlabel(r"size $\rightarrow$")
##p.ylabel(r"fraction of samples $\rightarrow$")
#
##-->    p.hist(ll.tkw, bins,normed=True,alpha=0.5,label="incident")
#p.hist(frac_ptp, bins=bins,normed=True,alpha=0.5,label="perifericos")
#p.legend(loc="upper right")
##p.legend(loc="upper right")
##p.xlabel(r"size $\rightarrow$")
##p.ylabel(r"fraction of samples $\rightarrow$")
#p.show()
#
#
#








## medidasLetras()
#nc=[ll.nc for ll in                     mlCHARS] # caracteres
#ne=[100*(ll.ne/ll.nc) for ll in         mlCHARS] # espacos
#np=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlCHARS] # punctuation
#nd=[100*(ll.nd/(ll.nc-ll.ne)) for ll in mlCHARS] # digits
#nl=[100*(ll.nl/(ll.nc-ll.ne)) for ll in mlCHARS] # letras 
#nv=[100*(ll.nv/(ll.nl)) for ll in       mlCHARS] # vogais
#nu=[100*(ll.nm/ll.nl) for ll in         mlCHARS] # uppercase
#
## p
#ncp=[ll.nc for ll in                     mlCHARSp] # caracteres
#nep=[100*(ll.ne/ll.nc) for ll in         mlCHARSp] # espacos
#npp=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlCHARSp] # punctuation
#ndp=[100*(ll.nd/(ll.nc-ll.ne)) for ll in mlCHARSp] # digits
#nlp=[100*(ll.nl/(ll.nc-ll.ne)) for ll in mlCHARSp] # letras 
#nvp=[100*(ll.nv/(ll.nl)) for ll in       mlCHARSp] # vogais
#nup=[100*(ll.nm/ll.nl) for ll in         mlCHARSp] # uppercase
#
## i
#nci=[ll.nc for ll in                     mlCHARSi] # caracteres
#nei=[100*(ll.ne/ll.nc) for ll in         mlCHARSi] # espacos
#npi=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlCHARSi] # punctuation
#ndi=[100*(ll.nd/(ll.nc-ll.ne)) for ll in mlCHARSi] # digits
#nli=[100*(ll.nl/(ll.nc-ll.ne)) for ll in mlCHARSi] # letras 
#nvi=[100*(ll.nv/(ll.nl)) for ll in       mlCHARSi] # vogais
#nui=[100*(ll.nm/ll.nl) for ll in         mlCHARSi] # uppercase
#
## h
#nch=[ll.nc for ll in                     mlCHARSh] # caracteres
#neh=[100*(ll.ne/ll.nc) for ll in         mlCHARSh] # espacos
#nph=[100*(ll.np/(ll.nc-ll.ne)) for ll in mlCHARSh] # punctuation
#ndh=[100*(ll.nd/(ll.nc-ll.ne)) for ll in mlCHARSh] # digits
#nlh=[100*(ll.nl/(ll.nc-ll.ne)) for ll in mlCHARSh] # letras 
#nvh=[100*(ll.nv/(ll.nl)) for ll in       mlCHARSh] # vogais
#nuh=[100*(ll.nm/ll.nl) for ll in         mlCHARSh] # uppercase
#
#
#
#
#labels=(r"$n\,chars$",r"$\left(\frac{n\,spaces}{n\,chars}\right)\times 100$",r"$\left(\frac{n\,punct}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,digits}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,letters}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,vogals}{n\,letters}\right)\times 100$",r"$\left(\frac{n\,Uppercase}{n\,letters}\right)\times 100$")
#nc_=[]
#for i in xrange(4):
#    nc_+=[nc[i],ncp[i],nci[i],nch[i]]
#nc__=[]
#for i in xrange(4):
#    nc__+=[nc[i],100*ncp[i]/nc[i],100*nci[i]/nc[i],100*nch[i]/nc[i]]
#
#np_=[]
#for i in xrange(4):
#    np_+=[np[i],npp[i],npi[i],nph[i]]
#ne_=[]
#for i in xrange(4):
#    ne_+=[ne[i],nep[i],nei[i],neh[i]]
#nd_=[]
#for i in xrange(4):
#    nd_+=[nd[i],ndp[i],ndi[i],ndh[i]]
#nl_=[]
#for i in xrange(4):
#    nl_+=[nl[i],nlp[i],nli[i],nlh[i]]
#
#
#
#nnn=(nc__,
#     ne_,
#     np_,
#     nd_,
#     nl_,
#     nv+nvp+nvi+nvh,
#     nu+nup+nui+nuh)
#i=0
#for ll in labels:
#    mstring= "%s " % (ll,)
#    if i == 0:
#        #print ("%s"+" & %i & %i & %i & %i"*4 +" \\\\") % tuple([ll]+nnn[i]); i+=1
#        mstring += (" & %i & %.2f & %.2f & %.2f"*4 +" \\\\") % tuple(nnn[i]); i+=1
#    else:
#        mstring+= (" & %.2f & %.2f & %.2f & %.2f"*4 +" \\\\") % tuple(nnn[i]); i+=1
#    mstring+="\\hline"
#    print(mstring)
#

#### tokens
#if "mlTOKS" not in dir(__builtin__):
#    try:
#        # geral
#        f=open("cpickleDIR/mlTOKS","rb")
#        mlTOKS= pickle.load(f)
#        f.close()
#        __builtin__.mlTOKS=mlTOKS
#        print("aproveitados textos do pickleDIR")
#        # perifericos
#        f=open("cpickleDIR/mlTOKSp","rb")
#        mlTOKSp= pickle.load(f)
#        f.close()
#        __builtin__.mlTOKSp=mlTOKSp
#        print("aproveitados textos do pickleDIRp")
#        # intermediarios
#        f=open("cpickleDIR/mlTOKSi","rb")
#        mlTOKSi= pickle.load(f)
#        f.close()
#        __builtin__.mlTOKSi=mlTOKSi
#        print("aproveitados textos do pickleDIRi")
#        # hubs
#        f=open("cpickleDIR/mlTOKSh","rb")
#        mlTOKSh= pickle.load(f)
#        f.close()
#        __builtin__.mlTOKSh=mlTOKSh
#        print("aproveitados textos do pickleDIRh")
#    except:
#        print("fazendo medidas de texto")
#        # geral
#        ml_cTOKS=MedidasLMensagens(m[0],0,20001)
#        print("processado cpp")
#        ml_dTOKS=MedidasLMensagens(m[1],0,20001)
#        print("processado lad")
#        ml_uTOKS=MedidasLMensagens(m[2],0,20001)
#        print("processado lau")
#        ml_eTOKS=MedidasLMensagens(m[3],0,20001)
#        print("processado ele")
#        mlTOKS=[ml_cTOKS,ml_dTOKS,ml_uTOKS,ml_eTOKS]
#        f=open("./cpickleDIR/mlTOKS", 'wb')
#        pickle.dump(mlTOKS,f,-1)
#        f.close()
#        __builtin__.mlTOKS=mlTOKS
#
#        # perifericos
#        ml_cTOKSp=MedidasLMensagens(m[0],0,20001,autores=pr2[0].perifericosf)
#        print("processado cpp perifericos")
#        ml_dTOKSp=MedidasLMensagens(m[1],0,20001,autores=pr2[1].perifericosf)
#        print("processado lad")
#        ml_uTOKSp=MedidasLMensagens(m[2],0,20001,autores=pr2[2].perifericosf)
#        print("processado lau")
#        ml_eTOKSp=MedidasLMensagens(m[3],0,20001,autores=pr2[3].perifericosf)
#        print("processado ele")
#        mlTOKSp=[ml_cTOKSp,ml_dTOKSp,ml_uTOKSp,ml_eTOKSp]
#        f=open("./cpickleDIR/mlTOKSp", 'wb')
#        pickle.dump(mlTOKSp,f,-1)
#        f.close()
#        __builtin__.mlTOKSp=mlTOKSp
#
#        # intermediarios
#        ml_cTOKSi=MedidasLMensagens(m[0],0,20001,autores=pr2[0].intermediariosf)
#        print("processado cpp intermediarios")
#        ml_dTOKSi=MedidasLMensagens(m[1],0,20001,autores=pr2[1].intermediariosf)
#        print("processado lad")
#        ml_uTOKSi=MedidasLMensagens(m[2],0,20001,autores=pr2[2].intermediariosf)
#        print("processado lau")
#        ml_eTOKSi=MedidasLMensagens(m[3],0,20001,autores=pr2[3].intermediariosf)
#        print("processado ele")
#        mlTOKSi=[ml_cTOKSi,ml_dTOKSi,ml_uTOKSi,ml_eTOKSi]
#        f=open("./cpickleDIR/mlTOKSi", 'wb')
#        pickle.dump(mlTOKSi,f,-1)
#        f.close()
#        __builtin__.mlTOKSi=mlTOKSi
#
#        # hubs
#        ml_cTOKSh=MedidasLMensagens(m[0],0,20001,autores=pr2[0].hubsf)
#        print("processado cpp hubs")
#        ml_dTOKSh=MedidasLMensagens(m[1],0,20001,autores=pr2[1].hubsf)
#        print("processado lad")
#        ml_uTOKSh=MedidasLMensagens(m[2],0,20001,autores=pr2[2].hubsf)
#        print("processado lau")
#        ml_eTOKSh=MedidasLMensagens(m[3],0,20001,autores=pr2[3].hubsf)
#        print("processado ele")
#        mlTOKSh=[ml_cTOKSh,ml_dTOKSh,ml_uTOKSh,ml_eTOKSh]
#        f=open("./cpickleDIR/mlTOKSh", 'wb')
#        pickle.dump(mlTOKSh,f,-1)
#        f.close()
#        __builtin__.mlTOKSh=mlTOKSh
#else:
#    print("aproveitando medidas de texto")
#    mlTOKS=__builtin__.mlTOKS
#    mlTOKSp=__builtin__.mlTOKSp
#    mlTOKSi=__builtin__.mlTOKSi
#    mlTOKSh=__builtin__.mlTOKSh

##############################
## medidasTokens()
#nt=[ll.nt for ll in mlTOKS] # ntokens
#ncpt=[len(ll.T.replace(" ",""))/ll.nt for ll in mlTOKS]
#ntd=[100*(ll.ntd/ll.nt) for ll in mlTOKS] # ntokens differentes
#ntp=[100*(ll.ntp/ll.nt) for ll in mlTOKS] # npontuacoes
##ntp=[100*(ll.ntp/ll.nt) for ll in mlTOKS] # npontuacoes
#nkw=  [100*(len(ll.kw)/(ll.nt-ll.ntp)) for ll in mlTOKS] # known words
#nkwd=  [100*(len(set(ll.kw))/len(ll.kw)) for ll in mlTOKS] # known words
#nkwss=[100*(len(ll.wss)/len(ll.kw)) for ll in mlTOKS] # known words that return synsets
#nkwsw=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlTOKS] # known words that are stopwords
#
##nukwsw=[100*(len(ll.ukwsw)/(ll.nt-ll.ntp)) for ll in mlTOKS] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#nukwsw=[100*(len(ll.ukwsw)/len(ll.kw)) for ll in mlTOKS] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#
#nwsssw=[100*(len(ll.wsssw)/len(ll.kw)) for ll in mlTOKS] # words that return synsets and are stopwords
#
#nwnsssw=[100*(len(ll.wnsssw)/len(ll.kw)) for ll in mlTOKS] # words that dont return synsets and are stopwords informality ############A
#
#ncontrac=[100*(ll.ncontractions/len(ll.kw)) for ll in mlTOKS]  # contractions per token informality ###########################
#nkwnssnsw=[100*(len(ll.kwnssnsw)/len(ll.kw)) for ll in mlTOKS] # words that are known, are not stopwords and do not return synset
#nkwssnsw=[100*(len(ll.kwssnsw)/len(ll.kw)) for ll in mlTOKS] # known words that are not stopwords and return synsets
#
#############################
## p
## medidasTokens()
#nt_p=[ll.nt for ll in mlTOKSp] # ntokens
#ncpt_p=[len(ll.T.replace(" ",""))/ll.nt for ll in mlTOKSp]
#ntd_p=[100*(ll.ntd/ll.nt) for ll in mlTOKSp] # ntokens differentes
#ntp_p=[100*(ll.ntp/ll.nt) for ll in mlTOKSp] # npontuacoes
##ntp_p=[100*(ll.ntp/ll.nt) for ll in mlTOKSp] # npontuacoes
#nkw_p=  [100*(len(ll.kw)/(ll.nt-ll.ntp)) for ll in mlTOKSp] # known words
#nkwd_p=  [100*(len(set(ll.kw))/len(ll.kw)) for ll in mlTOKSp] # known words
#nkwss_p=[100*(len(ll.wss)/len(ll.kw)) for ll in mlTOKSp] # known words that return synsets
#nkwsw_p=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlTOKSp] # known words that are stopwords
#
##nukwsw_p=[100*(len(ll.ukwsw)/(ll.nt-ll.ntp)) for ll in mlTOKSp] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#nukwsw_p=[100*(len(ll.ukwsw)/len(ll.kw)) for ll in mlTOKSp] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#
#nwsssw_p=[100*(len(ll.wsssw)/len(ll.kw)) for ll in mlTOKSp] # words that return synsets and are stopwords
#
#nwnsssw_p=[100*(len(ll.wnsssw)/len(ll.kw)) for ll in mlTOKSp] # words that dont return synsets and are stopwords informality ############A
#
#ncontrac_p=[100*(ll.ncontractions/len(ll.kw)) for ll in mlTOKSp]  # contractions per token informality ###########################
#nkwnssnsw_p=[100*(len(ll.kwnssnsw)/len(ll.kw)) for ll in mlTOKSp] # words that are known, are not stopwords and do not return synset
#nkwssnsw_p=[100*(len(ll.kwssnsw)/len(ll.kw)) for ll in mlTOKSp] # known words that are not stopwords and return synsets
#
#############################
## i
## medidasTokens()
#nt_i=[ll.nt for ll in mlTOKSi] # ntokens
#ncpt_i=[len(ll.T.replace(" ",""))/ll.nt for ll in mlTOKSi]
#ntd_i=[100*(ll.ntd/ll.nt) for ll in mlTOKSi] # ntokens differentes
#ntp_i=[100*(ll.ntp/ll.nt) for ll in mlTOKSi] # npontuacoes
##ntp_i=[100*(ll.ntp/ll.nt) for ll in mlTOKSi] # npontuacoes
#nkw_i=  [100*(len(ll.kw)/(ll.nt-ll.ntp)) for ll in mlTOKSi] # known words
#nkwd_i=  [100*(len(set(ll.kw))/len(ll.kw)) for ll in mlTOKSi] # known words
#nkwss_i=[100*(len(ll.wss)/len(ll.kw)) for ll in mlTOKSi] # known words that return synsets
#nkwsw_i=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlTOKSi] # known words that are stopwords
#
##nukwsw_i=[100*(len(ll.ukwsw)/(ll.nt-ll.ntp)) for ll in mlTOKSi] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#nukwsw_i=[100*(len(ll.ukwsw)/len(ll.kw)) for ll in mlTOKSi] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#
#nwsssw_i=[100*(len(ll.wsssw)/len(ll.kw)) for ll in mlTOKSi] # words that return synsets and are stopwords
#
#nwnsssw_i=[100*(len(ll.wnsssw)/len(ll.kw)) for ll in mlTOKSi] # words that dont return synsets and are stopwords informality ############A
#
#ncontrac_i=[100*(ll.ncontractions/len(ll.kw)) for ll in mlTOKSi]  # contractions per token informality ###########################
#nkwnssnsw_i=[100*(len(ll.kwnssnsw)/len(ll.kw)) for ll in mlTOKSi] # words that are known, are not stopwords and do not return synset
#nkwssnsw_i=[100*(len(ll.kwssnsw)/len(ll.kw)) for ll in mlTOKSi] # known words that are not stopwords and return synsets
#
#############################
## h
## medidasTokens()
#nt_h=[ll.nt for ll in mlTOKSh] # ntokens
#ncpt_h=[len(ll.T.replace(" ",""))/ll.nt for ll in mlTOKSh]
#ntd_h=[100*(ll.ntd/ll.nt) for ll in mlTOKSh] # ntokens differentes
#ntp_h=[100*(ll.ntp/ll.nt) for ll in mlTOKSh] # npontuacoes
##ntp_h=[100*(ll.ntp/ll.nt) for ll in mlTOKSh] # npontuacoes
#nkw_h=  [100*(len(ll.kw)/(ll.nt-ll.ntp)) for ll in mlTOKSh] # known words
#nkwd_h=  [100*(len(set(ll.kw))/len(ll.kw)) for ll in mlTOKSh] # known words
#nkwss_h=[100*(len(ll.wss)/len(ll.kw)) for ll in mlTOKSh] # known words that return synsets
#nkwsw_h=[100*(len(ll.wsw)/len(ll.kw)) for ll in mlTOKSh] # known words that are stopwords
#
##nukwsw_h=[100*(len(ll.ukwsw)/(ll.nt-ll.ntp)) for ll in mlTOKSh] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#nukwsw_h=[100*(len(ll.ukwsw)/len(ll.kw)) for ll in mlTOKSh] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#
#nwsssw_h=[100*(len(ll.wsssw)/len(ll.kw)) for ll in mlTOKSh] # words that return synsets and are stopwords
#
#nwnsssw_h=[100*(len(ll.wnsssw)/len(ll.kw)) for ll in mlTOKSh] # words that dont return synsets and are stopwords informality ############A
#
#ncontrac_h=[100*(ll.ncontractions/len(ll.kw)) for ll in mlTOKSh]  # contractions per token informality ###########################
#nkwnssnsw_h=[100*(len(ll.kwnssnsw)/len(ll.kw)) for ll in mlTOKSh] # words that are known, are not stopwords and do not return synset
#nkwssnsw_h=[100*(len(ll.kwssnsw)/len(ll.kw)) for ll in mlTOKSh] # known words that are not stopwords and return synsets
#
#nt_=[]
#for i in xrange(4):
#    nt_+=[nt[i],nt_p[i]/nt[i],nt_i[i]/nt[i],nt_h[i]/nt[i]]
#ncpt_=[]
#for i in xrange(4):
#    ncpt_+=[ncpt[i],ncpt_p[i],ncpt_i[i],ncpt_h[i]]
#ntd_=[]
#for i in xrange(4):
#    ntd_+=[ntd[i],ntd_p[i],ntd_i[i],ntd_h[i]]
#ntp_=[]
#for i in xrange(4):
#    ntp_+=[ntp[i],ntp_p[i],ntp_i[i],ntp_h[i]]
#nkw_=[]
#for i in xrange(4):
#    nkw_+=[nkw[i],nkw_p[i],nkw_i[i],nkw_h[i]]
#nkwd_=[]
#for i in xrange(4):
#    nkwd_+=[nkwd[i],nkwd_p[i],nkwd_i[i],nkwd_h[i]]
#nkwss_=[]
#for i in xrange(4):
#    nkwss_+=[nkwss[i],nkwss_p[i],nkwss_i[i],nkwss_h[i]]
#nkwsw_=[]
#for i in xrange(4):
#    nkwsw_+=[nkwsw[i],nkwsw_p[i],nkwsw_i[i],nkwsw_h[i]]
#nukwsw_=[]
#for i in xrange(4):
#    nukwsw_+=[nukwsw[i],nukwsw_p[i],nukwsw_i[i],nukwsw_h[i]]
#nwsssw_=[]
#for i in xrange(4):
#    nwsssw_+=[nwsssw[i],nwsssw_p[i],nwsssw_i[i],nwsssw_h[i]]
#nwnsssw_=[]
#for i in xrange(4):
#    nwnsssw_+=[nwnsssw[i],nwnsssw_p[i],nwnsssw_i[i],nwnsssw_h[i]]
#ncontrac_=[]
#for i in xrange(4):
#    ncontrac_+=[ncontrac[i],ncontrac_p[i],ncontrac_i[i],ncontrac_h[i]]
#nkwnssnsw_=[]
#for i in xrange(4):
#    nkwnssnsw_+=[nkwnssnsw[i],nkwnssnsw_p[i],nkwnssnsw_i[i],nkwnssnsw_h[i]]
#nkwssnsw_=[]
#for i in xrange(4):
#    nkwssnsw_+=[nkwssnsw[i],nkwssnsw_p[i],nkwssnsw_i[i],nkwssnsw_h[i]]
#
#labels=(r"$|tokens|$", r"$\frac{|chars|-|spaces|}{|tokens|}$", r"$100\frac{|tokens \neq|}{|tokens|}$",
#        r"$100\frac{|punct|}{|tokens|}$", r"$100\frac{|known\,words=kw|}{|tokens| - |punct|}$",r"$100\frac{|kw\neq|}{kw}$", r"$100\frac{|kw\,with\,wordnet\,synset=kwss|}{|kw|}$",
#        r"100$\frac{|kw\,that\,are\,stopwords=kwsw|}{|kw|}$",r"$100\frac{|unknown\,words\,that\,are\,sw=ukwsw|}{|kw|}$",r"$100\frac{|kw\,that\, are\, stopwords\,and\,have\,synsets|}{|kw|}$",
#        r"$100\frac{|stopwords\,without\,synsets|}{|kw|}$", r"$100\frac{|contractions|}{|kw|}$",r"$100\frac{|kw\,not\,stopwords\,no\,synset|}{|kw|}$",
#        r"$100\frac{|kw\,not\,stopword\,has\,synset|}{|kw|}$")
#
#nnnT=(nt_,ncpt_,ntd_,
#      ntp_,nkw_,nkwd_,   nkwss_,
#      nkwsw_,nukwsw_,nwsssw_,
#      nwnsssw_,ncontrac_,nkwnssnsw_,
#      nkwssnsw_)
#i=0
#for ll in labels:
#    mstring="%s"%(ll,)
#    if i==0:
#        mstring+=(" & %i  & %.2f & %.2f & %.2f"*4) % tuple(nnnT[i]); i+=1
#    else:
#        mstring+=( " & %.2f & %.2f & %.2f & %.2f"*4) % tuple(nnnT[i]); i+=1
#    mstring+=" \\\\\\hline"
#    print mstring
#
##############################
#Tam de tokens
#if "mlTAMS" not in dir(__builtin__):
#    try:
#        # geral
#        f=open("cpickleDIR/mlTAMS","rb")
#        mlTAMS= pickle.load(f)
#        f.close()
#        __builtin__.mlTAMS=mlTAMS
#        print("aproveitados textos do pickleDIR")
#        # perifericos
#        f=open("cpickleDIR/mlTAMSp","rb")
#        mlTAMSp= pickle.load(f)
#        f.close()
#        __builtin__.mlTAMSp=mlTAMSp
#        print("aproveitados textos do pickleDIRp")
#        # intermediarios
#        f=open("cpickleDIR/mlTAMSi","rb")
#        mlTAMSi= pickle.load(f)
#        f.close()
#        __builtin__.mlTAMSi=mlTAMSi
#        print("aproveitados textos do pickleDIRi")
#        # hubs
#        f=open("cpickleDIR/mlTAMSh","rb")
#        mlTAMSh= pickle.load(f)
#        f.close()
#        __builtin__.mlTAMSh=mlTAMSh
#        print("aproveitados textos do pickleDIRh")
#    except:
#        print("fazendo medidas de texto")
#        # geral
#        try:
#            f=open("cpickleDIR/ml_cTAMS","rb")
#            ml_cTAMS= pickle.load(f)
#            f.close()
#            print("reaproveitado geral cpp")
#        except:
#            print("processando cpp")
#            ml_cTAMS=MedidasLMensagens(m[0],0,20001)
#            print("processado cpp")
#        try:
#            f=open("cpickleDIR/ml_dTAMS","rb")
#            ml_dTAMS= pickle.load(f)
#            f.close()
#            print("reaproveitado geral lad")
#        except:
#            print("processando lad")
#            ml_dTAMS=MedidasLMensagens(m[1],0,20001)
#            print("processado lad")
#        try:
#            f=open("cpickleDIR/ml_uTAMS","rb")
#            ml_uTAMS= pickle.load(f)
#            f.close()
#            print("reaproveitado geral lau")
#        except:
#            print("processando lau")
#            ml_uTAMS=MedidasLMensagens(m[2],0,20001)
#            print("processado lau")
#        try:
#            f=open("cpickleDIR/ml_eTAMS","rb")
#            ml_eTAMS= pickle.load(f)
#            f.close()
#            print("reaproveitado geral ele")
#        except:
#            print("processando ele")
#            ml_eTAMS=MedidasLMensagens(m[3],0,20001)
#            print("processado ele")
#
#        mlTAMS=[ml_cTAMS,ml_dTAMS,ml_uTAMS,ml_eTAMS]
#        f=open("./cpickleDIR/mlTAMS", 'wb')
#        pickle.dump(mlTAMS,f,-1)
#        f.close()
#        __builtin__.mlTAMS=mlTAMS
#
#        # perifericos
#        ml_cTAMSp=MedidasLMensagens(m[0],0,20001,autores=pr2[0].perifericosf)
#        print("processado cpp perifericos")
#        ml_dTAMSp=MedidasLMensagens(m[1],0,20001,autores=pr2[1].perifericosf)
#        print("processado lad")
#        ml_uTAMSp=MedidasLMensagens(m[2],0,20001,autores=pr2[2].perifericosf)
#        print("processado lau")
#        ml_eTAMSp=MedidasLMensagens(m[3],0,20001,autores=pr2[3].perifericosf)
#        print("processado ele")
#        mlTAMSp=[ml_cTAMSp,ml_dTAMSp,ml_uTAMSp,ml_eTAMSp]
#        f=open("./cpickleDIR/mlTAMSp", 'wb')
#        pickle.dump(mlTAMSp,f,-1)
#        f.close()
#        __builtin__.mlTAMSp=mlTAMSp
#
#        # intermediarios
#        ml_cTAMSi=MedidasLMensagens(m[0],0,20001,autores=pr2[0].intermediariosf)
#        print("processado cpp intermediarios")
#        ml_dTAMSi=MedidasLMensagens(m[1],0,20001,autores=pr2[1].intermediariosf)
#        print("processado lad")
#        ml_uTAMSi=MedidasLMensagens(m[2],0,20001,autores=pr2[2].intermediariosf)
#        print("processado lau")
#        ml_eTAMSi=MedidasLMensagens(m[3],0,20001,autores=pr2[3].intermediariosf)
#        print("processado ele")
#        mlTAMSi=[ml_cTAMSi,ml_dTAMSi,ml_uTAMSi,ml_eTAMSi]
#        f=open("./cpickleDIR/mlTAMSi", 'wb')
#        pickle.dump(mlTAMSi,f,-1)
#        f.close()
#        __builtin__.mlTAMSi=mlTAMSi
#
#        # hubs
#        ml_cTAMSh=MedidasLMensagens(m[0],0,20001,autores=pr2[0].hubsf)
#        print("processado cpp hubs")
#        ml_dTAMSh=MedidasLMensagens(m[1],0,20001,autores=pr2[1].hubsf)
#        print("processado lad")
#        ml_uTAMSh=MedidasLMensagens(m[2],0,20001,autores=pr2[2].hubsf)
#        print("processado lau")
#        ml_eTAMSh=MedidasLMensagens(m[3],0,20001,autores=pr2[3].hubsf)
#        print("processado ele")
#        mlTAMSh=[ml_cTAMSh,ml_dTAMSh,ml_uTAMSh,ml_eTAMSh]
#        f=open("./cpickleDIR/mlTAMSh", 'wb')
#        pickle.dump(mlTAMSh,f,-1)
#        f.close()
#        __builtin__.mlTAMSh=mlTAMSh
#else:
#    print("aproveitando medidas de texto")
#    mlTAMS=__builtin__.mlTAMS
#    mlTAMSp=__builtin__.mlTAMSp
#    mlTAMSi=__builtin__.mlTAMSi
#    mlTAMSh=__builtin__.mlTAMSh
#
#
#
## medidastamanhos()
## tabela: medias e desvios de tokens
#mtkw=[ll.mtkw for ll in ml]
## desvio
#dtkw=[ll.dtkw for ll in ml]
## media e desvio das palavras conhecidas existentes:
#mtkw_=[ll.mtkw_ for ll in ml]
#dtkw_=[ll.dtkw_ for ll in ml]
## media e desvio dos tokens incidentes que nao sao stopwords e  retornam synsets:
#mtpv=[ll.mtpv for ll in ml]
#dtpv=[ll.dtpv for ll in ml]
## media e desvio dos tokens existentes que nao sao stopwords e  retornam synsets:
#mtpv_=[ll.mtpv_ for ll in ml]
#dtpv_=[ll.dtpv_ for ll in ml]
## de stopwords:
#mtsw=[ll.mtsw for ll in ml]
#dtsw=[ll.dtsw for ll in ml]
#mtsw_=[ll.mtsw_ for ll in ml]
#dtsw_=[ll.dtsw_ for ll in ml]
## de stopwords+sem synsets:
#mtsw2=[ll.mtsw2 for ll in ml]
#dtsw2=[ll.dtsw2 for ll in ml]
#mtsw2_=[ll.mtsw2_ for ll in ml]
#dtsw2_=[ll.dtsw2_ for ll in ml]
#
###########
## perifericos
#mtkwP=[ll.mtkw for ll in ml]
## desvio
#dtkwP=[ll.dtkw for ll in ml]
## media e desvio das palavras conhecidas existentes:
#mtkw_P=[ll.mtkw_ for ll in ml]
#dtkw_P=[ll.dtkw_ for ll in ml]
## media e desvio dos tokens incidentes que nao sao stopwords e  retornam synsets:
#mtpvP=[ll.mtpv for ll in ml]
#dtpvP=[ll.dtpv for ll in ml]
## media e desvio dos tokens existentes que nao sao stopwords e  retornam synsets:
#mtpv_P=[ll.mtpv_ for ll in ml]
#dtpv_P=[ll.dtpv_ for ll in ml]
## de stopwords:
#mtswP=[ll.mtsw for ll in ml]
#dtswP=[ll.dtsw for ll in ml]
#mtsw_P=[ll.mtsw_ for ll in ml]
#dtsw_P=[ll.dtsw_ for ll in ml]
## de stopwords+sem synsets:
#mtsw2P=[ll.mtsw2 for ll in ml]
#dtsw2P=[ll.dtsw2 for ll in ml]
#mtsw2_P=[ll.mtsw2_ for ll in ml]
#dtsw2_P=[ll.dtsw2_ for ll in ml]
#
###########
## intermediarios
#mtkwI=[ll.mtkw for ll in ml]
## desvio
#dtkwI=[ll.dtkw for ll in ml]
## media e desvio das palavras conhecidas existentes:
#mtkw_I=[ll.mtkw_ for ll in ml]
#dtkw_I=[ll.dtkw_ for ll in ml]
## media e desvio dos tokens incidentes que nao sao stopwords e  retornam synsets:
#mtpvI=[ll.mtpv for ll in ml]
#dtpvI=[ll.dtpv for ll in ml]
## media e desvio dos tokens existentes que nao sao stopwords e  retornam synsets:
#mtpv_I=[ll.mtpv_ for ll in ml]
#dtpv_I=[ll.dtpv_ for ll in ml]
## de stopwords:
#mtswI=[ll.mtsw for ll in ml]
#dtswI=[ll.dtsw for ll in ml]
#mtsw_I=[ll.mtsw_ for ll in ml]
#dtsw_I=[ll.dtsw_ for ll in ml]
## de stopwords+sem synsets:
#mtsw2I=[ll.mtsw2 for ll in ml]
#dtsw2I=[ll.dtsw2 for ll in ml]
#mtsw2_I=[ll.mtsw2_ for ll in ml]
#dtsw2_I=[ll.dtsw2_ for ll in ml]
#
###########
## hubs
#mtkwH=[ll.mtkw for ll in ml]
## desvio
#dtkwH=[ll.dtkw for ll in ml]
## media e desvio das palavras conhecidas existentes:
#mtkw_H=[ll.mtkw_ for ll in ml]
#dtkw_H=[ll.dtkw_ for ll in ml]
## media e desvio dos tokens incidentes que nao sao stopwords e  retornam synsets:
#mtpvH=[ll.mtpv for ll in ml]
#dtpvH=[ll.dtpv for ll in ml]
## media e desvio dos tokens existentes que nao sao stopwords e  retornam synsets:
#mtpv_H=[ll.mtpv_ for ll in ml]
#dtpv_H=[ll.dtpv_ for ll in ml]
## de stopwords:
#mtswH=[ll.mtsw for ll in ml]
#dtswH=[ll.dtsw for ll in ml]
#mtsw_H=[ll.mtsw_ for ll in ml]
#dtsw_H=[ll.dtsw_ for ll in ml]
## de stopwords+sem synsets:
#mtsw2H=[ll.mtsw2 for ll in ml]
#dtsw2H=[ll.dtsw2 for ll in ml]
#mtsw2_H=[ll.mtsw2_ for ll in ml]
#dtsw2_H=[ll.dtsw2_ for ll in ml]
#
#### organizando para fazer tabela
#mtkwO=[]
#for i in xrange(4):
#    mtkwO+=[mtkw[i],mtkwP[i],mtkwI[i],mtkwH[i]]
#dtkwO=[]
#for i in xrange(4):
#    dtkwO+=[dtkw[i],dtkwP[i],dtkwI[i],dtkwH[i]]
#mtkw_O=[]
#for i in xrange(4):
#    mtkw_O+=[mtkw_[i],mtkw_P[i],mtkw_I[i],mtkw_H[i]]
#dtkw_O=[]
#for i in xrange(4):
#    dtkw_O+=[dtkw_[i],dtkw_P[i],dtkw_I[i],dtkw_H[i]]
#mtpvO=[]
#for i in xrange(4):
#    mtpvO+=[mtpv[i],mtpvP[i],mtpvI[i],mtpvH[i]]
#dtpvO=[]
#for i in xrange(4):
#    dtpvO+=[dtpv[i],dtpvP[i],dtpvI[i],dtpvH[i]]
#mtpv_O=[]
#for i in xrange(4):
#    mtpv_O+=[mtpv_[i],mtpv_P[i],mtpv_I[i],mtpv_H[i]]
#dtpv_O=[]
#for i in xrange(4):
#    dtpv_O+=[dtpv_[i],dtpv_P[i],dtpv_I[i],dtpv_H[i]]
#mtswO=[]
#for i in xrange(4):
#    mtswO+=[mtsw[i],mtswP[i],mtswI[i],mtswH[i]]
#dtswO=[]
#for i in xrange(4):
#    dtswO+=[dtsw[i],dtswP[i],dtswI[i],dtswH[i]]
#mtsw_O=[]
#for i in xrange(4):
#    mtsw_O+=[mtsw_[i],mtsw_P[i],mtsw_I[i],mtsw_H[i]]
#dtsw_O=[]
#for i in xrange(4):
#    dtsw_O+=[dtsw_[i],dtsw_P[i],dtsw_I[i],dtsw_H[i]]
#mtsw2O=[]
#for i in xrange(4):
#    mtsw2O+=[mtsw2[i],mtsw2P[i],mtsw2I[i],mtsw2H[i]]
#dtsw2O=[]
#for i in xrange(4):
#    dtsw2O+=[dtsw2[i],dtsw2P[i],dtsw2I[i],dtsw2H[i]]
#mtsw2_O=[]
#for i in xrange(4):
#    mtsw2_O+=[mtsw2_[i],mtsw2_P[i],mtsw2_I[i],mtsw2_H[i]]
#dtsw2_O=[]
#for i in xrange(4):
#    dtsw2_O+=[dtsw2_[i],dtsw2_P[i],dtsw2_I[i],dtsw2_H[i]]
#
#labels=(r"$\mu(size\,of\,known\,word=skw)$",r"$\sigma(skw)$",r"$\mu(\neq skw)$",r"$\sigma(\neq skw)$",
#        r"$\mu(skwss)$",r"$\sigma(skwss)$",r"$\mu(\neq skwss)$",r"$\sigma(\neq skwss)$",
#        r"$\mu(ssw)$",r"$\sigma(ssw)$",r"$\mu(\neq ssw_)$",r"$\sigma(\neq ssw_)$",
#        r"$\mu(snsssw)$",r"$\sigma(snsssw)$",r"$\mu(\neq snsssw_)$",r"$\sigma(\neq snsssw_)$")
#nnnS=(mtkwO,dtkwO,mtkw_O,dtkw_O,
#      mtpvO,dtpvO,mtpv_O,dtpv_O,
#      mtswO,dtswO,mtsw_O,dtsw_O,
#      mtsw2O,dtsw2O,mtsw2_O,dtsw2_O)
#i=0
#for ll in labels:
#    mstring=("%s"+" & %.2f & %.2f & %.2f & %.2f"*4 + " \\\\") % tuple([ll]+nnnS[i])
#    if i in (3,7,11,15):
#        mstring+=" \\hline"
#    i+=1
#
#
#
#

sys.exit()
try:
    f=open("cpickleDIR/r","rb")
    r=pickle.load(f)
    f.close()
    print("aproveitadas redes do cpickleDIR")
except:
    rcpp=Rede(m[0],0,20001)
    rlad=Rede(m[1],0,20001)
    rlau=Rede(m[2],0,20001)
    rele=Rede(m[3],0,20001)
    r=[rcpp,rlad,rlau,rele]
    f=open("./cpickleDIR/r", 'wb')
    pickle.dump(r,f,-1)
    f.close()
    print time.time()-atime; atime=time.time()
try:
    f=open("cpickleDIR/pr","rb")
    pr=pickle.load(f)
    f.close()
    print("aproveitadas particoes do cpickleDIR")
except:
    prcpp=ParticionaRede(r[0])
    prlad=ParticionaRede(r[1])
    prlau=ParticionaRede(r[2])
    prele=ParticionaRede(r[3])
    pr=[prcpp,prlad,prlau,prele]
    f=open("./cpickleDIR/pr", 'wb')
    pickle.dump(pr,f,-1)
    f.close()
    print time.time()-atime; atime=time.time()
    
# obtendo ids em cada setor:
# pr[].perifericos_ // intermediarios_ // 
divisoes=[]
for pp in pr:
    divisoes.append([[],[],[]])
    f1=pp.f1
    f2=pp.f2
    graus=pp.g.degree(weight="weight")
    for kk in graus.keys():
        if graus[kk]>=f2:
            divisoes[-1][2].append(kk)
        elif graus[kk]<f1:
            divisoes[-1][0].append(kk)
        else:
            divisoes[-1][1].append(kk)
    
print( [(len(dd[0]),len(dd[1]),len(dd[2])) for dd in divisoes])
print( [(len(dd[0])/sum([len(ddd) for ddd in dd]),len(dd[1])/sum([len(ddd) for ddd in dd]),len(dd[2])/sum([len(ddd) for ddd in dd])) for dd in divisoes])
    
     
try:
    f=open("cpickleDIR/pr2","rb")
    pr2=pickle.load(f)
    f.close()
    print("aproveitadas particoes do cpickleDIR")
except:
    prcpp=ParticionaRede2(r[0])
    prlad=ParticionaRede2(r[1])
    prlau=ParticionaRede2(r[2])
    prele=ParticionaRede2(r[3])
    pr2=[prcpp,prlad,prlau,prele]
    f=open("./cpickleDIR/pr2", 'wb')
    pickle.dump(pr2,f,-1)
    f.close()
    print time.time()-atime; atime=time.time()

labels=(r"$N$",r"$N_{\%}$",r"$M$",r"$M_{\%}$",r"$\Gamma$",r"$\Gamma_{\%}$")
NN=[i.g.number_of_nodes() for i in pr2]
pp__=[i.distf_[0] for i in pr2]
pp_=[100*i.distf_[0]/sum(i.distf_) for i in pr2]
ii=[i.distf_[1] for i in pr2]
ii_=[100*i.distf_[1]/sum(i.distf_) for i in pr2]
hh=[i.distf_[2] for i in pr2]
hh_=[100*i.distf_[2]/sum(i.distf_) for i in pr2]

GM=[len([mm.mm[ID] for ID in mm.ids if mm.mm[ID][1]==None]) for mm in m]
GMp=[0,0,0,0]
GMi=[0,0,0,0]
GMh=[0,0,0,0]
i=0
for pp in pr2:
    for participante in pp.perifericosf:
        GMp[i]+=len([1 for msg in m[i].aa[participante] if msg[1]==None])
    for participante in pp.intermediariosf:
        GMi[i]+=len([1 for msg in m[i].aa[participante] if msg[1]==None])
    for participante in pp.hubsf:
        GMh[i]+=len([1 for msg in m[i].aa[participante] if msg[1]==None])
    i+=1

GMp_=[0,0,0,0]
GMi_=[0,0,0,0]
GMh_=[0,0,0,0]
i=0
for pp in pr2:
    GMp_[i]=100*GMp[i]/GM[i]
    GMi_[i]=100*GMi[i]/GM[i]
    GMh_[i]=100*GMh[i]/GM[i]
    i+=1

MM=[20000,20000,20000,20000]
MMp=[0,0,0,0]
i=0
for pp in pr2:
    for per in pp.perifericosf:
        MMp[i]+=len(m[i].aa[per]) # numero de mensagens do periferico
    i+=1
MMp_=[100*mmp/20000 for mmp in MMp]
MMi=[0,0,0,0]
i=0
for pp in pr2:
    for inter in pp.intermediariosf:
        MMi[i]+=len(m[i].aa[inter]) # numero de mensagens do intermediario 
    i+=1
MMi_=[100*mmi/20000 for mmi in MMi]

MMh=[0,0,0,0]
i=0
for pp in pr2:
    for hub in pp.hubsf:
        MMh[i]+=len(m[i].aa[hub]) # numero de mensagens do intermediario 
    i+=1
MMh_=[100*mmh/20000 for mmh in MMh]

        
i=0
for ll in labels:
    mstring= "%s " % (ll,)
    j=0
    for pr in pr2:
        if i==0:
            mstring+=" & %i & %i & %i & %i" % (NN[j],pp__[j],ii[j],hh[j]); j+=1
        if i==1:
            mstring+=" & - & %.2f\\%% & %.2f\\%% & %.2f\\%%" % (pp_[j], ii_[j],hh_[j]); j+=1
        if i==2:
            mstring+=" & %i & %i & %i & %i" % (MM[j],MMp[j],MMi[j],MMh[j]); j+=1
        if i==3:
            mstring+=" & - & %.2f\\%% & %.2f\\%% & %.2f\\%%" % (MMp_[j],MMi_[j],MMh_[j]); j+=1
        if i==4:
            mstring+=" & %i & %i & %i & %i" % (GM[j],GMp[j],GMi[j],GMh[j]); j+=1
        if i==5:
            mstring+=" & - & %.2f\\%% & %.2f\\%% & %.2f\\%%" % (GMp_[j],GMi_[j],GMh_[j]); j+=1

    i+=1

    mstring+=" \\\\\\hline"
    print(mstring)



sys.exit()
if "ml" not in dir(__builtin__):
    try:
        f=open("cpickleDIR/ml","rb")
        ml= pickle.load(f)
        f.close()
        __builtin__.ml=ml
        print("aproveitados textos do pickleDIR")
    except:
        print("fazendo medidas de texto")
        try:
            f=open("./cpickleDIR/ml_c", 'rb')
            ml_c=pickle.load(f)
            f.close()
            print("aproveitadas textos do cpp do pickleDIR")
        except:
            ml_c=MedidasLMensagens(m[0],0,20001)
            print("processado cpp")
            f=open("./cpickleDIR/ml_c", 'wb')
            pickle.dump(ml_c,f,-1)
            f.close()
        try:
            f=open("./cpickleDIR/ml_d", 'rb')
            ml_d=pickle.load(f)
            f.close()
            print("aproveitadas textos do lad do pickleDIR")
        except:
            ml_d=MedidasLMensagens(m[1],0,20001)
            print("processado lad")
            f=open("./cpickleDIR/ml_d", 'wb')
            pickle.dump(ml_d,f,-1)
            f.close()
        try:
            f=open("./cpickleDIR/ml_u", 'rb')
            ml_u=pickle.load(f)
            f.close()
            print("aproveitadas textos do lau do pickleDIR")
        except:
            ml_u=MedidasLMensagens(m[2],0,20001)
            print("processado lau")
            f=open("./cpickleDIR/ml_u", 'wb')
            pickle.dump(ml_u,f,-1)
            f.close()
        try:
            f=open("./cpickleDIR/ml_e", 'rb')
            ml_e=pickle.load(f)
            f.close()
            print("aproveitadas textos do ele do pickleDIR")
        except:
            ml_e=MedidasLMensagens(m[3],0,20001)
            print("processado ele")
            f=open("./cpickleDIR/ml_e", 'wb')
            pickle.dump(ml_e,f,-1)
            f.close()
        ml=[ml_c,ml_d,ml_u,ml_e]
        f=open("./cpickleDIR/ml", 'wb')
        pickle.dump(ml,f,-1)
        f.close()
        __builtin__.ml=ml
else:
    print("aproveitando medidas de texto")
    ml=__builtin__.ml

#--># medidasLetras()
#-->nc=[ll.nc for ll in ml] # caracteres
#-->ne=[100*(ll.ne/ll.nc) for ll in ml] # espacos
#-->np=[100*(ll.np/(ll.nc-ll.ne)) for ll in ml] # punctuation
#-->nd=[100*(ll.nd/(ll.nc-ll.ne)) for ll in ml] # digits
#-->nl=[100*(ll.nl/(ll.nc-ll.ne)) for ll in ml] # letras 
#-->nv=[100*(ll.nv/(ll.nl)) for ll in ml] # vogais
#-->nu=[100*(ll.nm/ll.nl) for ll in ml] # uppercase
#-->
#-->labels=(r"$n\,chars$",r"$\left(\frac{n\,spaces}{n\,chars}\right)\times 100$",r"$\left(\frac{n\,punct}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,digits}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,letters}{n\,chars-n\,spaces}\right)\times 100$",r"$\left(\frac{n\,vogals}{n\,letters}\right)\times 100$",r"$\left(\frac{n\,Uppercase}{n\,letters}\right)\times 100$")
#-->nnn=(nc,ne,np,nd,nl,nv,nu)
#-->i=0
#-->for ll in labels:
#-->    if i==0:
#-->        print "%s & %i & %i & %i & %i \\\\\\hline" % tuple([ll]+nnn[i]); i+=1
#-->    else:
#-->        print "%s & %.2f & %.2f & %.2f & %.2f \\\\" % tuple([ll]+nnn[i]); i+=1
#-->

#--># medidasTokens()
#-->nt=[ll.nt for ll in ml] # ntokens
#-->ncpt=[len(ll.T.replace(" ",""))/ll.nt for ll in ml]
#-->ntd=[100*(ll.ntd/ll.nt) for ll in ml] # ntokens differentes
#-->ntp=[100*(ll.ntp/ll.nt) for ll in ml] # npontuacoes
#-->#ntp=[100*(ll.ntp/ll.nt) for ll in ml] # npontuacoes
#-->nkw=  [100*(len(ll.kw)/(ll.nt-ll.ntp)) for ll in ml] # known words
#-->nkwd=  [100*(len(set(ll.kw))/len(ll.kw)) for ll in ml] # known words
#-->nkwss=[100*(len(ll.wss)/len(ll.kw)) for ll in ml] # known words that return synsets
#-->nkwsw=[100*(len(ll.wsw)/len(ll.kw)) for ll in ml] # known words that are stopwords
#-->
#-->#nukwsw=[100*(len(ll.ukwsw)/(ll.nt-ll.ntp)) for ll in ml] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#-->nukwsw=[100*(len(ll.ukwsw)/len(ll.kw)) for ll in ml] # unknown words that are stopwords, i t and s, as they come in 't and 's and minnor case i, which are sign of informality.
#-->
#-->nwsssw=[100*(len(ll.wsssw)/len(ll.kw)) for ll in ml] # words that return synsets and are stopwords
#-->
#-->nwnsssw=[100*(len(ll.wnsssw)/len(ll.kw)) for ll in ml] # words that dont return synsets and are stopwords informality ############A
#-->
#-->ncontrac=[100*(ll.ncontractions/len(ll.kw)) for ll in ml]  # contractions per token informality ###########################
#-->nkwnssnsw=[100*(len(ll.kwnssnsw)/len(ll.kw)) for ll in ml] # words that are known, are not stopwords and do not return synset
#-->nkwssnsw=[100*(len(ll.kwssnsw)/len(ll.kw)) for ll in ml] # known words that are not stopwords and return synsets
#-->
#-->labels=(r"$|tokens|$", r"$\frac{|chars|-|spaces|}{|tokens|}$", r"$100\frac{|tokens \neq|}{|tokens|}$",
#-->        r"$100\frac{|punct|}{|tokens|}$", r"$100\frac{|known\,words=kw|}{|tokens| - |punct|}$",r"$100\frac{|kw\neq|}{kw}$", r"$100\frac{|kw\,with\,wordnet\,synset=kwss|}{|kw|}$",
#-->        r"100$\frac{|kw\,that\,are\,stopwords=kwsw|}{|kw|}$",r"$100\frac{|unknown\,words\,that\,are\,sw=ukwsw|}{|kw|}$",r"$100\frac{|kw\,that\, are\, stopwords\,and\,have\,synsets|}{|kw|}$",
#-->        r"$100\frac{|stopwords\,without\,synsets|}{|kw|}$", r"$100\frac{|contractions|}{|kw|}$",r"$100\frac{|kw\,not\,stopwords\,no\,synset|}{|kw|}$",
#-->        r"$100\frac{|kw\,not\,stopword\,has\,synset|}{|kw|}$")
#-->
#-->nnnT=(nt,ncpt,ntd,
#-->      ntp,nkw,nkwd,   nkwss,
#-->      nkwsw,nukwsw,nwsssw,
#-->      nwnsssw,ncontrac,nkwnssnsw,
#-->      nkwssnsw)
#-->i=0
#-->for ll in labels:
#-->    if i in (0,3):
#-->        print "%s & %i & %i & %i & %i \\\\\\hline" % tuple([ll] +nnnT[i]); i+=1
#-->    else:
#-->        print "%s & %.2f & %.2f & %.2f & %.2f \\\\" % tuple([ll]+nnnT[i]); i+=1


   


# medidastamanhos()
# tabela: medias e desvios de tokens
# media do tamanho da palavra conhecida incidente (que retorna ou nao synset):
#### RETIRARRR JAH FEITO NO utilsRedes.py
#for i in xrange(len(ml)):
#    ml[i].mtkw =n.mean(ml[i].tkw)
#    ml[i].dtkw = n.std(ml[i].tkw)
#    ml[i].mtkw_=n.mean(ml[i].tkw_)
#    ml[i].dtkw_= n.std(ml[i].tkw_)

#-->mtkw=[ll.mtkw for ll in ml]
#--># desvio
#-->dtkw=[ll.dtkw for ll in ml]
#--># media e desvio das palavras conhecidas existentes:
#-->mtkw_=[ll.mtkw_ for ll in ml]
#-->dtkw_=[ll.dtkw_ for ll in ml]
#--># media e desvio dos tokens incidentes que nao sao stopwords e  retornam synsets:
#-->mtpv=[ll.mtpv for ll in ml]
#-->dtpv=[ll.dtpv for ll in ml]
#--># media e desvio dos tokens existentes que nao sao stopwords e  retornam synsets:
#-->mtpv_=[ll.mtpv_ for ll in ml]
#-->dtpv_=[ll.dtpv_ for ll in ml]
#--># de stopwords:
#-->mtsw=[ll.mtsw for ll in ml]
#-->dtsw=[ll.dtsw for ll in ml]
#-->mtsw_=[ll.mtsw_ for ll in ml]
#-->dtsw_=[ll.dtsw_ for ll in ml]
#--># de stopwords+sem synsets:
#-->mtsw2=[ll.mtsw2 for ll in ml]
#-->dtsw2=[ll.dtsw2 for ll in ml]
#-->mtsw2_=[ll.mtsw2_ for ll in ml]
#-->dtsw2_=[ll.dtsw2_ for ll in ml]
#-->
#-->labels=(r"$\mu(size\,of\,known\,word=skw)$",r"$\sigma(skw)$",r"$\mu(\neq skw)$",r"$\sigma(\neq skw)$",
#-->        r"$\mu(skwss)$",r"$\sigma(skwss)$",r"$\mu(\neq skwss)$",r"$\sigma(\neq skwss)$",
#-->        r"$\mu(ssw)$",r"$\sigma(ssw)$",r"$\mu(\neq ssw_)$",r"$\sigma(\neq ssw_)$",
#-->        r"$\mu(snsssw)$",r"$\sigma(snsssw)$",r"$\mu(\neq snsssw_)$",r"$\sigma(\neq snsssw_)$")
#-->nnnS=(mtkw,dtkw,mtkw_,dtkw_,
#-->      mtpv,dtpv,mtpv_,dtpv_,
#-->      mtsw,dtsw,mtsw_,dtsw_,
#-->      mtsw2,dtsw2,mtsw2_,dtsw2_)
#-->i=0
#-->for ll in labels:
#-->    print "%s & %.2f & %.2f & %.2f & %.2f \\\\" % tuple([ll]+nnnS[i]); i+=1




# figuras: histogramas em graficos de barra, 2 a 2, incidente e existencial:
#-->mmax=max([max(ll.tkw) for ll in ml])
#-->bins=range(mmax+2)
#-->i=0
#-->titulos={0:"CPP network",1:"LAD network",2:"LAU network",3:"ELE network"}
#-->for ll in ml:
#-->    p.subplot(int("41%i"%(i+1,)))
#-->    p.title(titulos[i]+ r", size histogram of known english words. $\sum |incident - existential| =$ %.2f)"%(n.abs(ml[i].htkw[0]-ml[i].htkw_[0]).sum(),)); i+=1
#-->    p.hist(ll.tkw, bins,normed=True,alpha=0.5,label="incident")
#-->    p.hist(ll.tkw_,bins,normed=True,alpha=0.5,label="existential")
#-->    p.legend(loc="upper right")
#-->    p.xlabel(r"size $\rightarrow$")
#-->    p.ylabel(r"fraction of samples $\rightarrow$")
#-->    p.xticks([bb+0.5 for bb in bins],bins)
#-->    p.yticks([0.05,0.1,0.15,0.2,0.25])
#-->    p.ylim(0,0.25)
#-->    p.xlim(0,mmax+2)
#-->p.show()
#-->
#-->i=0
#-->for ll in ml:
#-->    p.subplot(int("41%i"%(i+1,)))
#-->    p.title(titulos[i]+ ", size histogram of known words that are not stopwords. $\sum |incident - existential| =$ %.2f)"%(n.abs(ml[i].htkwnsw[0]-ml[i].htkwnsw_[0]).sum(),)); i+=1
#-->    p.hist(ll.tkwnsw, bins,normed=True,alpha=0.5,label="incident")
#-->    p.hist(ll.tkwnsw_,bins,normed=True,alpha=0.5,label="existential")
#-->    p.legend(loc="upper right")
#-->    p.xlabel(r"size $\rightarrow$")
#-->    p.ylabel(r"fraction of samples $\rightarrow$")
#-->    p.xticks([bb+0.5 for bb in bins],bins)
#-->    p.yticks([0.05,0.1,0.15,0.2,0.25])
#-->    p.ylim(0,0.25)
#-->    p.xlim(0,mmax+2)
#-->p.show()
#--> 
#-->
#-->
#-->
#-->    
#-->i=0
#-->for ll in ml:
#-->    p.subplot(int("41%i"%(i+1,)))
#-->    p.title(titulos[i]+ ", size histogram of known words that return wordnet synsets and are not stopwords. $\sum |incident - existential| =$ %.2f)"%(n.abs(ml[i].htams[0]-ml[i].htams_[0]).sum(),)); i+=1
#-->    p.hist(ll.tams, bins,normed=True,alpha=0.5,label="incident")
#-->    p.hist(ll.tams_,bins,normed=True,alpha=0.5,label="existential")
#-->    p.legend(loc="upper right")
#-->    p.xlabel(r"size $\rightarrow$")
#-->    p.ylabel(r"fraction of samples $\rightarrow$")
#-->    p.xticks([bb+0.5 for bb in bins],bins)
#-->    p.yticks([0.05,0.1,0.15,0.2,0.25])
#-->    p.ylim(0,0.25)
#-->    p.xlim(0,mmax+2)
#-->p.show()
#--> 
#-->
    
#-->i=0
#-->for ll in ml:
#-->    p.subplot(int("41%i"%(i+1,)))
#-->    p.title(titulos[i]+ ", size histogram of stopwords. $\sum |incident - existential| =$ %.2f)"%(n.abs(ml[i].htsw[0]/ml[i].htsw[0].sum()-ml[i].htsw_[0]/ml[i].htsw_[0].sum()).sum(),)); i+=1
#-->    p.hist(ll.tsw, bins,normed=True,alpha=0.5,label="incident")
#-->    p.hist(ll.tsw_,bins,normed=True,alpha=0.5,label="existential")
#-->    p.legend(loc="upper right")
#-->    p.xlabel(r"size $\rightarrow$")
#-->    p.ylabel(r"fraction of samples $\rightarrow$")
#-->    p.xticks([bb+0.5 for bb in bins],bins)
#-->    p.yticks([0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4])
#-->    p.ylim(0,0.40)
#-->    p.xlim(0,mmax+2)
#-->p.show()
 

#-->
#-->i=0
#-->for ll in ml:
#-->    p.subplot(int("41%i"%(i+1,)))
#-->    p.title(titulos[i]+ ", size histogram of words that are not stopwords and do not have synset. $\sum |incident - existential| =$ %.2f)"%(n.abs(ml[i].htsw2[0]/ml[i].htsw2[0].sum()-ml[i].htsw2_[0]/ml[i].htsw2_[0].sum()).sum(),)); i+=1
#-->    p.hist(ll.tsw2, bins,normed=True,alpha=0.5,label="incident")
#-->    p.hist(ll.tsw2_,bins,normed=True,alpha=0.5,label="existential")
#-->    p.legend(loc="upper right")
#-->    p.xlabel(r"size $\rightarrow$")
#-->    p.ylabel(r"fraction of samples $\rightarrow$")
#-->    p.xticks([bb+0.5 for bb in bins],bins)
#-->    p.yticks([0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4])
#-->    p.ylim(0,0.40)
#-->    p.xlim(0,mmax+2)
#-->p.show()
#--> 

#-->############################
#--># numero de sentencas:
#-->nsents=[len(ll.TS) for ll in ml]
#--># media e desvio dos tamanhos das sentencas em chars:
#-->mtTS=[ll.mtTS for ll in ml]
#-->dtTS=[ll.dtTS for ll in ml]
#--># media e desvio dos tamanhos das sentencas em tokens:
#-->mtsTS=[ll.mtsTS for ll in ml]
#-->dtsTS=[ll.dtsTS for ll in ml]
#--># media e desvio do tamanho das sentencas em palavras conhecidas:
#-->mtsTSkw=[ll.mtsTSkw for ll in ml]
#-->dtsTSkw=[ll.dtsTSkw for ll in ml]
#--># media e desvio do tamanho das sentencas em palavras conhecidas que retornam synsets e n sao stopwords:
#-->mtsTSpv=[ll.mtsTSpv for ll in ml]
#-->dtsTSpv=[ll.dtsTSpv for ll in ml]
#-->
#-->labels=(r"$|sents|$",r"$\mu\left(\frac{chars}{sent}\right)$",r"$\sigma\left(\frac{chars}{sent}\right)$",r"$\mu\left(\frac{tokens}{sent}\right)$",r"$\sigma\left(\frac{tokens}{sent}\right)$",r"$\mu\left(\frac{kw}{sent}\right)$",r"$\sigma\left(\frac{kw}{sent}\right)$",r"$\mu\left(\frac{kwssnsw}{sent}\right)$",r"$\sigma\left(\frac{kwssnsw}{sent}\right)$")
#-->nnnS2=(nsents,mtTS,dtTS,mtsTS,dtsTS,mtsTSkw,dtsTSkw,mtsTSpv,dtsTSpv)
#-->i=0
#-->for ll in labels:
#-->    if i==0:
#-->        print "%s & %i & %i & %i & %i \\\\" % tuple([ll]+nnnS2[i]); i+=1
#-->    else:
#-->        print "%s & %.2f & %.2f & %.2f & %.2f \\\\" % tuple([ll]+nnnS2[i]); i+=1
#-->

#############################
#--># media e desvio de chars/msg
#-->mtmT=[ll.mtmT for ll in ml]
#-->dtmT=[ll.dtmT for ll in ml]
#--># media e descio em n de tokens / msg
#-->mttmT=[ll.mttmT for ll in ml]
#-->dttmT=[ll.dttmT for ll in ml]
#--># media e descio em sents / msg
#-->mtsmT=[ll.mtsmT for ll in ml]
#-->dtsmT=[ll.dtsmT for ll in ml]
#-->
#-->labels=(r"$\mu\left(\frac{|chars|}{msg}\right)$",r"$\sigma\left(\frac{|chars|}{msg}\right)$",r"$\mu\left(\frac{|tokens|}{msg}\right)$",r"$\sigma\left(\frac{|tokens|}{msg}\right)$",r"$\mu\left(\frac{|sents|}{msg}\right)$",r"$\sigma\left(\frac{|sents|}{msg}\right)$")
#-->
#-->nnnM=(mtmT,dtmT,
#-->      mttmT, dttmT,
#-->      mtsmT, dtsmT)
#-->
#-->i=0
#-->for ll in labels:
#-->    print "%s & %.2f & %.2f & %.2f & %.2f \\\\" % tuple([ll]+nnnM[i]); i+=1

##############################
# incidencia das etiquetas morfossintáticas do corpus da Brown
#l=[]
#for k in ml[0].htags__.keys()[::-1]:
#    l.append(tuple([k]+[100*ll.htags__[k] for ll in ml]))
#
#for ll in l:
#    print "%s & %.4f & %.4f & %.4f & %.4f \\\\" % ll



sys.exit()
def retornamedidas(mensagens):
    m=mensagens
    t=[string.join(m.mm[i][3]) for i in m.ids]
    t=string.join(t)

    # incidencias de pontuacao, etc
    tk=k.word_tokenize(t)
    from nltk.corpus import wordnet as wn
    ok=[i for i in tk if wn.synsets(i)]
    frac1=len(ok)/len(tk)
    ss=[len(wn.synsets(i)) for i in ok]
    mss=n.mean(ss)
    dss=n.std(ss)

    pt=[i for i in tk if i in string.punctuation]
    frac2=len(pt)/len(tk)
    return len(t),len(tk),len(pt),frac1,frac2,mss,dss

f1=retornamedidas(__builtin__.cpp)
f2=retornamedidas(__builtin__.lad)
f3=retornamedidas(__builtin__.lau)
f4=retornamedidas(__builtin__.met)
sys.exit()
# 1) fazer junção de todos os textos do cpp
m=__builtin__.cpp

# todo texto
t=[string.join(m.mm[i][3]) for i in m.ids]
t=string.join(t)

# incidencias de pontuacao, etc
tk=k.word_tokenize(t)
from nltk.corpus import wordnet as wn
frac1=len([i for i in tk if wn.synsets(i)])/len(tk)

# 2) fazer junção de todos os textos do lad 
m=__builtin__.lad
                
# todo texto
t=[string.join(m.mm[i][3]) for i in m.ids]
t=string.join(t)
            
# incidencias de pontuacao, etc                                        
tk=k.word_tokenize(t)
from nltk.corpus import wordnet as wn                                  
frac2=len([i for i in tk if wn.synsets(i)])/len(tk)

# 3) fazer junção de todos os textos do lau 
m=__builtin__.lau
                
# todo texto
t=[string.join(m.mm[i][3]) for i in m.ids]
t=string.join(t)
            
# incidencias de pontuacao, etc                                        
tk=k.word_tokenize(t)
from nltk.corpus import wordnet as wn                                  
frac3=len([i for i in tk if wn.synsets(i)])/len(tk)

# 4) fazer junção de todos os textos do met
m=__builtin__.met
                
# todo texto
t=[string.join(m.mm[i][3]) for i in m.ids]
t=string.join(t)
            
# incidencias de pontuacao, etc                                        
tk=k.word_tokenize(t)
from nltk.corpus import wordnet as wn                                  
frac4=len([i for i in tk if wn.synsets(i)])/len(tk)

sys.exit()
texts=[]
for i in m.ids:
    text=m.mm[i][3]
    t=text.splitlines()
    t=[line for line in t if line]
    t_=[]
    for line in t:
        if line.startswith(">"):
            pass
        elif line.startswith("on mon"):
            pass
        elif line.startswith("on tue"):
            pass
        elif line.startswith("on wed"):
            pass
        elif line.startswith("on thu"):
            pass
        elif line.startswith("on fri"):
            pass
        elif line.startswith("on sat"):
            pass
        elif line.startswith("on sun"):
            pass
        elif line.endswith("wrote:"):
            pass
        # uma palavra soh sem ponto final
        elif len(line.split()) == 1 and line[-1]!=".":
            pass
        # duas palavras separadas, com a primeira letra caixa alta em cada
        elif line.istitle():
            pass
        elif line.startswith("--"):
            break
        else:
            t_.append(line)
    #m.mm[i][3]=string.join(t_)
    texts.append(t_)


sys.exit()
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
        mensagens=m=mensagens(caminho,de,ate)
        __builtin__.m=m
        __builtin__.de=de
        __builtin__.ate=ate
else:
    print("lendo mensagens")
    mensagens=m=mensagens(caminho,de,ate)
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
        e=evoluirede(0,20001,j,passo,m, caminho)
        ee.append(e)
        e.drawsections2()
    __builtin__.ee=ee

md=[]
countev=0
for e in ee: # for each evolution (each window size)
    print(countev)
    countpr=0
    md.append([])
    feature_vecs=[]
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
            #per  =pr.c.cas_exc[0]
            #inter=pr.c.cas_exc[1]
            #hubs =pr.c.cas_exc[2]
        else:
            per=pr.c.cas_exc[0]
            inter=pr.c.cas_exc[1]
            hubs=pr.c.cas_exc[2]
            
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
        assimarestam=[]
        assimarestadp=[]
        deseqarestam=[]
        deseqarestadp=[]
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
                assimarestam.append(n.mean(as_))
                assimarestadp.append(n.std(as_))
                deseqarestam.append(n.mean(de_))
                deseqarestadp.append(n.std(de_))
            else:
                assimarestam.append(0.)
                assimarestadp.append(0.)    
                deseqarestam.append(0.)
                deseqarestadp.append(0.)

        md[-1].append(n.vstack((degree_,id_,od_,strengh_,is_,os_,cc_,bc_,assimetrias,desequilibrios,assimarestam,assimarestadp,deseqarestam,deseqarestadp,tclass)))
        print("arrumacao e fazecao de vetor")

        r=[(cl==0) for cl in tclass]
        g=[(cl==1) for cl in tclass]
        b=[(cl==2) for cl in tclass]
        rgb=n.vstack((r,g,b)).t
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
        p.savefig("tempolau/ev%ipr%i.png" % (countev,countpr))
        p.clf()

        p.plot(degree_[:len(per)],cc_[:len(per)],"bo", ms=3.9,label="peripheral")
        p.plot(degree_[len(per):len(per)+len(inter)],cc_[len(per):len(per)+len(inter)],"go", ms=3.9,label="intermediary")
        p.plot(degree_[-len(hubs):],cc_[-len(hubs):],"ro", ms=3.9,label="hubs")
        p.legend(loc="upper right")
        p.xlabel(r"degree $\rightarrow$")
        p.ylabel(r"clustering coefficient $\rightarrow$")
        p.ylim(-0.1,1.1)
        p.title("clustering coefficient versus degree of vertex")
        p.xlim(min(degree_)-1,max(degree_)+1)
        p.savefig("tempolau/ev%ipr%icc.png" % (countev,countpr))
        p.clf()
        ###############
        # se foi feito com a matriz certinha (i,j)
        #m=md[-1][-1][:-1].t # tudo menos a classe

        ## tratamento, z-score
        #m[:,0]=(m[:,0]-m[:,0].mean())/m[:,0].std()

        #c_m=n.cov(m) # matriz de covariancia
        #eig_values, eig_vectors = n.linalg.eig(c_m)

        ## ordering eigenvalues and eigenvectors
        #args=n.argsort(eig_values)[::-1]
        #eig_values=eig_values[args]
        #eig_vectors=eig_vectors[:,args]

        ## retaining only a selected number of eigenvectors
        #feature_vec=eig_vectors[:,:2]

        #final_data=n.dot(feature_vec.t,m.t)

        ###############
        # se foi feito com a matriz invertida (j,i)
        #m=md[-1][-1][:-1] # tudo menos a classe
        #m=md[-1][-1][:-1] # tudo menos a classe
        m=md[-1][-1][:-7] # tudo menos a classe e medidas de sum

        # tratamento, z-score
        for i in xrange(m.shape[0]):
            m[i]=(m[i]-m[i].mean())/m[i].std()

        c_m=n.cov(m) # matriz de covariancia
        if not n.isnan(c_m).sum():
            eig_values, eig_vectors = n.linalg.eig(c_m)

            # ordering eigenvalues and eigenvectors
            args=n.argsort(eig_values)[::-1]
            eig_values=eig_values[args]
            eig_vectors=eig_vectors[:,args]

            # retaining only a selected number of eigenvectors
            feature_vec=eig_vectors[:,:2]
            #print(eig_vectors[:,3])

            final_data=n.dot(m.t,feature_vec)
            xx=final_data[:,0]
            yy=final_data[:,1]
            print feature_vec[:,:4]
            feature_vecs.append(eig_vectors[:,:3])
            eigs.append(eig_values)
            p.plot(xx[:len(per)],yy[:len(per)],"bo", ms=3.9,label="peripheral")
            p.plot(xx[len(per):len(per)+len(inter)],yy[len(per):len(per)+len(inter)],"go", ms=3.9,label="intermediary")
            p.plot(xx[-len(hubs):],yy[-len(hubs):],"ro", ms=3.9,label="hubs")
            foo=feature_vec[:,0]
            foo_=("%.2f, "*len(foo)) % tuple(foo)
            #p.xlabel(foo_, fontsize=10)
            p.xlabel("pc1", fontsize=10)
            foo=feature_vec[:,1]
            foo_=("%.2f, "*len(foo)) % tuple(foo)
            #p.ylabel(foo_, fontsize=10)
            p.ylabel("pc2", fontsize=10)
            foo=(eig_values[:4]/eig_values.sum())*100
            foo_=r"$\lambda = $"+("%.3f, "*len(foo) % tuple(foo))
            #p.title(foo_)
            p.title("vertex position in principal components (pca)")

            p.legend(loc="upper right")
            p.ylim(min(yy)-1,max(yy)+1)
            p.xlim(min(xx)-1,max(xx)+1)
            p.savefig("tempolau/ev%ipr%ipca.png" % (countev,countpr))
            p.clf()
        else:
            print("degenerou-se")
        countpr+=1
        print(countpr,countev,e.janela)
    countev+=1

fv=n.real(feature_vecs)
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
#in [169]: fv[:,:,0].mean(0)
#out[169]: 
#array([ 11.51575004,  11.45344434,  10.67880313,  11.37672484,
#        11.33302886,  10.74652016,   0.90582107,  10.87527092,
#         3.9887245 ,   4.15070248,   1.21117739,   5.7845798 ,
#         0.79451924,   5.18493323])
# para ler media e desvioa
# normalizandos os eigs e fv.
# eigs deve estar como percentagem

# cada vetor de fv deve ter composicao em percentagem



       
    # pca

# md[-1][-1][:,-1] eh um individuo
# md[-1][-1][:,-1][-1] == 2 eh hub
# md[-1][-1][:,-1][-1] == 1 eh intermediario 
# md[-1][-1][:,-1][-1] == 0 eh periferico
# md[-1][-1][:,-1][0] eh o grau do vértice

sys.exit()
#medidas_mensagens=mm=medidasmensagens( mensagens, 0,200 )
#rede=rede( mensagens, 0, 501 )
#mr=medidasrede( rede )
#pr=particionarede( mr )
#
d=5000 # tamanho da janela em mensagens (d=0 => g crescente; d<0 movimento começa do final da rede)
passo=500 # mensagens adiantadas em cada passo
# iniciando loop de observacao:

class l:
    n=[]
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
ate_=ate-d
contador=0
for pos in xrange(de,ate_,passo):
    print("criando rede"); t=time.time()
    rede=rede(mensagens, pos, pos+d)
    print("rede criada: ", t-time.time()); t= time.time()
    #mr=medidasrede( rede )
    #print("medidas obtidas da rede: ", t-time.time()); t= time.time()
    pr=particionarede( rede )
    print("rede particionada: ", t-time.time()); t= time.time()
    l.dist.append(pr.dist)
    l.dist_f.append(pr.dist_f)
    l.dist_i.append(pr.dist_i)
    l.dist_o.append(pr.dist_o)
    l.dist_fi.append(pr.dist_fi)
    l.dist_fo.append(pr.dist_fo)
    l.dist_exc.append(pr.c.dist_exc)
    l.dist_inc.append(pr.c.dist_inc)
    l.dist_cas_exc.append(pr.c.dist_cas_exc)
    l.dist_cas_inc.append(pr.c.dist_cas_inc)
    l.dist_ext_exc.append(pr.c.dist_ext_exc)
    l.dist_ext_inc.append(pr.c.dist_ext_inc)
    l.quebras.append(pr.quebras)
    l.n.append(pr.g.number_of_nodes())
    print(u"registradas as distribuições: ", t-time.time()); t= time.time()
    contador+=1
    print(contador)

l.s_exc=[]
l.s_inc=[]
for i in xrange(contador):
    l.s_exc.append(sum(l.dist_exc[i]))
    l.s_inc.append(sum(l.dist_inc[i]))

    

arq="%i.txt"%(d,)
f=open(arq,"wb")

#f.write)
f.close()

p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist]
intermediarios=[d[1]/sum(d) for d in l.dist]
hubs=[d[2]/sum(d) for d in           l.dist]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering degree")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_f]
intermediarios=[d[1]/sum(d) for d in l.dist_f]
hubs=[d[2]/sum(d) for d in           l.dist_f]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering strength")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes.png")

p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist_i]
intermediarios=[d[1]/sum(d) for d in l.dist_i]
hubs=[d[2]/sum(d) for d in           l.dist_i]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering in-degree")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_o]
intermediarios=[d[1]/sum(d) for d in l.dist_o]
hubs=[d[2]/sum(d) for d in           l.dist_o]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering out-degree")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_io.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist_fi]
intermediarios=[d[1]/sum(d) for d in l.dist_fi]
hubs=[d[2]/sum(d) for d in           l.dist_fi]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering in-strengh")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_fo]
intermediarios=[d[1]/sum(d) for d in l.dist_fo]
hubs=[d[2]/sum(d) for d in           l.dist_fo]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering out-strengh")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_fio.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist_exc]
intermediarios=[d[1]/sum(d) for d in l.dist_exc]
hubs=[d[2]/sum(d) for d in           l.dist_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification unanimous in all measures")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_inc]
intermediarios=[d[1]/sum(d) for d in l.dist_inc]
hubs=[d[2]/sum(d) for d in           l.dist_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification considering incidences in any measure")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_c_incexc.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist_cas_exc]
intermediarios=[d[1]/sum(d) for d in l.dist_cas_exc]
hubs=[d[2]/sum(d) for d in           l.dist_cas_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification unanimous cascade frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_cas_inc]
intermediarios=[d[1]/sum(d) for d in l.dist_cas_inc]
hubs=[d[2]/sum(d) for d in           l.dist_cas_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification inclusive frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_c_cas_incexc.png")


p.clf()
p.subplot(211)
perifericos=[d[0]/sum(d) for d in    l.dist_ext_exc]
intermediarios=[d[1]/sum(d) for d in l.dist_ext_exc]
hubs=[d[2]/sum(d) for d in           l.dist_ext_exc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification unanimous cascade frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)


p.subplot(212)
perifericos=[d[0]/sum(d) for d in    l.dist_ext_inc]
intermediarios=[d[1]/sum(d) for d in l.dist_ext_inc]
hubs=[d[2]/sum(d) for d in           l.dist_ext_inc]
p.plot(perifericos, "b"); p.plot(perifericos, "b")
p.plot(intermediarios, "g"); p.plot(intermediarios, "g")
p.plot(hubs, "r"); p.plot(hubs, "r")
p.title("classification inclusive frm hub to brder")
p.xlabel(r"messages $\rightarrow$")
p.ylabel(r"fraction of each network section $\rightarrow$")
p.xlim(-5,len(perifericos)+5)
p.ylim(0,1)

p.savefig("partes_c_ext_incexc.png")


