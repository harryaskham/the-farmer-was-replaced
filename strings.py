def join(ss, sep=""):
    out = ""
    for s in ss[:-1]:
        out += str(s) + sep
    out += ss[-1]
    return out