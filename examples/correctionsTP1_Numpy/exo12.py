L = [1]*1000

for i in range(1, len(L)):
    if L[i] == 1:
        for j in range(i + 1, len(L)):
            if (j + 1)%(i + 1) == 0:
                L[j] = 0

for i in range(1, len(L)):
    if L[i] != 0:
        print i+1,
