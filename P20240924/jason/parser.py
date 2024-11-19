def Serializza(s:list):
    if s is not str:
        st='['
        for element in s:
            st+=f"'{element}', "

        st=st[:-2]+"]"
        return st

def Deserializza(s:str):
    if s is not list:
        l=s.split(",")
        l[0]=l[0].replace("[","")
        l[-1]=l[-1].replace("]","")
        for n in range(len(l)):
            l[n]=l[n].replace("'","")
        return l

print(Deserializza("['s','a','b']"))
print(Serializza(['s','a','b']))

print(Deserializza("[1,2,3]"))
print(Serializza([1,2,3]))
    

