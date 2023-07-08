import random

min = 1
max = 100
count = 0
target = random.randint(min, max)
print(f"target is  {target}")
print("============= 猜數字遊戲 ==============")

while True:
    keyin = int(input(f"猜數字範圍{min}~{max}:"))
    count += 1
    if keyin == target:
        print(f"賓果! 猜對了，答案是：{target}")
        print(f"你共猜了{count}次")
        if input("要繼續玩嗎？(y/n)") == 'n':
            break
        else:
            min = 1
            max = 100
            count = 0
            target = random.randint(min, max)
            print(f"target is  {target}")
    elif keyin > target:
        print("再小一點")
        max = keyin - 1
    else:
        print("再大一點")
        min = keyin + 1
print("遊戲結束")
