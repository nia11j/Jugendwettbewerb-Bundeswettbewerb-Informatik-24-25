import sys
import math
Quaderliste = []

def wegbeschreibung(stack):
    text = f"Warte {stack.pop(0)} Minuten, laufe "
    zähler = 1
    while len(stack) > 0:
        if stack[0] == 0:
            stack.pop(0)
        else:
            text += f"zu Abschnitt {zähler}. Warte {stack.pop(0)} Minuten, laufe "
        zähler += 1
    text += f"zum Grabmal."
    return text
            
        

#Intervalle sind Paare von Zeitpunkten
def finde_offene_intervalle(jetziges_intervall, nächste_periode):
    nächste_iv_liste = []
    n = math.ceil(jetziges_intervall[0] / (2 * nächste_periode))
    if (2 * n - 1) * nächste_periode <= jetziges_intervall[0]:
        nächste_iv_liste.append((jetziges_intervall[0], 2 * n * nächste_periode))
    min_n = math.ceil(jetziges_intervall[0] / nächste_periode)
    if min_n % 2 == 0:
        min_n += 1
    max_n = int(jetziges_intervall[1] / nächste_periode)
    n = min_n
    while n <= max_n:
        nächste_iv_liste.append((min_n * nächste_periode, (min_n + 1) * nächste_periode))
        n += 2
    return nächste_iv_liste

def das_ägyptische_grabmal(file_name):
    file = open(file_name, "r")
    for line in file.readlines():
        Quaderliste.append(int(line))
    position = 0
    am_anfang = 1
    abschnitte = Quaderliste.pop(0)
    möglichkeiten = []
    while position < abschnitte:
        if position == 0:
            stack = [Quaderliste[0] * (2 * am_anfang - 1)]
            jetzige_möglichkeiten = [(Quaderliste[0] * (2 * am_anfang - 1), (Quaderliste[0] * 2 * am_anfang))]
            position = 1
            am_anfang += 1
        else:
            jetzige_möglichkeiten = möglichkeiten.pop()
            if len(jetzige_möglichkeiten) == 0:
                stack.pop()
                position -= 1
                continue
        jetziges_intervall = jetzige_möglichkeiten.pop(0) 
        intervalle = finde_offene_intervalle(jetziges_intervall, Quaderliste[position])
        if len(intervalle) == 0:
            stack.pop()
            position -= 1
            continue
        else:
            möglichkeiten.append(jetzige_möglichkeiten)
            nächstes_intervall = intervalle[0]
            möglichkeiten.append(intervalle)
            stack.append(nächstes_intervall[0] - jetziges_intervall[0])
            position += 1
    return wegbeschreibung(stack)

if __name__ == "__main__":
    print(das_ägyptische_grabmal(sys.argv[1]))