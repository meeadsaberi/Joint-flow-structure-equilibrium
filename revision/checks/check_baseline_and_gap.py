from model import *

xs,h=ue(0.0)
x=sum(xs.values())
print('notebook-criterion stop at iter',h[-1][0],'nb_gap %.3e true_gap %.3e'%(h[-1][1],h[-1][2]))
print('min nb gap over run %.3e; any negative nb gap? %s'%(min(r[1] for r in h), any(r[1]<0 for r in h)))
E0=Phi(x); print('E0 = %.0f  (paper 631,774,651)'%E0)
v=speed(x); raw=VFF*a0/tt(x)
print('share of links with speed clipped at 10: %.2f, at 90: %.2f; flow-weighted VKT share on clipped-low links: %.2f'%((raw<10).mean(),(raw>90).mean(), (x*L*(raw<10)).sum()/(x*L).sum()))
print('raw speed quantiles',np.round(np.quantile(raw,[0,.1,.25,.5,.75,1]),1))
print('v/c quantiles',np.round(np.quantile(x/cap,[0,.25,.5,.75,1]),2))

# tighter UE
xs2,h2=ue(0.0,iters=1500,true_tol=1e-5)
x2=sum(xs2.values()); print('tight UE: iters',h2[-1][0],'true gap %.2e'%h2[-1][2],'E0_tight=%.0f, diff vs nb %.3f%%'%(Phi(x2),100*(Phi(x2)-E0)/E0))
np.save('x0t.npy',x2)
