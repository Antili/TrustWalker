import random

class User:
    def __init__(self):
        self.Item = []
        self.Rating = []
        self.Following = []
        self.Follower = []
    def AddItem(self,I):
        self.Item.append(I)
    def GetItem(self):
        return self.Item
    def GetNumItem(self):
        return len(self.Item)
    
    def AddRating(self,R):
        self.Rating.append(R)
    def GetRating(self):
        return self.Rating
    def GetRatingItem(self, I):
        R = None
        for i in range (0 , self.GetNumItem()):
            if self.GetItem()[i] == I:
                R = self.GetRating()[i]
        return R
    def GetAveRating(self):
        SumR = 0
        for R in self.Rating:
            SumR += R
        if self.GetNumItem() > 0:
            AveR = float(SumR) / float(self.GetNumItem())
        else:
            AveR = None
        return AveR
    def AddFollowing(self,U):
        self.Following.append(U)
    def GetFollowing(self):
        return self.Following
    def GetNumFollowing(self):
        return len(self.Following)
    
    def AddFollower(self,U):
        self.Follower.append(U)
    def GetFollower(self):
        return self.Follower
    def GetNumFollower(self):
        return len(self.Follower)
    
    def GetRandFollowing(self):
        if self.GetNumFollowing() > 0:
            return self.Following[random.sample(range(self.GetNumFollowing()) , 1)[0]]
        else:
            return None
            