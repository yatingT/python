import numpy as np
import heapq 
import copy

def get_h(state):
    h=0
    x=np.array(state)
    x=x.reshape(3,3)
    goal={1:[0,0],2:[0,1],3:[0,2],
         4:[1,0],5:[1,1],6:[1,2],
         7:[2,0],8:[2,1],0:[2,2]}
    for i in range(1,9):
        if [np.where(x==i)[0],np.where(x==i)[1]] == goal[i]:
            continue
        else:
            h += abs(np.where(x==i)[0]-goal[i][0])+abs(np.where(x==i)[1]-goal[i][1])
    return int(h)

    
def succ(state):
    x=np.array(state)
    x=x.reshape(3,3)
    get_zero=np.where(x==0)
    zero=[get_zero[0][0],get_zero[1][0]]
    succ=[]
    if zero==[0,0]:
        succ.append([[zero[0],zero[1]+1],[zero[0]+1,zero[1]]])
    elif zero==[0,2]:
        succ.append([[zero[0],zero[1]-1],[zero[0]+1,zero[1]]])
    elif zero==[2,0]:
        succ.append([[zero[0]-1,zero[1]],[zero[0],zero[1]+1]])
    elif zero==[2,2]:
        succ.append([[zero[0]-1,zero[1]],[zero[0],zero[1]-1]])
    elif zero==[0,1]:
        succ.append([[zero[0],zero[1]-1],[zero[0],zero[1]+1],[zero[0]+1,zero[1]]])
    elif zero==[1,0]:
        succ.append([[zero[0]-1,zero[1]],[zero[0]+1,zero[1]],[zero[0],zero[1]+1]])
    elif zero==[2,1]:
        succ.append([[zero[0],zero[1]+1],[zero[0],zero[1]-1],[zero[0]-1,zero[1]]])
    elif zero==[1,2]:
        succ.append([[zero[0]+1,zero[1]],[zero[0]-1,zero[1]],[zero[0],zero[1]-1]])
    else:
        succ.append([[zero[0],zero[1]+1], [zero[0],zero[1]-1], 
                    [zero[0]+1,zero[1]], [zero[0]-1,zero[1]]])    
    final=[]
    for i in succ[0]:
        temp=copy.deepcopy(state)
        temp[state.index(0)]=x[i[0]][i[1]]
        temp[state.index(x[i[0]][i[1]])]=0
        final.append(temp)
    s_final=sorted(final)
    return s_final

def print_succ(state):
    s_final=succ(state)
    for i in s_final :
        h=get_h(i)
        print(str(i)+" h="+str(h))

def solve(state):
    path=[]
    parent_index=0
    goal = [1,2,3,4,5,6,7,8,0]
    op = []
    closed = {}
    start_h=get_h(state)
    heapq.heappush(op,(start_h,state,(0,start_h,parent_index)))
    closed={tuple(state):(0, start_h, None)}
    
    while len(op)!=0:
        cur=heapq.heappop(op)
        
        if cur[1]==goal:
            cur_state=cur[1]
            while(cur_state!=state):
                p=closed[tuple(cur_state)][2]
                path.append(cur_state)
                cur_state = p
            path.append(cur_state)
            
            move=0
            while (len(path) != 0):
                p=path.pop(-1)
                print(str(p)+" h="+ str(get_h(p))+" move: "+ str(move))
                move+=1
            return 
                
        parent_index+=1
        children=succ(cur[1])
        for s in children:
            if tuple(s) not in closed:
                g=1+closed[tuple(cur[1])][0]
                h=get_h(s)
                closed[tuple(s)]=(g,h,cur[1])
                heapq.heappush(op,(g+h,s,(g,h,parent_index)))

