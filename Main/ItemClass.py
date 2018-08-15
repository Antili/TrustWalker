import random

class Item:
    def __init__(self):
        self.User = []
        self.Rating = []

    def AddUser(self,U):
        self.User.append(U)
    def GetUser(self):
        return self.User
    def GetNumUser(self):
        return len(self.User)
    
    def AddRating(self,R):
        self.Rating.append(R)
    def GetRating(self):
        return self.Rating
    def GetRatingUser(self, U):
        R = None
        for i in range (0 , self.GetNumUser()):
            if self.GetUser()[i] == U:
                R = self.GetRating()[i]
        return R

            