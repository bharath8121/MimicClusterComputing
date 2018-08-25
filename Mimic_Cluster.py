import threading, os, time

class Map(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        l = []
        for i in self.data:
            m = Split_Map(i.strip('\n'), self.name)
            m.start()
            l.append(m)
        print("This is the "+self.name)

class Split_Map(threading.Thread):

    def __init__(self, data, to_append):
        threading.Thread.__init__(self)
        self.data = data
        self.append = to_append

    def run(self):
        self.map()

    def map(self):
        to_write = open("output_"+self.append, "a", encoding = 'utf-8')
        d = {}
        for i in self.data.split(' '):
            i = i.strip('.')
            if i in d:
                d[i]+=1
            else:
                d[i]=1
        for i in d:
            to_write.write(i + " " + str(d[i])+'\n')
        to_write.close()

    def combiner(self):
        pass
    


class Reduce(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        d = {}
        for i in self.data:
            key, value = [i.split(' ')[0], int(i.split(' ')[1])]
            if key in d:
                d[key]+=value
            else:
                d[key]=value
        
        with open('output_'+self.name, "w", encoding = 'utf-8') as f:
            for i in d:
                f.write(i + str(d[i]) + '\n')
        


class Joiner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        pass

def partition(li):
    all_data = []
    for i in li:
        with open("output_"+i.name, "r", encoding='utf-8') as f:
            all_data += map(lambda x: x.strip('\n'), f.readlines())
        os.remove("output_"+i.name)
    reduce_array = [[],[],[]]
    for i in all_data:
        s = len(i.split(' ')[0])
        if s<=5:
            reduce_array[0].append(i)
        elif s>=6 and s<=10:
            reduce_array[1].append(i)
        else:
            reduce_array[2].append(i)
    return reduce_array
    

def main(file_name):
    f = open(file_name, "r", encoding = 'utf-8')
    l = f.readlines()
    i=0
    li = []
    
    while i<len(l):
        s = Map(l[i:i+2])
        li.append(s)
        s.start()
        i+=2
    for j in li:
        j.join()
    
    reduce_array = partition(li)
    for i in reduce_array:
        Reduce(i).start()

if __name__ == "__main__":
    file_name = input()
    main(file_name)