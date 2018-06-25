import tkinter as tk
import datetime as dt
import matplotlib.pyplot as plot

danasnji_datum = dt.date.today()


class Uporabnik:
    def __init__(self, ime, teza=None, visina=None, bench=None):
        self.ime = ime
        self.teza = teza
        self.visina = visina
        self.bench = bench

    def __repr__(self):
        return "{} je visok/a {} cm in tezek/ka {} kg".format(self.ime, self.visina, self.teza)


def nov_uporabnik(ime, teza, visina, bench):
    uporabnik = Uporabnik(ime, teza, visina, bench)
    return uporabnik


def preveri(ustvarjen, im, tez, visin, benc):
    with open('baza.txt', 'r') as dat:
        for vrstica in dat:
            vrstica = vrstica.split(',')
            if vrstica[0] == im:
                ustvarjen.insert(tk.END, 'Uporabnik ze obstaja!')
                return 1
    if not tez.isdigit():
        ustvarjen.insert(tk.END, 'Popravi tezo!')
        return 1
    if not visin.isdigit():
        ustvarjen.insert(tk.END, 'Popravi visino!')
        return 1
    if not benc.isdigit():
        ustvarjen.insert(tk.END, 'Popravi benc!')
        return 1
    return 0


def preveri_posodobitev(posodobljen, teza, visina, benc):
    if not teza.isdigit():
        if teza == '':
            pass
        else:
            posodobljen.insert(tk.END, 'Popravi tezo!')
            return 1
    if not visina.isdigit():
        if visina == '':
            pass
        else:
            posodobljen.insert(tk.END, 'Popravi visino!')
            return 1
    if not benc.isdigit():
        if benc == '':
            pass
        else:
            posodobljen.insert(tk.END, 'Popravi benc!')
            return 1
    return 0


def prepisi_razen_vrstice(stevilka_vrstice, besedilo):
    vrstice = []
    with open('baza.txt') as dat:
        for vrstica in dat:
            vrstice.append(vrstica)
    vrstice[stevilka_vrstice - 1] = besedilo
    with open('baza.txt', 'w') as dat:
        for vrstica in vrstice:
            dat.write(str(vrstica))


def iz_str_v_datum(datum):
    datum = datum.split('-')
    list_a = []
    for i in datum:
        list_a.append(int(i))
    a = dt.date(list_a[0], list_a[1], list_a[2])
    return a


def ustvari():
    def klik_nov():
        ustvarjen.delete(1.0, tk.END)
        im = ime.get()
        tez = teza.get()
        benc = bench.get()
        datu = datum.get()
        visin = visina.get()
        a = preveri(ustvarjen, im, tez, visin, benc)
        if a == 0:
            uporabnik = nov_uporabnik(im, tez, visin, benc)
            ustvarjen.insert(tk.END, 'Racun je ustvarjen!')
            ime.delete(0, tk.END)
            teza.delete(0, tk.END)
            visina.delete(0, tk.END)
            bench.delete(0, tk.END)
            slovar_teza = dict()
            slovar_visina = dict()
            slovar_benc = dict()
            slovar_teza[datu] = tez
            slovar_visina[datu] = visin
            slovar_benc[datu] = benc
            with open('baza.txt', 'a+') as dat:
                dat.write('{}; {}; {}; {} \n'.format(im, slovar_teza, slovar_benc, slovar_visina))
                dat.close()
            return uporabnik

    okn = tk.Tk()
    tk.Label(okn, text='Ime?').grid(row=0, column=0)
    tk.Label(okn, text='Teza v kg?').grid(row=1, column=0)
    tk.Label(okn, text='Datum tehtanja? (yyyy-mm-dd)').grid(row=2, column=0)
    tk.Label(okn, text='Visina v cm?').grid(row=3, column=0)
    tk.Label(okn, text='Bench v kg?').grid(row=4, column=0)
    ime = tk.Entry(okn)
    ime.grid(row=0, column=1)
    teza = tk.Entry(okn)
    teza.grid(row=1, column=1)
    datum = tk.Entry(okn)
    datum.grid(row=2, column=1)
    datum.insert(0, danasnji_datum)
    visina = tk.Entry(okn)
    visina.grid(row=3, column=1)
    bench = tk.Entry(okn)
    bench.grid(row=4, column=1)
    tk.Button(okn, text='Ustvari racun', command=klik_nov).grid(row=5, column=0)
    ustvarjen = tk.Text(okn, width=20, height=5, wrap=tk.WORD)
    ustvarjen.grid(row=6)
    okn.mainloop()


def prijavi():
    def klik_prijavi():
        opozorilo.delete(1.0, tk.END)
        im = ime.get()
        preveritev = 0
        with open('baza.txt', 'r') as dat:
            for vrstica in dat:
                vrstica = vrstica.split(';')
                if vrstica[0] == im:
                    opozorilo.insert(tk.END, 'Prijava uspesna!')
                    preveritev = 1
        if preveritev == 0:
            ime.delete(0, tk.END)
            opozorilo.insert(tk.END, 'Uporabnisko ime ne obstaja.')
        if preveritev == 1:

            def klik_dodaj():
                posodobljen.delete(1.0, tk.END)
                tez = teza.get()
                benc = bench.get()
                datu = datum.get()
                visin = visina.get()
                a = preveri_posodobitev(posodobljen, tez, visin, benc)
                if a == 0:
                    posodobljen.insert(tk.END, 'Racun je posodobljen!')
                    teza.delete(0, tk.END)
                    visina.delete(0, tk.END)
                    bench.delete(0, tk.END)
                    with open('baza.txt', 'r+') as datoteka_a:
                        stevec_vrstic = 1
                        for vrstica_a in datoteka_a:
                            vrstica_a = vrstica_a.split('; ')
                            if vrstica_a[0] == im:
                                slovar_teza = eval(vrstica_a[1])
                                if tez != '':
                                    slovar_teza[datu] = tez
                                    vrstica_a[1] = str(slovar_teza)
                                slovar_bench = eval(vrstica_a[2])
                                if benc != '':
                                    slovar_bench[datu] = benc
                                    vrstica_a[2] = str(slovar_bench)
                                slovar_visina = eval(vrstica_a[3])
                                if visin != '':
                                    slovar_visina[datu] = visin
                                    vrstica_a[3] = str(slovar_visina)
                                prepisi_razen_vrstice(stevec_vrstic, '; '.join(vrstica_a))
                            stevec_vrstic += 1

            oknice = tk.Tk()

            def narisi_graf():
                klik_dodaj()
                datumi_t = []
                teze = []
                datumi_b = []
                benci = []
                datumi_v = []
                visine = []
                with open('baza.txt', 'r+') as datoteka_b:
                    for vrst in datoteka_b:
                        vrst = vrst.split(';')
                        if vrst[0] == im:
                            slovar_t = eval(vrst[1])
                            for datum_a, teza_a in sorted(slovar_t.items()):
                                datumi_t.append(iz_str_v_datum(datum_a))
                                teze.append(int(teza_a))
                            slovar_b = eval(vrst[2])
                            for datum_b, teza_b in sorted(slovar_b.items()):
                                datumi_b.append(iz_str_v_datum(datum_b))
                                benci.append(int(teza_b))
                            slovar_v = eval(vrst[3])
                            for datum_v, visina_v in sorted(slovar_v.items()):
                                datumi_v.append(iz_str_v_datum(datum_v))
                                visine.append(int(visina_v))
                x_v = datumi_v
                x_t = datumi_t
                x_b = datumi_b
                y_v = visine
                y_t = teze
                y_b = benci
                plot.plot(x_t, y_t)
                plot.plot(x_b, y_b)
                plot.plot(x_v, y_v)
                plot.gcf().autofmt_xdate()
                plot.legend(['Teza (kg)', 'Benc (kg)', 'visina (cm)'], loc='upper left')
                plot.show()

            tk.Label(oknice, text='Izpolnite podatke, ki jih zelite posodobiti.').grid(row=0, column=0)
            tk.Label(oknice, text='Teza v kg?').grid(row=1, column=0)
            tk.Label(oknice, text='Datum tehtanja? (yyyy-mm-dd)').grid(row=2, column=0)
            tk.Label(oknice, text='Visina v cm?').grid(row=3, column=0)
            tk.Label(oknice, text='Bench v kg?').grid(row=4, column=0)
            teza = tk.Entry(oknice)
            teza.grid(row=1, column=1)
            datum = tk.Entry(oknice)
            datum.grid(row=2, column=1)
            datum.insert(0, danasnji_datum)
            visina = tk.Entry(oknice)
            visina.grid(row=3, column=1)
            bench = tk.Entry(oknice)
            bench.grid(row=4, column=1)
            tk.Button(oknice, text='Posodobi racun', command=klik_dodaj).grid(row=5, column=0)
            tk.Button(oknice, text='Narisi graf', command=narisi_graf).grid(row=5, column=1)
            posodobljen = tk.Text(oknice, width=20, height=5, wrap=tk.WORD)
            posodobljen.grid(row=6)
            oknice.mainloop()

    okn = tk.Tk()
    tk.Label(okn, text='Ime?').grid(row=0)
    ime = tk.Entry(okn)
    ime.grid(row=1)
    tk.Button(okn, text='Prijavi se', command=klik_prijavi).grid(row=2)
    opozorilo = tk.Text(okn, width=20, height=3, wrap=tk.WORD)
    opozorilo.grid(row=6)
    okn.mainloop()


okno = tk.Tk()
okno.title('Fitnes program')
zgoraj = tk.Frame(okno)
spodaj = tk.Frame(okno)

pozdrav = tk.Label(zgoraj, text='Pozdravljeni!').grid(row=0, column=0)
nov = tk.Button(spodaj, text='Nov uporabnik', command=ustvari).grid(row=0, column=0)
obstojec = tk.Button(spodaj, text='Obstojec uporabnik', command=prijavi).grid(row=0, column=1)

zgoraj.pack()
spodaj.pack()

okno.mainloop()
