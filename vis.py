"""
Gebruik dit script op eigen risico!! Met dank aan Mozes vd Kar.
De boel is redelijk gehardcode dus verwacht bugs.

args:
    dim: M N - Dimensies van de matrix waarvoor je wilt testen
    offset: N - Aantal lines van de trace file om over te slaan. Je wilt eigenlijk alle data memory accesses die je doet voor je main loopjes
                niet mee laten nemen in het maken van de heatmap, kijk in je tracefile of je kunt ontdekken vanaf wanneer je alleen nog aan
                de matrices zit in data memory (bij de meegeleverde naive implementatie is de juiste offset 4).
    
usage:
    
    volgende command runt test-trans voor M=32, N=32, runt de sim op de resulterende tracefile, en creert hier een heatmap van
    waarbij de eerste 4 regels van de tracefile worden genegeerd.

        ./python3 mozes.py 32 32 --offset 4 



Known bugs: voor 61x67 klopt de output van geen kant
"""

import os
import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument("dim", nargs="+", type=int, default=[32, 32], help="M, N; dimensions of matrices in list.")
    argparser.add_argument("--offset", required=False, type=int, default=4, help="Offset from top of trace file, register only operations after this line number")

    args = argparser.parse_args()

    m, n = args.dim

    os.system('make')
    os.system('./test-trans -M %d -N %d' % (m, n))
    os.system('./csim-ref -v -s 5 -E 1 -b 5 -t trace.f0 > csim_trace.tmp')
    for op in ["L", "S"]:

        hmap = [[-1 for _ in range(n)] for _ in range(m)]

        with open("csim_trace.tmp", 'r') as f:
            index = 0
            try:
                lines = []
                for index, line in enumerate(f.readlines()[args.offset:-2]):
                    split_ln = line.split()

                    if len(split_ln) == 4:
                        ls, address_sz, hitmiss, evict = line.split()
                    else:
                        ls, address_sz, hitmiss = line.split()
                        evict = None
                    address = int(address_sz[:-2], 16)
                    size = int(address_sz[-1])

                    if ls == op and size==4:
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

                    hmap[row][col] = res
                    index += 1

                # simulate 1 hit, miss and eviction at least otherwise cmap bugs out
                hmap[-1][-1] = 2
                hmap[-2][-1] = 1
                hmap[-1][-2] = 0

            except IndexError as e:
                print(index, row, col, e)

            cmap = mpl.colors.ListedColormap(['red', 'black', 'green'], N=3)

            # tell imshow about color map so that only set colors are used
            img = plt.imshow(hmap, cmap=cmap, interpolation='None')
            red_patch = mpatches.Patch(color='red', label='Miss')
            black_patch = mpatches.Patch(color='black', label='Miss eviction')
            green_patch = mpatches.Patch(color='green', label='Hit')
            plt.legend(handles=[red_patch, black_patch, green_patch])

            plt.savefig("cache_usage_" + str(args.dim[0]) + "_" + str(args.dim[1]) + "_" + ("store" if op == "S" else "load") + ".png")
            #plt.show()
