import sys
def texthopsen(file_name):
    file = open(file_name, "r")
    wortliste = []
    bela = 0
    amira = 1
    schritt = 0
    dic = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21,"v": 22, "w": 23, "x": 24, "y": 25, "z": 26, "ä": 27, "ö": 28, "ü": 29, "ß": 30}
    for line in file.readlines(): 
        for ch in line:
            if ch.lower() in dic:
                wortliste.append(ch.lower())

    while bela < len(wortliste) and amira < len(wortliste):
        bela += dic[wortliste[bela]]
        amira += dic[wortliste[amira]]
        schritt += 1

    if bela > amira:
        return("Bela hat nach " + str(schritt) + " Schritten gewonnen.")
    else:
        return("Amira hat nach " + str(schritt) + " Schritten gewonnen.")
    
if __name__ == "__main__":
    print(texthopsen(sys.argv[1]))