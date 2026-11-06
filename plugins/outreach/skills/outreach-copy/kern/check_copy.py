#!/usr/bin/env python3
"""Prüft Cold-Mail-Copy gegen die mechanisch prüfbaren Regeln der Copy-Lehre.

Aufruf:
    python3 check_copy.py <copy-datei.md> [--firma "<Kurzname>"] …

Der Kurzname des Leads (bereinigt, ohne Rechtsform) zählt im Betreff B als ein Wort, wie in der
App. Er kommt aus --firma (mehrfach möglich) oder einer Zeile "Kurzname: …" in der Datei;
{{Firma}} und andere Platzhalter zählen ohnehin als ein Wort.

Erwartetes Format (siehe beispiele.md): jede Mail unter einer Überschrift
"## Step <n>: …" (oder "## Zusatz-Step: Dringlichkeit"), darin eine Zeile
"Betreff: …" (nur Step 1; "Betreff: (leer …)" für Step 2 bis 4 im Thread), in Step 1 optional
"Betreff B: …" (persönlicher Betreff des Betreff-Tests, 3 bis 6 Wörter), danach der Body bis
zur Grußformel ("Viele Grüße" o. Ä., nach zwei Leerzeilen), dann die Signatur und
nach einer Leerzeile die Abmeldezeile (Step 1 und 3).

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
OPT_OUT = r"\b(stopp?|abmeld\w*|abbestell\w*|austragen|unsubscribe|opt-?out)\b"
# Abmeldezeile seit 05.11.2026 „Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.“;
# die frühere Fassung „…, dann melde ich mich nicht mehr.“ trägt dasselbe Merkmal.
OPT_OUT_LINES = ("kein thema für", "a priority right now")
SIGN_OFF_GAP = 2  # Leerzeilen zwischen letztem Satz und Grußformel
KURZNAME = re.compile(r"^kurzname\s*:\s*(.+)$", re.IGNORECASE)
ANNOUNCE = r"\b(website|webseite|entwurf|idee|ideen|konzept|angebot|setup|anzeigen)\b.*\bfür\b|ist fertig"


def parse(text):
    mails, current = [], None
    for line in text.splitlines():
        m = HEADING.match(line.strip())
        if m:
            current = {"title": line.strip("# ").strip(), "kind": m.group(1).lower(),
                       "num": int(m.group(2)) if m.group(2) else None, "rest": m.group(3),
                       "subject": None, "subject_b": None, "body": [], "sig": [], "tail": [], "in_sig": False,
                       "blank": 0, "gap": None}
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
        if KURZNAME.match(stripped):
            continue  # Angabe für die Prüfung, kein Mailtext
        if current["subject_b"] is None and re.match(r"^betreff\s+b\s*:", stripped, re.IGNORECASE):
            current["subject_b"] = stripped.split(":", 1)[1].strip()
            continue
        if current["subject"] is None and stripped.lower().startswith("betreff:"):
            value = stripped.split(":", 1)[1].strip()
            current["subject"] = "" if (not value or value.lower().startswith("(leer")) else value
            continue
        if current["in_sig"]:
            if not stripped:
                current["after_sig"] = True  # Leerzeile nach der Signatur, danach folgt die Abmeldezeile
            elif current.get("after_sig"):
                current["tail"].append(stripped)
            else:
                current["sig"].append(stripped)
            continue
        if GREETING.match(stripped):
            current["in_sig"] = True
            current["sig"].append(stripped)
            current["gap"] = current["blank"] if current["body"] else None
            continue
        if stripped:
            current["body"].append(stripped)
            current["blank"] = 0
        else:
            current["blank"] += 1
    return mails


def role(mail):
    """Rolle, Wortlimit, ob die Mail einen Betreff trägt, ob die Abmeldezeile darunter steht.

    Seit 05.11.2026 laufen alle Mails im Thread von Step 1: nur Step 1 hat einen Betreff,
    die Abmeldezeile steht weiter in Step 1 und Step 3.
    """
    title = mail["title"].lower()
    if mail["kind"] == "zusatz-step" or "dringlichkeit" in title:
        return "dringlichkeit", 60, False, False
    n = mail["num"] or 0
    if n == 1:
        return "entry", 120, True, True
    if n == 2:
        return "erinnerung", 50, False, False
    if n == 3:
        return "neuer winkel", 80, False, True
    return "abschied", 60, False, False


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
    kind, limit, needs_subject, needs_opt_out = role(mail)
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
    if kind == "neuer winkel":
        if "?" not in body:
            hard.append("Step 3 ohne Schlussfrage: dieselbe Frage wie in Step 1 (mit dem Wort für die Sache, wo die Karte eins hat)")
        if len(mail["body"]) > 1 and re.match(r"^(Ein|Eine|Einen|Einem|Einer|Der|Die|Das|Den|Dem|Zwei|Drei|Vier|Fünf|Unser|Unsere|Mein|Meine|Viele)\b", mail["body"][1]):
            soft.append("Step 3 nach der Anrede groß weiter: klein weiterschreiben wie in Step 1")
    if mail["body"] and not re.match(r"^(hallo|guten tag|servus|moin|grüß)", mail["body"][0], re.IGNORECASE):
        soft.append("keine Anrede am Anfang")
    hit = re.search(OPT_OUT, "\n".join([subject, body] + mail["sig"] + mail["tail"]).lower())
    if hit:
        hard.append(f"Opt-out-Fachsprache: „{hit.group(0)}“, stattdessen die feste Abmeldezeile")
    if needs_opt_out and not any(marker in line.lower() for line in mail["tail"] for marker in OPT_OUT_LINES):
        soft.append("Abmeldezeile unter der Signatur fehlt (Step 1 und 3)")
    if mail["gap"] is not None and mail["gap"] != SIGN_OFF_GAP:
        soft.append(f"vor der Grußformel {mail['gap']} Leerzeile(n), erwartet {SIGN_OFF_GAP} (eine mehr als zwischen den Absätzen)")
    hit = re.search(TRANSLIT, full.lower())
    if hit:
        hard.append(f"Umlaut-Ersatz: „{hit.group(0)}“")

    # Betreff
    if needs_subject and not subject:
        hard.append("Betreff fehlt (Step 1 öffnet den Thread)")
    if not needs_subject and subject:
        hard.append(f"Betreff „{subject}“ muss leer sein (Mail läuft im Thread von Step 1)")
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
    subject_b = mail.get("subject_b")
    if subject_b is not None:
        hard.extend(check_subject_b(subject_b, kind, mail.get("company_names", ())))
    return kind, words, limit, hard, soft


def subject_words(subject, company_names=()):
    """Wörter des Betreffs; Platzhalter und der Kurzname der Firma zählen je als ein Wort."""
    text = re.sub(r"\{\{.*?\}\}", "x", subject)
    for name in sorted({n.strip() for n in company_names if n.strip()}, key=len, reverse=True):
        text = re.sub(r"(?<!\w)" + re.escape(name) + r"(?!\w)", "x", text, flags=re.IGNORECASE)
    return len(text.split())


def check_subject_b(subject, kind, company_names=()):
    """Betreff von Variante B im Betreff-Test (SOP vom 05.11.2026): 3 bis 6 Wörter, gleiches Detail wie das Intro."""
    problems = []
    if kind != "entry":
        return ["Betreff B gibt es nur in Step 1"]
    if not subject:
        return ["Betreff B ist leer (Rückfall: „Frage zu {{Firma}}“ oder „kurze Frage“)"]
    sl = subject.lower()
    count = subject_words(subject, company_names)
    if count > 6:
        problems.append(f"Betreff B hat {count} Wörter, höchstens 6")
    for word in SPAM + SUBJECT_EXTRA + ["angebot"]:
        if re.search(r"(?<!\w)" + re.escape(word), sl):
            problems.append(f"Spam-Wort im Betreff B: „{word}“")
    if re.search(r"\{\{\s*(vorname|firstname|first_name|first name)\s*\}\}", sl):
        problems.append("Vorname im Betreff B")
    if re.match(r"^\s*(re|aw|wg|fwd?)\s*:", sl):
        problems.append("Betreff B mit „Re:“ oder „Fwd:“")
    if "!" in subject or "%" in subject or re.search(r"[\"„“”«»]|\s[-–—]\s|[–—]", subject):
        problems.append("Betreff B mit Ausrufezeichen, %, Anführungszeichen oder Gedankenstrich")
    if subject.count("?") > 1 or ("?" in subject and not subject.endswith("?")):
        problems.append("Betreff B: höchstens ein Fragezeichen am Ende")
    if re.search(ANNOUNCE, sl):
        problems.append("Betreff B klingt nach Ankündigung („… für …“, „ist fertig“)")
    return problems


def arguments(argv):
    """Pfad der Copy-Datei und die Kurznamen aus --firma; None ohne gültigen Aufruf."""
    path, names, rest = None, [], list(argv)
    while rest:
        arg = rest.pop(0)
        if arg == "--firma" and rest:
            names.append(rest.pop(0))
        elif arg.startswith("--firma="):
            names.append(arg.split("=", 1)[1])
        elif path is None and not arg.startswith("--"):
            path = arg
        else:
            return None, []
    return path, names


def main():
    path, company_names = arguments(sys.argv[1:])
    if path is None:
        print(__doc__)
        sys.exit(2)
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        print(f"Datei nicht lesbar: {error}")
        sys.exit(2)

    mails = parse(text)
    company_names += [m.group(1).strip() for m in map(KURZNAME.match, (l.strip() for l in text.splitlines())) if m]
    for mail in mails:
        mail["company_names"] = company_names
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
