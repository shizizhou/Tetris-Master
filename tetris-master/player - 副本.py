from board import Direction, Rotation, Action,Shape
from random import Random
import time

counter=0
bombcount=5
discardcount=10
dis=False
lasth=24
class Player:
    def choose_action(self, board):
        raise NotImplementedError

def findHole(board,tempx,tempy):
    num=0
    for (x,y) in board.cells:
            for i in range(len(tempx)):
                if(tempx[i]==x and tempy[i]-1==y):
                    num+=1
                    for n in range(len(tempy)):
                        if(tempx[i]==x and tempy[n]>tempy[i]):
                            num+=1

                    
    return num
def createHole(board):
        tempx=[]
        tempy=[]
        num=0
        ha=True
        for i in range(10):
            for o in range(24):
                for (x,y) in board.cells:
                    if(i==x and o==y):
                        ha=False
                if(ha):
                    tempx.append(i)
                    tempy.append(o)
                ha=True
        num=findHole(board,tempx,tempy)
                
        return num
                 
                
def Bumpiness(board):
    sum=0
    temp=[]
    for i in range(10):
        tempy=0
        for o in range(24):
            for (x,y) in board.cells:
                if(24-y>tempy and x==i):
                    tempy=24-y
        temp.append(tempy)
    for i in range(0,9):
        sum+=abs(temp[i]-temp[i+1])
    return sum




class SmartPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    
                    
                        
    def choose_action(self, board):
        global bombcount,lasth,discardcount,dis,counter
        counter+=1
        act=[]
        temph=10000000
        tempy=0
        nowy=0
        tempmove=0
        tempRotate=0
        maxhight=24
        holes=createHole(board)
        print(counter)
        nowScore=board.score
        mmx=24
        try:
            
                for i in range(-5,5):
                    for n in range(0,4):
                        tempBoard=board.clone()
                        if(n==3):
                            tempBoard.rotate(Rotation.Anticlockwise)
                        else:
                            for h in range(n):
                                tempBoard.rotate(Rotation.Clockwise)
                        if(i<0):
                            for h in range(abs(i)):
                                tempBoard.move(Direction.Left)
                        else:
                            for h in range(i):
                                tempBoard.move(Direction.Right)
                        tempBoard.move(Direction.Drop)
                        for (x,y) in tempBoard.cells:
                            if(y<maxhight):
                                maxhight=y
                            tempy+=abs(24-y)
                        if(createHole(tempBoard)-holes>0):
                            for q in range(createHole(tempBoard)-holes):
                                tempy+=10
                        if(createHole(tempBoard)-holes<0):
                            for q in range(abs(createHole(tempBoard)-holes)):
                                tempy-=100
                        tempScore=tempBoard.score
                        if(tempScore-nowScore<100 and tempScore-nowScore>25):
                            tempy+=105
                        tempy+=Bumpiness(tempBoard)*2
                        if(temph>tempy):
                            mmx=maxhight
                            temph=tempy
                            tempRotate=n
                            tempmove=i
                        tempy=0
                        maxhight=24
                ttmpy=0
                tttmpy=0
                tempBoard=board.clone()
                oldholes=createHole(tempBoard)
                for (x,y) in tempBoard.cells:
                    ttmpy+=y
                if(tempRotate==3):
                    tempBoard.rotate(Rotation.Anticlockwise)
                else:
                    for i in range(tempRotate):
                        tempBoard.rotate(Rotation.Clockwise)
                if(tempmove<0):
                    for i in range(abs(tempmove)):
                        tempBoard.move(Direction.Left)
                else:
                    for i in range(tempmove):
                        tempBoard.move(Direction.Right)
                tempBoard.move(Direction.Drop)
                for (x,y) in tempBoard.cells:
                    tttmpy+=y  
                if(createHole(tempBoard)>2):
                    """createHole(tempBoard)>0"""
                    dis=True
        finally:
            time.sleep(0)
            if(discardcount>0):
                if(dis):
                    discardcount-=1
                    dis=False
                    return Action.Discard
            if(bombcount>0 and mmx<8):
                    bombcount-=1
                    return Action.Bomb,Direction.Drop
            lasth=mmx
            if(tempRotate==3):
                act.append(Rotation.Anticlockwise)
            else:
                for i in range(tempRotate):
                    act.append(Rotation.Clockwise)
            if(tempmove<0):
                for i in range(abs(tempmove)):
                    act.append(Direction.Left)
            else:
                for i in range(tempmove):
                    act.append(Direction.Right)
            act.append(Direction.Drop)
            return act
        


SelectedPlayer = SmartPlayer
