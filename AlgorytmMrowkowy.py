import random
import numpy as np
import copy
from datetime import datetime
from datetime import timedelta
import math

print("Podaj parametry poczatkowe.")

n = input("Podaj dlugosc generowanej nici DNA: ")
n = int(n)

k = input("Podaj dlugosc podciagu: ")
k = int(k)

b = input("Podaj % zawartosc bledow (przedzial (0, 1)): ")
b = float(b)

graf = {}
pierwszy = []
DNA_oryginalne = ""


def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1 - 1] == token2[t2 - 1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def Generator(n, k, b):
    global pierwszy
    global DNA_oryginalne
    # Czesc ponizej odpowiada za generowanie losowej nici DNA
    ile_podciagow = n - k + 1
    oligo_lib = []
    bases = ["A", "C", "G", "T"]
    DNA_lista = []

    for i in range(n):
        DNA_lista.append(random.choice(bases))

    DNA = ' '.join(DNA_lista)
    DNA = DNA.replace(" ", "")
    # DNA jest zapisane w liscie, funkcja wyzej jest po to zeby zamienic liste na string
    DNA_oryginalne = DNA

    print(DNA)

    for i in range(n):
        if i + k - 1 < n:
            oligo_lib.append(DNA[i:i + k])

    # Czesc ponizej odpowiada za bledy negatywne i pozytywne

    lista_bez_duplikatow = list(set(oligo_lib))
    lista_powtorzen = []
    # jezeli sa duplikaty to...
    if len(oligo_lib) != len(lista_bez_duplikatow):
        for i in range(len(oligo_lib)):
            for j in range(len(oligo_lib)):

                if oligo_lib[i] == oligo_lib[j] and i != j and oligo_lib[i] not in lista_powtorzen:
                    lista_powtorzen.append(oligo_lib[i])

    ile_duplikatow = len(oligo_lib) - len(lista_bez_duplikatow)

    # usuwanie duplikatow
    oligo_lib = list(dict.fromkeys(oligo_lib))

    ile_bledow = round(n * b)

    if ile_bledow - ile_duplikatow > 0:
        for i in range(ile_bledow):
            oligo_lib.remove(random.choice(oligo_lib[1:]))
    dna_temp1 = []

    while len(oligo_lib) != ile_podciagow:
        for i in range(k):
            dna_temp1.append(random.choice(bases))

        pozytywne = ' '.join(dna_temp1)
        pozytywne = pozytywne.replace(" ", "")
        dna_temp1.clear()

        if pozytywne not in oligo_lib:
            oligo_lib.append(pozytywne)

    pierwszy = oligo_lib[0]
    oligo_lib.sort()
    return oligo_lib


oligo_lib = Generator(n, k, b)


def dodaj_wierzcholek(v, graf):
    lw = 0
    if v in graf:
        print("Wierzcholek", v, "juz istnieje.")
    else:
        lw = lw + 1
        graf[v] = []


def dodaj_krawedz(v1, v2, e, graf):
    if v1 not in graf:
        print("Wierzcholek ", v1, "nie istnieje.")
    elif v2 not in graf:
        print("Wierzcholek ", v2, "nie istnieje.")
    else:
        temp = [v2, e]
        graf[v1].append(temp)


def stworz_graf(k, oligo_lib):
    for i in range(len(oligo_lib)):
        dodaj_wierzcholek(oligo_lib[i], graf)

    m = 0

    for i in range(len(oligo_lib)):
        for j in range(len(oligo_lib)):
            for m in range(k - 1):
                if oligo_lib[i][m:] == oligo_lib[j][:k - m] and i != j:
                    dodaj_krawedz(oligo_lib[i], oligo_lib[j], m, graf)


stworz_graf(k, oligo_lib)


def Odtwarzanie(rozwiazanie):
    global pierwszy


    DNA_odtworzone = rozwiazanie
    if len(DNA_odtworzone) == 0:
        DNA_odtworzone.insert(0, pierwszy)

    DNA_odtworzone = ' '.join(DNA_odtworzone)
    DNA_odtworzone = DNA_odtworzone.replace(" ", "")


    return DNA_odtworzone



def GeneratorRozwiazanLosowych():
    global DNA_oryginalne

    lista_wierzcholkow = []
    lista_wag = []
    odwiedzone = []
    sciezka_wagi = {}
    rozwiazanie = []
    index = 0
    odwiedzone.append(pierwszy)


    while len(Odtwarzanie(rozwiazanie)) <= len(DNA_oryginalne):

        #oznacza to ze graf w wierzcholki v nie ma zadnych nastepnikow
        if len(graf[odwiedzone[index]]) == 0:
            for i in odwiedzone:
                if len(graf[i]) > 1:
                    for nastepnik in graf[i]: #przegladam nastepnikow
                        if nastepnik[0] not in odwiedzone:
                            print(nastepnik[0])

                            lista_wierzcholkow.append(nastepnik[0])
                            lista_wag.append(nastepnik[1])

                    suma = sum(lista_wag)

                    for i in range(len(lista_wag)):
                        lista_wag[i] = suma/lista_wag[i]
                        if lista_wag[i] == suma:
                            lista_wag[i] = lista_wag[i] * 5
                        if lista_wag[i] == suma / 2:
                            lista_wag[i] = lista_wag[i] * 3
                        if lista_wag[i] == suma / 3:
                            lista_wag[i] = lista_wag[i] * 2

                    wybrany = random.choices(lista_wierzcholkow, weights=lista_wag)[0]


                    waga_wybranego = 0

                    for x in graf[i]:
                        if wybrany == x[0]:
                            waga_wybranego = x[1]


                    rozwiazanie.append(wybrany[k - waga_wybranego:])
                    index += 1
                    odwiedzone.append(wybrany)
                    sciezka_wagi[wybrany] = waga_wybranego
                    lista_wag = []
                    lista_wierzcholkow = []

                    #return GeneratorRozwiazanLosowych(wybrany)

        #jezeli ma nastepnikow
        #if len(graf[v]) > 0:
        else:
            for i in graf[odwiedzone[index]]:
                if i[0] not in odwiedzone:

                    lista_wierzcholkow.append(i[0])
                    lista_wag.append(i[1])

            suma = sum(lista_wag)

            for i in range(len(lista_wag)):
                lista_wag[i] = suma / lista_wag[i]
                if lista_wag[i] == suma:
                    lista_wag[i] = lista_wag[i] * 5
                if lista_wag[i] == suma/2:
                    lista_wag[i] = lista_wag[i] * 3
                if lista_wag[i] == suma/3:
                    lista_wag[i] = lista_wag[i] * 2



            wybrany = random.choices(lista_wierzcholkow, weights=lista_wag)[0]


            waga_wybranego = 0

            for x in graf[odwiedzone[index]]:
                if wybrany == x[0]:
                    waga_wybranego = x[1]

            rozwiazanie.append(wybrany[k - waga_wybranego:])
            index += 1
            odwiedzone.append(wybrany)

            sciezka_wagi[wybrany] = waga_wybranego

            lista_wag = []
            lista_wierzcholkow = []

            
    return sciezka_wagi








test = GeneratorRozwiazanLosowych()



# -------------------------------------------------------/


# ALGORYTM MROWKOWY

czas_trwania = input("Podaj ile czasu ma trwac algorytm: ")
czas_trwania = int(czas_trwania)

ile_mrowek = input("Podaj liczbe mrowek: ")
ile_mrowek = int(ile_mrowek)

alfa = input("Podaj parametr alfa: ")
alfa = int(alfa)

beta = input("Podaj parametr beta: ")
beta = int(beta)

pheromone_vaping = 0.1
pheromone_chance = 0.01
increase_pheromone = 0.001
solution_number = 1
smooth_limit = 35
smooth = 20



graf_feromonow = copy.deepcopy(graf)


for wierzcholek in graf_feromonow:
    for nastepnik in graf_feromonow[wierzcholek]:
        waga = float(1)
        nastepnik[1] = waga

graf_prawdopodobienstwa = copy.deepcopy(graf_feromonow)





def odtwarzanie_mrowki(odpowiedz):
    global pierwszy


    DNA_odtworzone1 = odpowiedz
    if len(DNA_odtworzone1) == 0:
        DNA_odtworzone1.insert(0, pierwszy)

    DNA_odtworzone1 = ' '.join(DNA_odtworzone1)
    DNA_odtworzone1 = DNA_odtworzone1.replace(" ", "")


    return DNA_odtworzone1


def mrowka(graf, graf_feromonow, graf_prawdopodobienstwa):
    odpowiedz = []
    odpowiedz.append(pierwszy)
    global DNA_oryginalne
    global oligo_lib
    sciezka_wagi = {}
    dic_pomocniczy = {}
    v = len(oligo_lib)
    sciezka = []

    sciezka.append(pierwszy)
    index = 0

    uzycie_feromonow = random.random() < pheromone_chance

    while len(odtwarzanie_mrowki(odpowiedz)) <= len(DNA_oryginalne):

        sasiedzi = []
        wagi = []

        for i in graf[sciezka[index]]:
            sasiedzi.append(i[0])
            wagi.append(i[1])



        dic_pomocniczy = dict(zip(sasiedzi, wagi))


        nieodwiedzeni_sasiedzi = sasiedzi

        if nieodwiedzeni_sasiedzi:
            if uzycie_feromonow:
                nieodwiedzeni_prawd = {}

                for i in graf_prawdopodobienstwa[sciezka[index]]:
                    nieodwiedzeni_prawd[i[0]] = i[1]

                wagi = list(nieodwiedzeni_prawd.values())

                nastepny = random.choices(list(nieodwiedzeni_prawd.keys()), weights=wagi)[0]
                while nastepny in sciezka:
                    nastepny = random.choices(list(nieodwiedzeni_prawd.keys()), weights=wagi)[0]



            else:

                nastepny = random.choice(nieodwiedzeni_sasiedzi)
                while nastepny in sciezka:
                    nastepny = random.choice(nieodwiedzeni_sasiedzi)




        else:
            if uzycie_feromonow:
                wagi = []
                for i in sasiedzi:
                    wagi.append(graf_prawdopodobienstwa[i][1])


                nastepny = random.choices(sasiedzi, weights=wagi)
                while nastepny in sciezka:
                    nastepny = random.choices(sasiedzi, weights=wagi)


            else:
                nastepny = random.choice(sasiedzi)
                while nastepny in sciezka:
                    nastepny = random.choice(sasiedzi)


        index += 1


        sciezka_wagi[nastepny] = dic_pomocniczy[nastepny]

        sciezka.append(nastepny)

        odpowiedz.append(nastepny[k - dic_pomocniczy[nastepny]:])

    return sciezka_wagi


print("MROWKA")

najlepsze_rozwiazanie = None




stop = datetime.now() + timedelta(seconds=czas_trwania)

licznik = 0
zbior_najlepszych = []
while datetime.now() < stop:
    paths = []
    paths_suma = []

    najlepsze_rozwiazanie = None

    for i in range(ile_mrowek):

        if licznik != ile_mrowek:

            przejscie_mrowki = GeneratorRozwiazanLosowych()
            #print(przejscie_mrowki)
            paths.append(przejscie_mrowki)
            paths_suma.append(sum(przejscie_mrowki.values()))
            licznik = licznik + 1


        else:
            przejscie_mrowki = mrowka(graf, graf_feromonow, graf_prawdopodobienstwa)
            #print(przejscie_mrowki)
            paths.append(przejscie_mrowki)

            paths_suma.append(sum(przejscie_mrowki.values()))

    #print(paths)
    paths_suma = sorted(paths_suma)
    #print(paths_suma)

    for i in range(len(paths_suma)):
        for j in paths:
            if paths_suma[i] == sum(j.values()):
                temp = j
                paths[i] = j
                j = paths[i]


    zbior_najlepszych.append(paths[0])

    roznica = paths_suma[-1] - paths_suma[0]

    for sciezka in paths:
        if roznica:
            moc_feromonow = (sum(sciezka.values())) / roznica * 0.9
        else:
            moc_feromonow = 1

        for j in sciezka.keys():
            for wierzcholek in graf_feromonow[j]:
                if j in wierzcholek:
                    graf_feromonow[wierzcholek][1] += 1 - moc_feromonow

    for i in graf_feromonow:
        for j in graf_feromonow[i]:
            j[1] *= 1 - pheromone_vaping

    for i in graf_prawdopodobienstwa:
        for j in range(len(graf_prawdopodobienstwa[i])):
            graf_prawdopodobienstwa[i][j][1] = (graf_feromonow[i][j][1] ** alfa)

    for i in graf_prawdopodobienstwa:
        for j in range(len(graf_prawdopodobienstwa[i])):
            graf_prawdopodobienstwa[i][j][1] *= (graf[i][j][1] / 1) ** beta

    for key, value in graf_feromonow.items():
        for wartosc in value:
            if wartosc[1] > smooth_limit:
                minimum = min(value)
                for i in range(len(value)):
                    if value[i] > 0:
                        value[i] = minimum * (1 + math.log(value[i] / minimum, smooth))
            graf_feromonow[key] = value

    pheromone_chance += increase_pheromone






def values_sum(row):

    return sum(list(row.values()))

zbior_najlepszych.sort(key = values_sum)

rozwiazanie_algorytmu = zbior_najlepszych[0]




print(rozwiazanie_algorytmu)
print("Najlepsze rozwiazanie: ", rozwiazanie_algorytmu)

rozwiazanie_mrowki = []
rozwiazanie_mrowki.append(pierwszy)

for ciag in rozwiazanie_algorytmu:
    rozwiazanie_mrowki.append(ciag[k - rozwiazanie_algorytmu[ciag]:])


rozwiazanie_mrowki = ' '.join(rozwiazanie_mrowki)
rozwiazanie_mrowki = rozwiazanie_mrowki.replace(" ", "")
print(rozwiazanie_mrowki)
print(int(levenshteinDistanceDP(DNA_oryginalne, rozwiazanie_mrowki)))