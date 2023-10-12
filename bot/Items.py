class UserItem () : 
    def __init__(self , Username , Session_ID) -> None:
        self.Username=Username
        self.Session_ID=Session_ID
    def __str__(self) -> str:
        return f'Username : {self.Username} , Session ID : {self.Session_ID}' 

class KeywordItem() :
    def __init__(self , Keyword , User : UserItem) -> None:
        self.Keyword=Keyword
        self.User=User
    def __str__(self) -> str:
        return f'Keyword : {self.Keyword} ,  User : {self.User}' 

class videoItem() : 
    def __init__(self , Title , Length , Link , Keyword : KeywordItem) -> None:
        self.Title = Title 
        self.Length = Length
        self.Link = Link
        self.Keyword=Keyword
        
    def __str__(self) -> str:
        return f'Title : {self.Title}, Length : {self.Length}, Keyword : {self.Keyword} \n Link : {self.Link }' 

class ShortItem() :
    def __init__(self , File , Caption ,Tags, User : UserItem) -> None:
        self.File = File
        self.Caption= Caption
        self.User=User
        self.Tags=Tags
    def __str__(self) -> str:
        return f'File : {self.File} ,Tags : {self.Tags} , Caption : {self.Caption} , User : {self.User}' 
