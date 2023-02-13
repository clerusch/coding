from numpy import array, zeros, hstack, vstack
def genSteaneLookupTable():
    H = array([[1, 0, 0, 1, 0, 1, 1],
               [0, 1, 0, 1, 1, 0, 1],
               [0, 0, 1, 0, 1, 1, 1]])
    null = zeros(H.shape)
    firstline = hstack((H, null))
    secondline = hstack((null, H))
    pcm = vstack((firstline, secondline))
    dict = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for h in range(2):
                    for l in range(2):
                        for m in range(2):
                            for n in range(2):
                                for l in range(2):
                                    for m in range(2):
                                        for n in range(2):
                                            for o in range(2):
                                                for p in range(2):
                                                    for q in range(2):
                                                        for r in range(2):
                                                            for s in range(2):
                                                                for t in range(2):
                                                                    for u in range(2):
                                                                        error = array([i,j,k,h,l,m,n,o,p,q,r,s,t,u])
                                                                        syndrome = tuple(pcm@error)
                                                                        if syndrome in dict:
                                                                            dict[syndrome].append(error)
                                                                        else:
                                                                            dict[syndrome] = [error]
    return dict
genSteaneLookupTable()
