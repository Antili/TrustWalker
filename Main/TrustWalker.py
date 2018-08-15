import scipy.io as sio
import UserClass, ItemClass
import numpy as np
import random
import math

random.seed(a=1000)

def ReadData():
    ## Read trust and rating
    global Rating, Trust
    Input = sio.loadmat('Input.mat')
    Trust = Input.get('trust')
    Rating = Input.get('rating')

def DevideDate(DevideRatio, option):
    global Rating, LearnRating, TestRating
    SelectIndex = random.sample(range(Rating.shape[0]), k=int(Rating.shape[0] * DevideRatio))
    if option is 'AllData':
        LearnRating = Rating[:,:]
    elif option is 'SomeData':
        LearnRating = Rating[SelectIndex,:]
        
        
    TestRating = np.delete(Rating , SelectIndex , 0)
    
    
def MakeUser():
    global LearnRating, Trust, User
    NumUser = max(np.max(LearnRating[:,0]),np.max(Trust)) + 1
    User = [] * NumUser
    ## Making user objects
    for i in range(0 , NumUser):
        User.append(UserClass.User())
    
    ## Populating item related info
    for i in range (0 , LearnRating.shape[0]):
        TempUser = LearnRating[i , 0]
        TempItem = LearnRating[i, 1]
        TempRate = LearnRating[i , 3]
        User[TempUser].AddItem(TempItem)
        User[TempUser].AddRating(TempRate)
        
    ## Populating user related info
    for i in range (0 , Trust.shape[0]):
        TempUser1 = Trust[i , 0]
        TempUser2 = Trust[i, 1]
        User[TempUser1].AddFollowing(TempUser2)
        User[TempUser2].AddFollower(TempUser1)

def MakeItem():
    global LearnRating, Trust, Item
    NumItem = np.max(LearnRating[:,1]) + 1
    Item = [] * NumItem
    ## Making user objects
    for i in range(0 , NumItem):
        Item.append(ItemClass.Item())
    
    ## Populating item related info
    for i in range (0 , LearnRating.shape[0]):
        TempUser = LearnRating[i , 0]
        TempItem = LearnRating[i, 1]
        TempRate = LearnRating[i , 3]
        Item[TempItem].AddUser(TempUser)
        Item[TempItem].AddRating(TempRate)

def RandomWalk(UserID, ItemID, Hob):
    global User, MaxHob
    Phi = 0.5
    Hob += 1
    NextUserID = User[UserID].GetRandFollowing()
    #print(UserID, NextUserID , 0)
    if NextUserID:
        PreRate =  User[NextUserID].GetRatingItem(ItemID)
        if Hob < MaxHob:
            if PreRate:
                return PreRate
            else:
                Sim = []
                for j in User[NextUserID].GetItem():
                    Sim.append(SimItem(ItemID, j))
                if len(Sim) > 0:
                    Phi = max(Sim)
                else:
                    Phi = 0
                if Phi > 0:
                    SimProb = Sim / sum(Sim)
                TempRand = random.uniform(0, 1)
                #print(TempRand, Phi)
                if TempRand >= Phi:
                    return RandomWalk(NextUserID , ItemID, Hob)
                else:
                    RandItem = User[NextUserID].GetItem()[RandSelectProb(SimProb)]
                    #print(RandItem)
                    return User[NextUserID].GetRatingItem(RandItem)
        else:
            return None
    else:
        return None

def RandomWalk_ItemBased(UserID, ItemID, Hob):
    global User, MaxHob
    Hob += 1
    NextUserID = User[UserID].GetRandFollowing()
    # print(UserID, NextUserID , 0)
    if NextUserID:
        PreRate = User[NextUserID].GetRatingItem(ItemID)
        if Hob < MaxHob:
            if PreRate:
                return PreRate
            else:
                Sim = []
                for j in User[NextUserID].GetItem():
                    Sim.append(SimItem(ItemID, j))
                if len(Sim) > 0:
                    Phi = 1
                else:
                    Phi = 1
                if sum(Sim) > 0:
                    SimProb = Sim / sum(Sim)
                else:
                    SimProb = Sim

                TempRand = random.uniform(0, 1)
                # print(TempRand, Phi)
                if TempRand >= Phi:
                    return RandomWalk(NextUserID, ItemID, Hob)
                else:
                    RandItem = User[NextUserID].GetItem()[RandSelectProb(SimProb)]
                    # print(RandItem)
                    return User[NextUserID].GetRatingItem(RandItem)
        else:
            return None
    else:
        return None
    
def RandSelectProb(probs):
    r = random.random()
    index = 0
    while(r >= 0 and index < len(probs)):
        r -= probs[index]
        index += 1
    return index - 1
        
def SimItem(Item1, Item2):
    global Item, User
    CommUser = intersect(Item[Item1].GetUser(), Item[Item2].GetUser())
    CorrNum , CorrDen1, CorrDen2 = 0 , 0 , 0
    Sim = 0.0
    for U in CommUser:
        AveRateUser = User[U].GetAveRating()
        CorrNum += (User[U].GetRatingItem(Item1) - AveRateUser) * (User[U].GetRatingItem(Item2) - AveRateUser)
        CorrDen1 += (User[U].GetRatingItem(Item1) - AveRateUser)**2
        CorrDen2 += (User[U].GetRatingItem(Item2) - AveRateUser)**2
    if CorrDen1 * CorrDen2 != 0:
        Corr = CorrNum / (CorrDen1**0.5 * CorrDen2**0.5)    
        Sim = 1. / (1. + math.exp(-1 * len(CommUser)/2.)) * max(Corr , 0)        
    return Sim


def intersect(a, b):
    return list(set(a) & set(b))

if __name__ == '__main__':
    global Rating , Trust, LearnRating, TestRating
    DevideRatio = 0.9
    ReadData()
    DevideDate(DevideRatio, 'SomeData')
    MakeUser()
    MakeItem()
    MaxHob = 6
    #print(Rating.shape , LearnRating.shape, TestRating.shape)

    Epsi = 0.001
    MaxStep = 10000
    MinStep = 10
    AllResults = []
    AllResultsArray =  np.asarray(AllResults)
    NotPredict = 0
    for preID in range (0 , TestRating.shape[0]):
        #try:
            UserID = TestRating[preID , 0]
            ItemID = TestRating[preID , 1]
            PredRaring = []
            Step = 0
            Sig1 = 0
            Sig2 = 1
            
            while (abs(Sig1 - Sig2) >= Epsi or Step <= MinStep) and Step <= MaxStep:
                Hob = 0
                TempR = RandomWalk(UserID, ItemID, Hob)
                if not TempR:
                    try:
                        TempR = RandomWalk_ItemBased(UserID, ItemID, Hob)
                    except:
                        TempR = None
                if TempR:
                    Sig1 = Sig2
                    PredRaring.append(TempR)
                    Sig2 = np.std(np.asarray(PredRaring))

                Step += 1
            #print(np.mean(np.asarray(PredRaring)) , Rating[preID , 3])
            if np.mean(np.asarray(PredRaring)) >= 0:
                AllResults.append([np.mean(np.asarray(PredRaring)) , TestRating[preID , 3]])
                AllResultsArray =  np.asarray(AllResults)
                RSME = np.mean((AllResultsArray[: , 0] - AllResultsArray[: , 1])**2)**0.5
                Coverage = AllResultsArray.shape[0] / float((AllResultsArray.shape[0] + NotPredict))
                print(preID, RSME , Coverage)
                np.savetxt('PredictedRating_SomeData.txt' , AllResultsArray)
            else:
                #print('NaN', Rating[preID , 3])
                NotPredict += 1
                #np.savetxt('PredictedRating.txt' , AllResultsArray)
        #except:
        #    NotPredict += 1
            
            

          
    
