import os
import json
from pprint import pprint
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def zpracuj_odpoved_serveru(url):
    """
    Odesli pozadavek na prislusnou adresu 'url' a vracenou
    odpoved parsuj pomoci 'BeautifulSoup'.
    """
    odpoved = requests.get(url)
    if odpoved.status_code == 200:
        print(f"OK - {url}")
    return BeautifulSoup(odpoved.text, 'html.parser')


def uloz_menu_do_json(slovnik: dict, nazev_souboru: str) -> None:
    with open(os.path.join("data", nazev_souboru), mode="w",
              encoding='utf-8') as json_soubor:
        json.dump(slovnik, json_soubor, ensure_ascii=False, indent=2)
    print(f"Soubor {nazev_souboru} ulozen.")


def vypis_do_konzole(tyden_slovnik, restaurace, oblibene_jidlo=''):
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    print(f"\n{restaurace:=^70}\n")
    for den, jidla in tyden_slovnik.items():
        print(f"{den:-^70}")
        for radek in jidla.values():
            nazev_jidla, cena = list(*radek.items())
            if oblibene_jidlo in nazev_jidla:
                print(f"• {R}{nazev_jidla} - {cena} Kč{W}")
            else:
                print(f"• {nazev_jidla} - {cena} Kč")


def taste_of_india(datum,
                   restaurace="Taste_of_india",
                   url="https://www.taste-of-india.cz/#daily-menu"):
    jmeno_souboru = f"{datum}_{restaurace}_menu.json"
    menu_slovnik = denni_menu_india(url, jmeno_souboru)
    uloz_menu_do_json(menu_slovnik, jmeno_souboru)
    # vypis_do_konzole(menu_slovnik, restaurace, oblibene_jidlo='Jalfrezi')


def denni_menu_india(url: str, jmeno_souboru: str) -> dict:
    """
    Funkce, ktera zajistuje cely proces web scrapingu.
    """
    soup = zpracuj_odpoved_serveru(url)
    sekce_menu = soup.find("ul", {"class": "daily-menu"})
    vsechny_li = sekce_menu.find_all("li")
    tento_tyden = [filtruj_jidlo_z_radku_india(li) for li in vsechny_li[1:6]]
    # pprint(tento_tyden)
    tento_tyden_slovnik = {den.pop('den'): den for den in tento_tyden}
    # pprint(tento_tyden_slovnik)
    return tento_tyden_slovnik


def filtruj_jidlo_z_radku_india(li_tag):
    """
    Z kazdeho radku ('\n') vyber jidlo a jeho cenu
    a zabal je do slovniku

    :return: dict
    """
    def jidlo_a_cena(radek: str) -> dict:
        """Pomocna funkce pro oddeleni nazvu jidla a ceny"""
        *jidlo, cena = radek.split(' ')
        return {' '.join(jidlo): int(cena[:-2])}

    radky = li_tag.get_text("\n").splitlines()
    # '&nbsp' = nonbreaking space is parsed as '\xa0'
    radky = [r.replace("\xa0", " ") for r in radky]
    return {
        "den": radky[0] + "2022",
        "polevka_1": jidlo_a_cena(radky[1]),
        "menu_1": jidlo_a_cena(radky[2]),
        "menu_2": jidlo_a_cena(radky[3]),
        "menu_3": jidlo_a_cena(radky[4]),
        "menu_4": jidlo_a_cena(radky[5])
    }


def na_purkynce(datum,
                restaurace="Na_Purkynce",
                url="https://www.menicka.cz/api/iframe/?id=2647"):
    jmeno_souboru = f"{datum}_{restaurace}_menu.json"
    menu_slovnik = denni_menu_purkynce(url, jmeno_souboru)
    uloz_menu_do_json(menu_slovnik, jmeno_souboru)


def denni_menu_purkynce(url, jmeno_souboru):
    soup = zpracuj_odpoved_serveru(url)
    sekce_menu = soup.find_all("table", {"class": "menu"})
    datumy = soup.find_all("h2")
    tento_tyden = [filtr_radku_purkynka(den) for den in sekce_menu[:5]]
    # pprint(tento_tyden)
    tento_tyden_slovnik = {
        datum.get_text().strip(): radek
        for datum, radek in zip(datumy, tento_tyden)
    }
    return tento_tyden_slovnik


def filtr_radku_purkynka(table_tag):
    _, polevka, *jidla = table_tag.get_text().splitlines()

    def jidlo_a_cena(radek):
        jidlo, cena = radek.split('/')
        return {jidlo[3:].strip(): int(cena[-6:-2])}

    return {
        # "den":
        "polevka_1": {
            polevka.split('/')[0][4:].strip(): 0
        },
        "menu_1": jidlo_a_cena(jidla[0]),
        "menu_2": jidlo_a_cena(jidla[1]),
        "menu_3": jidlo_a_cena(jidla[2])
    }


if __name__ == '__main__':
    datum = datetime.now().strftime("%Y%W")  # ROK+cislo tydne
    taste_of_india(datum)
    na_purkynce(datum)
