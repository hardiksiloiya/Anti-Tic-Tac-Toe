import argparse
import numpy as np

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--value-policy',type=str,required=True)
    parser.add_argument('--states',type=str,required=True)
    parser.add_argument('--player-id',type=int,required=True)

    args=parser.parse_args()
    f=open(args.states,'r')
    states=f.read().rstrip().split('\n')
    f.close()
    f=open(args.value_policy,'r')
    vp=f.read().rstrip().split('\n')
    f.close()

    ind2state=dict()
    i=0

    for s in states:
        ind2state[i]=s
        i+=1
    i=0
    print(args.player_id)
    for line in vp:
        v,pi=float(line.split()[0]),int(float(line.split()[1]))
        moves=list(map(str,[0,0,0,0,0,0,0,0,0]))
        if i not in ind2state:
            continue
        board=ind2state[i]
        moves[pi]="1"
        if board[pi]!='0':
            print("illegal move")
        print(board,' '.join(moves))
     #   print(board,' '.join(moves))
        i+=1

