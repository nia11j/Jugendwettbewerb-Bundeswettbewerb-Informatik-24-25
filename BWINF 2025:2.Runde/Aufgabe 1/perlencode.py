import sys
import string # für das Code-Alphabet aus string.ascii_uppercase

# Einlesen
def read_data(filename):
    file = open(filename, "r")
    contents = [l.rstrip() for l in file.readlines()]
    return {'kinds': contents[0],
            'sizes': contents[1],
            'text': contents[2]}

# nach Zahl der aufkommen sortieren
# siehe https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
def sort_by_number(tuple_list):
    return sorted(tuple_list, key=lambda element: element[1])

def analyze_text(text):
    # dict mit "Zeichen: Anzahl von Zeichen" Einträgen:
    alphabet = {c: text.count(c) for c in text}
    # Dict alphabet muss zum sortieren in eine liste von Paaren umgewandelt werden:
    # https://stackoverflow.com/questions/1679384/converting-dictionary-to-list
    return sort_by_number(alphabet.items())

def build_huffman_tree(tuple_list, num_branches):
    # tuple_list is die liste aus (Zeiche, Anzahl) Tupeln, sortiert nach Anzahl

    tree_list = tuple_list.copy()
    # Die nach Anzahl sortierte Liste soll in einen Baum umgewandelt
    # werden. Dabei werden die seltensten Zeichen zuerst genommen und
    # werden zu Gruppen von 'kinds' vielen Zeichen zusammen gefasst;
    # es wird die Gesamtanzahl der zusammengefassten Zeichen berechnet
    # und zur Zahl der Gruppe genommen und in einem Tupel (Gruppe,
    # Zahl) wieder in die liste gesteckt.  Die Liste wird wieder
    # sortiert und danach werden Zeichen und Gruppen gleich behandelt
    # und immer weiter zu Gruppen von Zeichen oder Gruppen zusammen
    # gefasst, bis es nur ein eiziges Element in der Liste gibt.

    while len(tree_list) > 1:
        # nehme die ersten 'num_branches' viele Elemente aus der
        # Liste, wenn es nicht mehr so viele elemente gibt, nehme alle
        # Elemente:
        num_group = min(num_branches, len(tree_list))
        group = tree_list[:num_group]
        tree_list = tree_list[num_group:]

        # Zeichen und Anzahl aus den Tupeln holen:
        symbols = [s[0] for s in group]
        numbers = [s[1] for s in group]

        # Tue das Tupel (symbols, numbers) zurück in tree_list
        tree_list.append((symbols, sum(numbers)))

        # und wieder sortieren:
        tree_list = sort_by_number(tree_list)

    # tree_list oben ist eine Liste mit einem einzigen Tuple, das
    # erste Element davon ist die geschachtelte Liste.  Das zweite
    # Element ist nicht mehr notwendig.
    return tree_list[0][0]


# Die tree_list besteht aus 'kinds' vielen Teilen, die Unter-Listen
# oder Zeichen sein können. Jede Unter-Liste besteht selbst aus
# 'kinds' vielen Teilen, die Unter-Listen oder Zeichen sein können.

# Wir gehen diese Listen und Unterlisten nach Tiefe-zuerst Methode
# durch und zeichnen auf, welchen Weg wir genommen haben.  Für kinds=3
# z.B. ist das Code-Alphabet ['A', 'B', 'C']; wenn wir das erste
# Element der Liste anschauen, so zeichnen wir ein 'A' auf, wenn wir
# das zweite Element ansehen, ein 'B' und beim letzten ein 'C' auf.
# Ist das angesehene Element eine Liste, werden wir auch hier der
# Reihe nach die Elemente anschauen und 'A' für das erste, 'B' für das
# zweite und 'C' für das dritte Element aufzeichnen.  Ist das
# jeweilige Element ein Zeichen, dann geben wir die aufgezeichneten
# Code-Alphabet-Buchstaben auf.  War nun das letzte aufgezeichnete
# Code-Buchstabe ein 'A' oder 'B', dann sehen wir uns das nächste
# Element an (und wechseln dan letzten aufgezeichneten Code-Buchstaben
# von 'A' nach 'B', bzw. von 'B' nach 'C', das heißt wir nehmen den im
# Code-Alphabet jeweils nächsten Buchstaben).  War der letzte
# aufgezeichnete Buchstabe ein 'C', dann sind wir am Ende der gerade
# angeschauten (Unter-) Liste und gehen zur nächsten Liste, wobei wir
# den letzten Buchstaben aus der Aufzeichnung entfernen und den dann
# letzten Code-Buchstaben ebenso verändern wie oben (A->B, B->C
# ... und wenn der dort vorgefundene Buchstabe 'C' war (oder der
# letzte im Code-Alphabet) dann wird dieser auch entfernt.  Und so
# weiter, bis die Aufzeichnung nur aus einem einzigen Buchstaben 'C'
# (allgemein: dem letzten im Code-Alphabet).  Auf diese Weise werden
# alle Zeichen des Eingabe-Alphabets gefunden.

# Statt Buchstaben verwenden wir hier Zahlen, da wir so mit + 1 zum
# nächsten 'Code-Buchstaben' gelangen, ohne Regeln zu definieren (wie
# A->B, B->C usw.).  Wir müssen nur sehen, dass wir nicht über
# 'kinds'-1 hinaus zählen.

def recursive_find(inlist, path):
    found_dict = {}
    for i in range(len(inlist)):
        element = inlist[i]
        nextpath = path.copy()
        nextpath.append(i)
        if type(element) is list:
            found_dict.update(recursive_find(element, nextpath))
        else:
            found_dict[element] = nextpath.copy()
    return found_dict

# Ausgabe Aufgabe A)
# 1. Berechne Codes für die Zeichen im Eingabetext:
#    Einlesen der Eingabedatei
data = read_data(sys.argv[1])
kinds = int(data['kinds'])
sizes = [int(s) for s in data['sizes'].split(' ')]
text = data['text']
#    Häufigkeiten der einzelnen Zeichen in sortierter Liste:
symbol_numbers = analyze_text(text)

#    Berechne Huffman-Baum zur Erzeugung der Codes
code_tree = build_huffman_tree(symbol_numbers, kinds)

#    Nehme Codes aus Baum -> Dict aus "Zeichen: Code"
codes = recursive_find(code_tree, [])

# 2. "Beipackzettel": Gebe Tabelle der Codes aus .
#    Einfach zeilenweise 'Zeichen: Coding' ausgeben (Zahlen zu
#    Buchstaben übersetzen).  Um es etwas schöner aussehen zu lassen,
#    die kürzesten Codes (häufigste Zeichen) zuerst.

# Code-alphabet aus der Anzahl 'kinds' erzeugen:
code_basis = list(string.ascii_uppercase)
if kinds > len(code_basis):
    error("Bitte die Basis des Codes vergrößern")

code_alphabet = code_basis[:kinds]

print("Übersetzungstabelle:")
print(f"Es gibt {kinds} Arten von Perlen: {code_alphabet}.")

# Ausgabe (und gleichzeitig Umwandlung in Dict aus 'Zeichen: Codestring':
translation_dict = {}
for symbol in reversed(symbol_numbers):
    code_string = "".join([code_alphabet[i] for i in codes[symbol[0]]])
    translation_dict[symbol[0]] = code_string
    print(f"\"{symbol[0]}\" => {code_string}")

# 3. Berechne Länge des codierten Eingabetextes:
#    Text zu Liste von Zeichen:
textlist = list(text)
#    Übersetzen
coded_textlist = [translation_dict[a] for a in textlist]
#    Zusammenfügen
coded_text = "".join(coded_textlist)

print("Der Text:")
print(text)
print("ist codiert:")
print(coded_text)
print(f"und ist {len(coded_text)} Perlen lang.")


# Aufgabe B)
# Im codierten Text sollte die häufigste Perle am kleinsten, und mit geringerer Häufigkeit größere Perlen verwendet werden.
# Leider habe ich in der Zeit keine Methode finden können um sicher zu stellen, dass die häufigsten Symbole im Originaltext die kleinsten Perlen benutzen usw.
print("\n\nAufgabe B:")

# Häufigkeiten:
numbers = analyze_text(coded_text)

# Zuordnung Perle (Code-Buchstabe) zu Größe:
# print({n: s for n in numbers for s in reversed(sorted(sizes))})
ordered_alphabet = [n[0] for n in numbers]
perl_sizes = dict(zip(ordered_alphabet, reversed(sorted(sizes))))

print("In der Codierung sind die Perlen so:")
print(", ".join([f"{n} => {perl_sizes[n]} mm" for n in perl_sizes]) + ".")

# Berechnung der Länge der Kette
chain_length = sum([perl_sizes[c] for c in list(coded_text)])
print(f"Damit ist der codierte Text {chain_length} mm lang")
