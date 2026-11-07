# Copy-Kern

Die software-freien Cold-Mail-Copy-Regeln. Hier ist die eine Quelle der Wahrheit für Copy:
Anatomie, Intro, Offer, Follow-ups, Betreff, Verbote, Selbstprüfung.

| Datei | Inhalt |
|---|---|
| `copy-lehre.md` | die vollständige Copy-Lehre |
| `marketing-offer.md` | Offer-Karten A bis E, Tests, Offer-Bibliothek |
| `beispiele.md` | vollständige Sequenz und Entry Mails je Karte, zugleich Ausgabeformat |
| `check_copy.py` | Prüfskript für die mechanisch prüfbaren Regeln |

## Wer den Kern nutzt

- **Heartbeat-Skill `cold-mail-copy`** (Repo heartbeat-skills, Plugin `cold-mail-copy`): bekommt den
  Kern per `scripts/export-copy-kern.sh` als generierte Kopie unter `references/kern/` und
  `scripts/check_copy.py`.
- **`outreach-copy`** (dieser Skill): führt die ListM8-Umsetzung (Variablen, Blueprint, Server).
  Noch nicht auf den Kern umgestellt, siehe unten.

## Regeln ändern

1. Nur hier ändern, nie in der exportierten Kopie.
2. `python3 check_copy.py beispiele.md` muss ohne Fehler durchlaufen.
3. Export: `scripts/export-copy-kern.sh` (Ziel per `HEARTBEAT_SKILLS_PATH`, Standard
   `../heartbeat-skills`).
4. Abweichungen prüfen: `scripts/export-copy-kern.sh --check` (Exit-Code 1 bei Drift).
5. Betrifft die Änderung auch die Generierung in ListM8, Server-Regeln und `outreach-copy` nachziehen.

## Offen: outreach-copy auf den Kern umstellen

`outreach-copy/SKILL.md` und `references/copy-lehre.md` tragen dieselben Regeln heute noch einmal,
mit ListM8-Begriffen. Ziel ist, dass `outreach-copy` nur noch die ListM8-Schicht enthält und für
alle Copy-Regeln auf `kern/` verweist. Das berührt `lead-agent`, `verify-agent` und die anderen
Skills, die `references/copy-lehre.md` laden, und wird deshalb als eigener Schritt mit Test gebaut.

Bis dahin gilt: Eine Regeländerung in `outreach-copy` auch hier eintragen und umgekehrt.

Im Kern bereits korrigiert gegenüber `outreach-copy/references/copy-lehre.md`: Beispiel-Intros mit
Mechanik-Nutzen ersetzt, Karte E mit nur einem CTA, Betreff in Step 1 und 3 einheitlich, keine echten
Kundennamen in Beispielen.
