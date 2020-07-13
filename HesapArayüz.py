from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

import os, sys, socket, getpass
import datetime as dt
import sqlite3 as sql

from automate_all import open_portakal

try:
    check_onlıne = open_portakal()
except:
    check_onlıne = "0,0"


try:
    os.mkdir(f"C:/Users/{getpass.getuser()}/OneDrive/Masaüstü/database")
except:
    pass

def ayikla(num):#sayı ayıkla
	veri = str(num)
	try:#eğer string cevrilebilicek ise
		return round(float(num), 2)
	except:
		if not veri:#eğer boş string ise
			return 0.0
		elif veri.count(",") >= 2:#eğer birden cok virgül var ise sondakini noktaya dönüştür ve gerikalanını yok et
			d = veri.rsplit(",", 1)
			return round(float(d[0].replace(",", "") + "." + d[1]), 2)
		elif veri.count(",") == 1:#virgülün bir adet olması durumunda
			if len(veri) <= 4:# örn 1,22-12,1-1,2 vs
				return round(float(veri.replace(",", ".")), 2)
			elif len(veri) == 5:#1,236 farklı & 123,5-12,35 farklı
				if veri.index(",") == 1:
					return round(float(veri.replace(",", "")), 2) #1,236 durumu
				elif veri.index(",") >= 2:#123,5-12,36 durumu
					return round(float(veri.replace(",", ".")), 2)
			elif len(veri) == 6:#1,2362-12,236-123,12-1236,5
				if veri.index(",") <= 2:#1,2364-12,236 durumu
					return round(float("".join(veri.replace(",", ""))), 2)
				elif veri.index(",") >= 3:#123,56-1235,5 durumu
					return round(float(veri.replace(",", ".")), 2)
			elif len(veri) >= 7:#12345,6 - 1234,56
				return round(float(veri.replace(",", ".")), 2)

def gecmis_tarih(gün_gecmisi):
    bugun = dt.datetime.now()
    fark = dt.timedelta(days=gün_gecmisi)
    d = bugun - fark
    date = dt.datetime.strftime(d, "%x")
    clock = dt.datetime.strftime(d, "%X")
    return date, clock

def veri_al(yol, tarih, db_ismi, veri_ismi = "*"):
    with sql.connect(yol) as vt:
        imlec = vt.cursor()
        imlec.execute("""SELECT name FROM sqlite_master""")
        if imlec.fetchall() == []:
            return 0.0
        else:
            im = vt.cursor()
            im.execute(f"""SELECT "{veri_ismi}" FROM "{db_ismi}" WHERE TARIH = "{tarih}" """)
            kalan_nakit = im.fetchone()[0]
            return ayikla(kalan_nakit)

database_connect = f"C:/Users/{getpass.getuser()}/OneDrive/Masaüstü/database/hesaplar.db"

def update():
    l = []
    with sql.connect(database_connect) as vt:
        im = vt.cursor()
        im.execute(f"""SELECT * FROM Hesap_detay WHERE TARIH = "{gecmis_tarih(0)[0]}" """)
        a = im.fetchall()
    for i in range(len(a[0])):
        b = a[0][i]
        l.append(b)
    return l#tarih ve saat bilgilerinide cekiyor

try:
    guncel = update()
except:
    guncel = None

try:
    gecmis_nakiti = veri_al(database_connect, gecmis_tarih(1)[0], "Hesap_sonuc", veri_ismi = "KALAN NAKIT")
    gecmis_kredi = veri_al(database_connect, gecmis_tarih(1)[0], "Hesap_sonuc", veri_ismi = "YARININ KREDISI")
except:
    try:
        gecmis_nakiti = veri_al(database_connect, gecmis_tarih(2)[0], "Hesap_sonuc", veri_ismi = "KALAN NAKIT")
        gecmis_kredi = veri_al(database_connect, gecmis_tarih(2)[0], "Hesap_sonuc", veri_ismi = "YARININ KREDISI")
    except:
        try:
            gecmis_nakiti = veri_al(database_connect, gecmis_tarih(3)[0], "Hesap_sonuc", veri_ismi = "KALAN NAKIT")
            gecmis_kredi = veri_al(database_connect, gecmis_tarih(3)[0], "Hesap_sonuc", veri_ismi = "YARININ KREDISI")
        except:
            try:
                gecmis_nakiti = veri_al(database_connect, gecmis_tarih(4)[0], "Hesap_sonuc", veri_ismi = "KALAN NAKIT")
                gecmis_kredi = veri_al(database_connect, gecmis_tarih(4)[0], "Hesap_sonuc", veri_ismi = "YARININ KREDISI")
            except:
                gecmis_nakiti = 0.0
                gecmis_kredi = 0.0

print(gecmis_kredi, type(gecmis_kredi))
print(gecmis_nakiti, type(gecmis_nakiti))


etiket_list = ["KREDI", "NAKIT", "SALON NAKIT", "ONLINE", "SETCARD", "SODEXO", "TICKET", "MULTINET",
                "METROPOL", "KUPON", "CUZDAN", "NAKIT GIDER", "KREDI GIDER", "NAKIT AVANS", "KREDI AVANS", "DASHBOARD", 
                "Fazla/Tip", "ALINAN CARI", "KALAN CARI", "NOTUNUZ"]
input_list = [i-i for i in range(len(etiket_list)-1)]#etiket listesi kadar değer girsin 0 olarak (i-i) - 1 not için (ayıklanmayacak) line:258

hesap_etiket = ["DASHBOARD", "GENEL TOPLAM", "Kasa Acık-Fazla", "BUGÜNÜN KREDISI", "YARININ KREDISI", "FAZLA/TIP", "DÜNÜN NAKITI", "KALAN NAKIT"]
hesap_sonuc = [i-i for i in range(len(hesap_etiket))]#hesap etiket listesi kadar değer girsin 0 olarak (i-i)


def son(name_list, value_list, hangi):
    a = list(zip(name_list, value_list))
    n = ["TARIH", "SAAT"]
    v = [gecmis_tarih(0)[0], gecmis_tarih(0)[1]]
    for i, j in a:
        n.append(i)
        v.append(j)
    if hangi == "name":
        return tuple(n)
    elif hangi == "value":
        return tuple(v)

Config.set('graphics', 'width', '780')
Config.set('graphics', 'height', '660')

class Hesap(App):
    def build(self):
        self.ana_pencere = BoxLayout(orientation="vertical")
        self.üst_pencere = GridLayout(cols=4)
        self.alt_pencere = GridLayout(cols=3, size_hint=(1.0, .1))#buton sayısı kadar ekleme yapılacak(cols=buton sayısı)
        self.etiket_pen = BoxLayout(orientation="vertical")
        self.textinput_pen = BoxLayout(orientation="vertical")
        self.hesap_pen = BoxLayout(orientation="vertical")
        self.hesap2_pen = BoxLayout(orientation="vertical")

        self.say = 0
        self.guncelle = False

        for s, i in enumerate(etiket_list):#etiketler
            if s <= 10:
                self.etiket_pen.add_widget(Label(text=i, font_size="20sp", bold=True, halign="center", color = [.8,.5,.1,2]))
            elif s >= 11 and s <= 14:
                self.etiket_pen.add_widget(Label(text=i, font_size="20sp", bold=True, halign="center", color = [.3,.5,.9,1]))
            elif s >= 15:
                self.etiket_pen.add_widget(Label(text=i, font_size="20sp", bold=True, halign="center", color = [1,.3,.4,1]))

        #inputs
        self.KREDI = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.NAKIT = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.SALON_NAKIT = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.ONLINE = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.SETCARD = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.SODEXO = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.TICKET = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.MULTINET = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.METROPOL = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.KUPON = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.CUZDAN = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.NAKIT_GIDER = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.KREDI_GIDER = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.NAKIT_AVANS = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.KREDI_AVANS = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.DASHBOARD = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.FAZLA = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.ALINAN_CARI = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.KALAN_CARI = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.NOTUNUZ = TextInput(multiline=False, write_tab=False, on_text_validate=self.hesapla)
        self.textinput_pen.add_widget(self.KREDI)
        self.textinput_pen.add_widget(self.NAKIT)
        self.textinput_pen.add_widget(self.SALON_NAKIT)
        self.textinput_pen.add_widget(self.ONLINE)
        self.textinput_pen.add_widget(self.SETCARD)
        self.textinput_pen.add_widget(self.SODEXO)
        self.textinput_pen.add_widget(self.TICKET)
        self.textinput_pen.add_widget(self.MULTINET)
        self.textinput_pen.add_widget(self.METROPOL)
        self.textinput_pen.add_widget(self.KUPON)
        self.textinput_pen.add_widget(self.CUZDAN)
        self.textinput_pen.add_widget(self.NAKIT_GIDER)
        self.textinput_pen.add_widget(self.KREDI_GIDER)
        self.textinput_pen.add_widget(self.NAKIT_AVANS)
        self.textinput_pen.add_widget(self.KREDI_AVANS)
        self.textinput_pen.add_widget(self.DASHBOARD)
        self.textinput_pen.add_widget(self.FAZLA)
        self.textinput_pen.add_widget(self.ALINAN_CARI)
        self.textinput_pen.add_widget(self.KALAN_CARI)
        self.textinput_pen.add_widget(self.NOTUNUZ)

        self.ONLINE.text = check_onlıne#checking onlıne with selenium automation

        if guncel:
            self.guncelle = True
            self.KREDI.text, self.NAKIT.text, self.SALON_NAKIT.text, self.ONLINE.text, self.SETCARD.text, self.SODEXO.text, self.TICKET.text, self.MULTINET.text, self.METROPOL.text, self.KUPON.text, self.CUZDAN.text, \
                self.NAKIT_GIDER.text, self.KREDI_GIDER.text, self.NAKIT_AVANS.text, self.KREDI_AVANS.text, self.DASHBOARD.text, self.FAZLA.text, self.ALINAN_CARI.text, \
                    self.KALAN_CARI.text, self.NOTUNUZ.text = str(guncel[2]), str(guncel[3]), str(guncel[4]), str(guncel[5]), str(guncel[6]), str(guncel[7]), str(guncel[8]), str(guncel[9]), str(guncel[10]), str(guncel[11]), str(guncel[12]), str(guncel[13]), \
                        str(guncel[14]), str(guncel[15]), str(guncel[16]), str(guncel[17]), str(guncel[18]), str(guncel[19]), str(guncel[20]), str(guncel[21])

        for i in hesap_etiket:
            self.hesap_pen.add_widget(Label(text=i, bold=True, italic=True, color = [.2,.9,.3,1], font_size="20sp"))

        self.dash = Label(text="0", bold=True, font_size = "20sp")
        self.genel = Label(text="0", bold=True, font_size = "20sp")
        self.kasa_acık = Label(text="0", bold=True, font_size = "20sp")
        self.dününkre = Label(text="0", bold=True, font_size = "20sp")
        self.kalankre = Label(text="0", bold=True, font_size = "20sp")
        self.fazla = Label(text="0", bold=True, font_size = "20sp")
        self.dününnak = Label(text="0", bold=True, font_size = "20sp")
        self.kalannak = Label(text="0", bold=True, font_size = "20sp")
        self.hesap2_pen.add_widget(self.dash)
        self.hesap2_pen.add_widget(self.genel)
        self.hesap2_pen.add_widget(self.kasa_acık)
        self.hesap2_pen.add_widget(self.dününkre)
        self.hesap2_pen.add_widget(self.kalankre)
        self.hesap2_pen.add_widget(self.fazla)
        self.hesap2_pen.add_widget(self.dününnak)
        self.hesap2_pen.add_widget(self.kalannak)

        for i in [self.etiket_pen, self.textinput_pen, self.hesap_pen, self.hesap2_pen]:
            self.üst_pencere.add_widget(i)

        self.hesap_but = Button(text=">| HESAPLA |<", background_color=[0,1,0,2], border=[0,0,0,0])
        self.save_but = Button(text=">| KAYDET |<", background_color=[0,1,1,2], border=[0,0,0,0])

        self.hesap_but.bind(on_press=self.hesapla)
        self.save_but.bind(on_press=self.save)
        
        for i in (self.hesap_but, self.save_but):
            self.alt_pencere.add_widget(i)

        for i in (self.üst_pencere, self.alt_pencere):
            self.ana_pencere.add_widget(i)

        return self.ana_pencere

    def hesapla(self, zorunlu_nesne):


        self.topla = []
        self.cıkar = sum([ayikla(self.NAKIT_GIDER.text), ayikla(self.NAKIT_AVANS.text)])
        for i in [self.KREDI.text, self.NAKIT.text, self.SALON_NAKIT.text, self.ONLINE.text, self.SETCARD.text, self.SODEXO.text, self.TICKET.text, self.MULTINET.text, self.METROPOL.text, 
                  self.KUPON.text, self.CUZDAN.text, self.KALAN_CARI.text]:
            self.topla.append(ayikla(i))

        self.toplam = str(sum(self.topla)- self.cıkar)
        self.nakit_kalanı = (ayikla(self.NAKIT.text) + ayikla(self.SALON_NAKIT.text) + ayikla(self.FAZLA.text) + gecmis_nakiti) - self.cıkar
        self.kredi_kalanı = (gecmis_kredi + ayikla(self.KREDI.text)) - (ayikla(self.KREDI_GIDER.text) + ayikla(self.KREDI_AVANS.text))

        self.dash.text = str(ayikla(self.DASHBOARD.text))
        self.genel.text = str(ayikla(sum(self.topla)))
        self.kasa_acık.text = str(ayikla(self.genel.text) - ayikla(self.dash.text))
        self.dününkre.text = str(ayikla(gecmis_kredi))
        self.kalankre.text = str(ayikla(self.kredi_kalanı))
        self.fazla.text = str(ayikla(self.FAZLA.text))
        self.dününnak.text = str(ayikla(gecmis_nakiti))
        self.kalannak.text = str(ayikla(self.nakit_kalanı))

    def save(self, zorunlu_nesne):
        if self.say == 0:
            for s, i in enumerate([self.KREDI.text, self.NAKIT.text, self.SALON_NAKIT.text, self.ONLINE.text, self.SETCARD.text, self.SODEXO.text, self.TICKET.text, self.MULTINET.text, self.METROPOL.text, 
                                self.KUPON.text, self.CUZDAN.text, self.NAKIT_GIDER.text, self.KREDI_GIDER.text, self.NAKIT_AVANS.text, self.KREDI_AVANS.text, self.DASHBOARD.text, 
                                self.FAZLA.text, self.ALINAN_CARI.text, self.KALAN_CARI.text]):
                input_list[s] = ayikla(i)
            input_list.append(self.NOTUNUZ.text)
            
            for s, i in enumerate([self.dash.text, self.genel.text, self.kasa_acık.text, self.dününkre.text, self.kalankre.text, self.fazla.text, self.dününnak.text, self.kalannak.text]):
                hesap_sonuc[s] = ayikla(i)

            if guncel:
                with sql.connect(database_connect) as vt:
                    im = vt.cursor()
                    im.execute(f"""DELETE FROM hesap_detay WHERE TARIH = "{gecmis_tarih(0)[0]}" """)
                    im.execute(f"""DELETE FROM hesap_sonuc WHERE TARIH = "{gecmis_tarih(0)[0]}" """)

            with sql.connect(database_connect) as vt:
                im = vt.cursor()
                im.execute("""CREATE TABLE IF NOT EXISTS Hesap_detay {} """.format(son(etiket_list, input_list, "name")))
                im.execute("""INSERT INTO Hesap_detay VALUES {} """.format(son(etiket_list, input_list, "value")))
                im.execute("""CREATE TABLE IF NOT EXISTS Hesap_sonuc {} """.format(son(hesap_etiket, hesap_sonuc, "name")))
                im.execute("""INSERT INTO Hesap_sonuc VALUES {} """.format(son(hesap_etiket, hesap_sonuc, "value")))
                self.say += 1
                self.save_but.text = ">|Kayıt Edildi|<"
        else:
            self.save_but.text = ">| Kapat |<"
            self.save_but.background_color = [9, 0, 0, 1]
            self.save_but.border = [0, 0, 0, 0]
            self.save_but.bind(on_press=self.stop)

    def send(self, zorunlu_nesne):
        pass

if __name__ == "__main__":
        Hesap().run()
