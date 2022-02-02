# menu-scraper

Scraping denního menu z okolních restaurací. Zobrazení nabídky jako Flask webová stránka.

## Soubory

- `data` - `json` soubory s informacemi o denním menu, pojmenování rok + číslo týdne
- `templates` - `html` stránky pro Flask
- `app.py` - hlavní Flask skript, zobrazí dnešní memnu z `json` souborů
- `scraper.py` - stáhne denní menu z vybraných podniků a uloží je do složky `data`

## Scraping

Společné funkce

- `zpracuj_odpoved_serveru()` = vrací html zadané stránky
- `uloz_menu_do_json()` = uloží slovník s denním menu do složky `data`
- `vypis_do_konzole()` = výpis s možností zvýraznit oblíbené jídlo

## Struktura souboru json

- Název restaurace v názvu souboru
- Název dne a datum
- Typ jídla (`polevka_i`/`menu_i`)
- Název jídla, cena v CZK

```json
{
  "Pondělí 31.1.2022": {
    "polevka_1": {
      "Česneková s opečeným chlebem": 0
    },
    "menu_1": {
      "Kuřecí prsa zapečená s rajčaty, bazalkou a mozzarellou, hranolky": 135
    },
    "menu_2": {
      "Hovězí guláš s cibulí a feferonkou, špekové knedlíky": 139
    },
    "menu_3": {
      "Smažený květák, vařené brambory, tatarská omáčka": 129
    }
  },
  "Úterý 1.2.2022": {
      ...
  }
}
```

## TODO

- [x] Scraping restaurací
- [x] Jednotný formát `json` souboru
- [x] Výpis z `json` na web
- [x] Flask na server
- [ ] HTML layout a styl = ukaž dnes/celý týden
- [ ] Automatické spuštění scraperu každý týden
- [ ] Automatické načtení dnešního týdne
