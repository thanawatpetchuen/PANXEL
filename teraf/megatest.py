import numpy as np
def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root

C = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
print("Length of C : ", len(C))
def list_slice(S, step):
    return [S[i::step] for i in range(step)]
# print(list(iterFlatten(list_slice(C, 7))))
n = 2
for item in range(n):

    print(C[item::n])

    print(np.arange(start=item, stop=len(C), step=n))
    # print(C[item::2])

