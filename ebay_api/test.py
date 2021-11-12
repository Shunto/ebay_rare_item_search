import random
l = list(range(0,5))

def test():
    global l
    #local_l = l
    print(l)
    random.shuffle(l)
    print(l)
    for i in l:
        print(i)
    #random.shuffle(local_l)
    #print(local_l)

if __name__ == "__main__":
    test()
    print(l)
