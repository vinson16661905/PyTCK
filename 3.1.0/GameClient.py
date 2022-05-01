import socket
def main() :
    host=input("Input the server IP :")
    port=int(input("Input the server port :"))
    try :
        c=socket.socket(socket.AF_INET,socket.SOCK_STREAM ,0)
        c.connect((host,port))
        while True :
            buffer=c.recv(1024)
            buffer=buffer.decode(encoding='UTF-8',errors='strict')
            if buffer[:3]=="ask" :
                ans=input(buffer)
                while ans == '' :
                    ans = input(buffer)
                c.send(ans.encode(encoding='UTF-8',errors='strict'))
            elif buffer[:3]=="die" :
                print("您失败了！")
                break
            elif buffer[:3]=="win" :
                print("您胜利了！")
                break
            elif buffer == 'rst' :
                print("有玩家掉线，游戏终止。")
                break            
            else :
                print(buffer)
        c.close()
    except ConnectionAbortedError :
        print("网络异常!")

    except KeyboardInterrupt :
        print("Process has been force stopped .")
        
    print("再见，欢迎下次使用！")
    exits=input('按任意键继续...')
if __name__ == '__main__' :
    main()
