import sqlite3
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

# print(sqlite3.version)
# print(sqlite3.sqlite_version)

conn = sqlite3.connect("game_hs.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS userScore \
     (num float, dura float , name text)")
c.execute("CREATE TABLE IF NOT EXISTS userid \
     (id text,pw text)")
c.execute("CREATE TABLE IF NOT EXISTS que \
     (level text,quiz text PRIMARY KEY)")

while True:
    try:
        print("{0:>30s}".format("======================================="))
        print("{0:>30s}".format("============ Hello World!  ============"))
        print("{0:>30s}".format("======================================="))
        print()
        print("0. 회원가입 ")
        print("1. 로그인")
        print("2. 비회원으로 시작")
        print()
        userinput=int(input("번호를 입력하세요 :"))

        if userinput==0:
            name = input("이름을 입력하세요:")

            result = c.execute("SELECT id FROM userid WHERE id = ?", (name,)).fetchone()
            if result is None:

                while True:
                    print("비밀번호는 숫자와 영문만 가능합니다. ")
                    password = input("비밀번호를 입력하세요 : ")

                    import re
                    pattern1 = re.compile('[0-9a-zA-Z]')
                    pattern2 = re.compile('[^0-9a-zA-Z]')
                    user_id = password

                    result1 = pattern1.search(user_id)
                    result2 = pattern2.search(user_id)
                    if  result1 and not result2 :
                        print(f" \n 이름 : {name} \n 비밀번호 : {password} \n       ★ 회원가입이 완료되었습니다. ★ ")
                        c.execute("INSERT INTO userid(id, pw) VALUES(?,?)", (name, password))
                        conn.commit()
                        break

                    else:
                        print('비밀번호 형식 오류. 다시 입력하세요')
            else:
                print("중복된 이름입니다. 다시 시도하세요.")

        elif userinput==1:

            while True:
                print("{0:>30s}".format("----------- 1.로그인  -----------"))
                name = input("이름을 입력하세요:")
                password = input("비밀번호를 입력하세요:")
                try:
                    call_id = c.execute("SELECT id ,pw FROM userid WHERE id LIKE ?", (f"%{name}%",)).fetchone()
                    id_name=call_id[0]
                    id_pw = call_id[1]
                    if id_pw == password :
                        print("{0:>30s}".format("로그인 되었습니다."))
                        break

                    else :
                        print("{0:>30s}".format("비밀번호오류! 비밀번호를 확인하세요"))
                except TypeError:
                    print("{0:>30s}".format("오류! 이름과 비밀번호를 확인하세요 "))
            break


        elif userinput==2:
            print("{0:>30s}".format("guest로 입장합니다."))
            print()
            name="Guest"
            break

        else:
            print("{0:>30s}".format("번호를 정확히 입력하세요"))
    except ValueError :   #문자 입력시 Err 방지
        print("{0:>30s}".format("번호를 정확히 입력하세요"))




c.execute("SELECT level,quiz FROM que where level= 'easy'")
q_list_easy = c.fetchall()
c.execute("SELECT level,quiz FROM que where level= 'hard'")
q_list_hard = c.fetchall()




print("{0:>30s}".format("======================================="))
print("{0:>30s}".format("============ Hello World!  ============"))
print("손이느린 개발자를 위한 타이핑 연습 게임입니다.")
while True:
    print('----------------------------------------')
    print("1. 게임시작 ")
    print("2. 명예의 전당")
    print("3. 나의 기록")
    print("4. 종료")

    try:
        userinput=int(input("번호를 입력하세요 :"))

        if userinput==1:


            start = time.time()
            n=1
            i=5 #문항수

            print()
            print("*대소문자가 일치해야 합니다. ")
            input(f"{i}개 문항이 출제됩니다. 시작하려면 Enter를 누르세요")
            q1= random.choice(q_list_easy)[1]
            q2= random.choice(q_list_hard)[1]
            while n<= i :
                if n<=i-2 :
                    print("{0:>10s}".format(f"문제{n}"))
                    print(q1)
                    x= input()
                    if q1==x :
                        n=n+1
                        q1= random.choice(q_list_easy)[1]
                    else:
                        print("다시입력하세요")
                elif n>i-2:
                    print("{0:>10s}".format(f"문제{n}"))
                    print(q2)
                    x = input()
                    if q2 == x:
                        n = n + 1
                        q2 = random.choice(q_list_hard)[1]
                    else:
                        print("다시입력하세요")

            end = time.time()
            dura = end - start
            dura = format(dura,".2f")



            c.execute("INSERT INTO userScore(num, dura, name) VALUES(?,?,?)", (format(start,".2f"),dura, name))
            conn.commit()


            c.execute("SELECT name,dura FROM userScore")
            result = c.fetchall()
            result.sort(key=lambda x: x[1])
            #   print(result)

            totaluser=len(result)

            # print(totaluser)
            yourrank = result.index((name, float(dura)))

            print("{0:>30s}".format("============ 게임 결과 ============"))
            print(f"{name}님, 수고하셨습니다.")
            print("소요시간 : ", dura,"초")
            print(" "*11,f" {totaluser}명중 {yourrank+1}위 입니다.")
            if yourrank < 6:
                print("축하합니다~! 명예의 전당에 오르셨습니다.")
            print()
            print("{0:>30s}".format("----------- 명예의 전당 ----------"))
            print("{0:>20s}".format("기록(초)  이 름"))
            for i in range(0, 5):
                print("%6d위 %6.2f %6s" % (i + 1, result[i][1], result[i][0]))

            print("{0:>30s}".format("================================="))



        elif userinput==2:
            c.execute("SELECT name,dura FROM userScore")
            result = c.fetchall()
            result.sort(key=lambda x: x[1])
            print()

            print("=========== 명예의 전당 ===========")
            print()
            for i  in range(0,5):
                print(" "*5,f"{i+1}위",f"{result[i][1]}초",result[i][0])
            print("{0:>20s}".format("==========================="))

            for i in range(10,0,-2):
                print(' '*(10-i),'<',2*i*'*','>',' '*(10-i))
            print('   ', 18*'$')
            print('   ', 5*'*','TROPHY',5*'*')
            print('   ', 18*'$')



        elif userinput == 3:
            call_id = c.execute("SELECT num,dura FROM userScore WHERE name LIKE ? order by num", (f"%{name}%",)).fetchall()

            time = []
            time_num=[]
            values = []
            for i in range(0, len(call_id), 1):
                time.append(call_id[i][0])
                values.append(call_id[i][1])
                time_num.append(i+1)
                print(f"{time_num[i]}회 시도 : {values[i]}")

            x = np.arange(len(time))
            plt.xticks(x, time_num)
            plt.bar(x, values, width=0.5,color='y',label=f'My Score')
            plt.xlabel('your_trial')
            plt.ylabel('score_time')
            plt.legend()
            plt.show()



        elif userinput == 4:
            print("프로그램을 종료합니다.")
            sys.exit()



        else:
            print("번호를 정확히 입력하세요")
    except ValueError:  # 문자 입력시 Err 방지
        print("{0:>30s}".format("번호를 정확히 입력하세요"))
