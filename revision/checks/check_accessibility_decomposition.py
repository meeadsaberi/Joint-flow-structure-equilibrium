from model import *
xy=[]
for line in open('SiouxFalls_node.tntp'):
    p=line.strip().split()
    if p and p[0].isdigit(): xy.append([float(p[1]),float(p[2])])
xy=np.array(xy); d=np.hypot(*(xy-xy.mean(0)).T)
per=np.where(d>=np.quantile(d,.75))[0]
W=Q.sum(0)
def acc(cost,beta,orig):
    G=csr_matrix((cost,(tail,head)),shape=(N,N)); D=dijkstra(G,directed=True)
    return np.mean([np.sum(W*np.exp(-beta*np.where(np.isfinite(D[o]),D[o],np.inf))) for o in orig])
x0=(np.load('x0t.npy') if os.path.exists('x0t.npy') else sum(ue(0.0,iters=1500,true_tol=1e-5)[0].values()))
base=acc(ccost(x0,'P','ICE'),0.22,per); print('A_P(0)=%.0f'%base)
for mu in [1.36e-4,2.51e-4,1e-3,1e-2]:
    xs,h=ue(0.0,mu=mu,iters=600,true_tol=1e-4,x0=None); x=sum(xs.values())
    full=acc(ccost(x,'P','ICE',mu=mu),0.22,per)
    notoll=acc(ccost(x,'P','ICE'),0.22,per)
    print('mu=%.2e  E/E0=%.4f  A_P tolled=%.0f (%.1f%%)  A_P same flows w/o toll in cost=%.0f (%.1f%%)'%(mu,Phi(x)/Phi(x0),full,100*(full/base-1),notoll,100*(notoll/base-1)))
