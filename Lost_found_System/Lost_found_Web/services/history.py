#クラスを複数生成、インスタンスもここで作る
from typing import List 
from ..models import Post

#確認情報管理部
class findinfo:
    def findhistory(self, historyID: int) -> list[Post]:
        historydata = Post.objects.filter(user_id=historyID).order_by('-created_at')
        return historydata
    
    def finddetail(self, historyID: int) -> list[Post]:
        historydata = Post.objects.filter(user_id=historyID)
        return historydata

#確認処理部
class Checkhistory:
    def __init__(self):
        self.finder = findinfo()
    def getuserid(self,userID : int) -> List[Post]:
        historydata = self.finder.findhistory(userID)
        return historydata

    def getpostid(self,postID : int) -> List[Post]:
        detaildata = self.finder.finddetail(postID)
        return detaildata  



