import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999



def default_Q_value():
    return 0


if __name__ == "__main__":



    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)


    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        state = env.reset()
        done=False
        
        while done==False:
            if random.uniform(0,1) < EPSILON:
                action = env.action_space.sample()
            else:
                prediction = np.array([Q_table[(state,i)] for i in range(env.action_space.n)])
                action =  np.argmax(prediction)

            next_state,reward,done,info = env.step(action)
            episode_reward+=reward
            new_Q = max([Q_table[(next_state,i)] for i in range(env.action_space.n)] )
            
            if done==False:
                sa_next=np.argmax([Q_table[(next_state,i)] for i in range(env.action_space.n)])
                Q_table[(state,action)]=Q_table[(state,action)]+LEARNING_RATE*(reward+DISCOUNT_FACTOR*new_Q-Q_table[(state,action)])
            else:
                episode_reward_record.append(episode_reward)
                Q_table[(state,action)]=Q_table[(state,action)]+LEARNING_RATE*(reward-Q_table[(state,action)])
                
            state = next_state
                
        EPSILON=EPSILON*EPSILON_DECAY   
        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    ####DO NOT MODIFY######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################







