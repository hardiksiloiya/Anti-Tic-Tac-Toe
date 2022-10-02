import numpy as np
import argparse

def is_winning_state(board,player):
  #  print("potential win of ",player)
    if player==1:
        for index1 in [0,3,6]:
            if board[index1]=='2' and board[index1+1]=='2' and board[index1+2]=='2':
                return True
        for index1 in [0,1,2]:
            if board[index1]=='2' and board[index1+3]=='2' and board[index1+6]=='2':
                return True
        if (board[0]=='2' and board[4]=='2' and board[8]=='2') or (board[2]=='2' and board[4]=='2' and board[6]=='2'):
            return True
    elif player==2:
        for index1 in [0,3,6]:
            if board[index1]=='1' and board[index1+1]=='1' and board[index1+2]=='1':
                return True
        for index1 in [0,1,2]:
            if board[index1]=='1' and board[index1+3]=='1' and board[index1+6]=='1':
                return True
        if (board[0]=='1' and board[4]=='1' and board[8]=='1') or (board[2]=='1' and board[4]=='1' and board[6]=='1'):
            return True
    return False

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--policy',type=str,required=True)
    parser.add_argument('--states',type=str,required=True)

    args=parser.parse_args()
    f=open(args.states,'r')
    states=f.read().rstrip().split('\n')
    f.close()
    f=open(args.policy,'r')
    policy=f.read().rstrip().split('\n')
    f.close()

    if policy[0]=="1":
        player=2
        other=1
    elif policy[0]=="2":
        player=1
        other=2

    nstates=len(states)
    state2ind=dict()
    ind2state=dict()
    otherpolicy=dict()
    T=dict()
    R=dict()
    i=0
    for s in states:
        state2ind[s]=i
        ind2state[i]=s
        i+=1
    winstate=i
    losestate=i+1

    for p in policy:
        words=p.split()
        if len(words)!=10:
            continue
        distrib=list(map(float,words[1:]))
        otherpolicy[words[0]]=distrib

    for s in states:
       # print("board found - ",s)
        for i in range(9):
            if(s[i]=='0'):                                      #found a move
                stateaftermove=s[:i]+str(player)+s[i+1:]        # apply the move
                ac=i
                if is_winning_state(stateaftermove,other):                                               #other player won 
                    if state2ind[s] not in T:
                        T[state2ind[s]]=dict()
                        R[state2ind[s]]=dict()
                    if ac not in T[state2ind[s]]:
                        T[state2ind[s]][ac]=dict()
                        R[state2ind[s]][ac]=dict()
                    T[state2ind[s]][ac][losestate]=1.0                      # go to lose state with prob 0 if we make this move and get 0 reward
                    R[state2ind[s]][ac][losestate]=0.0
                else:
                    if state2ind[s] not in T:
                        T[state2ind[s]]=dict()
                        R[state2ind[s]]=dict()
                    if ac not in T[state2ind[s]]:
                        R[state2ind[s]][ac]=dict()
                        T[state2ind[s]][ac]=dict()


                    checkowndraw=True
                    for j in range(9):
                        if stateaftermove[j]=='0':
                            checkowndraw=False
                    if checkowndraw==True:         # draw because of our own move
                        T[state2ind[s]][ac][losestate]=1.0
                        R[state2ind[s]][ac][losestate]=0.0
                        continue

                    pnextstates=otherpolicy[stateaftermove]   
                    for j in range(9):
                        if pnextstates[j]!=0.0:
                            bbb=stateaftermove
                            stateaftermove=stateaftermove[:j]+str(other)+stateaftermove[j+1:]
                            if is_winning_state(stateaftermove,player):                                                      #we won
                                T[state2ind[s]][ac][winstate]=pnextstates[j]                   # go to winstate with prob of other making this move
                                R[state2ind[s]][ac][winstate]=1.0
                            else:
                                if stateaftermove not in state2ind:       # indicates a draw because of other's move
                                    T[state2ind[s]][ac][losestate]=pnextstates[j]
                                    R[state2ind[s]][ac][losestate]=0.0
                                else:
                                    T[state2ind[s]][ac][state2ind[stateaftermove]]=pnextstates[j]
                                    R[state2ind[s]][ac][state2ind[stateaftermove]]=0.0  
                            stateaftermove=bbb  
    
    print("numStates",nstates+2)
    print("numActions",9)            
    print("end",winstate,losestate)
    for i,j in T.items():
        for p,q in j.items():
            for i1,j1 in q.items():
                print("transition",i,p,i1,R[i][p][i1],T[i][p][i1])
                 #   print(otherpolicy[ind2state[i]])

    print("mdtype continuous")       
    print("discount 1.0")
    




