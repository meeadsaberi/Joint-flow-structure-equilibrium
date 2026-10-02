from model import *
from scipy.optimize import minimize_scalar
x0=(np.load('x0t.npy') if os.path.exists('x0t.npy') else sum(ue(0.0,iters=1500,true_tol=1e-5)[0].values())); E0=Phi(x0)
def link_em(x): return x*L*ef(speed(x))
def marg(x,h=1e-3):
    return (link_em(x+h)-link_em(np.maximum(x-h,0)))/(x+h-np.maximum(x-h,0))
# check monotonicity of per-link emissions in flow over [0, 3*cap]
nonmono=0
for a in range(A):
    g=np.linspace(0,3*cap[a],400); tg=a0[a]+a4[a]*g**4; vg=np.clip(VFF*a0[a]/tg,10,90); m=np.diff(g*L[a]*ef(vg))
    if (m<0).any(): nonmono+=1
print('links where x*e(x) is non-increasing somewhere on [0,3cap]:',nonmono)
def fw_min(x,iters=400):
    for it in range(iters):
        y,_=aon(marg(x),Q)
        d=y-x
        r=minimize_scalar(lambda t: Phi(x+t*d),bounds=(0,1),method='bounded',options={'xatol':1e-6})
        x=x+r.x*d
    return x
starts={'UE':x0, 'AON_freeflow':aon(L.copy(),Q)[0]}
best=None
for k,xs0 in starts.items():
    xm=fw_min(xs0.copy())
    print(k,'start Phi/E0=%.4f -> min Phi/E0=%.4f'%(Phi(xs0)/E0,Phi(xm)/E0))
    if best is None or Phi(xm)<best: best=Phi(xm)
print('best min Phi/E0 = %.4f  -> s_viab(0.8E0)=%.3f, s_viab(0.57E0)=%.3f'%(best/E0, max(0,1-0.8*E0/best), max(0,1-0.57*E0/best)))
# system-optimal (time) total travel time vs UE, for context
