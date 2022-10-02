import numpy as np
import argparse
import pulp
from pulp.apis.coin_api import PULP_CBC_CMD
def value_iteration(n,T,R,gamma,nactions,endstates):
    v=np.zeros(n)
    diff=1.0
    while diff > 1e-8:
        v_temp=np.zeros(n)
        for i in range(n):
            res=np.zeros(nactions)
            for a in range(nactions):
                for j in range(n):
                    if i in T and a in T[i] and j in T[i][a]:
                        res[a]+=T[i][a][j]*(R[i][a][j]+gamma*v[j])
            v_temp[i]=np.max(res)
            #v_temp[i]=np.max(np.sum(np.multiply(T[i],R[i]+gamma*v),axis=1))    byebye matrix mult
        diff=np.sqrt(np.sum(np.square(v_temp-v)))
        v=v_temp
    pi=np.zeros(n)
    q=np.zeros(nactions)
    for i in range(n):
        if i in endstates:
            continue
        q=dict()
        for key,val in T[i].items():
            q[key]=0.0
        for a in range(nactions):
            for j in range(n):
                if i in T and a in T[i] and j in T[i][a]:
                    q[a]+=T[i][a][j]*(R[i][a][j]+gamma*v[j])
        pi[i]=max(q,key=q.get)
    return v, pi

def policy_iteration(n,T,R,gamma,nactions,endstates):
    v=np.zeros(n)
    improved=True
    while improved==True:
        v_temp=np.zeros(n)
        improved=False
        for i in range(n):
            q=np.zeros(nactions)
            for a in range(nactions):
                for j in range(n):
                    if i in T and a in T[i] and j in T[i][a]:
                        q[a]+=T[i][a][j]*(R[i][a][j]+gamma*v[j])
            v_temp[i]=np.max(q)
            if v_temp[i]>v[i]:
                improved=True
        if improved==True:
            v=v_temp
    pi=np.zeros(n)
    q=np.zeros(nactions)
    for i in range(n):
        if i in endstates:
            continue
        q=dict()
        for key,val in T[i].items():
            q[key]=0.0
        for a in range(nactions):
            for j in range(n):
                if i in T and a in T[i] and j in T[i][a]:
                    q[a]+=T[i][a][j]*(R[i][a][j]+gamma*v[j])
        pi[i]=max(q,key=q.get)
    return v, pi           

def linear_programming(n,T,R,gamma,nactions,endstates):
    prob=pulp.LpProblem('LinearProg',pulp.LpMaximize)
    variables=[]
    total=""
    for i in range(n):
        var=str('v'+str(i))
        var=pulp.LpVariable(str(var))
        variables.append(var)
        total-=var
    prob+=total

    for i in range(n):
        for a in range(nactions):
            rhs=""
            for j in range(n):
                if i in T and a in T[i] and j in T[i][a]:
                    rhs+=T[i][a][j]*(R[i][a][j]+gamma*variables[j])
            prob+=(variables[i]>=rhs)

    v=np.zeros(n)
    result=prob.solve(PULP_CBC_CMD(msg=0))
    assert result == pulp.LpStatusOptimal
    for i in prob.variables():
        index=int(i.name[1:])
        v[index]=i.varValue
    pi=np.zeros(n)
    q=np.zeros(nactions)
    for i in range(n):
        if i in endstates:
            continue
        q=dict()
        for key,val in T[i].items():
            q[key]=0.0
        for a in range(nactions):
            for j in range(n):
                if i in T and a in T[i] and j in T[i][a]:
                    q[a]+=T[i][a][j]*(R[i][a][j]+gamma*v[j])
        pi[i]=max(q,key=q.get)
    return v, pi


    


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--mdp',type=str,required=True)
    parser.add_argument('--algorithm',type=str,required=False)

    T=dict()
    R=dict()
    endst=[]
    args=parser.parse_args()
    gamma=1.0
    f=open(args.mdp)
    lines=f.readlines()
    for line in lines:
        words=line.split()
        if words[0]=='numStates':
            nstates=int(words[1])
        elif words[0]=='numActions':
            nactions=int(words[1])
        elif words[0]=='transition':
            s1=int(words[1])
            ac=int(words[2])
            s2=int(words[3])
            r=float(words[4])
            p=float(words[5])
            if s1 not in T:
                T[s1]=dict()
            if ac not in T[s1]:
                T[s1][ac]=dict()
            if s1 not in R:
                R[s1]=dict()
            if ac not in R[s1]:
                R[s1][ac]=dict()
            T[s1][ac][s2]=p
            R[s1][ac][s2]=r
        elif words[0]=='discount':
            gamma=float(words[1])
        elif words[0]=='end':
            endst=list(map(int,words[1:]))
    f.close()
    if args.algorithm=='vi':
        v,pi=value_iteration(nstates,T,R,gamma,nactions,endst)
    elif args.algorithm=='hpi':
        v,pi=policy_iteration(nstates,T,R,gamma,nactions,endst)
    elif args.algorithm=='lp':
        v,pi=linear_programming(nstates,T,R,gamma,nactions,endst)
    elif args.algorithm==None:
        v,pi=linear_programming(nstates,T,R,gamma,nactions,endst)
    for i in range(nstates):
        print("{:.6f}".format(v[i]),pi[i])




