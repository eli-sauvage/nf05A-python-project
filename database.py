
import pickle
##
# @file database.py
# @brief This file allows us to store and edit all the informations of the users
# @author THARAUD Valentin & SAUVAGE Eli
# @version 1.0
# @date 07/06/2021

##
# @mainpage Snapch'UTT documentation
# @section intro Introduction
#  This project was created for the NF05A course <br/>
# Original instructions : <a href="../NF05A_Project_Snapch_UTT_Python.pdf">NF05A_Project_Snapch_UTT_Python.pdf</a>
# @section install Installation
# @subsection run To run the project
# you will have to start the database.py file.
# For this, and with python installed on your computer, just type
# @code{.bat}
# py database.py
# @endcode
# the required python packages (http, pickle and json) are part of the default modules installed with python



## Each user of the database will we a type User variable
class User:
    ## This initialyze the user by default
    #  @param self The object pointer.
    def __init__(self, name="none", age=0, year=0, field="none",pseudo="none",city="none" ):# we create a class "User" each user of the database will be a "User"
        ##the name of the user
        self.Name=name
        ##the age of the user
        self.Age=age
        ##the year of study of the user
        self.YearofStudy=year
        ##the field of study of the user
        self.FieldofStudy=field
        ##the username of the user
        self.Username=pseudo
        ##the city of the user
        self.City=city
        ##a list of the areas of interest of the user
        self.Areaofinterests=[]
        ##ab list of user followed by this user
        self.followers = []
    ##this function is used to transform an object user to a simple dict <br/>
    # the followers field for example has to be modified to contain only the usernames, because we won't be able to transform it into json otherwise
    # @param self The object pointer.
    # @return a dict with fields that aren't objects (only strings or ints)
    def export(self):
        res = dict(self.__dict__)
        res["iFollow"] = sorted([follower.Username for follower in res["followers"]])#convert user object reference to only usernames
        res["followers"] = sorted([follow.Username for follow in ReturnFollow(self.Username)])
        res["suggestions"] = Suggestion(self.Username)
        return res
    ##Every user will be saved in the database using his username
    # @param self The object pointer.
    # @return the username
    def __repr__(self):
        return self.Username


filename = 'save.pkl'
##loads the informations from the save file
# @return the dict stored in the file (basically the database ordered by the first letter as asked)
def load():
    try:
        infile = open(filename,'rb')
        new_dict = pickle.load(infile)
        infile.close()
    except:#if file doesn't exist or is corrupted, we erase everything and start back to an empty list
        print("error while reading file")
        res = {"GlobalList":{}, "ListofUsername":[]}
        for c in range(65,91):res["GlobalList"][chr(c)] = []
        return res
    return new_dict


content = load()
GlobalList = content["GlobalList"]
ListofUsername=content["ListofUsername"]
## Save the information in a file
def save():#We save the information in a file using this function
    tosave = {"GlobalList":GlobalList, "ListofUsername":ListofUsername}#We save the content of the globalList(all the user and their informations) and the list of Username
    outfile = open(filename, "wb")
    pickle.dump(tosave, outfile)
    outfile.close()
## This function return the User with the corresponding username
# @param Username 
# @return The User with the corresponding username
def FindUsername(username):#This function return the User with the corresponding username
    for u in everyUser():
        if u.Username.lower()==username.lower():
            return u
##This function return all the Users with the corresponding name in a list
# @param Name name of the users we search for
# @return The list of Users with the corresponding name
def FindName(name):
    ListofUser=[]
    for u in everyUser():
        if u.Name.lower()==name.lower():
                ListofUser.append(u)
    return ListofUser
##This function return all the Users with the corresponding field of study in a list
# @param Field field of study of the users we search for
# @return The list of Users with the corresponding field of study
def FindField(field):
    ListofUser=[]
    for u in everyUser():
        if u.FieldofStudy.lower()==field.lower():
                ListofUser.append(u)
    return ListofUser
##This function return all the Users with the corresponding year of study in a list
# @param Year year of study of the users we search for
# @return The list of Users with the corresponding year of study
def FindYear(year):
    ListofUser=[]
    for u in everyUser():
        if u.YearofStudy==year:
                ListofUser.append(u)
    return ListofUser
##This function return all the Users with the corresponding areas of interst in a list
# @param area list of area of interst of the users we search for
# @return The Users with the corresponding areas of interst
def FindArea(area):
    Test=False
    ListofUser=[]
    if type(area)==list:
        for u in everyUser():
            for i in area:
                if i in u.Areaofinterests:
                    Test=True
                else:
                    Test=False
                    break
            if Test:
                ListofUser.append(u)
    return ListofUser
## This function add an user to the dictionary GlobalList in the good section depending on the first letter of his name
# @param User the user type variable we want to add to the GlobalList
def AddtoGlobal(user):#This function add an user to the dictionary GlobalList in the good section depending on the first letter of his name
    for c in range(65,91):
        if chr(c)==user.Name[0] or chr(c+32)==user.Name[0]:
            GlobalList[chr(c)].append(user)
##This function check if an username is already taken (return false if it is)
# @param Username 
#@return True if the username does not exist
def CheckForPseudo(username):
    for x in ListofUsername:
        if x == username:
            return False
    return True
##this function initialyze an user, with all his information (only a unique pseudo and a name are needed) it also add it to the globallist and save the information in a the file
# @param pseudo,name,age,year,field,city,areaofinterests
# @return True or False depending on if the user as been created or not
def CreateUser(pseudo, name,age=None,year=None,field=None,city=None,areaofinterests=[]):
    if CheckForPseudo(pseudo):
        user=User(name,age,year,field,pseudo,city)
        user.Areaofinterests=areaofinterests
        ListofUsername.append(user.Username)
        AddtoGlobal(user)
        save()
        return True
    else:
        return False
##This function Update an user, we need to enter his username and we can uppdate every information it saves the information in a file at the end
# @param pseudo,name,age,year,field,city,areaofinterests
def UppdateUser(username,NewName="none",NewAge=0,NewYear=0,NewField="none",NewPseudo="none",NewCity="none",NewAreas=None):
    y=FindUsername(username)
    if NewName != "none":
        y.Name=NewName
    if NewAge != 0:
        y.Age=NewAge
    if NewYear != 0:
        y.YearofStudy=NewYear
    if NewField != "none":
        y.FieldofStudy=NewField
    if NewPseudo != "none":
        y.Username=NewPseudo
    if NewCity != "none":
        y.City=NewCity
    if NewAreas != None:
        y.Areaofinterests=NewAreas
    save()#it saves the infoin the file

##This function delete an user from globallist (it delete the user and all his information but it also search all the people following him and erase him from their list) it also erase his username from the pseudo list
# @param Username           
def DeleteUser(username):
    
    for c in GlobalList.keys():
        for user in GlobalList[c]:
            if user.Username == username:
                GlobalList[c].remove(user)
    for u in everyUser():
        for f in u.followers:
            if f.Username==username:
                u.followers.remove(f)
    ListofUsername.remove(username)
    save()#it saves the infoin the file


##this function return a list of evry user of the globalList without sorting them by letter in a dictionary 
# @return a list with every user in the database
def everyUser():
    res = []
    for c in range(65,91):
        res += GlobalList[chr(c)]
    return res
##this function add an user to the follower list of an other just by entering their usernames
# @param Username,Usernametofollow The username of the user who will follow the user who correspond  to the usernametofollow
#@return False if the user Usernametofollow is already in the follower of the user 
def Follow(username,usernametofollow):
    user=FindUsername(username)
    userToFollow=FindUsername(usernametofollow)
    if userToFollow in user.followers:
        return False
    else:
        user.followers.append(userToFollow)
    save()#it saves the info in the file

##this function delete an user of the follower list of an other just by entering their usernames
# @param Username,usernametounfollow The username of the user who will unfollow the user who correspond  to the usernametounfollow
#@return False if the user usernametounfollow is not in the follower of the user 
def UnFollow(username,usernametounfollow):
    y=FindUsername(username)
    x=FindUsername(usernametounfollow)
    if x not in y.followers:
        return False
    else:
        y.followers.remove(x)
    save()#it saves the infoin the file
## this function return all the followers of an user in a list
#@param username the username of the user we want the list
def ReturnFollower(username):
    y=FindUsername(username)
    return y.followers

##This foncion call FindArea(), FindField(), FindUsername(), FindName() and FindYear() and search in all the user who correspond to what we are searching
# @param searchfor the keyword you want to research
#@return the list of user corresponding 
def SearchForUser(searchfor):
    #this function search in all the user info what we want (it could be a name an area or multiple areas of interst a year or a field of study or a username) and return all the users corresponding to that information in a list
    if searchfor == "":
        return everyUser()
    else:
        ListofUser=list(set(FindArea(searchfor.split())+FindField(searchfor)+[FindUsername(searchfor)]+FindName(searchfor)+FindYear(searchfor)))
        ListofUser.remove(None)
        return ListofUser


## this function first search for all the followers of an USER then search for all the user that the USER followers follow, then it attibutes a score for evry USER followers followers.
#@param username the username of the user we want the suggestion for
#@return the list of list of the user with their score
def SuggestionSharedfollowers(username):# this function first search for all the followers of an USER then search for all the user that the USER followers follow, then it attibutes a score for evry USER followers followers.
    ListofUser=[]
    ListofFollower=[]
    y=FindUsername(username)
    for j in y.followers:
        for i in j.followers:
            ListofFollower.append(i)
    ListofFollower=list(set(ListofFollower))
    ListofFollower.remove(y)
    for x in range(len(ListofFollower)):
        total=0
        for j in y.followers:
            for i in j.followers:
                if i==ListofFollower[x]:
                    total=total+1
        ListofUser.append([ListofFollower[x],total])
        ListofUser.sort(key=lambda elem:elem[1], reverse=True)
    return ListofUser
##this function attribute a score for each user depending on how many areas of interest corespond to the area of the user we input, rach area in common is a point, it return a list a list(off all the list) of list(with a user and his score)
#@param username the username of the user we want the suggestion for
#@return the list of list of the user with their score
def AreaSuggestion (username):
    #this function attribute a score for each user depending on how many areas of interest corespond to the area of the user we input, rach area in common is a point, it return a list a list(off all the list) of list(with a user and his score)
    ListofUser=[]
    y=FindUsername(username)
    for u in everyUser():
        if u!=y:
            total=0
            for area in u.Areaofinterests:
                if area in y.Areaofinterests:
                    total=total+1
            ListofUser.append([u.Username,total])
    return ListofUser
## this function first search for all the followers of an USER then search for all the user that the USER followers follow, then it attibutes a score for evry USER followers followers.
#@param username the username of the user we want the suggestion for
#@return the list of the five users we suggest
def Suggestion(username):# this function first search for all the followers of an USER then search for all the user that the USER followers follow, then it attibutes a score for evry USER followers followers.
    ListofUser=[]
    ListofFollower=[]
    y=FindUsername(username)
    for j in y.followers:
        for i in j.followers:
            ListofFollower.append(i.Username)
    ListofFollower=list(set(ListofFollower))
    if y.Username in ListofFollower:
        ListofFollower.remove(y.Username)
    for x in range(len(ListofFollower)):
        total=0
        for j in y.followers:
            for i in j.followers:
                if i.Username==ListofFollower[x]:
                    total=total+1
        ListofUser.append([ListofFollower[x],total])
    ListofUser2=AreaSuggestion(username)#this function attribute a score for each user depending on how many areas of interest corespond to the area of the user we input, rach area in common is a point, it return a list a list(off all the list) of list(with a user and his score) 
    ListofUser=ListofUser+ListofUser2#Next we add the two list 
    UserToRemove=[]
    if username == "pierredu91330":
        a="poid,godkgdfo"
    for x in range(len(ListofUser)-1):#for all the users who are in the two list we add both of the score to have the total 
        for i in range(x,len(ListofUser)-1):
            if ListofUser[x][0]==ListofUser[i+1][0]:
                UserToRemove.append(ListofUser[i+1])
        if ListofUser[x][0] in [user.Username for user in y.followers] and ListofUser[x] not in UserToRemove:
            UserToRemove.append(ListofUser[x])
    for x in UserToRemove:
        try:
            ListofUser.remove(x)
        except:
            a=0
    ListofUser.sort(key=lambda elem: elem[1], reverse=True)
    return [elem[0] for elem in ListofUser[:5] if elem[1]>0]#we only take the 5 first usernames if their score is > 0

## this function return all the people that follow an user in a list
#@param username the username of the user we want the list
def ReturnFollow(username): 
    ListofUser=[]
    for u in everyUser():
        for uF in u.followers:
            if uF.Username==username:
                ListofUser.append(u)
    return ListofUser