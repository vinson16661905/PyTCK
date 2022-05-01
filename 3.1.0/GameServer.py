from logging import exception
import random
import socket
from time import sleep

PORT = 21421    #This is the default port , if this port is in use , please change a available port manully .

class card : 

    '''
    卡牌类，用于提供游戏所需卡牌
    '''

    lostbox=[]
    cardbox=["杀","杀","杀","杀","杀","杀","杀","杀","杀","杀","杀","杀","杀","杀",
    "杀","杀","闪","闪","闪","闪","闪","闪","闪","闪","桃","桃","桃","桃","桃",
    "闪","五谷丰登","过河拆桥","过河拆桥","过河拆桥","顺手牵羊","顺手牵羊","顺手牵羊",
    "南蛮入侵","南蛮入侵","南蛮入侵","万箭齐发","万箭齐发","万箭齐发","无中生有",
    "无中生有","无中生有","无懈可击","无懈可击","无懈可击","五谷丰登","五谷丰登",
    "桃园结义","桃园结义","决斗","决斗","无懈可击"]              #共56张
    five=[]                                                 #“五谷丰登”使用的临时列表

    def choose(whose):                                              #摸牌函数
        card.washcard()
        havecard=random.choice(card.cardbox)
        whose.cards.append(havecard)
        print(whose.name+"得到了1张牌")
        broadcast(whose.name+"得到了1张牌")
        card.cardbox.remove(havecard)
    def washcard():                    #洗牌
        if len(card.cardbox)<20:
            card.cardbox.extend(card.lostbox)
            card.lostbox=[]
    def wugu():                                            #五谷丰登函数
        five=[]
        num=len(playerbox)
        for i in range(num):
            havecard=random.choice(card.cardbox)
            card.five.append(havecard)
            card.cardbox.remove(havecard)


class name:

    '''
    武将类，用于选取武将
    '''

    namebox=['曹操（乱世奸雄）','司马懿','张辽','许褚（虎威熊胆）','夏侯惇','典韦','刘备','诸葛亮','关羽',
    '张飞','赵云（白龙出云）','马超','孙权','黄盖','周瑜','吕蒙（白衣渡江）','太史慈','甘宁','陆逊','周泰','华佗','吕布',
    '华雄','袁绍','袁术','张角（黄天邪道）','张宝','周泰','黄月英','华佗','孙策']  
    def choosename():
        havename=random.choice(name.namebox)
        name.namebox.remove(havename)
        return havename


class player:

    '''
    玩家类，实现玩家的操作
    '''

    def __init__(self,mynum):       #初始化玩家
        self.blood=4
        self.cards=[]
        self.message=[]
        self.cardnum=0
        self.name=mynum
        self.killtime=0
        self.psocket=socketbox[mynum][0]
        self.paddress=socketbox[mynum][1]
        print("player"+str(mynum)+"has been connected . The IP and port is :"+str(self.paddress))
        print("player"+str(mynum)+"has been ready .")


    def ready(self):        #开局准备
        self.name=name.choosename()
        for i in range(0,4):
            card.choose(self)

            
    def role(self):     #玩家回合函数
        self.die()
        card.choose(self)
        card.choose(self)
        self.killtime=0
        while True:
            print("您的手牌："+str(self.cards))
            a=socketsend(True,self,"您的手牌："+str(self.cards))
            msgtemp=socketsend(False,self,"请出牌：（结束回合请按q）")
            print(2,msgtemp)
            if(msgtemp=='q'):
                while len(self.cards) > self.blood :
                    print("您的手牌："+str(self.cards))
                    a=socketsend(True,self,"您的手牌："+str(self.cards))
                    num=int(socketsend(False,self,"弃哪张牌？（输入一个序号，从0开始）"))
                    while (num>len(self.cards) or num<0 ):
                        num=int(socketsend(False,self,"弃哪张牌？（输入一个序号，从0开始）"))
                        a=socketsend(True,self,"您的手牌："+str(self.cards))
                        print("您的手牌："+str(self.cards))
                    print(self.name+"弃了"+self.cards[num])
                    broadcast(self.name+"弃了"+self.cards[num])
                    card.lostbox.append(self.cards[num])
                    self.cards.pop(num)
                break            
            if not (msgtemp in self.cards) :
                continue
            self.msg(msgtemp)

            assert(not msgtemp=="debug") , "Debug on ."         #内置调试入口


    def msg(self,msgtemp):      #出牌处理
        print(3, msgtemp)
        if msgtemp in self.cards :
            if(msgtemp=="闪"):
                print(msgtemp+"不是这样用的")
                broadcast(msgtemp+"不是这样用的")

            elif msgtemp=="无懈可击" :
                print(msgtemp+"不是这样用的")
                broadcast(msgtemp+"不是这样用的")
    
            elif msgtemp=="杀" and self.killtime==1 :
                print("一回合只能出一次杀")
                broadcast("一回合只能出一次杀")

            elif msgtemp=="桃园结义" :
                card.lostbox.append("桃园结义")
                self.cards.remove("桃园结义")
                for j in playerbox:
                    j.message.append(("桃园结义",self))
                    j.call()                        
            elif msgtemp=="南蛮入侵" :
                card.lostbox.append("南蛮入侵")
                self.cards.remove("南蛮入侵")                        
                mynum=playerbox.index(self)
                for j in range(len(playerbox)):
                    if(not j==mynum):
                        playerbox[j].message.append(("南蛮入侵",self))
                        playerbox[j].call()
            elif msgtemp=="万箭齐发" :
                card.lostbox.append("万箭齐发")
                self.cards.remove("万箭齐发")
                mynum=playerbox.index(self)
                for j in range(len(playerbox)):
                    if(not j==mynum):
                        playerbox[j].message.append(("万箭齐发",self))
                        playerbox[j].call()
            elif msgtemp=="五谷丰登" :
                card.lostbox.append("五谷丰登")
                self.cards.remove("五谷丰登")
                card.wugu()
                self.message.append((msgtemp,self))
                self.call()
                mynum=playerbox.index(self)
                for j in range(len(playerbox)):
                    if(not j==mynum):
                        playerbox[j].message.append((msgtemp,self))
                        playerbox[j].call()
            elif msgtemp=="无中生有" :
                card.lostbox.append("无中生有")
                self.cards.remove("无中生有")
                self.message.append(("无中生有",self))
                self.call()
            else:
                card.lostbox.append(msgtemp)
                self.cards.remove(msgtemp)
                if(msgtemp=="杀"):
                    self.killtime+=1
                for i in range(0,len(playerbox)):
                    print(str(i)+":"+playerbox[i].name+" ")   
                    a=socketsend(True,self,str(i)+":"+playerbox[i].name+" ")
                target_s=socketsend(False,self,"对谁？（输入序号）")
                target=int(target_s)
                if (target>=0 and target<len(playerbox)):
                    print(self.name+"对"+playerbox[target].name+"出"+msgtemp)
                    broadcast(self.name+"对"+playerbox[target].name+"出"+msgtemp)

                    playerbox[target].message.append((msgtemp,self))
                    playerbox[target].call()
                else :
                    print("目标无效，视为弃牌")
                    broadcast("目标无效，视为弃牌")

        else :
            print("您没有此牌")


                                      
    def call(self):     #被指定为目标后处理
        msg=(self.message[0])[0]
        source=(self.message[0])[1]
        if msg=="杀":
            have=self.askfor("闪")
            if(not have):
                self.blood-=1
                print(self.name+"掉1滴血")
                broadcast(self.name+"掉1滴血")
                broadcast(self.name + "的血量为" + str(self.blood))
                self.die()

        elif msg=="万箭齐发":
            have=self.askfor("闪")
            if(not have):
                self.blood-=1
                print(self.name+"掉1滴血")
                broadcast(self.name+"掉1滴血")
                broadcast(self.name + "的血量为" + str(self.blood))
                self.die()   

        elif msg=="桃"and self.blood<4:
            self.blood+=1
            print(self.name+"回1滴血")
            broadcast(self.name+"回1滴血")

        elif msg=="南蛮入侵":
            have=self.askfor("杀")
            if(not have):
                self.blood-=1
                print(self.name+"掉1滴血")
                broadcast(self.name+"掉1滴血")
                broadcast(self.name + "的血量为" + str(self.blood))
                self.die() 

        elif msg=="无中生有" :
            card.choose(self)
            card.choose(self)
            
        elif msg=="桃园结义" :
            for i in playerbox:
                if(i.blood<4):
                    i.blood+=1
                    print(i.name+"回1滴血")
                    for i in playerbox :
                        a=socketsend(True,i,i.name+"回1滴血")
        elif msg=="决斗" :
            have=self.askfor("杀")
            if(not have):
                self.blood-=1
                print(self.name+"掉1滴血")
                broadcast(self.name+"掉1滴血")
                broadcast(self.name + "的血量为" + str(self.blood))
                self.die()                    
            else:
                source.message.append(("决斗",self))
                source.call()
        elif msg=="过河拆桥" :
            have=self.askfor("无懈可击")
            if((not have) and len(self.cards)>0):
                cardtemp=source.question(1,"拆啥？",self)
                broadcast("拆到"+self.cards[cardtemp])
                self.cards.pop(cardtemp)
                self.cardnum-=1
        elif msg=="顺手牵羊" :
            have=self.askfor("无懈可击")
            if (not have) and len(self.cards)>0 :
                cardtemp=source.question(1,"牵啥？",self)
                print(source.name+"获得"+self.cards[cardtemp])
                broadcast(source.name+"获得"+self.cards[cardtemp])
                source.cards.append(self.cards[cardtemp])                
                source.cardnum+=1
                self.cards.pop(cardtemp)
                self.cardnum-=1
        elif msg=="五谷丰登" :
            havecard=self.question(0,"选啥？")
            self.cards.append(card.five[havecard])
            card.five.pop(havecard)
            self.cardnum+=1
        self.message=[]


    def askfor(self,cardtemp):      #索要指定卡牌
        if(cardtemp not in self.cards):
            print(self.name+"没有"+cardtemp)
            broadcast(self.name+"没有"+cardtemp)
            return False
        else:
            have=socketsend(False,self,"是否出"+cardtemp+"(y/n)")
            if(have=="y"):
                print(self.name+"出了"+cardtemp)
                broadcast(self.name+"出了"+cardtemp)
                self.cards.remove(cardtemp)
                card.lostbox.append(cardtemp)
                self.cardnum-=1
                return True
            else:
                print(self.name+"没有使用"+cardtemp)
                broadcast(self.name+"没有使用"+cardtemp)
                return False


    def question(self,ID,question,target=0):        #询问
        if(ID==1):
            print("数量："+str(len(target.cards)))
            a=socketsend(True,self,"数量："+str(len(target.cards)))
            num=int(socketsend(False,self,question+"（输入序号,从0开始，不得大于等于数量）"))
            return num
        elif(ID==0):
            for i in range(len(card.five)):
                print(str(i)+":"+card.five[i])
                a=socketsend(True,self,str(i)+":"+card.five[i])
            num=int(socketsend(False,self,question+"（输入序号）"))
            return num

    
    def die(self) :     #濒死处理

        if self.blood > 0 : return

        need = -(self.blood) + 1
        have = self.cards.count('桃')

        if need <= have :       #个人手中有足够'桃'
            for i in range(0, need):
                self.cards.remove('桃')
                self.cardnum -= 1
                self.blood += 1
                card.lostbox.append('桃')
                broadcast(self.name + "使用了桃，血量为" + str(self.blood))
            return
        else :
            for i in range(0, have) :
                self.cards.remove('桃')
                self.cardnum-=1
                self.blood += 1
                card.lostbox.append('桃')
                broadcast(self.name + "使用了桃，血量为" + str(self.blood))

            for i in playerbox :
                socketsend(True, i, self.name + "需要救助")
                ans = i.askfor('桃')
                if ans :
                    self.blood += 1
                    broadcast(self.name + "的血量为" + str(self.blood))
                if self.blood > 0 : break
            
            if self.blood <= 0 :
                card.lostbox.extend(self.cards)
                broadcast(self.name + "失败")
                socketsend(True, self, "die")
                playerbox.remove(self)
                self.psocket.close()
                del self


def socketsend(isprint,target,msg):     #发送消息
    if isprint :
        target.psocket.send(msg.encode(encoding='UTF-8',errors='strict'))
        sleep(0.3)
        return 0
    else :
        target.psocket.send(("ask"+msg).encode(encoding='UTF-8',errors='strict'))
        sleep(0.3)
        buffer=target.psocket.recv(1024)
        buffer=buffer.decode(encoding='UTF-8',errors='strict')
        print(1,buffer)
        return buffer


def broadcast(msg) :        #对全体玩家发送消息
    print(msg)
    for i in playerbox :
        socketsend(True, i, msg)


numtemp=int(input("server@host#请输入玩家人数>>>"))
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host="127.0.0.1"

try :

    try :
        s.bind((host,PORT))
    except OSError :
        print("端口被占用，请到Line 5手动修改")
        from sys import exit
        exit(1)

    socketbox=[]
    while len(socketbox)<numtemp :
        s.listen(numtemp)
        sockettemp,addresstemp=s.accept()
        socketbox.append((sockettemp,addresstemp))
    playerbox=[]
    for i in range(0,numtemp):
        playerbox.append(player(i))
        playerbox[i].ready()
    print("------欢迎使用PyTCK------")
    print("v3.1.0    powered by 北极熊,believe the science,鬼帝")
    broadcast("------欢迎使用PyTCK------\nv3.1.0    powered by 北极熊,believe the science,鬼帝")

    
    while(len(playerbox)>1):
        for i in playerbox :
            i.role()
            if len(playerbox) == 1 :
                break

    print(playerbox[0].name+"赢得了本局游戏！")
    a=socketsend(True,playerbox[0],"win")


except ConnectionAbortedError:

    print("有用户掉线")

except ConnectionResetError :

    print("有用户退出")
    
except KeyboardInterrupt :

    print("强制退出")
    
exits=input("按任意键退出...")
