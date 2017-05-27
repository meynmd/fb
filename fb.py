from collections import defaultdict

'''
forward

    eprons:     list of all English sounds
    jprons:     list of all tuples of 1, 2 or 3 Japanese sounds
    priorProb:  dict mapping ephon->jseq->current prob. estimate
'''
def forward(eprons, jprons, priorProb, maxE2J):
    # alpha: the probability of getting to this state by some path
    alpha = [[0. for i in range(len(jprons) + 1)] for j in range(len(eprons) + 1)]
    alpha[0][0] = 1.

    for i in range(len(eprons)):
        for j in range(len(jprons)):
            for k in range(1, min(len(jprons) - j, maxE2J) + 1):
                ep, js = eprons[i], tuple(jprons[j : j + k])
                alpha[i + 1][j + k] += alpha[i][j] * priorProb[ep][js]

    return alpha


def readEpronJpron(filename):
    wordPairs = []
    with open(filename, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            if i % 3 == 0:
                eword = line.strip('\n')
            elif i % 3 == 1:
                jword = line.strip('\n')
            else:
                wordPairs.append((eword, jword))

    return wordPairs


def initProb(ejWordPairs):
    counts = defaultdict(lambda : defaultdict(int))
    # count every possible aligned pair
    for ew, jw in ejWordPairs:
        jw = jw.split()
        for i, ep in enumerate(ew.split()):
            for j in range(len(jw)):
                # match to 1, 2 or 3 Japanese
                for k in range(min(3, len(jw) - j)):
                    js = jw[j : j + k]
                    if len(js) != 0:
                        js = tuple(js)
                        counts[ep][js] += 1

    # initialize probabilities from "observed" counts
    probs = defaultdict(lambda : defaultdict(float))
    for ep, js_co in counts.items():
        n = sum(js_co.values())
        for js, co in js_co.items():
            probs[ep][js] = float(co) / n

    return probs


def printProbMatrix(eng, jap, pm):
    print '\t\t\t\t\t\t\t\t',
    for c in jap[0]:
        print '{:10}\t'.format(c),
    print

    for i, row in enumerate(pm):
        if i > 0:
            print '{:10}'.format( eng[0][i-1] ),
        else:
            print '\t\t\t',
        for col in row:
            print '{:10.2}\t'.format(col),
        print


if __name__ == '__main__':
    fname = 'data/epron-jpron.data'
    wpairs = readEpronJpron(fname)
    probs = initProb(wpairs)
    eng = [x.split() for (x, y) in wpairs]
    jap = [y.split() for (x, y) in wpairs]
    alpha = forward(eng[0], jap[0], probs, 3)


    printProbMatrix(eng, jap, alpha)
