import math

def bck(st,pos): #Function to retrieve the number followed by the operator
    i=pos-1
    while st[i].isnumeric() is True or st[i] == '.':
        i-=1
        if i<0:
            break
    return st[i+1:pos]

def ahd(st,pos): #Function to retrieve the number following the operator
    i=pos+1
    while st[i].isnumeric() is True or st[i] == '.':
        i+=1
        if i>=len(st):
             break
    return st[pos+1:i]

def neg(st,sn): #Function to deal with negative numbers
    if sn == '^':  #For exponential operator followed by a negative number, a^-b is changed into 1/a^b
        npos = st.find(sn + '-') + 1
        eop1 = bck(st, npos-1)
        eop2 = ahd(st, npos)
        st = st[:npos-1-len(eop1)] + '1/' + eop1 + '^' + eop2 +st[npos+len(eop2)+1:]
    else: #For other operators, negative is shifted leftward until it encounters a + or -, and then changes it accordingly
        npos = st.find(sn+'-')+1
        flag=-1
        i=npos
        st = st[:npos] + st[npos+1:]
        while i>=0:
            if st[i] == '+':
                st = st[:i] + '-' + st[i+1:]
                flag=0
                break
            elif st[i] =='-':
                st = st[:i] + '+' + st[i + 1:]
                flag=0
                break
            else:
                i-=1
        if flag == -1: #If no + or - were found to the left, the first number becomes negative
            st = '-' + st
    return st

def checkneg(st): #Function to check at any point if any negative numbers are in the expression, if yes, it calls neg()
    while '*-' in st or '/-' in st or '+-' in st or '--' in st or '^-' in st:
        if '^-' in st :
            st = neg(st, '^')
        elif '*-' in st:
            st = neg(st, '*')
        elif '/-' in st:
            st = neg(st, '/')
        elif '+-' in st:
            st = neg(st, '+')
        elif '--' in st:
            st = neg(st, '-')
    return st

def eva(st): #Function to evaluate an expression without parenthesis

    st = checkneg(st)

    while 'sin' in st:
        snpos = st.find('sin')
        npos = snpos + 2
        if st[npos+1] == '-':
            snop = '-' + ahd(st, npos+1)
        else:
            snop = ahd(st, npos)
        st = st[:snpos] + str(math.sin(float(snop))) + st[npos + len(snop) + 1:]

    while 'cos' in st:
        snpos = st.find('cos')
        npos = snpos + 2
        snop = ahd(st, npos)
        st = st[:snpos] + str(math.cos(float(snop))) + st[npos + len(snop) + 1:]

    while 'tan' in st:
        snpos = st.find('tan')
        npos = snpos + 2
        snop = ahd(st, npos)
        st = st[:snpos] + str(math.tan(float(snop))) + st[npos + len(snop) + 1:]

    while '^' in st:
        epos=st.find('^')
        eop1=bck(st,epos)
        eop2=ahd(st,epos)
        eres=str(float(eop1)**float(eop2))
        st = st[:epos-len(eop1)] + eres +st[epos+len(eop2)+1:]

    st=checkneg(st)

    while '/' in st:
        dpos=st.find('/')
        dop1=bck(st,dpos)
        dop2=ahd(st,dpos)
        dres=str(float(dop1)/float(dop2))
        st = st[:dpos-len(dop1)] + dres +st[dpos+len(dop2)+1:]
    st = checkneg(st)

    while '*' in st:
        mpos=st.find('*')
        mop1=bck(st,mpos)
        mop2=ahd(st,mpos)
        mres = str(float(mop1) * float(mop2))
        st = st[:mpos - len(mop1)] + mres + st[mpos + len(mop2) + 1:]
    st = checkneg(st)

    while '+' in st or '-' in st: #Addition and subtraction are done parallely by adding all negative and positive numbers separately and the subtracting the negative sum from the positive sum
        if st[0] != '-':
            aop1=''
            for i in st:
                if i.isnumeric() is True or i == '.':
                    aop1=aop1 + i
                else:
                    break
        else:
            aop1=''
        j=0
        ares=sres=0
        while j<len(st):
            if st[j] == '+':
                aop2=ahd(st,j)
                ares=ares+float(aop2)
                j=j+len(aop2)+1
            elif st[j] == '-':
                sop2 = ahd(st, j)
                sres = sres + float(sop2)
                j = j + len(sop2) + 1
            else:
                j+=1
        if aop1 != '':
            ares = ares+float(aop1)
        res = ares - sres
        st=str(res)
        c=0
        for k in st:
            if k == '+' or k == '-' or k == '*' or k == '/' or k == '^':
                c+=1
        if c == 1:
            break
    st = checkneg(st)
    return st

def bra(st): #Function to solve any parenthesis by treating the innermost parenthesis as an expression and substituting its resullt is the original expression
    while '(' in st:
        posc=st.find(')')
        i=posc
        while st[i] != '(':
            i=i-1
        poso=i
        stbr=st[poso+1:posc]
        resb=str(eva(stbr))
        st = st[:poso] + resb +st[posc+1:]
    return st

st=str(input('Enter:'))
i=1
while i<len(st):
    if st[i] == '(':
        if st[i-1].isnumeric() is True or st[i-1] == ')':
            st = st[:i] + '*' +st[i:]
    i+=1
if st[0] == '+':
    st = st[1:]
while 'cosec' in st:
    pos = st.find('cosec')
    st = st[:pos] + '1/sin' + st[pos+5:]
while 'sec' in st:
    pos = st.find('sec')
    st = st[:pos] + '1/cos' + st[pos + 3:]
while 'cot' in st:
    pos = st.find('cot')
    st = st[:pos] + '1/tan' + st[pos + 3:]
st=bra(st)
print(eva(st))

#7-8*-9*((2+4.11+-2.10)^-15)
#3*sin(6*-9)+cos(9^-2)--sec(22.5)*-((cosec(45)+cot(50))*-4)