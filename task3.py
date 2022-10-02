import numpy as np
import subprocess
import random

def initialise(path):
    f=open(path,'r')
    lines=f.read().rstrip().split('\n')
    f.close()
    f=open("p1_0",'w')
    f.writelines('1\n')
    for l in lines:
        temp=[]
        move=["0","0","0","0","0","0","0","0","0"]
        for i in range(9):
            if l[i]=='0':
                temp.append(i)
        ind=random.choice(temp)
        move[ind]="1"
        temp=l+" "+' '.join(move)+'\n'
        f.writelines(temp)
    f.close()
        
    

if __name__ == "__main__":
    p1path="data/attt/states/states_file_p1.txt"
    p2path="data/attt/states/states_file_p2.txt"
    initialise(p1path)
    print("Initialized Policy of Player 1")
    
    
    for i in range(9):
        # player 1 makes policy
        cmd_encoder = "python","encoder.py","--policy","p1_{}".format(i),"--states",p2path
        f = open('temp_encoder_out','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        cmd_encoder = "python","planner.py","--mdp","temp_encoder_out"
        f = open('temp_planner_out','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        cmd_encoder = "python","decoder.py","--value-policy","temp_planner_out","--states",p2path,"--player-id","2"
        f = open('p2_{}'.format(i+1),'w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        count=0

        if i!=0:
            f1=open("p2_{}".format(i+1),"r")
            f2=open("p2_{}".format(i),"r")
            for l1,l2 in zip(f1,f2):
                if l1!=l2:
                    count+=1
            f1.close()
            f1.close()
            print("For iteration {}, the number of differences in actions for Player 2 is {}".format(i,count))

       

        cmd_encoder = "python","encoder.py","--policy","p2_{}".format(i+1),"--states",p1path
        f = open('temp_encoder_out','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        cmd_encoder = "python","planner.py","--mdp","temp_encoder_out"
        f = open('temp_planner_out','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        cmd_encoder = "python","decoder.py","--value-policy","temp_planner_out","--states",p1path,"--player-id","1"
        f = open('p1_{}'.format(i+1),'w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()
        count=0

        f1=open("p1_{}".format(i+1),"r")
        f2=open("p1_{}".format(i),"r")
        for l1,l2 in zip(f1,f2):
            if l1!=l2:
                count+=1
        f1.close()
        f1.close()
        print("For iteration {}, the number of differences in actions for Player 1 is {}".format(i,count))

        

