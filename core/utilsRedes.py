#-*- coding: utf8 -*-
from __future__ import division
import numpy as n, pylab as p, networkx as x, random as r, collections as c, string, cPickle as pickle
import mailbox, pytz, os
from dateutil import parser
from datetime import datetime
from scipy import special, misc # special.binom(x,y) ~ binom(x,y)
utc=pytz.UTC
from nltk.corpus import wordnet as wn
import nltk as k
from collections import Counter
import time, __builtin__
import re
replacement_patterns = [
(r'won\'t', 'will not'),
(r'can\'t', 'can not'),
(r'i\'m', 'i am'),
(r'ain\'t', 'is not'),
(r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d', '\g<1> would')
]
class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        count_=0
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
            count_+=count
        return s, count_
REPLACER=RegexpReplacer()
class Mensagens:
    """Always initiante with (from - to) == total -1 messages"""
    def cleanText(self, text):
        t=text.splitlines()
        t=[line for line in t if line]
        t_=[]
        for line in t:
            if line.startswith(">"):
                pass
            elif line.startswith("On Mon"):
                pass
            elif line.startswith("On Tue"):
                pass
            elif line.startswith("On Wed"):
                pass
            elif line.startswith("On Thu"):
                pass
            elif line.startswith("On Fri"):
                pass
            elif line.startswith("On Sat"):
                pass
            elif line.startswith("On Sun"):
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
            elif "----" in line:
                pass
            else:
                t_.append(line)
        return t_




    def __init__(self,caminho="./cpp/", de=0,ate=1001, text="no"):
        self.mm=mm={} # dicionário com infos necessárias das msgs
        self.ids=ids=[] # ordem dos ids que apareceram
        self.vz=vz=[] # msgs vazias, para verificação
        self.aa=aa={} # dicionario com autores como chaves, valores sao msgs
        self.N=len(mm)
        self.ids_r=ids_r={} # dicionario com chaves que sao ids das msgs aas quais sao resposta
        for i in xrange(de,ate): # soh 500 msgs
            mbox = mailbox.mbox(caminho+str(i))
            if mbox.keys(): # se msg nao vazia
                m=mbox[0]
                au=m['from']
                au=au.replace('"','')
                au=au.split("<")[-1][:-1]
                if " " in au: 
                    au=au.split(" ")[0]
                if au not in aa:
                    aa[au]=[]
                date=m['date']
                date=date.replace("METDST","MEST")
                date=date.replace("MET DST","MEST")
                #date=date.replace(" CST"," (CST)")
                date=date.replace("(GMT Standard Time)","")
                date=date.replace(" CDT"," (CDT)")
                date=date.replace(" GMT","")
                date=date.replace("(WET DST)","")
                date=date.replace(" PST (-0800)","")
                date=date.replace("-0600 CST","-0600")
                #print date
                if "GMT-" in date:
                    index=date[::-1].index("-")
                    date=date[:-index-1]+")"
                if 'added' in date: date = date.split(" (")[0]
                if m['references']:
                    id_ant=m['references'].split('\t')[-1]
                    id_ant=id_ant.split(' ')[-1]
                else:
                    id_ant=None
                if id_ant not in ids_r.keys():
                    ids_r[id_ant]=[]

                date=parser.parse(date)
                try: # colocando localizador em que não tem, para poder comparar
                    date=utc.localize(date)
                except:
                    pass

                ids_r[id_ant].append( (au,m["message-id"],date) )
                if text=="yes":
                    t=m.get_payload()
                    #if type(t)==type("astring"):
                    #    pass
                    #else:
                    #    t=t[0].get_payload()
                    #if type(t)==type("astring"):
                    #    pass
                    #else:
                    #    t=t[0].get_payload()
                    while type(t)!=type("astring"):
                        t=t[0].get_payload()
                    #print t
                    t=self.cleanText(t)
                    mm[m["message-id"]]=(au,id_ant,date,t)
                else:
                    mm[m["message-id"]]=(au,id_ant,date)
                aa[au].append( (m["message-id"], id_ant, date)  )
                ids.append(m['message-id'])
            else:
                vz.append(i)


class MensagensPacotes:
    """Para dividir as mensagens em pacotes de autores diferentes"""
    def __init__(self,m=Mensagens(),autores=None):
        self.aa=aa={}
        self.mm=mm={}
        for au in autores:
            aa[au]=m.aa[au]
            m_au=m.aa[au]
            for mens in m_au:
                mm[mens[0]]=m.mm[mens[0]]

        self.ids=ids=[]
        mids=mm.keys()
        for ii in m.ids:
            if ii in mids:
                ids.append(ii)




class MedidasLMensagens:
    if "WL_" in dir(__builtin__):
        WL_=__builtin__.WL_
        stopwords=__builtin__.stopwords
        brill_tagger=__builtin__.brill_tagger
    else:
        try:
            f=open("cpickleDIR/brill_tagger","rb")
            brill_tagger=pickle.load(f)
            __builtin__.brill_tagger=brill_tagger
            f.close()
            print("lido tagger do cpickleDIR")
            w=open("wordsEn.txt","rb")
            ww=w.read()
            WL=ww.split()
            WL.append("email")
            WL.append("e-mail")
            WL_=set(WL)
            stopwords=set(k.corpus.stopwords.words('english'))
        except:
            w=open("wordsEn.txt","rb")
            ww=w.read()
            WL=ww.split()
            WL.append("email")
            WL.append("e-mail")
            WL_=set(WL)
            __builtin__.WL_=WL_
            stopwords=set(k.corpus.stopwords.words('english'))
            __builtin__.stopwords=stopwords

            nn_cd_tagger = k.tag.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),                                       (r'.*', 'NN')])
            tagged_data = k.corpus.treebank.tagged_sents()
            num_sents=3914
            train=0.8
            cutoff = int(num_sents*train)
            training_data = tagged_data[:cutoff]
            gold_data = tagged_data[cutoff:num_sents]
            testing_data = [[t[0] for t in sent] for sent in gold_data]
            print "Done loading."
            unigram_tagger = k.tag.UnigramTagger(training_data,backoff=nn_cd_tagger)
            bigram_tagger = k.tag.BigramTagger(training_data,
                                             backoff=unigram_tagger)
            templates = [
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,1)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (2,2)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,2)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (1,3)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,1)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (2,2)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,2)),
              k.tag.brill.SymmetricProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (1,3)),
              k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateTagsRule, (-1, -1), (1,1)),
              k.tag.brill.ProximateTokensTemplate(k.tag.brill.ProximateWordsRule, (-1, -1), (1,1)),
              ]
            trace=5 
            trainer = k.tag.brill.FastBrillTaggerTrainer(bigram_tagger, templates, trace)
            #trainer = brill.BrillTaggerTrainer(u, templates, trace)
            max_rules=40000
            min_score=2
            brill_tagger = trainer.train(training_data, max_rules, min_score)
            __builtin__.brill_tagger=brill_tagger
            f=open("./cpickleDIR/brill_tagger", 'wb')
            pickle.dump(brill_tagger,f,-1)
            f.close()
        #testing_data = brill_tagger.batch_tag(testing_data)

    def __init__(self,mensagens=Mensagens(), de=50,ate=151, lang="en", autores=None):
        self.m=m=mensagens
        if autores==None:
            self.ids=ids=m.ids[de:ate]
        else:
            self.ids=ids=[mid for mid in m.ids[de:ate] if m.mm[mid][0] in autores]
            

        atime=time.time()
        self.fooBar()
        print atime - time.time()
        atime=time.time()
	if self.T.strip() and (len(set(self.T))>1) and len(self.T) > 20:
            self.medidasLetras()
            #-->print atime - time.time()
            #-->atime=time.time()

            self.medidasTokens()
            print atime - time.time()

            self.medidasTamanhos()

            atime=time.time()
            self.medidasPOS()
            #print atime - time.time()

            #-->atime=time.time()
            self.medidasWordnet()
            print atime - time.time()
            atime=time.time()

    def medidasTamanhos(self):
        # MDok eh marcador para presenca no analsaRedesTexto.py da medie desvio, tanto incidente quanto existencial
        # Hok eh marcador para presenca como histograma
        # palavras conhecidas MDok
        kw=self.kw
        kw_=set(kw)
        self.tkw=tkw=[len(pp) for pp in kw]
        self.tkw_=tkw_=[len(pp) for pp in kw_]
        self.mtkw=mtkw=n.mean(tkw)
        self.dtkw=dtkw= n.std(tkw)
        self.mtkw_=mtkw_=n.mean(tkw_)
        self.dtkw_=dtkw_= n.std(tkw_)
        self.htkw=n.histogram(tkw,bins=range(100),normed=True)
        self.htkw_=n.histogram(tkw_,bins=range(100),normed=True)

        kwnsw=self.kwnsw
        kwnsw_=set(kwnsw)
        self.tkwnsw= tkwnsw =[len(pp) for pp in kwnsw]
        self.tkwnsw_=tkwnsw_=[len(pp) for pp in kwnsw_]
        self.htkwnsw= n.histogram(tkwnsw,bins=range(100),normed=True)
        self.htkwnsw_=n.histogram(tkwnsw_,bins=range(100),normed=True)

        # palavras mais significativas: n são stopwords e retornam synsets
        self.palavras=pv=self.kwssnsw
        pv_=set(pv)
        self.tams=tams=[len(pp) for pp in pv]
        self.tams_=tams_=[len(pp) for pp in pv_]
        self.htams=n.histogram(tams,bins=range(100),normed=True)
        self.htams_=n.histogram(tams_,bins=range(100),normed=True)

        # stopwords
        sw=self.wsw
        sw_=set(sw)
        self.tsw=tsw=[len(pp) for pp in sw]
        self.tsw_=tsw_=[len(pp) for pp in sw_]
        self.htsw=n.histogram(tsw,bins=range(100)  ,normed=True)
        self.htsw_=n.histogram(tsw_,bins=range(100),normed=True)

        # consideradas nao informativas palavras conhecidas, mas stopwords ou sem synset
        sw2=sw+self.kwnssnsw 
        sw2_=set(sw2)
        self.tsw2=tsw2=[len(pp) for pp in sw2]
        self.tsw2_=tsw2_=[len(pp) for pp in sw2_]
        self.htsw2=n.histogram(tsw2,bins=range(100))
        self.htsw2_=n.histogram(tsw2_,bins=range(100))

        ###### medias e desvios
        # das palavras conhecidas
        self.mtkw=n.mean(tkw)
        self.dtkw=n.std(tkw)
        self.mtkw_=n.mean(tkw_)
        self.dtkw_=n.std(tkw_)

        # das palavras que retornam synsets e n são stopwords
        self.mtpv=n.mean(tams)
        self.dtpv=n.std(tams)
        self.mtpv_=n.mean(tams_)
        self.dtpv_=n.std(tams_)

        # das stopwords
        self.mtsw=n.mean(tsw)
        self.dtsw=n.std(tsw)
        self.mtsw_ =n.mean(tsw_)
        self.dtsw_ = n.std(tsw_)

        # das stopwords+conhecidas sem synset
        self.mtsw2=  n.mean(tsw2)
        self.dtsw2=   n.std(tsw2)
        self.mtsw2_ =n.mean(tsw2_)
        self.dtsw2_ = n.std(tsw2_)

        ############
        # medidas de sentencas
        self.TS=TS=k.sent_tokenize(self.T)
        # media e desvio de numero de caracteres por sentenca
        self.tTS=tTS=[len(i) for i in TS]
        self.mtTS=n.mean(tTS)
        self.dtTS=n.std(tTS)
        
        # media e desvio do tamanho das sentencas em tokens
        self.sTS=sTS=[k.tokenize.wordpunct_tokenize(i) for i in TS]
        self.tsTS=tsTS=[len(i) for i in sTS]
        self.mtsTS=n.mean(tsTS)
        self.dtsTS=n.std(tsTS)

        # media e desvio do tamanho das sentencas em palavras conhecidas
        self.tsTSkw=tsTSkw=[len([ii for ii in i if ii in kw_]) for i in sTS]
        self.mtsTSkw=n.mean(tsTSkw)
        self.dtsTSkw=n.std(tsTSkw)
        # media e desvio do tamanho das sentencas em palavras que retornam synsets e nao sao stopwords
        self.tsTSpv=tsTSpv=[len([ii for ii in i if ii in pv_]) for i in sTS]
        self.mtsTSpv=n.mean(tsTSpv)
        self.dtsTSpv=n.std(tsTSpv)

        ########### tamanhos nas mensagens
        ### texto das mensagens:
        self.mT=mT=[string.join(self.m.mm[i][3]) for i in self.ids]

        self.tmT=tmT=[len(t) for t in mT] # chars
        self.ttmT=ttmT=[len(k.tokenize.wordpunct_tokenize(t)) for t in mT] # tok
        self.tsmT=tsmT=[len(k.sent_tokenize(t)) for t in mT] # sents

        self.mtmT=n.mean(tmT)
        self.dtmT=n.std(tmT)
        self.mttmT=n.mean(ttmT)
        self.dttmT=n.std(ttmT)
        self.mtsmT=n.mean(tsmT)
        self.dtsmT=n.std(tsmT)

    def medidasTokens(self):
        atime=time.time()
        T=self.T
        self.wtok=wtok=k.tokenize.wordpunct_tokenize(T)
        self.wtok_=wtok_=[t.lower() for t in wtok]
        #wtok_=["did" if i=="didn" else i for i in wtok_]
        #wtok_=["does" if i=="doesn" else i for i in wtok_]
        #wtok_=["ain" if i=="is" else i for i in wtok_]
        #wtok_=["aren" if i=="are" else i for i in wtok_]
        #wtok_=["aren" if i=="are" else i for i in wtok_]
        # tokens
        self.nt=len(wtok)
        # tokens diferentes
        self.ntd=len(set(wtok))
        # tokens que sao pontuacoes
        print "MT0:", atime-time.time(); atime=time.time()
        self.ntp=ntp=sum([sum([tt in string.punctuation for tt in t])==len(t) for t in wtok])
        print "MT01:", atime-time.time(); atime=time.time()
        # known and unkown words
        self.kw=kw=[]
        self.ukw=ukw=[]
        for t in wtok_:
            if t in self.WL_:
                kw.append(t)
            else:
                ukw.append(t)
        #self.kw=kw=[t for t in wtok if t.lower() in self.WL]
        print "MT02:", atime-time.time(); atime=time.time()
        #self.ukw=[t for t in wtok if not t.lower() in self.WL]
        #self.nkw=nkw=len(kw) # number of known words
        # known words that have synsets
        #print "MT1:", atime-time.time(); atime=time.time()
        self.wss=wss=[i for i in kw if wn.synsets(i)]
        self.wss_=wss_=set(wss)
        # known words that does not have synsets
        self.wnss=wnss=[i for i in kw if i not in wss_]
        print "MT2:", atime-time.time(); atime=time.time()
        wnss_=set(wnss)
        # words that are stopwords
        self.wsw=wsw=[i for i in kw if i in self.stopwords]
        print "MT3:", atime-time.time(); atime=time.time()
        # known words that are not stopwords
        self.kwnsw=kwnsw=[i for i in kw if i not in self.stopwords]
        # unknown words that are stopwords
        self.ukwsw=ukwsw=[i for i in ukw if i in self.stopwords]
        print "MT4:", atime-time.time(); atime=time.time()
        # words that return synsets and are stopwords
        self.wsssw=[i for i in wss if i in self.stopwords]
        print "MT5:", atime-time.time(); atime=time.time()
        # words that dont return synsets and are stopwords
        self.wnsssw=[i for i in wnss if i in self.stopwords]
        print "MT6:", atime-time.time(); atime=time.time()
        # words that are known, are not stopwords and do not return synset
        foo_=wnss_.difference(self.stopwords)
        self.kwnssnsw=[i for i in kw if i in foo_]
        print "MT7:", atime-time.time(); atime=time.time()

        ###
        # For usage:
        # Words that are known, return synsets and are not stopwords
        foo_=wss_.difference(self.stopwords)
        self.kwssnsw=[i for i in kw if i in foo_]
        print "MT8:", atime-time.time(); atime=time.time()

    def medidasLetras(self):
        T=self.T
        # quantos caracteres
        self.nc=nc=len(T)
        # espacos
        self.ne=ne=T.count(" ")
        # letras (e maiusculas)
        self.nl=nl=sum([t.isalpha() for t in T])
        self.nm=nm=sum([t.isupper() for t in T])
        # vogais
        self.nv=nv=sum([t in ("a","e","i","o","u") for t in T])
        # pontuacao
        self.np=np=sum([t in string.punctuation for t in T])
        # numerais
        self.nd=nd=sum([t.isdigit() for t in T])

        self.letrasTudo=nc,ne/nc,nl/(nc-ne),nm/nl,nv/nl,np/(nc-ne),nd/(nc-ne)

    def medidasPOS(self):
        #TS=self.TS
        self.TS=TS=k.sent_tokenize(self.T)
        # em cada sentença, pegando os tags
        # é preciso trocar este pos_tag
        #self.tags=tags=[k.pos_tag(k.tokenize.wordpunct_tokenize(sent)) for sent in TS]
        self.tags=tags=[self.brill_tagger.tag(k.tokenize.wordpunct_tokenize(sent)) for sent in TS]
        self.tags_=tags_=[filter(lambda x: x[0].lower() in self.WL_, i) for i in tags]
        self.tags__=tags__=[map(lambda x: x[1], i) for i in tags_]
        #self.tags_=tags_=[map(lambda x: x[1], i) for i in tags]
        self.tags___=tags___=[item for sublist in tags__ for item in sublist]
        self.htags=htags=Counter(tags___)

        if htags:
       	    factor=1.0/sum(htags.values())
            self.htags_=htags_={}
            for i in htags.keys(): htags_[i]=htags[i]*factor    
            self.htags__=htags__=c.OrderedDict(sorted(htags_.items(), key=lambda x: x[1]))
            # falta plurais, genero e construcoes sintaticas

    def medidasWordnet(self):
        # dentre as palavras conhecidas e que retornam synsets:
        wss=self.wss#=[i for i in kw if wn.synsets(i)]
        self.swss=swss=[wn.synsets(i) for i in wss]
        # numero de synsets por palavra conhecida
        self.lwss=lwss=[len(i) for i in swss]
        self.mlwss=mlwss=n.mean(lwss)
        self.dlwss=dlwss=n.std(lwss)
        #Synsets mais incidentes:
        self.swss_=swss_=[i[0] for i in swss]
        # verbetes cujo synset principal possui mais de um caminho até o hiperonimo raiz
        self.ERROR=ERROR=[i for i in swss_ if len(i.hypernym_paths())==2]
        # dentre estes mais incidentes, medir:
        # incidencias de synsets dentre as hypernimias
        self.sshe=sshe=[i.hypernym_paths()[0] for i in swss_]
        # histograma das incidencias
        self.sshe_=sshe_=[item for sublist in sshe for item in sublist]
        self.hsshe=hsshe=Counter(sshe_)
        # histograma das hypernimias mais genericas
        self.ssheg=ssheg=[i[0] for i in sshe]
        self.hssheg=hssheg=Counter(ssheg)
        # profundidade das especificações dos significados
        self.profundidade=[i.max_depth() for i in swss_]

        # incidência de meronimias e holonimias
        self.mero=[i.member_meronyms() for i in swss_]
        self.holo=[i.member_holonyms() for i in swss_]

    def fooBar(self):
        t=[string.join(self.m.mm[i][3]) for i in self.ids]

        self.T_=T_=string.join(t) # todo o texto, com contracoes
        self.T,self.ncontractions=T,ncontractions=REPLACER.replace(T_) # todo o texto, sem contracoes
        

        # incidencias de pontuacao, etc
        #tk=k.word_tokenize(t)
        #self.css=ok=[i for i in tk if wn.synsets(i)]
        #self.frac1=frac1=len(ok)/len(tk)
        #self.ss=ss=[wn.synsets(i) for i in ok]
        #self.ssl=ssl=[len(i) for i in ss]
        #self.mssl=mssl=n.mean(ssl)
        #self.dssl=dssl=n.std(ssl)

        #self.pt=pt=[i for i in tk if i in string.punctuation]
        #self.frac2=frac2=len(pt)/len(tk)
        #self.areturn=len(t),len(tk),len(pt),frac1,frac2,mssl,dssl


class MedidasMensagens:
    """mensagens is an instance of Mensagens class, defined in this script"""
    def __init__(self,mensagens=Mensagens(), de=50,ate=151):
        # de e ateh dentre os que Mensagens leu
        self.m=m=mensagens
        ids=m.ids[de:ate]
        mm=dict([(k,m.mm[k]) for k in ids])
        au=[mm[i][0] for i in ids]
        au=set(au)
        aa=dict([(a,[]) for a in au])
        for i in ids:
            au=mm[i][0]
            id_ant=mm[i][1]
            date=mm[i][2]
            aa[au].append((i,id_ant,date))

        #mm=[m.mm[i] for i in ids]

        # recuperar rotinas do script verificaAnalisa.py
        self.N=N=len(mm)

        #### medidas:
        # quantas msgs nao sao resposta a outras?
        reps=[]
        for i in ids: reps.append(mm[i][1])
        self.prop_msgs_novas=sum([r==None for r in reps])/len(reps)

        # a data em uma id deve sempre (?) ser anterios aa das proximas ids
        self.dates=dates=[mm[i][2] for i in ids]
        dd=[]
        ###for i in xrange(len(dates)-1): dd.append(dates[i]<dates[i+1]) TTM 
        # fracao de casos em que msgs atrasam e chegam depois
        # de outras posteriores
        #self.frac_delay=sum([1-d for d in dd])/len(mm) TTM removido

        # qual a incidencia das msgs em dias da semana?
        wd=[d.weekday() for d in dates]
        self.frac_wd=[]
        for i in xrange(7): # cada dia da semana, comeca na segunda 0
            self.frac_wd.append(sum([d==i for d in wd])/len(wd))


        # sao enviadas mais msgs de manha (0-11h) ou de noite(12-23h)?
        hr=[d.hour for d in dates]
        self.frac_manha=sum([h<12 for h in hr])/len(hr)

        # qual a distribuicao de msgs a cada 6h?
        self.frac_6h=[sum([h<6 for h in hr])/len(hr), sum([h>=6 and h<12 for h in hr])/len(hr), sum([h>=12 and h<18 for h in hr])/len(hr), sum([h>=18 for h in hr])/len(hr)]

        # qual a distribuicao nas horas do dia?
        self.frac_h=[]
        for i in xrange(24):
            self.frac_h.append(sum([h==i for h in hr])/len(hr))

        ##########
        # qual a distribuicao nos minutos das horas?
        mi=[d.minute for d in dates]
        self.frac_mi=[]
        for i in xrange(60):
            self.frac_mi.append(sum([mii==i for mii in mi])/len(mi))

        # proporcao entre o minuto mais e menos intenso
        #max(frac_mi)/min(frac_mi)

        # qual a distribuicao nos segundos das horas?
        se=[d.second for d in dates]
        self.frac_s=[]
        for i in xrange(60):
            self.frac_s.append(sum([s==i for s in se])/len(se))

        # qual a distribuicao nos dias do mes?
        dias=[d.day for d in dates]
        self.frac_dias=[]
        for i in xrange(1,32):
            self.frac_dias.append(sum([d==i for d in dias])/len(dias))

        # considerados somente dias ateh 29:
        self.frac_dias_=self.frac_dias[:-2]

        # qual a distribuicao nos meses do ano?
        # é preciso considerar o ano fechando 
        # no dia em que começaram os registros
        last_month=dates[0].month
        last_day=dates[0].day
        last_year=dates[-1].year
        if dates[-1].month > dates[0].month:
            pass
        elif dates[-1].month == dates[0].month and abs(dates[-1].day-dates[-1].day) < 10:
            last_day=dates[-1].day
        else:
            last_year -= 1
        last_date=datetime(last_year,last_month,last_day)    
        self.last_date=last_date=utc.localize(last_date)

        i=0
        while dates[i]<last_date:
            i+=1

        mes=[d.month for d in dates[:i]]
        self.frac_mes=[]
        for i in xrange(1,13):
            self.frac_mes.append(sum([m==i for m in mes])/len(mes))

        ################
        # duração total considerada
        self.dur=dur=dates[-1]-dates[0]
        dur.days # número de dias
        dur.seconds # segundos que sobraram depois dos dias
        dur.total_seconds # segundos total do período

        # média de mensagens por dia:
        self.msgs_dia=len(mm)/dur.days

        # quantas msgs/dia em cada ano
        anos=[d.year for d in dates]
        self.msgs_dia_ano=[]
        for i in xrange(2002,2010):
            self.msgs_dia_ano.append(sum([a==i for a in anos])/365.25)

        ############
        # Observando dispersao nos horarios de envio
        # conversão para segundos
        ds=[]
        ds_=[]
        for d in dates:
            ds.append((d.hour*60+d.minute)*60+d.second)

        self.mu_s=mu_s=n.mean(ds)
        maximo=60*12
        quadrados=[]
        for d in ds:
            if abs(d-mu_s)>maximo:
                quadrados.append((abs(d-mu_s)-maximo)**2)
            else:
                quadrados.append((d-mu_s)**2)
        mq=n.sum(quadrados)/len(quadrados)
        self.sigma_s=sigma_s=n.sqrt(mq)

        #################
        ###############
        foo=aa.values()
        bar_d=[]
        bar_s=[]
        bar_s_=[]
        for i in xrange(len(foo)): # para cada autor
            bar_d.append([])
            bar_s.append([])
            bar_s_.append([])
            for y in xrange(len(foo[i])): # para cada mensagem do autor
                foo[i][y]=foo[i][y][2] # foo soh quer a data
                date=foo[i][y]
                try: # colocando localizador em que não tem, para poder comparar
                    date=utc.localize(date)
                except:
                    pass
                bar_d[-1].append(date)
                bar_s[-1].append( (date.hour*60+date.minute)*60+date.second )
                if date.hour>=12:
                    h=24-date.hour-1
                    m=60-date.minute-1
                    s=60-date.second-1
                    bar_s_[-1].append( (h*60+m)*60+s )
                else:
                    bar_s_[-1].append( bar_s[-1][-1] )
        bbar_s = [b for b in bar_s if len(b)>10] # somente quem tem + de 10 msgs enviadas

        dd=[]
        for b in bbar_s: dd+=b
        self.mu10=n.mean(dd) # média dos horários das msgs enviadas por enderecos c mais de 10 msgs
        self.sigma10=n.std(dd) # desvio padrao destas msgs

        bar_s_m=[] # media em segundos de cada autor para envio de mensagens
        for b in bbar_s:
            bar_s_m.append(n.mean(b))

        self.mu_mu=n.mean(bar_s_m)

        # 33333333333   
        b_s_d=[] # desvio padrao circular
        maximo=12*60*60 # maximo de 12h em segundos
        for b in bbar_s: # para cada autor c mais de 10 msgs
            media=n.mean(b)
            quadrados=[]
            for bs in b: # para cada momento de mensagem
                if abs(bs-media)>maximo: # se a distancia passar de 12h
                    quadrado=(abs(bs-media)-maximo)**2
                else:
                    quadrado=(bs-media)**2
                quadrados.append(quadrado)
            mq=sum(quadrados)/len(quadrados) # media das áreas do quadrados
            dp=mq**0.5 # aresta do quadrado médio == desvio padrao
            b_s_d.append(dp)
        bb=[b for b in b_s_d if b] # removendo que tem std == 0
        # medidas estocasticas
        self.mu_sigma=n.mean(bb)
        self.sigma_sigma=n.std(bb)

        # achando o desvio padrao das medias dos autores
        # padrao circular tambem
        media=n.mean(bar_s_m)
        quadrados=[]
        for b in bar_s_m:
            if abs(b-media)> maximo:
                quadrado = (abs(b-media)-maximo)**2
            else:
                quadrado = (b-media)**2
            quadrados.append(quadrado)
        mq=sum(quadrados)/len(quadrados) # média das áreas dos quadrados
        self.sigma_mu=mq**0.5 # aresta do quadrado médio

        q=quadrados[:]
        q.sort()
        # numero de mensagens enviadas por cada endereco por ordem de dispersao
        self.ordem_longe=[len(bbar_s[quadrados.index(i)]) for i in q]
        self.q=[it**.5 for it in q] # arestas

        # indo observar por dispersão
        # desvio padrao por autor:
        bb=b_s_d[:]
        bb.sort()
        ordem_dispersao=[len(bbar_s[b_s_d.index(i)]) for i in bb]
        qq=[i/(60*60) for i in q]
        # ver plots no verificaAnalisa.py

class Rede:
    def __init__(self,mensagens=Mensagens(), de=50, ate=151):
        # de e ateh dentre os que Mensagens leu
        self.m=m=mensagens
        ids=m.ids[de:ate]
        mm=dict([(k,m.mm[k]) for k in ids])
        au=[mm[i][0] for i in ids]
        au=set(au)
        aa=dict([(a,[]) for a in au])
        for i in ids:
            au=mm[i][0]
            id_ant=mm[i][1]
            date=mm[i][2]
            aa[au].append((i,id_ant,date))

        # Criando o Digrafo
        g=x.DiGraph()

        resposta_perdida=[] # para os ids das msgs cuja resposta está perdida
        respondido_antes=[]
        for i in ids:
            m=mm[i]
            if m[0] in g.nodes():
                if "weight" in g.node[m[0]].keys():
                    g.node[m[0]]["weight"]+=1
                else:
                    g.add_node(m[0],weight=1.)
                    respondido_antes.append(i)
            else:
                g.add_node(m[0],weight=1.)
            if m[1]:
                if m[1] in mm.keys():
                    m0=mm[m[1]]

                    if g.has_edge(m0[0],m[0]):
                        g[m0[0]][m[0]]["weight"]+=1
                    else:
                        g.add_edge(m0[0], m[0], weight=1.)
                else:
                    resposta_perdida.append(i)

        self.g=g
        self.resposta_perdida=resposta_perdida
        self.respondido_antes=respondido_antes
        # retirando os selfloops, pois o interesse é na interação
        g_=x.copy.deepcopy(g)
        g_.remove_edges_from(g_.selfloop_edges())
        self.g_=g_

class MedidasRede:
    def __init__(self, rede=Rede()):
        self.g=g=rede.g_
        self.gu=gu=g.to_undirected()
        self.c=x.clustering( gu ,weight="weight")
        self.triangles=x.triangles(gu)
        print("marcador1")

        self.ncc=x.number_connected_components(gu)
        self.nwc=x.number_weakly_connected_components(g)
        self.nsc=x.number_strongly_connected_components(g)

        print("marcador2")
        self.component=c=x.connected_component_subgraphs(gu)[0]
        self.diameter=x.diameter(c)
        self.radius=x.radius(c)
        self.center=x.center(c)
        self.periphery=x.periphery(c)
        if self.ncc>1:
            nodes=[foo.nodes() for foo in x.connected_component_subgraphs(gu)[1:]]
            nodes_=[]
            for node in nodes: nodes_+=node
            self.periphery_=nodes_
        else:
            self.periphery_=[]

        print("marcador3")
        self.bc=x.betweenness_centrality(g,weight="weight")
        self.wi=x.vitality.weiner_index(g,weight="weight")
        self.cv=x.vitality.closeness_vitality(g,weight="weight")
        self.transitivity=x.transitivity(g)
        rc=x.richclub.rich_club_coefficient(gu)
        print("marcador4")
        #self.fh=x.hierarchy.flow_hierarchy(rede.g_,weight="weight")
        self.sl=rede.g.number_of_selfloops()

        self.d=g.degree()

        self.id_=g.in_degree()
        self.od=g.out_degree()

        self.s=     g.degree(weight="weight")
        self.is_= g.in_degree(weight="weight")
        self.os=g.out_degree(weight="weight")
        print("marcador5")

class C:
    """para as classificacoes mais apuradas"""
    pass
    exc=[[],[],[]]
    inc=([],[],[])
    cas_exc=([],[],[])
    cas_inc=([],[],[])
    ext_exc=([],[],[])
    ext_inc=([],[],[])
class ParticionaRede:
    def __init__(self,rede=Rede()):
        self.g=g=rede.g

        N=g.number_of_nodes()
        z=g.number_of_edges()
        print("====+"+ str(N))
        #self.p_=p_=z/(N**2.-N) # probabilidade de presença da aresta
        self.p_=p_=z/(N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*(misc.factorial(N-1))) # probabilidade de presença da aresta

        self.grau_max=grau_max=2*(N-1) # porque os selfloops foram removidos

        # P do artigo, usado para todas as comparações
        self.pg=pg=[] # probabilidade de ocorrência p cada grau.
        graus=range(grau_max+1) # graus entre 0 e o grau máximo

        b=special.binom(grau_max,graus[0])
        prob_g=b*  (p_**graus[0])*((1-p_)**(grau_max-graus[0]))
        pg.append(prob_g)
        for grau in graus[1:]:
            if pg[-1]==0.0:
                pg.append(0.0)
            else:
                b=special.binom(grau_max,grau)
                prob_g=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pg.append(prob_g)

        ###############
        self.ordenacao=ordenacao=c.OrderedDict(sorted(g.degree().items(), key=lambda x: x[1]))
        self.graus_incidentes=graus_incidentes=ordenacao.values()

        self.perifericos=perifericos=[]
        self.intermediarios=intermediarios=[]
        self.hubs=hubs=[]
        self.quebras=quebras=[]
        setor="periferico"
        for grau in graus:
            prob_i=sum([o==grau for o in graus_incidentes])/len(ordenacao)
            if prob_i > 0:
                prob_r=pg[grau]
                incidente_maior=prob_i>=prob_r
                #print("\ngrau: %i; pi: %f; pr: %f; im: %i" % (grau, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA - grau",grau)
                        quebras.append("grau %i" % (grau,))
                        intermediarios+=hubs
                        hubs=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos.append(grau)
                elif setor == "intermediario":
                        intermediarios.append(grau)
                elif setor == "hub":
                    hubs.append(grau)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios)>0:
            self.g1=g1=intermediarios[0] # grau minimo dos intermediarios
            if len(hubs)>0:
                self.g2=g2=hubs[0] # grau minimo dos hubs
            else:
                print(u"DEGENERADO, não há hubs", "grau")
                self.g1=g1=0
                self.g2=g2=grau_max+1
        else:
            print(u"DEGENERADO, não há intermediário", "grau")
            # ajustando de forma que sejam todos intermediários
            self.g1=g1=0 # grau minimo dos intermediarios
            self.g2=g2=grau_max +1# grau minimo dos hubs

# contando os vertices em cada setor
        n_perifericos=sum([gi<g1 for gi in graus_incidentes])
        n_intermediarios=sum([gi<g2 for gi in graus_incidentes])-n_perifericos
        n_hubs=g.number_of_nodes()-(n_perifericos+n_intermediarios)
        self.dist=(n_perifericos,n_intermediarios,n_hubs)



        ############################# 
        # REPETICAO PARA FORCA (IGUAL ROTINA PARA GRAU)
        # Quando observadas as forcas, se distribuída a atividade
        # por igual nas arestas, a distribuição segue a dos graus.

        # enquanto grau_max eh o maximo grau possivel 2*(N-1)
        # a forca maxima é a forca maxima encontrada no grafo:
        self.forca_max=forca_max=int(max(g.degree(weight="weight").values()))
        self.pf=pf=c.OrderedDict() # probabilidade de ocorrência p cada forca.
        forcas=range(forca_max+1) # forcas entre 0 e a força máxima

        # calculando a probabilidade para quem tem forca zero (0)
        b=special.binom(grau_max,   0)
        prob_f=b*  (p_**   0)*((1-p_)**(grau_max-  0))
        pf[0]=prob_f
        self.peso_medio=peso_medio=sum([i[2]["weight"] for i in g.edges(data=True)])/g.number_of_edges()
        for forca in forcas[1:]:
            if pf.values()[-1]==0.0:
                pf[forca]=0.0
            else:
                kappa=grau=forca/peso_medio
                b=special.binom(grau_max,grau)
                prob_f=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pf[forca]=prob_f

        ordenacao_f=c.OrderedDict(sorted(g.degree(weight="weight").items(), key=lambda x: x[1]))
        forcas_incidentes=ordenacao_f.values()
        self.forcas_=forcas_=list(set(forcas_incidentes))
        forcas_.sort()

        self.perifericos_f   =perifericos_f=[]
        self.intermediarios_f=intermediarios_f=[]
        self.hubs_f          =hubs_f=[]
        setor="periferico"
        for forca in forcas_:
            prob_f=sum([o==forca for o in forcas_incidentes])/len(ordenacao_f)
            if prob_f > 0:
                prob_r=pf[forca]
                incidente_maior=prob_f>=prob_r
                #print("\nforca: %i; pf: %f; pr: %f; im: %i" % (forca, prob_f,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca",forca)
                        quebras.append("forca %i" % (forca,))
                        intermediarios_f+=hubs_f
                        hubs_f=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"

                if setor == "periferico":
                    perifericos_f.append(forca)
                elif setor == "intermediario":
                    intermediarios_f.append(forca)
                elif setor == "hub":
                    hubs_f.append(forca)
                else:
                    print("forca nao categorizada")
                #print setor
            else:
                print("probabilidade igual ou menor que zero para forca incidente!!! (ERRO)")

        # 2 forcas de quebra:
        if len(intermediarios_f)>0:
            self.f1=f1=intermediarios_f[0] # grau minimo dos intermediarios
            self.f2=f2=hubs_f[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca")
            # ajustando de forma que sejam todos intermediários
            self.f1=f1=0 # grau minimo dos intermediarios
            self.f2=f2=forca_max +1 # forca minima dos hubs


        # contando os vertices em cada setor
        n_perifericos_f=sum([fi<f1 for fi in forcas_incidentes])
        n_intermediarios_f=sum([fi<f2 for fi in forcas_incidentes])-n_perifericos_f
        n_hubs_f=g.number_of_nodes()-(n_perifericos_f+n_intermediarios_f)
        self.dist_f=dist_f=(n_perifericos_f,n_intermediarios_f,n_hubs_f)




        ##############################################3
        # REPETICAO PARA para GRAU DE ENTRADA
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pgi=pgi=c.OrderedDict() # probabilidade de ocorrência p cada grau.
        graus=range(grau_max*2) # graus entre 0 e o grau máximo

        b=special.binom(grau_max,graus[0])
        prob_gi=b*  (p_**graus[0])*((1-p_)**(grau_max-graus[0]))
        pgi[0]=prob_gi
        for grau in graus[1:]:
            if pgi.values()[-1]==0.0:
                pgi[grau]=0.0
            else:
                b=special.binom(grau_max,grau)
                prob_gi=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pgi[grau]=prob_gi


        self.ordenacao_i=ordenacao_i=c.OrderedDict(sorted(g.in_degree().items(), key=lambda x: x[1]))
        self.grausi_incidentes=grausi_incidentes=ordenacao_i.values()
        
        self.grausi_=grausi_=list(set(grausi_incidentes))
        grausi_.sort()

        self.perifericos_i=perifericos_i=[]
        self.intermediarios_i=intermediarios_i=[]
        self.hubs_i=hubs_i=[]
        setor="periferico"
        for graui in grausi_:
            prob_i=sum([o==graui for o in grausi_incidentes])/len(ordenacao_i)
            if prob_i > 0:
                kappa=2*graui
                prob_r=pgi[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\ngraui: %i; pi: %f; pr: %f; im: %i" % (graui, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA grau de entrada",graui)
                        quebras.append("gi %i" % (graui,))
                        intermediarios_i+=hubs_i
                        hubs_i=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_i.append(graui)
                elif setor == "intermediario":
                    intermediarios_i.append(graui)
                elif setor == "hub":
                    hubs_i.append(graui)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios_i)>0:
            self.gi1=gi1=intermediarios_i[0] # grau minimo dos intermediarios
            self.gi2=gi2=hubs_i[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário", "grau de entrada")
            # ajustando de forma que sejam todos intermediários
            self.gi1=gi1=0 # grau minimo dos intermediarios
            self.gi2=gi2=grau_max+1 # grau minimo dos hubs


        # contando os vertices em cada setor
        n_perifericos_i=sum([gi<gi1 for gi in grausi_incidentes])
        n_intermediarios_i=sum([gi<gi2 for gi in grausi_incidentes])-n_perifericos_i
        n_hubs_i=g.number_of_nodes()-(n_perifericos_i+n_intermediarios_i)
        self.dist_i=dist_i=(n_perifericos_i,n_intermediarios_i,n_hubs_i)

        ##############################################3
        # REPETICAO PARA para GRAU DE SAÍDA 
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pgo=pgo=pgi

        self.ordenacao_o=ordenacao_o=c.OrderedDict(sorted(g.out_degree().items(), key=lambda x: x[1]))
        self.grauso_incidentes=grauso_incidentes=ordenacao_o.values()
        
        self.grauso_=grauso_=list(set(grauso_incidentes))
        grauso_.sort()

        self.perifericos_o=perifericos_o=[]
        self.intermediarios_o=intermediarios_o=[]
        self.hubs_o=hubs_o=[]
        setor="periferico"
        for grauo in grauso_:
            prob_i=sum([o==grauo for o in grauso_incidentes])/len(ordenacao_o)
            if prob_i > 0:
                kappa=2*grauo
                prob_r=pgo[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\ngrauo: %i; pi: %f; pr: %f; im: %i" % (grauo, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA grau de saida",grauo)
                        quebras.append("go %i" % (grauo,))
                        intermediarios_o+=hubs_o
                        hubs_o=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_o.append(grauo)
                elif setor == "intermediario":
                    intermediarios_o.append(grauo)
                elif setor == "hub":
                    hubs_o.append(grauo)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios_o)>0:
            self.go1=go1=intermediarios_o[0] # grau minimo dos intermediarios
            self.go2=go2=hubs_o[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","grau de saida")
            # ajustando de forma que sejam todos intermediários
            self.go1=go1=0 # grau minimo dos intermediarios
            self.go2=go2=grau_max+1 # grau minimo dos hubs

        # contando os vertices em cada setor
        n_perifericos_o=sum([go<go1 for go in grauso_incidentes])
        n_intermediarios_o=sum([go<go2 for go in grauso_incidentes])-n_perifericos_o
        n_hubs_o=g.number_of_nodes()-(n_perifericos_o+n_intermediarios_o)
        self.dist_o=dist_o=(n_perifericos_o,n_intermediarios_o,n_hubs_o)

        ##############################################3
        # REPETICAO PARA para FORÇA DE ENTRADA
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pfi=pfi=pgi

        self.ordenacao_fi=ordenacao_fi=c.OrderedDict(sorted(g.in_degree(weight="weight").items(), key=lambda x: x[1]))
        self.forcasi_incidentes=forcasi_incidentes=ordenacao_fi.values()
        
        self.forcasi_=forcasi_=list(set(forcasi_incidentes))
        forcasi_.sort()

        self.perifericos_fi=perifericos_fi=[]
        self.intermediarios_fi=intermediarios_fi=[]
        self.hubs_fi=hubs_fi=[]
        setor="periferico"
        for forcai in forcasi_:
            prob_i=sum([o==forcai for o in forcasi_incidentes])/len(ordenacao_fi)
            if prob_i > 0:
                kappa=n.round(2*(forcai/peso_medio))
                prob_r=pfi[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\nforcai: %i; pi: %f; pr: %f; im: %i" % (forcai, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca de entrada",forcai)
                        quebras.append("fi %i" % (forcai,))
                        intermediarios_fi+=hubs_fi
                        hubs_fi=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_fi.append(forcai)
                elif setor == "intermediario":
                    intermediarios_fi.append(forcai)
                elif setor == "hub":
                    hubs_fi.append(forcai)
                else:
                    print("forca de entrada nao categorizada")

                #print setor

        # 2 forcas de quebra:
        if len(intermediarios_fi)>0:
            self.fi1=fi1=intermediarios_fi[0] # grau minimo dos intermediarios
            if len(hubs_fi)>0:
                self.fi2=fi2=hubs_fi[0] # grau minimo dos hubs
            else:
    
                print(u"DEGENERADO, há intermediário mas não hub","forca de entrada")
                # ajustando de forma que sejam todos intermediários
                #self.fi1=fi1=0 # grau minimo dos intermediarios
                self.fi2=fi2=forca_max +1 # forca minima dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca de entrada")
            # ajustando de forma que sejam todos intermediários
            self.fi1=fi1=0 # grau minimo dos intermediarios
            self.fi2=fi2=forca_max +1 # forca minima dos hubs


        # contando os vertices em cada setor
        n_perifericos_fi=sum([fi<fi1 for fi in forcasi_incidentes])
        n_intermediarios_fi=sum([fi<fi2 for fi in forcasi_incidentes])-n_perifericos_fi
        n_hubs_fi=g.number_of_nodes()-(n_perifericos_fi+n_intermediarios_fi)
        self.dist_fi=dist_fi=(n_perifericos_fi,n_intermediarios_fi,n_hubs_fi)

        ##############################################3
        # REPETICAO PARA para FORÇA DE SAÍDA 
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pfo=pfo=pgi

        self.ordenacao_fo=ordenacao_fo=c.OrderedDict(sorted(g.out_degree(weight="weight").items(), key=lambda x: x[1]))
        self.forcaso_incidentes=forcaso_incidentes=ordenacao_fo.values()
        
        self.forcaso_=forcaso_=list(set(forcaso_incidentes))
        forcaso_.sort()

        self.perifericos_fo=perifericos_fo=[]
        self.intermediarios_fo=intermediarios_fo=[]
        self.hubs_fo=hubs_fo=[]
        setor="periferico"
        for forcao in forcaso_:
            prob_i=sum([o==forcao for o in forcaso_incidentes])/len(ordenacao_fo)
            if prob_i > 0:
                kappa=n.round(2*(forcao/peso_medio))
                prob_r=pfo[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\nforcao: %i; pi: %f; pr: %f; im: %i" % (forcao, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca de saida",forcao)
                        quebras.append("fo %i" % (forcao,))
                        intermediarios_fo+=hubs_fo
                        hubs_fo=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_fo.append(forcao)
                elif setor == "intermediario":
                    intermediarios_fo.append(forcao)
                elif setor == "hub":
                    hubs_fo.append(forcao)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 forcas de quebra:
        if len(intermediarios_fo)>0:
            self.fo1=fo1=intermediarios_fo[0] # grau minimo dos intermediarios
            self.fo2=fo2=hubs_fo[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca de saida")
            # ajustando de forma que sejam todos intermediários
            self.fo1=fo1=0 # grau minimo dos intermediarios
            self.fo2=fo2=forca_max +1 # forca minima dos hubs

        # contando os vertices em cada setor
        n_perifericos_fo=sum([fo<fo1 for fo in forcaso_incidentes])
        n_intermediarios_fo=sum([fo<fo2 for fo in forcaso_incidentes])-n_perifericos_fo
        n_hubs_fo=g.number_of_nodes()-(n_perifericos_fo+n_intermediarios_fo)
        self.dist_fo=dist_fo=(n_perifericos_fo,n_intermediarios_fo,n_hubs_fo)

        # divisao que contempla todas as medidas:
        # C_exc

        self.C=C()
        C.exc[0]=self.perifericos_=perifericos_=[]
        C.exc[1]=self.intermediarios_=intermediarios_=[]
        C.exc[2]=self.hubs_=hubs_=[]
        nodes=g.nodes()
        for node in nodes:
            grau=g.degree(node)
            gi=g.in_degree(node)
            go=g.out_degree(node)
            f=g.degree(node,weight="weight")
            fi=g.in_degree(node,weight="weight")
            fo=g.out_degree(node,weight="weight")
            # hub só é hub se for hub em todas as medidas:
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                hubs_.append(node)
            # periférico é periférico se for periférico em todas as medidas
            elif grau < g1 and gi < gi1 and go < go1 and f < f1 and fi < fi1 and fo < fo1:
                perifericos_.append(node)
            elif grau < g2 and gi < gi2 and go < go2 and f < f2 and fi < fi2 and fo < fo2   and   grau >= g1 and gi >= gi1 and go >= go1 and f >= f1 and fi >= fi1 and fo >= fo1:
                intermediarios_.append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.inc[2].append(node)
            # periférico é periférico se for periférico em qualquer das medidas
            if grau < g1 or gi < gi1 or go < go1 or f < f1 or fi < fi1 or fo < fo1:
                C.inc[0].append(node)
            # intermediario eh se for em qualquer das medidas
            if ( grau < g2 and  grau >= g1 ) or ( gi < gi2 and gi >= gi1) or (go < go2 and go >= go1) or ( f < f2 and f >= f1) or ( fi < fi2 and fi >= fi1) or ( fo < fo2 and fo >= fo1):
                C.inc[1].append(node)

            # hubs, soh se forem hubs em todas as medidas
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                C.cas_exc[2].append(node)
            # intermediario eh se for intermediario ou hub em todas as medidas
            elif grau >= g1 and gi >= gi1 and go >= go1 and f >= f1 and fi >= fi1 and fo >= fo1:
                C.cas_exc[1].append(node)
            # periférico é periférico se for periférico em todas as medidas
            else: #o resto eh periferico:
                C.cas_exc[0].append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.cas_inc[2].append(node)
            # é intermediario se o for em qualquer das medidas
            elif grau >= g1 or gi >= gi1 or go >= go1 or f >= f1 or fi >= fi1 or fo >= fo1:
                C.cas_inc[1].append(node)
            # sobrou é periférico
            else:
                C.cas_inc[0].append(node)

            # hubs, soh se forem hubs em todas as medidas:
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                C.ext_exc[2].append(node)
            # periférico é periférico se for periférico em todas as medidas:
            elif grau < g1 and gi < gi1 and go < go1 and f < f1 and fi < fi1 and fo < fo1:
                C.ext_exc[0].append(node)
            else: #o resto eh intermediário:
                C.ext_exc[1].append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.ext_inc[2].append(node)
            # é periférico se o for em qualquer das medidas
            elif grau < g1 or gi < gi1 or go < go1 or f < f1 or fi < fi1 or fo < fo1:
                C.ext_inc[0].append(node)
            # sobrou é periférico
            else:
                C.ext_inc[1].append(node)




        C.dist_exc=(len(C.exc[0]),len(C.exc[1]),len(C.exc[2]),)
        C.dist_inc=(len(C.inc[0]),len(C.inc[1]),len(C.inc[2]),)
        C.dist_cas_exc=(len(C.cas_exc[0]),len(C.cas_exc[1]),len(C.cas_exc[2]),)
        C.dist_cas_inc=(len(C.cas_inc[0]),len(C.cas_inc[1]),len(C.cas_inc[2]),)
        C.dist_ext_exc=(len(C.ext_exc[0]),len(C.ext_exc[1]),len(C.ext_exc[2]),)
        C.dist_ext_inc=(len(C.ext_inc[0]),len(C.ext_inc[1]),len(C.ext_inc[2]),)

############################
### Para histograma suavizado

class ParticionaRede2:
    def __init__(self,rede=Rede(), neta=None):

        self.g=g=rede.g

        N=g.number_of_nodes()
        z=g.number_of_edges()
        if neta == None:
           neta=int(2*N/100) # 1% ou menos dos vértices é a resolução
        if neta == 0:
           print("CUIDADO! menos de 100 vertices")
           neta=int(N/50) # 2% ou menos dos vértices é a resolução
        if neta == 0:
           print("CUIDADO! menos de 50 vertices")
           neta=int(N/20) #
        if neta == 0:
           print("CUIDADO! menos de 20 vertices")
           neta=int(N/5) #
        if neta == 0:
           print("CUIDADO! menos de 5 vértices")
           neta=1

        self.neta=neta
        #self.p_=p_=z/(N**2.-N) # probabilidade de presença da aresta
        self.p_=p_=z/(N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*(misc.factorial(N-1))) # probabilidade de presença da aresta
        print("====N: %i, z: %i, neta: %i, p: %f"%(N,z,neta,p_))

        self.grau_max=grau_max=2*(N-1) # porque os selfloops foram removidos

        # P do artigo, usado para todas as comparações
        self.pg=pg=[] # probabilidade de ocorrência p cada grau.
        graus=range(grau_max+1) # graus entre 0 e o grau máximo

        b=special.binom(grau_max,graus[0])
        prob_g=b*  (p_**graus[0])*((1-p_)**(grau_max-graus[0]))
        pg.append(prob_g)
        for grau in graus[1:]:
            if pg[-1]==0.0:
                pg.append(0.0)
            else:
                b=special.binom(grau_max,grau)
                prob_g=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pg.append(prob_g)

        ###############
        self.ordenacao=ordenacao=c.OrderedDict(sorted(g.degree().items(), key=lambda x: x[1]))
        self.graus_incidentes=graus_incidentes=ordenacao.values()

        self.perifericos=perifericos=[]

        self.neta=neta
        #self.p_=p_=z/(N**2.-N) # probabilidade de presença da aresta
        self.p_=p_=z/(N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*N*(N-1)) # probabilidade de presença da aresta
        #self.p_=p_=z/(2*(misc.factorial(N-1))) # probabilidade de presença da aresta
        print("====N: %i, z: %i, neta: %i, p: %f"%(N,z,neta,p_))

        self.grau_max=grau_max=2*(N-1) # porque os selfloops foram removidos

        # P do artigo, usado para todas as comparações
        self.pg=pg=[] # probabilidade de ocorrência p cada grau.
        graus=range(grau_max+1) # graus entre 0 e o grau máximo

        b=special.binom(grau_max,graus[0])
        prob_g=b*  (p_**graus[0])*((1-p_)**(grau_max-graus[0]))
        pg.append(prob_g)
        for grau in graus[1:]:
            if pg[-1]==0.0:
                pg.append(0.0)
            else:
                b=special.binom(grau_max,grau)
                prob_g=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pg.append(prob_g)

        ###############
        self.ordenacao=ordenacao=c.OrderedDict(sorted(g.degree().items(), key=lambda x: x[1]))
        self.graus_incidentes=graus_incidentes=ordenacao.values()

        self.perifericos=perifericos=[]
        self.intermediarios=intermediarios=[]
        self.hubs=hubs=[]
        self.quebras=quebras=[]
        setor="periferico"

        ######### Implementar histograma suavizado
        apontador=0
        mgi=n.array(graus_incidentes)
        self.binsg=binsg=[]
        while apontador+neta < N:
            graus=graus_incidentes[apontador:apontador+neta+1]
            bin0=min(graus)
            bin1=max(graus)
            contagem=((mgi>=bin0)*(mgi<=bin1)).sum()
            prob=contagem/N

            probER=sum(pg[bin0:bin1+1])
            binsg.append((bin0,bin1,prob, probER, prob < probER))
            apontador+=contagem

        if apontador < N:
            graus=graus_incidentes[apontador:]
            bin0=min(graus)
            bin1=max(graus)
            contagem=((mgi>=bin0)*(mgi<=bin1)).sum()
            prob=contagem/N
            probER=sum(pg[bin0:bin1+1])
            binsg.append((bin0,bin1,prob, probER, prob < probER))


        for grau in graus:
            prob_i=sum([o==grau for o in graus_incidentes])/len(ordenacao)
            if prob_i > 0:
                prob_r=pg[grau]
                incidente_maior=prob_i>=prob_r
                #print("\ngrau: %i; pi: %f; pr: %f; im: %i" % (grau, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA - grau",grau)
                        quebras.append("grau %i" % (grau,))
                        intermediarios+=hubs
                        hubs=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos.append(grau)
                elif setor == "intermediario":
                        intermediarios.append(grau)
                elif setor == "hub":
                    hubs.append(grau)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios)>0:
            self.g1=g1=intermediarios[0] # grau minimo dos intermediarios
            if len(hubs)>0:
                self.g2=g2=hubs[0] # grau minimo dos hubs
            else:
                print(u"DEGENERADO, não há hubs", "grau")
                self.g1=g1=0
                self.g2=g2=grau_max+1
        else:
            print(u"DEGENERADO, não há intermediário", "grau")
            # ajustando de forma que sejam todos intermediários
            self.g1=g1=0 # grau minimo dos intermediarios
            self.g2=g2=grau_max +1# grau minimo dos hubs

# contando os vertices em cada setor
        n_perifericos=sum([gi<g1 for gi in graus_incidentes])
        n_intermediarios=sum([gi<g2 for gi in graus_incidentes])-n_perifericos
        n_hubs=g.number_of_nodes()-(n_perifericos+n_intermediarios)
        self.dist=(n_perifericos,n_intermediarios,n_hubs)



        ############################# 
        # REPETICAO PARA FORCA (IGUAL ROTINA PARA GRAU)
        # Quando observadas as forcas, se distribuída a atividade
        # por igual nas arestas, a distribuição segue a dos graus.

        # enquanto grau_max eh o maximo grau possivel 2*(N-1)
        # a forca maxima é a forca maxima encontrada no grafo:
        self.forca_max=forca_max=int(max(g.degree(weight="weight").values()))
        self.pf=pf=c.OrderedDict() # probabilidade de ocorrência p cada forca.
        forcas=range(forca_max+1) # forcas entre 0 e a força máxima


        ####### Histograma suavizado
        self.peso_medio=peso_medio=sum([i[2]["weight"] for i in g.edges(data=True)])/g.number_of_edges()
        self.ordenacaof=ordenacaof=c.OrderedDict(sorted(g.degree(weight="weight").items(), key=lambda x: x[1]))
        self.forcas_incidentes=forcas_incidentes=ordenacaof.values()
        apontador=0
        self.mf=mf=n.array(forcas_incidentes)
        self.binsf=binsf=[]
        while apontador+neta < N:
            aforcas=forcas_incidentes[apontador:apontador+neta]
            bin0=min(aforcas)
            bin1=max(aforcas)
            contagem=((mf>=bin0)*(mf<=bin1)).sum()
            prob=contagem/N

            probER=sum(pg[int(bin0/peso_medio):int(bin1/peso_medio)+1])
            binsf.append((bin0,bin1,prob, probER, prob < probER, contagem, N))
            apontador+=contagem

        if apontador < N:
            aforcas=forcas_incidentes[apontador:]
            bin0=min(aforcas)
            bin1=max(aforcas)
            contagem=((mf>=bin0)*(mf<=bin1)).sum()
            prob=contagem/N

            probER=sum(pg[int(bin0/peso_medio):int(bin1/peso_medio)+1])
            binsf.append((bin0,bin1,prob, probER, prob < probER))

        interf1=[binf[0] for binf in binsf if binf[-3]==True]
        interf2=[binf[1] for binf in binsf if binf[-3]==True]
        f1=min(interf1) # forca minima do intermediario
        f2=max(interf2)+1 # forca minima do hub (por convencao)
        # achando dist_f_ e quem estah em que lugar
        nperifericosf=( mf<f1).sum()
        nhubsf       =(mf>=f2).sum()
        nintermediariosf=N-nperifericosf-nhubsf
        self.distf_=(nperifericosf,nintermediariosf,nhubsf)
        self.hubsf=[key for key in ordenacaof.keys() if ordenacaof[key]>=f2]
        self.perifericosf=[key for key in ordenacaof.keys() if ordenacaof[key]<f1]
        self.intermediariosf=[key for key in ordenacaof.keys() if ordenacaof[key]>=f1 and ordenacaof[key]<f2]
        



        # calculando a probabilidade para quem tem forca zero (0)
        b=special.binom(grau_max,   0)
        prob_f=b*  (p_**   0)*((1-p_)**(grau_max-  0))
        pf[0]=prob_f
        for forca in forcas[1:]:
            print forca
            if pf.values()[-1]==0.0:
                pf[forca]=0.0
            else:
                kappa=grau=forca/peso_medio
                b=special.binom(grau_max,grau)
                prob_f=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pf[forca]=prob_f

        ordenacao_f=c.OrderedDict(sorted(g.degree(weight="weight").items(), key=lambda x: x[1]))
        forcas_incidentes=ordenacao_f.values()
        self.forcas_=forcas_=list(set(forcas_incidentes))
        forcas_.sort()

        self.perifericos_f   =perifericos_f=[]
        self.intermediarios_f=intermediarios_f=[]
        self.hubs_f          =hubs_f=[]
        setor="periferico"
        for forca in forcas_:
            prob_f=sum([o==forca for o in forcas_incidentes])/len(ordenacao_f)
            if prob_f > 0:
                prob_r=pf[forca]
                incidente_maior=prob_f>=prob_r
                #print("\nforca: %i; pf: %f; pr: %f; im: %i" % (forca, prob_f,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca",forca)
                        quebras.append("forca %i" % (forca,))
                        intermediarios_f+=hubs_f
                        hubs_f=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"

                if setor == "periferico":
                    perifericos_f.append(forca)
                elif setor == "intermediario":
                    intermediarios_f.append(forca)
                elif setor == "hub":
                    hubs_f.append(forca)
                else:
                    print("forca nao categorizada")
                #print setor
            else:
                print("probabilidade igual ou menor que zero para forca incidente!!! (ERRO)")

        # 2 forcas de quebra:
        if len(intermediarios_f)>0:
            self.f1=f1=intermediarios_f[0] # grau minimo dos intermediarios
            self.f2=f2=hubs_f[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca")
            # ajustando de forma que sejam todos intermediários
            self.f1=f1=0 # grau minimo dos intermediarios
            self.f2=f2=forca_max+1 # forca minima dos hubs


        # contando os vertices em cada setor
        n_perifericos_f=sum([fi<f1 for fi in forcas_incidentes])
        n_intermediarios_f=sum([fi<f2 for fi in forcas_incidentes])-n_perifericos_f
        n_hubs_f=g.number_of_nodes()-(n_perifericos_f+n_intermediarios_f)
        self.dist_f=dist_f=(n_perifericos_f,n_intermediarios_f,n_hubs_f)




        ##############################################3
        # REPETICAO PARA para GRAU DE ENTRADA
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pgi=pgi=c.OrderedDict() # probabilidade de ocorrência p cada grau.
        graus=range(grau_max*2) # graus entre 0 e o grau máximo

        b=special.binom(grau_max,graus[0])
        prob_gi=b*  (p_**graus[0])*((1-p_)**(grau_max-graus[0]))
        pgi[0]=prob_gi
        for grau in graus[1:]:
            if pgi.values()[-1]==0.0:
                pgi[grau]=0.0
            else:
                b=special.binom(grau_max,grau)
                prob_gi=b*  (p_**grau)*((1-p_)**(grau_max-grau))
                pgi[grau]=prob_gi


        self.ordenacao_i=ordenacao_i=c.OrderedDict(sorted(g.in_degree().items(), key=lambda x: x[1]))
        self.grausi_incidentes=grausi_incidentes=ordenacao_i.values()
        
        self.grausi_=grausi_=list(set(grausi_incidentes))
        grausi_.sort()

        self.perifericos_i=perifericos_i=[]
        self.intermediarios_i=intermediarios_i=[]
        self.hubs_i=hubs_i=[]
        setor="periferico"
        for graui in grausi_:
            prob_i=sum([o==graui for o in grausi_incidentes])/len(ordenacao_i)
            if prob_i > 0:
                kappa=2*graui
                prob_r=pgi[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\ngraui: %i; pi: %f; pr: %f; im: %i" % (graui, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA grau de entrada",graui)
                        quebras.append("gi %i" % (graui,))
                        intermediarios_i+=hubs_i
                        hubs_i=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_i.append(graui)
                elif setor == "intermediario":
                    intermediarios_i.append(graui)
                elif setor == "hub":
                    hubs_i.append(graui)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios_i)>0:
            self.gi1=gi1=intermediarios_i[0] # grau minimo dos intermediarios
            self.gi2=gi2=hubs_i[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário", "grau de entrada")
            # ajustando de forma que sejam todos intermediários
            self.gi1=gi1=0 # grau minimo dos intermediarios
            self.gi2=gi2=grau_max+1 # grau minimo dos hubs


        # contando os vertices em cada setor
        n_perifericos_i=sum([gi<gi1 for gi in grausi_incidentes])
        n_intermediarios_i=sum([gi<gi2 for gi in grausi_incidentes])-n_perifericos_i
        n_hubs_i=g.number_of_nodes()-(n_perifericos_i+n_intermediarios_i)
        self.dist_i=dist_i=(n_perifericos_i,n_intermediarios_i,n_hubs_i)

        ##############################################3
        # REPETICAO PARA para GRAU DE SAÍDA 
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pgo=pgo=pgi

        self.ordenacao_o=ordenacao_o=c.OrderedDict(sorted(g.out_degree().items(), key=lambda x: x[1]))
        self.grauso_incidentes=grauso_incidentes=ordenacao_o.values()
        
        self.grauso_=grauso_=list(set(grauso_incidentes))
        grauso_.sort()

        self.perifericos_o=perifericos_o=[]
        self.intermediarios_o=intermediarios_o=[]
        self.hubs_o=hubs_o=[]
        setor="periferico"
        for grauo in grauso_:
            prob_i=sum([o==grauo for o in grauso_incidentes])/len(ordenacao_o)
            if prob_i > 0:
                kappa=2*grauo
                prob_r=pgo[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\ngrauo: %i; pi: %f; pr: %f; im: %i" % (grauo, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA grau de saida",grauo)
                        quebras.append("go %i" % (grauo,))
                        intermediarios_o+=hubs_o
                        hubs_o=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_o.append(grauo)
                elif setor == "intermediario":
                    intermediarios_o.append(grauo)
                elif setor == "hub":
                    hubs_o.append(grauo)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 graus de quebra:
        if len(intermediarios_o)>0:
            self.go1=go1=intermediarios_o[0] # grau minimo dos intermediarios
            self.go2=go2=hubs_o[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","grau de saida")
            # ajustando de forma que sejam todos intermediários
            self.go1=go1=0 # grau minimo dos intermediarios
            self.go2=go2=grau_max+1 # grau minimo dos hubs

        # contando os vertices em cada setor
        n_perifericos_o=sum([go<go1 for go in grauso_incidentes])
        n_intermediarios_o=sum([go<go2 for go in grauso_incidentes])-n_perifericos_o
        n_hubs_o=g.number_of_nodes()-(n_perifericos_o+n_intermediarios_o)
        self.dist_o=dist_o=(n_perifericos_o,n_intermediarios_o,n_hubs_o)

        ##############################################3
        # REPETICAO PARA para FORÇA DE ENTRADA
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pfi=pfi=pgi

        self.ordenacao_fi=ordenacao_fi=c.OrderedDict(sorted(g.in_degree(weight="weight").items(), key=lambda x: x[1]))
        self.forcasi_incidentes=forcasi_incidentes=ordenacao_fi.values()
        
        self.forcasi_=forcasi_=list(set(forcasi_incidentes))
        forcasi_.sort()

        self.perifericos_fi=perifericos_fi=[]
        self.intermediarios_fi=intermediarios_fi=[]
        self.hubs_fi=hubs_fi=[]
        setor="periferico"
        for forcai in forcasi_:
            prob_i=sum([o==forcai for o in forcasi_incidentes])/len(ordenacao_fi)
            if prob_i > 0:
                kappa=n.round(2*(forcai/peso_medio))
                prob_r=pfi[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\nforcai: %i; pi: %f; pr: %f; im: %i" % (forcai, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca de entrada",forcai)
                        quebras.append("fi %i" % (forcai,))
                        intermediarios_fi+=hubs_fi
                        hubs_fi=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_fi.append(forcai)
                elif setor == "intermediario":
                    intermediarios_fi.append(forcai)
                elif setor == "hub":
                    hubs_fi.append(forcai)
                else:
                    print("forca de entrada nao categorizada")

                #print setor

        # 2 forcas de quebra:
        if len(intermediarios_fi)>0:
            self.fi1=fi1=intermediarios_fi[0] # grau minimo dos intermediarios
            self.fi2=fi2=hubs_fi[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca de entrada")
            # ajustando de forma que sejam todos intermediários
            self.fi1=fi1=0 # grau minimo dos intermediarios
            self.fi2=fi2=forca_max +1 # forca minima dos hubs


        # contando os vertices em cada setor
        n_perifericos_fi=sum([fi<fi1 for fi in forcasi_incidentes])
        n_intermediarios_fi=sum([fi<fi2 for fi in forcasi_incidentes])-n_perifericos_fi
        n_hubs_fi=g.number_of_nodes()-(n_perifericos_fi+n_intermediarios_fi)
        self.dist_fi=dist_fi=(n_perifericos_fi,n_intermediarios_fi,n_hubs_fi)

        ##############################################3
        # REPETICAO PARA para FORÇA DE SAÍDA 
        # grau_max se mantem, pois 2*k_in eh usado para comparacao
        # k_in maximo é N-1 e grau_max=2*(N-1)

        self.pfo=pfo=pgi

        self.ordenacao_fo=ordenacao_fo=c.OrderedDict(sorted(g.out_degree(weight="weight").items(), key=lambda x: x[1]))
        self.forcaso_incidentes=forcaso_incidentes=ordenacao_fo.values()
        
        self.forcaso_=forcaso_=list(set(forcaso_incidentes))
        forcaso_.sort()

        self.perifericos_fo=perifericos_fo=[]
        self.intermediarios_fo=intermediarios_fo=[]
        self.hubs_fo=hubs_fo=[]
        setor="periferico"
        for forcao in forcaso_:
            prob_i=sum([o==forcao for o in forcaso_incidentes])/len(ordenacao_fo)
            if prob_i > 0:
                kappa=n.round(2*(forcao/peso_medio))
                prob_r=pfo[kappa]
                incidente_maior=prob_i>=prob_r
                #print("\nforcao: %i; pi: %f; pr: %f; im: %i" % (forcao, prob_i,prob_r,incidente_maior))
                if incidente_maior:
                    if setor in ("periferico", "hub"):
                        pass
                    else:
                        setor = "hub"
                else:
                    if setor == "hub":
                        print("QUEBRA DA ESTRUTURA forca de saida",forcao)
                        quebras.append("fo %i" % (forcao,))
                        intermediarios_fo+=hubs_fo
                        hubs_fo=[]
                    if setor == "intermediario":
                        pass
                    else:
                        setor = "intermediario"
                if setor == "periferico":
                    perifericos_fo.append(forcao)
                elif setor == "intermediario":
                    intermediarios_fo.append(forcao)
                elif setor == "hub":
                    hubs_fo.append(forcao)
                else:
                    print("grau nao categorizado")

                #print setor

        # 2 forcas de quebra:
        if len(intermediarios_fo)>0:
            self.fo1=fo1=intermediarios_fo[0] # grau minimo dos intermediarios
            self.fo2=fo2=hubs_fo[0] # grau minimo dos hubs
        else:
            print(u"DEGENERADO, não há intermediário","forca de saida")
            # ajustando de forma que sejam todos intermediários
            self.fo1=fo1=0 # grau minimo dos intermediarios
            self.fo2=fo2=forca_max +1 # forca minima dos hubs

        # contando os vertices em cada setor
        n_perifericos_fo=sum([fo<fo1 for fo in forcaso_incidentes])
        n_intermediarios_fo=sum([fo<fo2 for fo in forcaso_incidentes])-n_perifericos_fo
        n_hubs_fo=g.number_of_nodes()-(n_perifericos_fo+n_intermediarios_fo)
        self.dist_fo=dist_fo=(n_perifericos_fo,n_intermediarios_fo,n_hubs_fo)

        # divisao que contempla todas as medidas:
        # C_exc

        self.C=C()
        C.exc[0]=self.perifericos_=perifericos_=[]
        C.exc[1]=self.intermediarios_=intermediarios_=[]
        C.exc[2]=self.hubs_=hubs_=[]
        nodes=g.nodes()
        for node in nodes:
            grau=g.degree(node)
            gi=g.in_degree(node)
            go=g.out_degree(node)
            f=g.degree(node,weight="weight")
            fi=g.in_degree(node,weight="weight")
            fo=g.out_degree(node,weight="weight")
            # hub só é hub se for hub em todas as medidas:
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                hubs_.append(node)
            # periférico é periférico se for periférico em todas as medidas
            elif grau < g1 and gi < gi1 and go < go1 and f < f1 and fi < fi1 and fo < fo1:
                perifericos_.append(node)
            elif grau < g2 and gi < gi2 and go < go2 and f < f2 and fi < fi2 and fo < fo2   and   grau >= g1 and gi >= gi1 and go >= go1 and f >= f1 and fi >= fi1 and fo >= fo1:
                intermediarios_.append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.inc[2].append(node)
            # periférico é periférico se for periférico em qualquer das medidas
            if grau < g1 or gi < gi1 or go < go1 or f < f1 or fi < fi1 or fo < fo1:
                C.inc[0].append(node)
            # intermediario eh se for em qualquer das medidas
            if ( grau < g2 and  grau >= g1 ) or ( gi < gi2 and gi >= gi1) or (go < go2 and go >= go1) or ( f < f2 and f >= f1) or ( fi < fi2 and fi >= fi1) or ( fo < fo2 and fo >= fo1):
                C.inc[1].append(node)

            # hubs, soh se forem hubs em todas as medidas
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                C.cas_exc[2].append(node)
            # intermediario eh se for intermediario ou hub em todas as medidas
            elif grau >= g1 and gi >= gi1 and go >= go1 and f >= f1 and fi >= fi1 and fo >= fo1:
                C.cas_exc[1].append(node)
            # periférico é periférico se for periférico em todas as medidas
            else: #o resto eh periferico:
                C.cas_exc[0].append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.cas_inc[2].append(node)
            # é intermediario se o for em qualquer das medidas
            elif grau >= g1 or gi >= gi1 or go >= go1 or f >= f1 or fi >= fi1 or fo >= fo1:
                C.cas_inc[1].append(node)
            # sobrou é periférico
            else:
                C.cas_inc[0].append(node)

            # hubs, soh se forem hubs em todas as medidas:
            if grau >= g2 and gi >= gi2 and go >= go2 and f >= f2 and fi >= fi2 and fo >= fo2:
                C.ext_exc[2].append(node)
            # periférico é periférico se for periférico em todas as medidas:
            elif grau < g1 and gi < gi1 and go < go1 and f < f1 and fi < fi1 and fo < fo1:
                C.ext_exc[0].append(node)
            else: #o resto eh intermediário:
                C.ext_exc[1].append(node)

            # hub é se for em qualquer das medidas
            if grau >= g2 or gi >= gi2 or go >= go2 or f >= f2 or fi >= fi2 or fo >= fo2:
                C.ext_inc[2].append(node)
            # é periférico se o for em qualquer das medidas
            elif grau < g1 or gi < gi1 or go < go1 or f < f1 or fi < fi1 or fo < fo1:
                C.ext_inc[0].append(node)
            # sobrou é periférico
            else:
                C.ext_inc[1].append(node)




        C.dist_exc=(len(C.exc[0]),len(C.exc[1]),len(C.exc[2]),)
        C.dist_inc=(len(C.inc[0]),len(C.inc[1]),len(C.inc[2]),)
        C.dist_cas_exc=(len(C.cas_exc[0]),len(C.cas_exc[1]),len(C.cas_exc[2]),)
        C.dist_cas_inc=(len(C.cas_inc[0]),len(C.cas_inc[1]),len(C.cas_inc[2]),)
        C.dist_ext_exc=(len(C.ext_exc[0]),len(C.ext_exc[1]),len(C.ext_exc[2]),)
        C.dist_ext_inc=(len(C.ext_inc[0]),len(C.ext_inc[1]),len(C.ext_inc[2]),)



class EvoluiRede:
    def __init__(self,de,ate,janela,passo,mensagens,label="CPP",mdir="atempo",neta=None):
        self.neta=neta
        #os.system("rm -R %s"%(mdir,))
        #os.system("rm -R %s_"%(mdir,))
        try:
            os.system("mkdir %s"%(mdir,))
        except:
            pass
        try:
            os.system("mkdir %s_"%(mdir,))
        except:
            pass
        self.mdir=mdir
        self.label=label
        self.de=de
        self.ate=ate
        self.janela=janela
        self.passo=passo
        self.mensagens=mensagens
        self.ate_=ate_=ate-janela
        self.gs=gs=[]
        self.redes=redes=[]
        self.prs=prs=self.prs2=prs2=[]
        #self.prs2=prs2=[]
        self.mrs=mrs=[]
        self.sobra=sobra = (ate_)%passo
        for pos in xrange(de,ate_,passo):
            print("pos: %s" % (str(pos),))
            rede=Rede(mensagens, pos, pos+janela)
            pr=ParticionaRede( rede)
            redes.append(rede)
            prs.append(pr)
            #pr2=ParticionaRede2( rede ,neta=neta)
            #prs2.append(pr2)
            #mr=MedidasRede( rede )
            #mrs.append(mr)
            gs.append(pr.g)


    def drawSections2(self):
        p.clf()
        prs2=self.prs2
        p.subplot(521)
        p.title("degree", fontsize=12)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)

        
        p.subplot(522)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)
        p.title("strength", fontsize=12)
 
        p.subplot(523)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.ylabel(r"fraction of section $\rightarrow$")
        p.title("in-degree", fontsize=12)
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)
       
        p.subplot(524)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("in-strengh", fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)

        p.subplot(525)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("out-degree", fontsize=12)
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)

        p.subplot(526)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("out-strengh", fontsize=12)
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)



        p.subplot(527)
        pesos=[sum([i[2]["weight"] for i in pr.g.edges(data=True)]) for pr in prs2]
        p.plot(range(self.de,self.ate_,self.passo),pesos,"r")
        p.title("Total strength", fontsize=12)
        p.ylim(min(pesos)*.99,max(pesos)*1.01)
        p.xlim(-5,self.ate_+5)
        p.suptitle(u"Primary divisions. Window: %i messages. Placement resolution: %i messages. %s" % (self.janela,self.passo,self.label))
        p.ylabel(r"$\sum s_i \;\;\rightarrow$")

        p.subplot(528)
        p.title("Number of edges.", fontsize=12)
        Es=[pr.g.number_of_edges() for pr in prs2]
        p.plot(range(self.de,self.ate_,self.passo),Es,"g")
        p.ylim(min(Es)*.99,max(Es)*1.01)
        p.xlim(-5,self.ate_+5)
        p.ylabel(r"$\mathfrak{z} \rightarrow$",fontsize=20)





        p.subplot(529)
        p.title("Number of vertexes.", fontsize=12)
        Vs=[pr.g.number_of_nodes() for pr in prs2]
        p.plot(range(self.de,self.ate_,self.passo),Vs,"b")
        p.ylim(min(Vs)*.99,max(Vs)*1.01)
        p.xlim(-5,self.ate_+5)
        p.xlabel(r"messages $\rightarrow$")
        p.ylabel(r"N $\rightarrow$")


        p.subplot(5,2,10)
        p.title("Center, periphery and discon.", fontsize=12)

        centers=[]
        peripherys=[]
        peripherys_=[]
        for pr in prs2:
            self.gu=gu=pr.g.to_undirected()
            self.component=c=x.connected_component_subgraphs(gu)[0]
            self.center=x.center(c)
            self.periphery=x.periphery(c)
            self.ncc=x.number_connected_components(gu)
            if self.ncc>1:
                nodes=[foo.nodes() for foo in x.connected_component_subgraphs(gu)[1:]]
                nodes_=[]
                for node in nodes: nodes_+=node
                self.periphery_=nodes_
            else:
                self.periphery_=[]
            centers.append(len(self.center))
            peripherys.append(len(self.periphery))
            peripherys_.append(len(self.periphery_))


        p.plot(range(self.de,self.ate_,self.passo),centers,"r")
        p.plot(range(self.de,self.ate_,self.passo),peripherys,"b")
        p.plot(range(self.de,self.ate_,self.passo),peripherys_,"g")
        p.ylim(-2,max(max(centers),max(peripherys),max(peripherys_))+2)
        p.xlim(-5,self.ate_+5)
        p.xlabel(r"messages $\rightarrow$")
        p.ylabel(r"number of nodes $\rightarrow$")

        #p.show()
        p.subplots_adjust(left=.1, bottom=0.1, right=.95, top=.9, wspace=.3, hspace=.6)
        p.savefig("%s_/%i.eps"%(self.mdir,self.janela,))


        p.clf()

        p.subplot(321)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.plot(range(self.de,self.ate_,self.passo),[sum(pr.C.dist_exc)/pr.g.number_of_nodes() for pr in prs2],"k")
        p.title("Vertex with unanimous classification", fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.suptitle(u"Compound divisions. Window: %i messages. Placement resolution: %i messages. %s" % (self.janela,self.passo,self.label))

        p.subplot(322)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.plot(range(self.de,self.ate_,self.passo),[(sum(pr.C.dist_inc)-pr.g.number_of_nodes())/pr.g.number_of_nodes() for pr in prs2],"k")
        p.title("Vertex with classification",fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)

        p.subplot(323)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("Vertex classified by exclusive cascade",fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.ylabel(r"fraction of section $\rightarrow$")

        p.subplot(324)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("Vertex classified by inclusive cascade",fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)


        p.subplot(325)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("Vertex classified by exclusive externals",fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.xlabel(r"messages $\rightarrow$")

        p.subplot(326)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[0]/pr.g.number_of_nodes() for pr in prs2],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[1]/pr.g.number_of_nodes() for pr in prs2],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[2]/pr.g.number_of_nodes() for pr in prs2],"r")
        p.title("Vertex classified by inclusive externals",fontsize=12)
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.xlabel(r"messages $\rightarrow$")

        #p.tight_layout(pad=1.0, w_pad=0.1, h_pad=.0)
        p.subplots_adjust(left=.1, bottom=None, right=.9, top=.9, wspace=.3, hspace=.4)
        #p.tight_layout(pad=-1.)#, w_pad=0.5, h_pad=1.0)
        #p.show()
        p.savefig("%s_/%i_2.eps"%(self.mdir,self.janela,))






    def drawSections(self):
        prs=self.prs
        p.subplot(521)
        p.title("degree")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)

        
        p.subplot(522)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_f[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)
        p.title("strength")
 
        p.subplot(523)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_i[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.ylabel(r"fraction of section $\rightarrow$")
        p.title("in-degree")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)
       
        p.subplot(524)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fi[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("in-strengh")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)

        p.subplot(525)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_o[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("out-degree")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)

        p.subplot(526)
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.dist_fo[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("out-strengh")
        p.ylim(0,1)
        p.xlim(-5,self.ate_+5)



        p.subplot(527)
        pesos=[sum([i[2]["weight"] for i in pr.g.edges(data=True)]) for pr in prs]
        p.plot(range(self.de,self.ate_,self.passo),pesos,"r")
        p.title("Total strength")
        p.ylim(min(pesos)*.99,max(pesos)*1.01)
        p.xlim(-5,self.ate_+5)
        p.suptitle(u"Primary divisions. Window: %i messages. Placement resolution: %i messages. %s" % (self.janela,self.passo,self.label))
        p.ylabel(r"$\sum s_i \;\;\rightarrow$")

        p.subplot(528)
        p.title("Number of edges.")
        Es=[pr.g.number_of_edges() for pr in prs]
        p.plot(range(self.de,self.ate_,self.passo),Es,"g")
        p.ylim(min(Es)*.99,max(Es)*1.01)
        p.xlim(-5,self.ate_+5)
        p.ylabel(r"$\mathfrak{z} \rightarrow$",fontsize=20)





        p.subplot(529)
        p.title("Number of vertexes.")
        Vs=[pr.g.number_of_nodes() for pr in prs]
        p.plot(range(self.de,self.ate_,self.passo),Vs,"b")
        p.ylim(min(Vs)*.99,max(Vs)*1.01)
        p.xlim(-5,self.ate_+5)
        p.xlabel(r"messages $\rightarrow$")
        p.ylabel(r"N $\rightarrow$")


        p.subplot(5,2,10)
        p.title("Nodes in center, periphery and discon.")

        centers=[]
        peripherys=[]
        peripherys_=[]
        for pr in prs:
            self.gu=gu=pr.g.to_undirected()
            self.component=c=x.connected_component_subgraphs(gu)[0]
            self.center=x.center(c)
            self.periphery=x.periphery(c)
            self.ncc=x.number_connected_components(gu)
            if self.ncc>1:
                nodes=[foo.nodes() for foo in x.connected_component_subgraphs(gu)[1:]]
                nodes_=[]
                for node in nodes: nodes_+=node
                self.periphery_=nodes_
            else:
                self.periphery_=[]
            centers.append(len(self.center))
            peripherys.append(len(self.periphery))
            peripherys_.append(len(self.periphery_))


        p.plot(range(self.de,self.ate_,self.passo),centers,"r")
        p.plot(range(self.de,self.ate_,self.passo),peripherys,"b")
        p.plot(range(self.de,self.ate_,self.passo),peripherys_,"g")
        p.ylim(-2,max(max(centers),max(peripherys),max(peripherys_))+2)
        p.xlim(-5,self.ate_+5)
        p.xlabel(r"messages $\rightarrow$")
        p.ylabel(r"number of nodes $\rightarrow$")

        #p.show()
        p.savefig("%s/%i.eps"%(self.mdir,self.janela,))


        p.clf()

        p.subplot(321)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_exc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.plot(range(self.de,self.ate_,self.passo),[sum(pr.C.dist_exc)/pr.g.number_of_nodes() for pr in prs],"k")
        p.title("Vertex with unanimous classification")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.suptitle(u"Compound divisions. Window: %i messages. Placement resolution: %i messages. %s" % (self.janela,self.passo,self.label))

        p.subplot(322)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_inc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.plot(range(self.de,self.ate_,self.passo),[(sum(pr.C.dist_inc)-pr.g.number_of_nodes())/pr.g.number_of_nodes() for pr in prs],"k")
        p.title("Vertex with classification")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)

        p.subplot(323)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_exc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("Vertex classified by exclusive cascade")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.ylabel(r"fraction of section $\rightarrow$")

        p.subplot(324)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_cas_inc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("Vertex classified by inclusive cascade")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)


        p.subplot(325)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_exc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("Vertex classified by exclusive externals")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.xlabel(r"messages $\rightarrow$")

        p.subplot(326)
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[0]/pr.g.number_of_nodes() for pr in prs],"b")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[1]/pr.g.number_of_nodes() for pr in prs],"g")
        p.plot(range(self.de,self.ate_,self.passo),[pr.C.dist_ext_inc[2]/pr.g.number_of_nodes() for pr in prs],"r")
        p.title("Vertex classified by inclusive externals")
        p.xlim(-5,self.ate_+5)
        p.ylim(0,1)
        p.xlabel(r"messages $\rightarrow$")

        #p.show()
        p.savefig("%s/%i_2.eps"%(self.mdir,self.janela,))



if __name__ == "__main__":
    mensagens=m=Mensagens(de=0,ate=5001)
    medidas_mensagens=mm=MedidasMensagens( mensagens, 0,200 )
    rede=Rede( mensagens, 0, 5001 )
    mr=MedidasRede( rede )
    pr=ParticionaRede( mr )

