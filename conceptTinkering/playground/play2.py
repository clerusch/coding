from ldpc import mod2
import numpy as np

def gen_noisified_message(message, p):

    """makes a noisified message under p/3 probability distriubution 
    of x y and z erors occuring"""
    i = np.eye(2)
    x = np.array([[0,1],
                  [1,0]])
    y = np.array([[0,-1j],
                  [1j,0]])
    z = np.array([[1,0],
                  [0,-1]])
    xs, ys, zs = np.array([[]]), np.array([[]]), np.array([[]])
    for _ in range(int(len(message))):
        if np.random.rand() > p/3:
            xs = np.kron(x, xs)
        else:
            xs = np.kron(i, xs)
        if np.random.rand() > p/3:
            ys = np.kron(y, ys)
        else:
            ys = np.kron(i, ys)
        if np.random.rand() > p/3:
            zs = np.kron(z, zs)
        else:
            zs = np.kron(i, zs)
    noisified_message = xs@ys@zs@message % 2
    return noisified_message

i = np.eye(2)
x = np.array([[0,1],
                [1,0]])
y = np.array([[0,-1j],
                [1j,0]])
z = np.array([[1,0],
                [0,-1]])    
ding = np.hstack((np.zeros(x.shape),x))
bla = np.hstack((x, np.zeros(x.shape)))
pi = np.vstack((ding, bla))
# list = csr_matrix(np.array([1,2]))
print(np.hstack((x,i)))


def toricXLogicals(dist):
    """
    binary csr matrix with each row being an x logical operator of a toric code
    """
    H1 = csr_matrix(([1], ([0],[0])), shape=(1,dist), dtype=np.uint8)
    H0 = csr_matrix(np.ones((1, dist), dtype=np.uint8))
    x_logicals = block_diag([kron(H1, H0), kron(H0, H1)])
    x_logicals.data = x_logicals.data % 2
    x_logicals.eliminate_zeros()
    return csr_matrix(x_logicals)