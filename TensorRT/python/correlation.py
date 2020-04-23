from math import hypot, pi, sqrt, fabs
import numpy as np
import ROOT
import sys
import matplotlib.pyplot as plt
from DataFormats.FWLite import Handle, Events
import pandas as pd
from collections import defaultdict

faci, faciLabel = Handle("edm::SortedCollection<HBHERecHit,edm::StrictWeakOrdering<HBHERecHit> >"), "hltHbherecoclient"
mahi, mahiLabel = Handle("edm::SortedCollection<HBHERecHit,edm::StrictWeakOrdering<HBHERecHit> >"), "hltHbhePhase1Reco"

events = Events("file:test2.root")
faci_e_1 = [] #defaultdict(list)
mahi_e_1 = [] #defaultdict(list)
faci_e_all = [] #defaultdict(list)
mahi_e_all = [] #defaultdict(list)
print ('#events = ',events.size())
for ievent,event in enumerate(events):

   event.getByLabel(faciLabel,faci)
   event.getByLabel(mahiLabel,mahi)

   #print('#faci = ', faci.product().size())
   #print('#mahi = ', mahi.product().size())

   for iM, iF in zip(mahi.product(),faci.product()):
       if iM.id().ieta() != iF.id().ieta(): 
           raise ValueError('Tower failure')
       if iM.id().iphi() != iF.id().iphi():
           raise ValueError('Tower failure')
 
       #if abs(iM.id().ieta()) < 15: continue
       
       if iM.id().depth() == 1: #continue
         faci_e_1.append(iF.energy()*5/12)
         mahi_e_1.append(iM.energy())
       else: #iM.id().depth() == 1: continue
         faci_e_all.append(iF.energy())
         mahi_e_all.append(iM.energy())

import matplotlib.colors as mcolors
h,_,_,_ = plt.hist2d(faci_e_all, mahi_e_all, bins=50,range=[[0,50],[0,50]],norm=mcolors.PowerNorm(0.1))

#plt.scatter(faci_e_1,mahi_e_1,c='black',label='depth=1',marker='o',s=10,alpha=0.5)
#plt.scatter(faci_e_all,mahi_e_all,c='red',label='depth>1',marker='o',s=10,alpha=0.5)

plt.legend(loc='upper right')
plt.xlim([0,50])
plt.ylim([0,50])
plt.xlabel('facile [GeV]')
plt.ylabel('mahi [GeV]')
plt.savefig('test.png')
plt.savefig('test.pdf')
