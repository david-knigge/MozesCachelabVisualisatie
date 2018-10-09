"""
yooo
ff niet stiekem naar de code kijken, het is een zooi
zet dit bestandje gwn in je  cachelab mappie

1. doet python3 bla.py
2. vul de grootte van je matrix in eerst m, dan n
3. wacht
4. je grafiekjes staan opgeslagen als bla + aantal elementen + [L/S] .png
   L staat hier voor loads, en S voor saves
5. In de grafiekjes, groen: hit, rood: miss, zwart: miss eviction

groetjes

ps. heb het gevoel dat het nog niet helemaal werkt voor 61x67
"""

import matplotlib as mpl
mpl.use('agg')
import os
from matplotlib import pyplot as plt

if __name__ == "__main__":
    m = int(input("matrix size: m "))
    n = int(input("n "))
    os.system('make')
    os.system('./test-trans -M %d -N %d' % (m, n))
    os.system('./csim-ref -v -s 5 -E 1 -b 5 -t trace.f0 > ffkijken.txt')
    for blab in ["S", "L"]:

        allus = [[-1 for _ in range(n)] for _ in range(m)]

        with open("ffkijken.txt", 'r') as f:
            index = 0
            try:
                lines = []
                for index, line in enumerate(f.readlines()[4:-2]):
                    splitted = line.split()

                    if len(splitted) == 4:
                        ls, address, hitmiss, evict = line.split()
                    else:
                        ls, address, hitmiss = line.split()
                        evict = None
                    address = int(address[:-2], 16)

                    if ls == blab:
                        lines.append([ls, address, hitmiss, evict, index])

                lines.sort(key=lambda x: x[1])

                index = 0
                for line in lines:
                    ls, address, hitmiss, evict, _ = line

                    row = index // n
                    col = index % n

                    if hitmiss == "miss":
                        if evict == "eviction":
                            res = 1
                        else:
                            res = 0
                    else:
                        res = 2

                    allus[row][col] = res

                    index += 1


            except IndexError as e:
                print(index, row, col, e)

            cmap = mpl.colors.ListedColormap(['red', 'black', 'green'])

            # tell imshow about color map so that only set colors are used
            img = plt.imshow(allus, cmap=cmap, interpolation='None')

            plt.savefig("blab" + str(index) + blab + ".png")