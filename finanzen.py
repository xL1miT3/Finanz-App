from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import csv
import datetime


# alles in Dictionarys speichern / daten durch ein dic. in die csv datei speichern
# {username:{id: passwort, einkommen: ,fixkosten: , ausgaben: {Fleisch: ,ObstUndGemüse: ,Milchprodukte: , Auto: , Sonderausgaben, Anderes: }}}


class Login(Screen):
    # daten aus .kv file
    username = ObjectProperty(None)
    passwort = ObjectProperty(None)
    login_fehler = ObjectProperty(None)
    login = ObjectProperty(None)
    datum_input = ObjectProperty(None)

    def get_username(self):
        with open("username.csv", "w") as file:
            file.write(self.username.text)

    def zeilen_leer(self):
        self.username.text = ""
        self.passwort.text = ""

    # Regestrierungs-Popup
    def fire_popup(self):
        self.zeilen_leer()
        self.login_fehler.color = (1, 1, 1, 1)
        popup = Regestrierung_Popup()
        popup.open()

    def changer_home(self, *args):
        if self.username.text == "" or self.passwort.text == "":
            self.login_fehler.color = (1, .2, .2, 1)
        else:
            # changed screen
            self.manager.transition.direction = 'left'
            self.manager.current = 'second'
            self.zeilen_leer()

    def login_daten(self):
        if self.username.text == "" or self.passwort.text == "":
            self.login_fehler.color = (1, .2, .2, 1)
        else:
            self.login_fehler.color = (1, .2, .2, 0)
            with open("Finanz - Excel.csv", "r") as file:
                for line in file:
                    line_splitted = line.strip().split(",")
                    if line_splitted[0] != self.username.text:
                        continue
                    elif line_splitted[0] == self.username.text and line_splitted[1] == self.passwort.text:
                        # gibt homescreen user info
                        self.get_username()
                        self.changer_home()
                        return True
                if line_splitted[0] not in file:
                    self.login_fehler.color = (1, .2, .2, 1)
                    self.zeilen_leer()

    def datum_weitergabe(self):
        x = Daten_sammlung.get_date()
        Homescreen.datum_homepage(self)
        print(x)


class Regestrierung_Popup(Popup):
    username_1 = ObjectProperty(None)
    passwort_1 = ObjectProperty(None)
    passwort_2 = ObjectProperty(None)
    falsches_psw = ObjectProperty(None)
    username_vorhanden = ObjectProperty(None)

    def zeilen_leer(self):
        self.passwort_1.text = ""
        self.passwort_2.text = ""

    def write_file(self):
        if self.passwort_1.text == self.passwort_2.text:
            Daten_sammlung.add_user(self, self.username_1, self.passwort_1, Daten_sammlung.get_date())
            self.dismiss()
        else:
            self.username_vorhanden.color = (1, .2, .2, 0)
            self.zeilen_leer()
            self.falsches_psw.color = (1, .2, .2, 1)

    def anmelden(self):
        self.i = 0
        if self.username_1.text == "":
            self.username_vorhanden.color = (1, .2, .2, 1)
            self.falsches_psw.color = (1, .2, .2, 0)
        elif self.passwort_1.text == "":
            self.falsches_psw.color = (1, .2, .2, 1)
            self.username_vorhanden.color = (1, .2, .2, 0)
        else:
            # anmeldung überprüft ob name schon in csv
            with open("Finanz - Excel.csv", "r") as file:
                for line in file:
                    line_splitted = line.strip().split(",")
                    if self.username_1.text != line_splitted[0]:
                        continue
                    else:
                        self.username_vorhanden.color = (1, .2, .2, 1)
                        self.zeilen_leer()
                        self.i += 1

                if self.i == 0:
                    self.write_file()


class Daten_sammlung:

    def add_user(self, username, passwort, date):
        try:
            x = username.text
            y = passwort.text
        except AttributeError:
            x = username
            y = passwort

        self.dictionary = {"Username": x, "Passwort": y, "Datum": date, "Einkommen": 0,
                           "Fixkosten": 0, "Ausgaben": 0, "Lebensmittel": 0,
                           "Backwaren": 0, "Fleisch": 0, "Wurst": 0, "ObstUndGemüse": 0, "Milchprodukte": 0,
                           "Getränke": 0,
                           "Süßware": 0, "Sonstiges": 0, "Kosmetik": 0, "Luxus": 0, "Auto": 0, "Verderb": 0,
                           "Eingabe-Datum": 0}

        # writer
        with open("Finanz - Excel.csv", "a", newline="") as csvfile:
            fieldnames = ["Username", "Passwort", "Datum", "Einkommen", "Fixkosten", "Ausgaben", "Lebensmittel",
                          "Backwaren",
                          "Fleisch", "Wurst", "ObstUndGemüse", "Milchprodukte", "Getränke", "Süßware", "Sonstiges",
                          "Kosmetik", "Luxus", "Auto", "Verderb", "Eingabe-Datum"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(self.dictionary)

    def angegebene_datum(self):
        with open("username.csv", "r") as file:
            for line in file:
                if line.strip().split(",")[-1] == line.strip().split(",")[0]:
                    return Daten_sammlung.get_date()
                else:
                    return line.strip().split(",")[-1]

    def neue_daten(self, position, menge):
        Ausgaben_Popup.get_username(self)
        doc = []
        self.datum = Daten_sammlung.angegebene_datum(self)
        self.i = 0
        self.username_count = 0
        self.stimmt = 0
        # liest daten in doc ein
        with open('Finanz - Excel.csv', 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                if row[0] == self.username:
                    self.username_count += 1
        with open('Finanz - Excel.csv', 'r') as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                # username check
                if row[0] == self.username:
                    self.stimmt += 1
                    if row[2] == self.datum:
                        self.i += 1
                    if row[2] != self.datum:
                        if row[2] == "Datum":
                            row[2] = "Datum"
                        elif self.i == 0 and self.stimmt == self.username_count:
                            self.i += 1
                            # datum übernahme / neue Reihe pro tag
                            x = [row[0], row[1], self.datum, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0]
                            x[position] = float(x[position]) + menge  # id += menge
                            # berechnet die insgesamt ausgaben
                            x[5] = float(x[5]) + menge
                            # berechnet die Lebensmittel kosten
                            if position >= 7 and position <= 14:
                                x[6] = float(x[6]) + menge
                            doc.append(x)
                    else:
                        row[position] = float(row[position]) + menge  # id += menge
                        # berechnet die insgesamt asugaben ohne verderb
                        if position < 18:
                            row[5] = float(row[5]) + menge
                        # berechnet die Lebensmittel kosten
                        if position >= 7 and position <= 14:
                            row[6] = float(row[6]) + menge
                    doc.append(row)
                else:
                    doc.append(row)
                    continue
            # löscht die alten csv daten
            with open("Finanz - Excel.csv", "w") as f:
                writer = csv.writer(f)

        # schreibt neue daten in die leete csv datei
        with open("Finanz - Excel.csv", "a") as outputfile:
            writer = csv.writer(outputfile)
            for i in doc:
                writer.writerow(i)

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


class Homescreen(Screen):
    datum_input = ObjectProperty(None)

    def changer_login(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'
        # löscht datum
        with open("username.csv", "w") as file:
            writer = csv.writer(file)
        self.datum_input.text = ""

    def Lebensmittel(self):
        popup = Lebensmittel_Definition()
        popup.open()

    # displays right name for the popup
    def alle(self, name):
        StrokeLabel.text = name
        popup = Ausgaben_Popup(title=name)
        popup.open()

    def show_ausgaben(self):
        popup = Anzeige_Ausgaben()
        popup.open()

    def open_datum(self, datum):
        self.i = 0
        with open("username.csv", "r") as file:
            for line in file:
                line_splitted = line.strip().split(",")
            with open("username.csv", "w") as cfile:
                cfile.write(str(line_splitted[0] + datum))

    def datum_homepage(self):
        # datum festlegen welcher tag eingetragen werden soll
        self.achtung.color = 1, 1, 1, 0
        x = Daten_sammlung.get_date().strip().split("-")
        if self.datum_input.text == "":
            self.datum_input.text = x[2] + "/" + x[1] + "/" + x[0]
            self.datum = "," + self.datum_input.text[6:] + "-" + self.datum_input.text[
                                                                 3:5] + "-" + self.datum_input.text[0:2]
            self.open_datum(self.datum)
        if int(self.datum_input.text[:2]) > 31 or int(self.datum_input.text[3:5]) > 12 or int(
                self.datum_input.text[6:]) > int(x[0]):
            self.datum_input.text = ""
            self.achtung.color = 1, 0.2, 0.2, 1
        if self.datum_input.text != x[2] + "/" + x[1] + "/" + x[0]:
            if len(self.datum_input.text) < 10 or self.datum_input.text[2] and self.datum_input.text[5] != "/":
                self.datum_input.text = ""
                self.achtung.color = 1, 0.2, 0.2, 1
        if self.datum_input.text != x[2] + "/" + x[1] + "/" + x[0] and self.datum_input.text != "" and len(
                self.datum_input.text) == 10:
            self.datum = "," + self.datum_input.text[6:] + "-" + self.datum_input.text[
                                                                 3:5] + "-" + self.datum_input.text[0:2]
            self.open_datum(self.datum)


class Anzeige_Ausgaben(Popup):

    def const(self):
        self.Ausgaben = 0
        self.Lebensmittel = 0
        self.Kosmetik = 0
        self.Luxus = 0
        self.Auto = 0
        self.Verderb = 0
        self.Backwaren = 0
        self.Fleisch = 0
        self.Wurst = 0
        self.ObstUndGemuese = 0
        self.Milchprodukte = 0
        self.drinks = 0
        self.snacks = 0
        self.Sonstiges = 0

    def show_it(self):
        self.const()
        self.datum_falsch.color = 1, 1, 1, 1
        self.text_ausgaben.color = 0, 0, 0, 1
        self.text_Ausgaben.color = 0, 0, 0, 1
        self.text_Ausgaben2.color = 0, 0, 0, 1
        self.richtig = True

        date = Daten_sammlung.get_date().strip().split("-")
        # überprüft ob datum existiert
        if int(self.tag_von.text) > 31 or int(self.monat_von.text) > 12 or int(
                self.jahr_von.text) > int(date[0]) or int(self.tag_bis.text) > 31 or int(self.monat_bis.text) > 12 or int(
                self.jahr_bis.text) > int(date[0]):
            self.datum_falsch.color = 1, 0.2, 0.2, 1
            self.text_ausgaben.color = 0, 0, 0, 0
            self.text_Ausgaben.color = 0, 0, 0, 0
            self.text_Ausgaben2.color = 0, 0, 0, 0
            self.richtig = False
        else:
            with open("username.csv", "r") as u_file:
                for line in u_file:
                    line_splitted = line.strip().split(",")
                    self.username = line_splitted[0]

            with open("Finanz - Excel.csv", "r") as file:
                for line in file:
                    # datum richtig eingetragen ?
                    try:
                        int(self.jahr_von.text) and int(self.monat_von.text) and int(self.tag_von.text) and int(
                            self.jahr_bis.text) and int(self.monat_bis.text) and int(self.tag_bis.text)
                    except ValueError:
                        self.text_ausgaben.color = 0, 0, 0, 0
                        self.text_Ausgaben.color = 0, 0, 0, 0
                        self.text_Ausgaben2.color = 0, 0, 0, 0
                        self.datum_falsch.color = 1, .2, .2, 1
                        self.richtig = False
                        break
                    line_splitted = line.strip().split(",")
                    x = line_splitted[2].split("-")
                    ####### Hier ist der Fehler ########
                    if line_splitted[0] == self.username:
                        if int(x[0]) >= int(self.jahr_von.text) and int(x[1]) >= int(self.monat_von.text) and int(
                                x[2]) >= int(self.tag_von.text) and int(x[0]) <= int(self.jahr_bis.text) and int(
                            x[1]) <= int(self.monat_bis.text) and int(x[2]) <= int(self.tag_bis.text):
                            self.Ausgaben = self.Ausgaben + float(line_splitted[5])
                            self.Lebensmittel = self.Lebensmittel + float(line_splitted[6])
                            self.Backwaren = self.Backwaren + float(line_splitted[7])
                            self.Fleisch = self.Fleisch + float(line_splitted[8])
                            self.Wurst = self.Wurst + float(line_splitted[9])
                            self.ObstUndGemuese = self.ObstUndGemuese + float(line_splitted[10])
                            self.Milchprodukte = self.Milchprodukte + float(line_splitted[11])
                            self.drinks = self.drinks + float(line_splitted[12])
                            self.snacks = self.snacks + float(line_splitted[13])
                            self.Sonstiges = self.Sonstiges + float(line_splitted[14])
                            self.Kosmetik = self.Kosmetik + float(line_splitted[15])
                            self.Luxus = self.Luxus + float(line_splitted[17])
                            self.Auto = self.Auto + float(line_splitted[16])
                            self.Verderb = self.Verderb + float(line_splitted[18])

            if self.richtig == True:
                self.text_ausgaben.text = "Ausgaben: " + str(round(self.Ausgaben, 2)) + "€"
                self.text_Ausgaben.text = "Lebensmittel: " + str(round(self.Lebensmittel, 2)) + " €\nBackware: " + str(
                    self.Backwaren) + " €\nFleisch: " + str(self.Fleisch) + " €\nWurst: " + str(
                    self.Wurst) + " €\nObst und Gemüse: " + str(self.ObstUndGemuese) + " €\nMilchprodukte: " + str(
                    self.Milchprodukte) + " €\nGetränke: " + str(self.drinks) + " €\nSüßware: " + str(
                    self.snacks) + " €\nSonstiges: " + str(self.Sonstiges) + " €\n"
                self.text_Ausgaben2.text = "Kosmetik: " + str(self.Kosmetik) + " €\nLuxus: " + str(
                    self.Luxus) + " €\nAuto: " + str(self.Auto) + " €\nVerderb: " + str(self.Verderb) + " €\n"


class Ausgaben_Popup(Popup):
    hinzufuegen = ObjectProperty(None)
    menge_falsch = ObjectProperty(None)
    menge_hinzugefuegt = ObjectProperty(None)

    def get_username(self):
        with open("username.csv", "r") as u_file:
            for line in u_file:
                line_splitted = line.strip().split(",")
                self.username = line_splitted[0]
                return self.username

    def btn_hinzufuegen(self, name):
        self.name = name
        fieldnames = ["Username", "Passwort", "Datum", "Einkommen", "Fixkosten", "Ausgaben", "Lebensmittel",
                      "Backwaren",
                      "Fleisch", "Wurst", "Obst und Gemüse", "Milchprodukte", "Getränke", "Süßware", "Sonstiges",
                      "Kosmetik / Haushalt", "Sonderausgaben", "Auto", "Verderb"]

        self.zahl = 0
        for i in fieldnames:
            if i == self.name:
                self.position = self.zahl
            else:
                self.zahl += 1

        self.menge_falsch.color = (0, 0, 0, 0)
        try:
            self.menge = float(self.hinzufuegen.text)
            self.menge_hinzugefuegt.color = (.1, .6, 0, 1)
            self.menge_hinzugefuegt.text = "+ " + str(self.menge) + "€"
            self.hinzufuegen.text = ""
            # daten werden weitergeleitet zur eingabe in csv
            Daten_sammlung.neue_daten(self, self.position, self.menge)
            self.zahl = 0
        except ValueError:
            self.hinzufuegen.text = ""


# spezifisches Popup
class Lebensmittel_Definition(Popup):
    # displays right name for the popup
    def alle(self, name):
        StrokeLabel.text = name
        popup = Ausgaben_Popup(title=name)
        popup.open()


class StrokeLabel(Label):
    pass


class StrokeButton(Button):
    pass


# ab hier stoff zum App bauen...
class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = Login()
        screen2 = Homescreen()
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        return my_screenmanager


if __name__ == "__main__":
    MyMainApp().run()
