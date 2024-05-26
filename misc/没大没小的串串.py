import itertools, tqdm, hashlib

x = 'y0U_RE4lLy_kn0W_TH1S_ConGr4tUlAT10Ns'
u = [i.upper() for i in x if i.isalpha()]
a = [i.lower() for i in x if i.isalpha()]
n = list(itertools.product(*zip(u, a)))

for i in tqdm.tqdm(n):
    s = '%s0%s_%s%s4%s%s%s_%s%s0%s_%s%s1%s_%s%s%s%s%s4%s%s%s%s%s10%s%s' % i
    if hashlib.md5(s.encode()).hexdigest() == '7513209051f455fa44d0fa5cd0f3e051':
        print(s)
        break