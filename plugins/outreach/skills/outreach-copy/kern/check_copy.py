#!/usr/bin/env python3
"""Prüft Cold-Mail-Copy gegen die mechanisch prüfbaren Regeln der Copy-Lehre.

Aufruf:
    python3 check_copy.py <copy-datei.md>

Erwartetes Format (siehe beispiele.md): jede Mail unter einer Überschrift
"## Step <n>: …" (oder "## Zusatz-Step: Dringlichkeit"), darin eine Zeile
"Betreff: …" ("Betreff: (leer …)" für Mails im Thread), danach der Body bis
zur Grußformel ("Viele Grüße" o. Ä.), dann die Signatur.

Exit-Code 0: keine harten Fehler. Exit-Code 1: mindestens ein harter Fehler.
Hinweise (weich) sind kein Fehler, müssen aber begründet werden können.
"""
import re
import sys

INTRO_WORDS = 30  # Obergrenze des Intros, wird für {{Intro}} eingerechnet

SPAM = [
    "gratis", "100 %", "100%", "garantiert", "garantie", "jetzt zugreifen", "jetzt handeln",
    "begrenztes angebot", "nur heute", "exklusives angebot", "hier klicken", "rabatt",
    "sonderpreis", "gewinner", "sie haben gewonnen", "dringend", "risikofrei", "ohne risiko",
    "geld verdienen",
]
SUBJECT_EXTRA = ["kostenlos", "kostenfrei", "unverbindlich"]

PITCH = [
    r"\bwir helfen\b",
    r"\bwir sind (ein|eine|der|die|seit)\b",
    r"\bwir bieten\b",
    r"\bseit (über |mehr als )?\d+ jahren\b",
    r"\bals (zertifiziert\w*|offiziell\w*|google|meta)\b[^.?!]{0,30}\bpartner\b",
    r"\bmein name ist\b",
    r"\bunser unternehmen\b",
]
OFFER_TERMS = r"\b(analyse|audit|potenzial-check|erstgespräch|beratung|strategiegespräch)\b"
NEGATION = r"(statt|kein|keine|keinen|ohne)\s+(\w+\s+){0,2}$"
SECOND_CTA = (r"\boder\b[^.?!]{0,80}\b(buch\w*|klick\w*|vereinbar\w*|reservier\w*|"
              r"anruf\w*|ruf\w* (mich )?an|termin\w*)\b")
LINK = r"https?://|www\.|calendly|hier buchen"
TRANSLIT = (r"\b\w*(fuer|ueber|gruess|koennen|koennt|moecht|persoenlich|moeglich|waere|"
            r"haette|groess|naechst|spaeter|muess|wuerd|schoen|fuehr|gefaell|auffaell)\w*")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅‼⁉]")
GREETING = re.compile(r"^(viele|beste|liebe|herzliche|schöne)\s+grüße\b|^grüße\b|^gruß\b|^lg\b",
                      re.IGNORECASE)
HEADING = re.compile(r"^##\s+(Zusatz-Step|Step)\b\s*(\d*)(.*)$", re.IGNORECASE)
ANNOUNCE = r"\b(website|webseite|entwurf|idee|ideen|konzept|angebot|setup|anzeigen)\b.*\bfür\b|ist fertig"


def parse(text):
    mails, current = [], None
    for line in text.splitlines():
        m = HEADING.match(line.strip())
        if m:
            current = {"title": line.strip("# ").strip(), "kind": m.group(1).lower(),
                       "num": int(m.group(2)) if m.group(2) else None, "rest": m.group(3),
                       "subject": None, "body": [], "sig": [], "in_sig": False}
            mails.append(current)
            continue
        if current is None:
            continue
        if line.startswith("#") or line.strip() == "---":
            current["in_sig"] = True  # Abschnitt zu Ende, Rest ignorieren
            current["closed"] = True
            continue
        if current.get("closed"):
            continue
        stripped = line.strip()
        if current["subject"] is None and stripped.lower().startswith("betreff:"):
            value = stripped.split(":", 1)[1].strip()
            current["subject"] = "" if (not value or value.lower().startswith("(leer")) else value
            continue
        if current["in_sig"]:
            if stripped:
                current["sig"].append(stripped)
            else:
                current["closed"] = True  # Leerzeile nach Signatur beendet die Mail
            continue
        if GREETING.match(stripped):
            current["in_sig"] = True
            current["sig"].append(stripped)
            continue
        if stripped:
            current["body"].append(stripped)
    return mails


def role(mail):
    title = mail["title"].lower()
    if mail["kind"] == "zusatz-step" or "dringlichkeit" in title:
        return "dringlichkeit", 60, False
    n = mail["num"] or 0
    if n == 1:
        return "entry", 120, True
    if n == 2:
        return "erinnerung", 50, False
    if n == 3:
        return "neuer winkel", 80, True
    return "abschied", 60, False


def count_words(body_lines):
    words = 0
    for token in " ".join(body_lines).split():
        if re.fullmatch(r"\{\{\s*intro\s*\}\}[.,]?", token, re.IGNORECASE):
            words += INTRO_WORDS
        elif re.search(r"\{\{.*?\}\}", token):
            continue
        elif re.search(r"\w", token):
            words += 1
    return words


def check(mail):
    hard, soft = [], []
    kind, limit, needs_subject = role(mail)
    subject = mail["subject"] or ""
    body = "\n".join(mail["body"])
    low = body.lower()
    full = "\n".join([subject, body] + mail["sig"])

    words = count_words(mail["body"])
    if words > limit:
        hard.append(f"Wortlimit: {words} Wörter, erlaubt {limit}")
    if kind == "entry" and words < 50:
        soft.append(f"Entry Mail hat nur {words} Wörter: trägt der Bezug?")

    if "—" in full or "–" in full:
        hard.append("Gedankenstrich (— oder –) gefunden")
    if re.search(r"[ \t]-[ \t]", body):
        soft.append("Bindestrich mit Leerzeichen als Trenner im Body")
    if '"' in body or '"' in subject:
        hard.append("gerades Anführungszeichen (\") statt „…“")
    if body.count("„") != body.count("“"):
        hard.append("Anführungszeichen nicht geschlossen („ ohne “)")
    for pattern in PITCH:
        hit = re.search(pattern, low)
        if hit:
            hard.append(f"Pitch: „{hit.group(0)}“")
    for hit in re.finditer(r"\[[^\]]+\]", body + " " + subject):
        hard.append(f"sichtbarer Platzhalter {hit.group(0)}")
    if EMOJI.search(full):
        hard.append("Emoji oder Symbol gefunden")
    if "**" in body or any(re.match(r"^[-*•]\s", l) for l in mail["body"]):
        soft.append("Formatierung (Fettdruck oder Aufzählung) im Body")
    if len(re.findall(r"\bkostenlos\w*", low)) > 1:
        soft.append("„kostenlos“ mehr als einmal")
    for word in SPAM:
        if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", low):
            soft.append(f"Spam-Wort im Body: „{word}“")
    if re.search(SECOND_CTA, low):
        hard.append("zweiter CTA (oder … buchen/klicken/Termin)")
    links = len(re.findall(LINK, low))
    if kind == "entry" and links:
        hard.append("Link in der Entry Mail")
    elif kind == "erinnerung" and links:
        soft.append("Link in Step 2 (Links erst ab Step 3)")
    elif links > 1:
        soft.append(f"{links} Links, höchstens einer")
    if re.search(r"\{\{\s*intro\s*\}\}", low) and kind != "entry":
        hard.append("{{Intro}} steht außerhalb der Entry Mail")
    if kind == "entry":
        for hit in re.finditer(OFFER_TERMS, low):
            before = low[max(0, hit.start() - 30):hit.start()]
            if not re.search(NEGATION, before):
                hard.append(f"verbotener Offer-Begriff: „{hit.group(0)}“")
    else:
        lines = mail["body"][1:] if mail["body"] else []
        if lines and re.match(r"^[^.?!:]{1,30}:", lines[0]) and len(lines[0].split(":")[0].split()) <= 3:
            hard.append(f"Doppelpunkt-Opener: „{lines[0].split(':')[0]}:“")
    if mail["body"] and not re.match(r"^(hallo|guten tag|servus|moin|grüß)", mail["body"][0], re.IGNORECASE):
        soft.append("keine Anrede am Anfang")
    hit = re.search(TRANSLIT, full.lower())
    if hit:
        hard.append(f"Umlaut-Ersatz: „{hit.group(0)}“")

    # Betreff
    if needs_subject and not subject:
        hard.append("Betreff fehlt (Step 1 und 3 öffnen einen neuen Thread)")
    if not needs_subject and subject:
        hard.append(f"Betreff „{subject}“ muss leer sein (Mail läuft im Thread)")
    if subject:
        sl = subject.lower()
        for word in SPAM + SUBJECT_EXTRA:
            if re.search(r"(?<!\w)" + re.escape(word), sl):
                hard.append(f"Spam-Wort im Betreff: „{word}“")
        if re.search(r"\{\{\s*(vorname|firstname|first_name|first name)\s*\}\}", sl):
            hard.append("Vorname im Betreff")
        if re.search(r"\{\{\s*(companyname|company|lead\.company|firmenname)\s*\}\}", sl):
            soft.append("roher Firmenname im Betreff, nur bereinigter Kurzname {{Firma}}")
        if len(re.sub(r"\{\{.*?\}\}", "x", subject).split()) > 5:
            soft.append("Betreff länger als 5 Wörter")
        if "!" in subject or re.search(r"\b[A-ZÄÖÜ]{4,}\b", subject):
            soft.append("Betreff mit Ausrufezeichen oder Großbuchstaben-Wort")
        if re.search(ANNOUNCE, sl):
            soft.append("Betreff klingt nach Ankündigung („… für …“, „ist fertig“)")
    return kind, words, limit, hard, soft


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        print(f"Datei nicht lesbar: {error}")
        sys.exit(2)

    mails = parse(text)
    if not mails:
        print("Keine Mail gefunden. Erwartet werden Überschriften wie „## Step 1: Entry Mail“.")
        sys.exit(2)

    total_hard = total_soft = 0
    for mail in mails:
        kind, words, limit, hard, soft = check(mail)
        status = "FEHLER" if hard else ("Hinweis" if soft else "OK")
        print(f"{mail['title']}: {words}/{limit} Wörter [{status}]")
        for item in hard:
            print(f"  FEHLER: {item}")
        for item in soft:
            print(f"  Hinweis: {item}")
        total_hard += len(hard)
        total_soft += len(soft)

    print()
    print(f"{len(mails)} Mails geprüft: {total_hard} Fehler, {total_soft} Hinweise.")
    if total_hard:
        print("Fehler korrigieren und den Prüfdurchlauf von vorne starten.")
    sys.exit(1 if total_hard else 0)


if __name__ == "__main__":
    main()
