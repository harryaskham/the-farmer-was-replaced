import terminate

def staps(state, xs):
    xs = list(xs)
    xs.insert(1, state)
    aps(xs)

def aps(xs):
    #quick_print(xs)
    if len(xs) == 0:
        return
    if len(xs) == 1:
        return xs[0]()
    if len(xs) == 2:
        return xs[0](xs[1])
    if len(xs) == 3:
        return xs[0](xs[1], xs[2])
    if len(xs) == 4:
        return xs[0](xs[1], xs[2], xs[3])
    if len(xs) == 5:
        return xs[0](xs[1], xs[2], xs[3], xs[4])
    if len(xs) == 6:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5])
    if len(xs) == 7:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6])
    if len(xs) == 8:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7])
    if len(xs) == 9:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8])
    if len(xs) == 10:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9])
    if len(xs) == 11:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10])
    if len(xs) == 12:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11])
    if len(xs) == 13:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12])
    if len(xs) == 14:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13])
    if len(xs) == 15:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14])
    if len(xs) == 16:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15])
    if len(xs) == 17:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16])
    if len(xs) == 18:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17])
    if len(xs) == 19:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18])
    if len(xs) == 20:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19])
    if len(xs) == 21:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20])
    if len(xs) == 22:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21])
    if len(xs) == 23:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21], xs[22])
    if len(xs) == 24:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21], xs[22], xs[23])
    if len(xs) == 25:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21], xs[22], xs[23], xs[24])
    if len(xs) == 26:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21], xs[22], xs[23], xs[24], xs[25])
    if len(xs) == 27:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8], xs[9], xs[10], xs[11], xs[12], xs[13], xs[14], xs[15], xs[16], xs[17], xs[18], xs[19], xs[20], xs[21], xs[22], xs[23], xs[24], xs[25], xs[26])
    return terminate.terminate_(("aps: too many arguments", len(xs)))

def applyN(f, args):
    fa = [f]
    for arg in args:
        fa.append(arg)
    return aps(fa)

def applyS(fs, args):
    fa = list(fs)
    for arg in args:
        fa.append(arg)
    return aps(fa)
