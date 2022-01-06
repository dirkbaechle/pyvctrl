
def vt(rtsoll, at, atged, neigung, niveau):
    return neigung * 1.8317984 * (rtsoll - (atged*0.7 + at*0.3))**0.8281902 + niveau + rtsoll

def vt2(rtsoll, at, atged, neigung, niveau):
    mixedat = (atged*0.7 + at*0.3)
    dar = mixedat - rtsoll
    return niveau + rtsoll - neigung * dar * (1.4347 + 0.021 * dar + 247.9 * 10**-6 * dar * dar)

def main():
    print vt(23.0, 8.0, 8.0, 0.4, 27.0)
    print vt2(23.0, 8.0, 8.0, 0.4, 27.0)

if __name__ == "__main__":
    main()

