class game: 

    def __init__(self):
        self.reset_state()
    
    def return_state(self): 
        full_state= self.state[self.current_player] + self.state[self.current_opponent]+self.playable[self.current_player] + [ self.score[self.current_player], self.score[self.current_opponent]]
        return(full_state)
    
    def reset_state(self): 
        self.state= [[4 for i in range(6)], [4 for i in range(6)]]
        self.playable= [[1 for i in range(6)], [1 for i in range(6)]]
        self.score = [0,0]
        self.reward = [0,0]
        self.end_of_party = False
        self.current_player = 0
        self.current_opponent = 1
        self.current_turn = 0

    def turn(self, hole):
        self.move(hole)
        self.current_turn +=1
        self.current_player = 1 - self.current_player
        self.current_opponent = 1 - self.current_opponent
        self.fill_playable()
        
    def move(self,hole): 
        if self.playable[self.current_player][hole] == 0: 
            score = -100 #played an illegal action
            self.end_of_party = True
        else: 
            self.state,score = self.simulation(hole)
        
        self.score[self.current_player] += score


    def fill_playable(self):
        for case in range(6): 
            if self.state[self.current_player][case] == 0: 
                self.playable[self.current_player][case] = 0
            else: 
                new_state,score =self.simulation(case)
                if new_state[self.current_opponent] == [0,0,0,0,0,0]:
                    self.playable[self.current_player][case] = 0
                else: 
                    self.playable[self.current_player][case] = 1
        if self.playable[self.current_player] == [0,0,0,0,0,0]: 
            self.end_of_party = True        

    def simulation(self,hole):
        #check hole [0;5]
        # check palyer =0/1
        virtualstate= self.state[self.current_player] +self.state[self.current_opponent]
        grain = virtualstate[hole]
        virtualstate[hole]=0
        i = 0
        score = 0
        while grain > 0 :
            i+=1
            if i%12 == 0 :
                i+=1
            virtualstate[(hole+i)%12]+=1
            grain -=1
            
        while ( (hole+i)%12 >= 6 ) and (virtualstate[(hole+i)%12] in [2,3]): 
            score += virtualstate[(hole+i)%12]
            virtualstate[(hole+i)%12]= 0
            i-=1

        if self.current_player == 0: 
            new_state = [virtualstate[0:6],virtualstate[6:12]]
        else : 
            new_state = [virtualstate[6:12],virtualstate[0:6]]  

        return(new_state,score)
  


def afficher_partie(G):
    state = G.return_state()
    print(state[0:6])
    print(state[6:12])
    print(state[12:18])
    print(state[18:20])
    
def jouer_une_partie():
    G = game()
    for i in [0,5,1,2,2,5,4]:
        G.turn(i)
        afficher_partie(G)
    while(1):
        a=int( input("quelle case jouer?:"))
        G.turn(a)
        afficher_partie(G)
        if G.end_of_party :
            print("fin de partie")

jouer_une_partie()



