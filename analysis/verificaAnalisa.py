#-#- coding: utf8 -*-
from __future__ import division
from dateutil import parser
import mailbox, pytz
utc=pytz.UTC

figs=1
#figs=False
if figs:
    import pylab as p
caminho="/home/rfabbri/repos/FIM/python/cppStdLib/"
mm={} # dicionário com infos necessárias das msgs
ids=[] # ordem dos ids que apareceram
vz=[] # msgs vazias, para verificação
aa={} # dicionario com autores como chaves, valores sao msgs
for i in xrange(1,20001):
    mbox = mailbox.mbox(caminho+str(i))
    if mbox.keys(): # se msg nao vazia
        m=mbox[0]
        au=m['from']
        au=au.replace('"','')
        au=au.split("<")[-1][:-1]
        if au not in aa:
            aa[au]=[]
        date=m['date']
        if 'added' in date: date = date.split(" (")[0]
        if m['references']:
            id_ant=m['references'].split('\t')[-1]
            id_ant=id_ant.split(' ')[-1]
        else:
            id_ant=None

        mm[m["message-id"]]=(au,id_ant,date)
        aa[au].append( (m["message-id"], id_ant, date)  )
        ids.append(m['message-id'])
    else:
        vz.append(i)

#### testes:
# deve haver 20k msgs
len(mm)


#### medidas:
# quantas msgs nao sao resposta a outras?
reps=[]
for i in ids: reps.append(mm[i][1])
prop_msgs_novas=sum([r==None for r in reps])/len(reps)

# a data em uma id deve sempre (?) ser anterios aa das proximas ids
dates=[]
for i in ids:
    date=parser.parse(mm[i][-1])
    try: # colocando localizador em que não tem, para poder comparar
        date=utc.localize(date)
    except:
        pass
    dates.append(date)

dd=[]
for i in xrange(len(dates)-1): dd.append(dates[i]<dates[i+1])
# fracao de casos em que msgs atrasam e chegam depois
# de outras posteriores
frac_delay=sum([1-d for d in dd])/len(mm)

# qual a incidencia das msgs em dias da semana?
wd=[d.weekday() for d in dates]
frac_wd=[]
for i in xrange(7): # cada dia da semana, comeca na segunda 0
    frac_wd.append(sum([d==i for d in wd])/len(wd))

# sao enviadas mais msgs de manha (0-11h) ou de noite(12-23h)?
hr=[d.hour for d in dates]
frac_manha=sum([h<12 for h in hr])/len(hr)

# qual a distribuicao de msgs a cada 6h?
frac_6h=[sum([h<6 for h in hr])/len(hr), sum([h>=6 and h<12 for h in hr])/len(hr), sum([h>=12 and h<18 for h in hr])/len(hr), sum([h>=18 for h in hr])/len(hr)]

# qual a distribuicao nas horas do dia?
frac_h=[]
for i in xrange(24):
    frac_h.append(sum([h==i for h in hr])/len(hr))

# proporção entre hora mais intensa e mais amena:
max(frac_h)/min(frac_h)

# qual a distribuicao nos minutos das horas?
mi=[d.minute for d in dates]
frac_mi=[]
for i in xrange(60):
    frac_mi.append(sum([mii==i for mii in mi])/len(mi))

# proporcao entre o minuto mais e menos intenso
max(frac_mi)/min(frac_mi)

# qual a distribuicao nos segundos dos minutos?
se=[d.second for d in dates]
frac_s=[]
for i in xrange(60):
    frac_s.append(sum([s==i for s in se])/len(se))

# qual a distribuicao nos dias do mes?
dias=[d.day for d in dates]
frac_dias=[]
for i in xrange(1,32):
    frac_dias.append(sum([d==i for d in dias])/len(dias))

# considerados somente dias ateh 29:
ff=frac_dias[:-2]

# qual a distribuicao nos meses do ano?
mes=[d.month for d in dates]
frac_mes=[]
for i in xrange(1,13):
    frac_mes.append(sum([m==i for m in mes])/len(mes))

# duração total considerada
dur=dates[-1]-dates[0]
dur.days # número de dias
dur.seconds # segundos que sobraram depois dos dias
dur.total_seconds # segundos total do período

# média de mensagens por dia:
len(mm)/dur.days

# quantas msgs/dia em cada ano
anos=[d.year for d in dates]
msgs_dia=[]
for i in xrange(2002,2010):
    msgs_dia.append(sum([a==i for a in anos])/365.25)
print("anos 2002 a 2009 " + str(msgs_dia))


########################
### dispersão de horário de envio de mensagens:
# rever processos estocáticos algum dia!!!
import numpy as n 

# conversão para segundos
ds=[]
ds_=[]
for d in dates:
    ds.append((d.hour*60+d.minute)*60+d.second)
#    if d.hour>=12:
#        h=24-d.hour-1
#        m=60-d.minute-1
#        s=60-d.second-1
#        ds_.append((h*60+d.minute)*60+s)
#    else:
#        ds_.append(ds[-1])

mu_s=n.mean(ds)
maximo=60*12
quadrados=[]
for d in ds:
    if abs(d-mu_s)>maximo:
        quadrados.append((abs(d-mu_s)-maximo)**2)
    else:
        quadrados.append((d-mu_s)**2)
mq=n.sum(quadrados)/len(quadrados)
sigma_s=n.sqrt(mq)
#sigma_s=n.std(ds_)

#media_horas= int(mu_s/(60*60)) # Out[680]: 14.154651628069825
#
#media_minutos=int((mu_s/(60*60) - media_horas)*60) # Out[683]: 9.2790976841894945
#
#media_segundos=int(((mu_s/(60*60) - media_horas)*60-media_minutos)*60) # Out[684]: 16.745861051369673

#print("horario medio de envio: %ih%im%is"%(media_horas,media_minutos,media_segundos))


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
        date=parser.parse(foo[i][y])
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
mu10=n.mean(dd) # média dos horários das msgs enviadas por enderecos c mais de 10 msgs
sigma10=n.std(dd) # desvio padrao destas msgs

bar_s_m=[] # media em segundos de cada autor para envio de mensagens
for b in bbar_s:
    bar_s_m.append(n.mean(b))
#
#bar_s_m_=[] # media circular 12h p desvio padrao da media
#for b in bar_s_:
#    bar_s_m_.append(n.mean(b))
#
#bar_s_d=[] # desvio padrao do horario de envio de cada mensagem
#for b in bar_s_:
#    bar_s_d.append(n.std(b))
#
#
mu_mu=n.mean(bar_s_m)
#sigma_mu=n.std(bar_s_m_)
#mu_sigma=n.mean(bar_s_d)
#sigma_sigma=n.std(bar_s_d)

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
mu_sigma=n.mean(bb)
sigma_sigma=n.std(bb)

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
sigma_mu=mq**0.5 # aresta do quadrado médio

q=quadrados[:]
q.sort()
# numero de mensagens enviadas por cada endereco por ordem de dispersao
ordem_longe=[len(bbar_s[quadrados.index(i)]) for i in q]
q=[it**.5 for it in q] # arestas
# na lista de c++, é marcante a maior atividade dos enderecos com média temporal perto da média temporal global
# os 2 hubs estao no primeiro quartil (com média temporal mais próxima da geral).
# O ultimo quartil eh claramente o menos movimentado
# a metade do meio parece equivalente em termo dos quartis que possui.

if figs:
    qq=[i/(60*60) for i in q]
    p.subplot(211)
    p.plot(qq,ordem_longe); p.plot(qq,ordem_longe,"ro")
    p.xlabel(u"distância do horário médio do endereço com a média das médias de cada endereço"+r" $\rightarrow$")
    p.ylabel(r"mensagens enviadas $\rightarrow$")
    p.title(u"Número de mensagens enviadas por cada endereço, ordenado segundo média próxima da média global")


    p.subplot(212)
    qq=[n.log(i) for i in qq]
    p.plot(qq,ordem_longe); p.plot(qq,ordem_longe,"ro")
    p.xlabel(u"log( distância do horário médio do endereço com a média das médias de cada endereço )"+r" $\rightarrow$")
    p.ylabel(r"mensagens enviadas $\rightarrow$")
    p.title(u"Número de mensagens enviadas por cada endereço, ordenado segundo média próxima da média global")
    p.show()

# indo observar por dispersão
# desvio padrao por autor:
bb=b_s_d[:]
bb.sort()
ordem_dispersao=[len(bbar_s[b_s_d.index(i)]) for i in bb]
if figs:
    p.subplot(211)
    bb_=[b/(60*60) for b in bb]
    p.plot(bb_,ordem_dispersao); p.plot(bb_,ordem_dispersao, "ro")
    p.xlabel(u"desvio padrão em horas " + r"$\rightarrow$")
    p.ylabel(r"mensagens enviadas $\rightarrow$")
    p.title(u"Mensagens enviadas por autores com desvio padrão crescente")

    p.subplot(212)
    ix=n.argsort(ordem_dispersao)
    nmsgs_cres=n.array(ordem_dispersao)[ix]
    dps=n.array(bb_)[ix]
    p.plot(nmsgs_cres,dps); p.plot(nmsgs_cres,dps,"ro")
    p.xlabel(u"mensagens enviadas " + r"$\rightarrow$")
    p.ylabel(u"desvio padrão em horas"+ r" $\rightarrow$")
    p.title(u"Desvio padrão de acordo com o número de mensagens enviadas")

    p.show()
