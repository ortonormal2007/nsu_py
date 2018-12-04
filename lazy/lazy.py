#!/usr/bin/env python3
from fractions import Fraction

class Series:

    def __init__(self,l):
        self.l=[Fraction(x) for x in l]

    def __str__(self):
        s=''
        cont=False
        for n,x in enumerate(self.l):
            if x!=0:
                s+=('+' if cont else '') if x>0 else '-'
                xa=abs(x)
                if xa!=1:
                    s+=str(abs(x))
                    s+='*x' if n>=1 else ''
                else:
                    s+='x' if n>=1 else '1'
                s+=f'^{n}' if n>1 else ''
                cont=True
        n=len(self.l)
        s+=('+' if cont else '')+'O('+('x'+(f'^{n}' if n>1 else '') if n>0 else '1')+')'
        return s

    def __repr__(self):
        return f'Series({self.l})'

    def step(self):
        self.l.append(0)

    def __getitem__(self,n):
        if isinstance(n,slice):
            m=max(n.start,n.stop)
        else:
            m=n
        while len(self.l)<=m:
            self.step()
        return self.l[n]

    def __add__(self,x):
        if isinstance(x,Series):
            return Sum(self,x)
        else:
            return self+Series([x])

    def __radd__(self,x):
        if isinstance(x,Series):
            return Sum(self,x)
        else:
            return self+Series([x])

    def __sub__(self,x):
        return self+(-x)

    def __rsub__(self,x):
        return (-self)+x

    def __mul__(self,x):
        if isinstance(x,Series):
            return Product(self,x)
        else:
            return Product1(self,x)

    def __rmul__(self,x):
        if isinstance(x,Series):
            return Product(self,x)
        else:
            return Product1(self,x)

    def __neg__(self):
        return Product1(self,-1)

    def __call__(self,x):
        return Apply(self,x)

    def __pow__(self,n):
        if n==0:
            return Series([1])
        elif n<0:
            assert self[0]!=0
        if isinstance(n,Fraction):
            if n.denominator==1:
                n=n.numerator
        a,m=self.norm()
        m*=n
        if isinstance(m,Fraction):
            assert m.denominator==1
            m=m.numerator
        return Shift(Pow(a,n),m)

    def __truediv__(self,x):
        if isinstance(x,Series):
            a,n=self.norm()
            b,m=x.norm()
            assert n>=m
            return Div(a,b).shift(n-m)
        else:
            return self*(Fraction(1)/x)

    def __rtruediv__(self,x):
        return x*self**(-1)

    def inv(self):
        return Inv(self)

    def scale(self,c):
        return Apply1(self,c)

    def shift(self,n):
        if n==0:
            return self
        else:
            return Shift(self,n)

    def norm(self,max=100):
        m=0
        while self[m]==0:
            m+=1
            assert m<=max
        return (self.shift(-m),m)

    def diff(self):
        return Diff(self)

    def int(self):
        return Int(self)


class Exp(Series):
    "Р СЏРґ РґР»СЏ exp(x)"

    def __init__(self):
        self.l=[Fraction(1)]

    def __repr__(self):
        return 'Exp()'

    def step(self):
        n=len(self.l)
        self.l.append(self.l[-1]/n)


class Cos(Series):
    "Р СЏРґ РґР»СЏ cos(x)"

    def __init__(self):
        self.l=[Fraction(1)]

    def __repr__(self):
        return 'Cos()'

    def step(self):
        n=len(self.l)+1
        self.l+=[0,-self.l[-1]/((n-1)*n)]

class Sin(Series):
    "Р СЏРґ РґР»СЏ sin(x)"

    def __init__(self):
        self.l=[0,Fraction(1)]

    def __repr__(self):
        return 'Sin()'

    def step(self):
        n=len(self.l)+1
        self.l+=[0,-self.l[-1]/((n-1)*n)]

class Log(Series):
    "Р СЏРґ РґР»СЏ log(1+x)"

    def __init__(self):
        self.l=[0,Fraction(1)]
        self.sign=1

    def step(self):
        n=len(self.l)
        self.sign=-self.sign
        self.l.append(Fraction(self.sign,n))

class Binom(Series):
    "Р СЏРґ РґР»СЏ (1+x)^n"

    def __init__(self,n):
        self.l=[Fraction(1)]
        self.n=n

    def __repr__(self):
        return f'Binom({self.n})'

    def step(self):
        n=len(self.l)
        self.l.append(self.l[-1]*Fraction((self.n-n+1),n))

class Sum(Series):
    "РЎСѓРјРјР° СЂСЏРґРѕРІ"

    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.l=[a[0]+b[0]]

    def __repr__(self):
        return f'({repr(self.a)}+{repr(self.b)})'

    def step(self):
        n=len(self.l)
        self.l.append(self.a[n]+self.b[n])

class Product(Series):
    "РџСЂРѕРёР·РІРµРґРµРЅРёРµ СЂСЏРґРѕРІ"

    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.l=[a[0]*b[0]]

    def __repr__(self):
        return f'{repr(self.a)}*{repr(self.b)}'

    def step(self):
        n=len(self.l)
        self.l.append(sum(self.a[i]*self.b[n-i] for i in range(n+1)))

class Product1(Series):
    "Р СЏРґ СѓРјРЅРѕР¶РёС‚СЊ РЅР° С‡РёСЃР»Рѕ"

    def __init__(self,a,b):
        self.a = a
        self.b = b
        self.l=[a.l[i]*b for i in range(len(a.l))]

    def __repr__(self):
        return Product.__repr__(self)

    def step(self):
        n=len(self.l)
        self.l.append(self.a[n]*self.b)

class Pow(Series):
    "a^n"

    def __init__(self,a,n):
        self.a=a
        self.n=n
        a0=Fraction(a[0])
        an,ad=a0.numerator,a0.denominator
        if isinstance(n,Fraction):
            nn,nd=n.numerator,n.denominator
            an=pow1(an,nd)**nn
            ad=pow1(ad,nd)**nn
            a0=Fraction(an,ad)
        else:
            a0=a0**n
        self.l=[a0]

    def __repr__(self):
        return f'{repr(self.a)}**{repr(self.n)}'

    def step(self):
        m=len(self.l)
        self.l.append(sum((k*self.n-m+k)*self.a[k]*self.l[m-k] for k in range(1,m+1))/(m*self.a[0]))

class Div(Series):
    "Р”РµР»РµРЅРёРµ СЂСЏРґРѕРІ"

    def __init__(self,a,b):
        assert b[0]!=0
        self.a=a
        self.b=b
        self.l=[a[0]/b[0]]

    def __repr__(self):
        return f'{repr(self.a)}/{repr(self.b)}'

    def step(self):
        n=len(self.l)
        self.l.append((self.a[n]-sum(self.b[k]*self.l[n-k] for k in range(1,n+1)))/self.b[0])

class Apply(Series):
    "a(b)"

    def __init__(self,a,b):
        assert isinstance(b,Series) and b[0]==0
        self.a=a
        self.b=b
        self.l=[a[0]]
        self.bell=Bell()
        self.c=1

    def __repr__(self):
        return f'{repr(a)}({repr(b)})'

    def step(self):
        n=len(self.l)
        self.c*=n
        self.bell.step(self.c*self.b[n])
        r=0
        c=1
        for k in range(1,n+1):
            c*=k
            r+=c*self.a[k]*self.bell[n,k]
        self.l.append(r/c)

class Apply1(Series):
    "a(c*x)"

    def __init__(self,a,c):
        self.a=a
        self.c=c
        self.x=c
        self.l=[a[0]]

    def __repr__(self):
        return f'Apply1({self.a},{self.c})'

    def step(self):
        n=len(self.l)
        self.l.append(self.x*self.a[n])
        self.x*=self.c

class Shift(Series):
    "a*x^n"

    def __init__(self,a,n):
        if n<0:
            for i in range(-n):
                assert a[i]==0
            self.l=[a[-n]]
            self.n=-n
        else:
            self.l=[0 for i in range(n)]
            self.n=-1
        self.a=a

    def __repr__(self):
        return f'Shift({repr(self.a)})'

    def step(self):
        self.n+=1
        self.l.append(self.a[self.n])

class Inv(Series):
    "Р РµС€РёС‚СЊ СѓСЂР°РІРЅРµРЅРёРµ a(x)=y РІ РІРёРґРµ СЂСЏРґР° РїРѕ y"

    def __init__(self,a):
        assert a[0]==0 and a[1]!=0
        self.a=a
        self.l=[0,1/a[1]]
        self.bell=Bell()
        self.f=1
        self.c=1

    def __repr__(self):
        return f'{repr(self.a)}.inv()'

    def step(self):
        n=len(self.l)
        self.bell.step(self.f*self.a[n]/self.a[1])
        self.f*=n
        self.c/=(n*self.a[1])
        r=0
        c=1
        for k in range(1,n):
            c*=1-n-k
            r+=c*self.bell[n-1,k]
        self.l.append(self.c*r)

class Diff(Series):
    "РџСЂРѕРёР·РІРѕРґРЅР°СЏ"

    def __init__(self,a):
        self.a=a
        self.l=[a[1]]

    def __repr__(self):
        return f'Diff({repr(self.a)})'

    def step(self):
        n=len(self.l)+1
        self.l.append(n*self.a[n])

class Int(Series):
    "РРЅС‚РµРіСЂР°Р»"

    def __init__(self, a):
        self.a = a
        self.l = [0]

    def __repr__(self):
        return f'Int({repr(self.a)})'

    def step(self):
        n = len(self.l)
        self.l.append(self.a[n-1]/Fraction(n))

class Bell:
    """
    Bell polynomials $B_{n,k}(x_1,...,x_{n-k+1})$ ($k \le n$)
    https://en.wikipedia.org/wiki/Bell_polynomials
    """

    def __init__(self):
        self.x=[]
        self.b={(0,0):Fraction(1)}

    def __getitem__(self,n):
        return self.b[n]

    def step(self,x):
        """
        Add a new $n$ (with its $x_n$)
        and calculate all $B_{n,k}$ for $k\in[0,n]$
        """
        self.x.append(x)
        n=len(self.x)
        self.b[n,0]=0
        c=Fraction(1,n)
        for k in range(1,n+1):
            r=0
            c=1
            for i in range(1,n-k+2):
                r+=c*self.x[i-1]*self.b[n-i,k-1]
                c*=Fraction(n-i,i)
            self.b[n,k]=r

def pow1(x,n):
    "x**(1/n)"
    y=round(x**(1/n))
    assert y**n==x
    return y

if __name__=='__main__':
    n=10

    def zero(s):
        for i in range(n):
            assert s[i]==0

    def test_sincos():
        c=Cos()
        s=Sin()
        # cos(x)**2 + sin(x)**2 = 1
        zero(c**2+s**2-1)
        # (1+cos(x))/2 = cos(x/2)**2
        zero((1+c)/2-c.scale(Fraction(1,2))**2)
        # (1-cos(x))/2 = sin(x/2)**2
        zero((1-c)/2-s.scale(Fraction(1,2))**2)
        # sin(asin(x)) = x, asin(sin(x)) = x
        asin=s.inv()
        x=Series([0,1])
        zero(s(asin)-x)
        zero(asin(s)-x)
        # 1 + tan(x)**2 = 1/cos(x)**2
        t=s/c
        zero(1+t**2-1/c**2)
        # 2*cos(x)*sin(x) = sin(2*x)
        zero(2*c*s-s.scale(2))
        # cos(x)**2 - sin(x)**2 = cos(2*x)
        zero(c**2-s**2-c.scale(2))
        # 2*tan(x/2)/(1+tan(x/2)**2) = sin(x)
        t=t.scale(Fraction(1,2))
        zero(2*t/(1+t**2)-s)
        # (1-tan(x/2)**2)/(1+tan(x/2)**2) = cos(x)
        zero((1-t**2)/(1+t**2)-c)

    def test_explog():
        e=Exp()
        l=Log()
        # exp(log(1+x)) = 1+x
        x=Series([0,1])
        zero(e(l)-1-x)
        # log(1+(exp(x)-1)) = x
        zero(l(e-1)-x)
        # cosh(x)**2 - sinh(x)**2 = 1
        ch=(e+e.scale(-1))/2
        sh=(e-e.scale(-1))/2
        zero(ch**2-sh**2-1)
        # tanh(x) = (exp(2*x)-1)/(exp(2*x)+1)
        th=sh/ch
        zero((e.scale(2)-1)/(e.scale(2)+1)-th)
        # atanh(x) = 1/2*log((1+x)/(1-x))
        ath=th.inv()
        zero(ath(th)-x)
        zero(th(ath)-x)
        zero((l-l.scale(-1))/2-ath)
        zero(l-l.scale(-1)-l(2*x/(1-x)))
        # asinh(x) = log(sqrt(1+x**2)+x
        ash=sh.inv()
        zero(l((1+x**2)**Fraction(1,2)-1+x)-ash)
        # ((1+x)**(1/3))**3 = 1+x
        b=Binom(Fraction(1,3))
        zero(b**3-1-x)
        b**=Fraction(3,5)
        zero(Binom(Fraction(1,5))-b)

    test_sincos()
    test_explog()