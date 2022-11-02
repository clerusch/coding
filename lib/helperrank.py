import copy
def rref_mod_2(A):
    """ Applies Gaussian Algorithm to matrix A with coefficients in GF(2).
    """
    m, n = A.shape # m: rows, n: cols
    A = A%2
    Pcols = []
    h = 0 
    k = 0 
    while h<m and k<n:
        found = False
        i=h
        while not found and i<m:
            if A[i,k]==1:
                found = True
                break
            i+=1
        if not found:
            k+=1
        else:
            Pcols.append(k)
            temp = copy.deepcopy(A[h,:])
            A[h,:] = A[i,:]
            A[i,:] = temp
            for i in list(range(h))+list(range(h+1, m)):
                A[i,:] = (A[i,:] + A[i,k]*A[h,:])%2
            h += 1
            k += 1
    return [A, Pcols]

def rankmod2(A):
    return len(rref_mod_2(A)[1])