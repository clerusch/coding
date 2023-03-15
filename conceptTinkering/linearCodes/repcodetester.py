import numpy as np
from pymatching import Matching

pcm = np.array([[1, 1, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1]])

matching = Matching(pcm)

message = np.array([0,0,0,0,0])

error = np.array([1,1,1,1,1])

# syndrome = pcb@error % 2

# noisy = (message+error) % 2

# corguess = matching.decode(syndrome)

# corrected = (noisy + corguess) % 2

syndrome=(pcm@error)% 2
correction = matching.decode(syndrome)
result = (correction + error)%2

print(message, error,pcm@error, syndrome, correction, result)