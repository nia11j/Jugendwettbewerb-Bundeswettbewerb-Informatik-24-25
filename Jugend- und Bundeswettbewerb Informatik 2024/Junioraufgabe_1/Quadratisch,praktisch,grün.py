import math
import sys

def get_divisors(n):
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sorted(divisors)

def quadratisch_praktisch_grün(file_name):
    file = open(file_name, "r")
    INputliste = []
    factorpairs = []
    dictio = {}
    for line in file.readlines():
        INputliste.append(int(line))
    [Interessant, lang, breit] = INputliste
    if breit > lang:
        größere_seite = breit
        kleinere_seite = lang
    else:
        größere_seite = lang
        kleinere_seite = breit
    PARZELlen = int(Interessant * 1.1)
    for n in range(Interessant, PARZELlen+1):
        factors = get_divisors(n)
        factorpairs = []
        for i in range(len(factors)):
            if n/factors[i] < factors[i]:
                break
            factorpairs.append((factors[i], int(n/factors[i])))
        for pair in factorpairs:
            differenz = kleinere_seite / pair[0] - größere_seite / pair[1]
            dictio[abs(differenz)] = pair # Noch seitenlängen der parzellen anhängen und später ausgeben.
    ausgabe = dictio[min(dictio.keys())]
    text = f"Die beste Aufteilung ergibt {ausgabe[0]} mal {ausgabe[1]} = {ausgabe[0] * ausgabe[1]} Parzellen für {Interessant} Interessenten."
    return text

if __name__ == "__main__":
    print(quadratisch_praktisch_grün(sys.argv[1]))