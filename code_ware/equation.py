import timeit
import numpy as np
import math
import cmath

para = [[15.9178, 46863], [13.4808, 67875], [12.3063, 61635], [-13.392, 91385], [15.4758, 55527], [13.3607, 125932],
        [-13.47, 106572], [12.2896, 167264], [13.6723, 54051], [15.3503, 30815]]
e = 2.718281828459045
# abs(10*math.log(A+B*e**(1.001*D*(0.367*rho-337))-sigma0)<=100
a, b, c = [(i + 1) / 10 for i in range(100000)], [(i + 1) / 10 for i in range(100000)], [(i + 1) / 10 for i in
                                                                                         range(100000)]
s = []
x = 0
for p in para:
    rho = p[1]
    sigma0 = p[0]
    for i in a:
        for j in b:
            for k in c:
                x += 1
                print(i, j, k)
                print(i + j * e ** (1.001 * -k * (0.367 * rho - 337)))
                print((1.001 * k * (0.367 * rho - 337)))
                if abs(10 * math.log(i + j * e ** (1.001 * -k * (0.367 * rho - 337)) - sigma0)) <= 100:
                    s.append([sigma0, rho, i, j, k])
                if x % 10000000 == 0:
                    print(x // 10000000)
