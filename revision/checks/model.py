"""Minimal vectorised re-implementation of the Sioux Falls model in the notebook.

Used only to verify claims in the paper / draft response letter (see ../REVISION_PLAN.md).
Data are downloaded from bstabler/TransportationNetworks on first use.
"""
import os, urllib.request
_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "data")
os.makedirs(_DATA, exist_ok=True)
for _f in ["SiouxFalls_net.tntp", "SiouxFalls_trips.tntp", "SiouxFalls_node.tntp"]:
    _p = os.path.join(_DATA, _f)
    if not os.path.exists(_p):
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/bstabler/TransportationNetworks/master/SiouxFalls/" + _f, _p)
os.chdir(_DATA)
import numpy as np, re
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
# ---- load
rows=[]
for line in open('SiouxFalls_net.tntp'):
    p=line.strip().split()
    if len(p)>=6 and p[0].isdigit(): rows.append([float(v) for v in p[:6]])
R=np.array(rows); tail=R[:,0].astype(int)-1; head=R[:,1].astype(int)-1; cap=R[:,2]; fft=R[:,4]
A=len(R); N=24
a0=fft; a4=fft*0.15/cap**4
txt=open('SiouxFalls_trips.tntp').read()
Q=np.zeros((N,N))
for blk in re.split(r'Origin\s+',txt)[1:]:
    o=int(blk.split()[0])-1
    for d,v in re.findall(r'(\d+)\s*:\s*([\d.]+)',blk): Q[o,int(d)-1]=float(v)
print('links',A,'demand',Q.sum())
VFF=56.3; L=VFF*a0/60
VOT={'P':10/60,'C':25/60}; OC={'ICE':0.17,'EV':0.085}
def tt(x): return a0+a4*np.maximum(x,0)**4
def speed(x): return np.clip(VFF*a0/np.maximum(tt(x),1e-8),10,90)
def ef(v): return 120+900/v+0.08*(v-50)**2
def Phi(x): return float(np.sum(x*L*ef(speed(x))))
def E(x,s): return (1-s)*Phi(x)
idx={(t,h):i for i,(t,h) in enumerate(zip(tail,head))}
def aon(cost,dem):
    G=csr_matrix((cost,(tail,head)),shape=(N,N))
    dist,pred=dijkstra(G,directed=True,return_predecessors=True)
    y=np.zeros(A)
    for o in range(N):
        for d in range(N):
            q=dem[o,d]
            if q<=0 or o==d: continue
            j=d
            while j!=o:
                i=pred[o,j]; y[idx[(i,j)]]+=q; j=i
    return y,dist
classes=[('P','ICE'),('P','EV'),('C','ICE'),('C','EV')]
def ccost(x,g,k,mu=0.0): 
    c=VOT[g]*tt(x)+L*OC[k]
    if k=='ICE' and mu>0: c=c+mu*L*ef(speed(x))  # pv toll at s=0
    return c
def ue(s,iters=150,tol=1e-4,mu=0.0,x0=None,report=False,true_tol=None):
    dem={c:0.5*Q*((1-s) if c[1]=='ICE' else s) for c in classes}
    xs={c:aon(ccost(np.zeros(A),*c,mu=mu),dem[c])[0] for c in classes} if x0 is None else {c:v.copy() for c,v in x0.items()}
    hist=[]
    for it in range(iters):
        x=sum(xs.values())
        ys={c:aon(ccost(x,*c,mu=mu),dem[c])[0] for c in classes}
        # notebook gap: weighted avg cost on aggregated flows
        cbar=sum(0.5*((1-s) if k=='ICE' else s)*ccost(x,g,k,mu) for g,k in classes)
        nb=float(cbar@(x-sum(ys.values()))/(cbar@x))
        # proper multiclass gap
        num=sum(ccost(x,*c,mu=mu)@(xs[c]-ys[c]) for c in classes); den=sum(ccost(x,*c,mu=mu)@xs[c] for c in classes)
        rg=num/den
        hist.append((it+1,nb,rg))
        stop = (rg<true_tol) if true_tol else (nb<tol)
        if stop: break
        lam=2/(it+2)
        for c in classes: xs[c]=xs[c]+lam*(ys[c]-xs[c])
    return xs,hist
