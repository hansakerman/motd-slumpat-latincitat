#!/usr/bin/env python3
"""
Normaliserar latin_citat.txt (skrapad från Wikipedia) till en enkel
pipe-separerad textfil (latin_citat_normaliserat.txt) med formatet:

    Latinskt citat|Svensk översättning/förklaring

En rad per citat. Städar bort wikipedia-länkar, fotnotsmarkeringar
(^[1]) och kursiv-/fetmarkup (/text/, /*text*/) från källfilen.
"""
import re
import sys

SRC = "latin_citat.txt"
DST = "latin_citat_normaliserat.txt"

# Citat-avsnittet slutar där "Se även"-listan med relaterade
# wikipedialänkar tar vid.
END_MARKER = "Se även"


def load_quote_lines(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == END_MARKER:
            end = i
            break
    return lines[:end]


def join_entries(lines):
    """Slår ihop radbrutna rader till en logisk rad per citat (bullet)."""
    entries = []
    current = None
    for line in lines:
        if re.match(r"^  \* ", line):
            if current is not None:
                entries.append(current)
            current = line.rstrip("\n")
        elif line.strip() in ("", "*") or re.match(r"^[A-ZÅÄÖ]$", line.strip()):
            # tomma rader, ensamma bokstavsrubriker (A, B, C, ...) och
            # lösryckta "*"-rader (formateringsrester)
            continue
        else:
            if current is not None:
                current += " " + line.strip()
    if current is not None:
        entries.append(current)
    return entries


def clean(text):
    text = text[3:].strip()  # ta bort inledande "  * "
    text = re.sub(r"<[^>]*>", "", text)  # wikipedia-/fotnotslänkar <...>
    text = re.sub(r"\^\[\d+\]", "", text)  # fotnotsmarkeringar ^[1]
    text = re.sub(r"/\*(.*?)\*/", r"\1", text)  # fetkursiv /*text*/
    text = re.sub(r"\*([^*]+)\*", r"\1", text)  # kursiv *text*
    text = re.sub(r"/([^/]+)/", r"\1", text)  # kursiv /text/
    text = text.replace("−", "-")  # normalisera minustecken till bindestreck
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([.,;:!?)])", r"\1", text)  # skräpmellanslag
    text = re.sub(r"\(\s*\)", "", text)  # tomma parenteser efter borttagna länkar
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def split_entry(text):
    """Delar en rad i (latinskt citat, svensk översättning/förklaring)."""
    m = re.search(r"\s[–—-]\s?", text)
    if m:
        return text[: m.start()].strip(), text[m.end() :].strip()
    m2 = re.search(r'\s(?=")', text)
    if m2:
        return text[: m2.start()].strip(), text[m2.end() :].strip()
    return text.strip(), ""


# Manuella rättningar av stavfel/obalanserade citattecken-parenteser som
# finns i själva Wikipedia-källartikeln (verifierat mot aktuell version av
# "Latinska ordspråk och talesätt" 2026-09-21). Nyckel = det städade
# citatet, värde = korrigerad översättning.
TRANSLATION_FIXES = {
    "Exempli gratia": (
        'till exempel, exempelvis. Förkortningen e.g. används ofta på '
        'engelska. Förväxlas ofta med i.e., id est, med betydelsen '
        '"det vill säga" (d.v.s.) eller "med andra ord".'
    ),
    "Mens sana in corpore sano": (
        '"En sund själ i en sund kropp" (Citatet används ofta på detta '
        "sätt, vilket är taget ur sitt sammanhang. Som det oftast skrivs "
        "kan det tolkas som att en sund kropp är nödvändigt för att ha en "
        "sund själ. Det fullständiga citatet lyder Orandum est ut sit mens "
        'sana in corpore sano "Låt oss hoppas att det finns en sund själ i '
        'en sund kropp" (Juvenalis, Satirer 10, 356))'
    ),
    "Noli me tangere": (
        '"Rör icke vid mig." De ord, som Jesus yttrade till Maria '
        "Magdalena, då han efter sin uppståndelse uppenbarade sig för "
        "henne som örtagårdsmästaren (Joh. 20:14-17)."
    ),
    "Optime olere occisum hostem": '"En dödad fiende luktar (alltid) gott"',
    "Orandum est ut sit mens sana in corpore sano": (
        '"Låt oss hoppas att det finns en sund själ i en sund kropp" '
        "(Juvenalis, Satirer 10, 356)"
    ),
    "Si tacuisses, philosophus mansisses": (
        '"Om du hade hållit käften, hade du fortfarande varit filosof" '
        "(Seneca)"
    ),
    "Verba volant, (littera) scripta manent.": (
        '"De talade orden förflyger (glöms), det skrivna består."'
    ),
}


def main():
    lines = load_quote_lines(SRC)
    entries = join_entries(lines)
    rows = []
    for raw in entries:
        cleaned = clean(raw)
        phrase, translation = split_entry(cleaned)
        if not phrase:
            continue
        if phrase in TRANSLATION_FIXES:
            translation = TRANSLATION_FIXES[phrase]
        rows.append((phrase, translation))

    # Sortera och ta bort ev. dubbletter på citatet
    seen = set()
    unique_rows = []
    for phrase, translation in rows:
        if phrase in seen:
            continue
        seen.add(phrase)
        unique_rows.append((phrase, translation))
    unique_rows.sort(key=lambda r: r[0].lower())

    with open(DST, "w", encoding="utf-8") as f:
        for phrase, translation in unique_rows:
            f.write(f"{phrase}|{translation}\n")

    print(f"Skrev {len(unique_rows)} citat till {DST}", file=sys.stderr)


if __name__ == "__main__":
    main()
