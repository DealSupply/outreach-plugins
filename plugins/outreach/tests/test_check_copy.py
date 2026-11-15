#!/usr/bin/env python3
"""Tests für check_copy.py: python3 -I plugins/outreach/tests/test_check_copy.py

Die Bodies eines Blueprints tragen Platzhalter: {{ai.hallo}} ist die Anrede, {{ai.intro}} zählt
wie {{Intro}} mit 30 Wörtern.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "outreach-copy" / "kern" / "check_copy.py"

BODY = """{{ai.hallo}}

{{ai.intro}}

Genau deshalb bieten wir aktuell für eine Handvoll Betriebe in der Region eine kleine Vorschau an.

Wäre es in Ordnung, wenn ich das auch für dich erstelle? Völlig unverbindlich natürlich.


Viele Grüße
{{accountSignature}}

Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.
"""


def run(text: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "copy.md"
        path.write_text(text, encoding="utf-8")
        done = subprocess.run([sys.executable, "-I", str(SCRIPT), str(path)], capture_output=True, text=True)
    return done.returncode, done.stdout + done.stderr


def main() -> None:
    code, out = run("## Step 1\nBetreff: kurze Frage\n\n" + BODY)
    assert "keine Anrede am Anfang" not in out, out
    assert "Entry Mail hat nur" not in out, out  # {{ai.intro}} zählt mit 30 Wörtern
    assert code == 0, out

    code, out = run("## Step 1\nBetreff: kurze Frage\n\n" + BODY.replace("{{ai.hallo}}\n\n", ""))
    assert "keine Anrede am Anfang" in out, out

    code, out = run("## Step 2\nBetreff: (leer)\n\n{{ai.hallo}}\n\n{{ai.intro}}\n\nkurze Erinnerung an meine Frage von letzter Woche.\n\n\nViele Grüße\n{{accountSignature}}\n")
    assert "steht außerhalb der Entry Mail" in out, out
    assert code == 1, out

    code, out = run("## Step 1\nBetreff: kurze Frage\n\n" + BODY.replace("{{ai.hallo}}", "Hallo Max,").replace("{{ai.intro}}", "{{Intro}}"))
    assert "keine Anrede am Anfang" not in out and code == 0, out
    print("OK")


if __name__ == "__main__":
    main()
