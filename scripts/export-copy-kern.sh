#!/usr/bin/env bash
# Exportiert den Copy-Kern in den Heartbeat-Skill cold-mail-copy.
# Quelle ist immer plugins/outreach/skills/outreach-copy/kern/, im Ziel wird nichts von Hand gepflegt.
#
#   scripts/export-copy-kern.sh           kopiert den Kern ins Ziel
#   scripts/export-copy-kern.sh --check   meldet nur Abweichungen (Exit-Code 1 bei Drift)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KERN="$ROOT/plugins/outreach/skills/outreach-copy/kern"
HB="${HEARTBEAT_SKILLS_PATH:-$ROOT/../heartbeat-skills}"
SKILL="$HB/plugins/cold-mail-copy/skills/cold-mail-copy"

[ -d "$SKILL" ] || { echo "Ziel nicht gefunden: $SKILL"; exit 2; }

# Quelle -> Ziel (relativ zum Skill-Ordner)
PAIRS=(
  "copy-lehre.md:references/kern/copy-lehre.md"
  "marketing-offer.md:references/kern/marketing-offer.md"
  "beispiele.md:references/kern/beispiele.md"
  "check_copy.py:scripts/check_copy.py"
)

python3 "$KERN/check_copy.py" "$KERN/beispiele.md" > /dev/null \
  || { echo "beispiele.md besteht check_copy.py nicht. Erst den Kern reparieren."; exit 1; }

if [ "${1:-}" = "--check" ]; then
  drift=0
  for pair in "${PAIRS[@]}"; do
    src="$KERN/${pair%%:*}"; dst="$SKILL/${pair#*:}"
    if ! cmp -s "$src" "$dst"; then
      echo "Abweichung: ${pair#*:}"
      drift=1
    fi
  done
  [ "$drift" = 0 ] && echo "Kern und Heartbeat-Skill stimmen überein."
  exit "$drift"
fi

mkdir -p "$SKILL/references/kern" "$SKILL/scripts"
for pair in "${PAIRS[@]}"; do
  cp "$KERN/${pair%%:*}" "$SKILL/${pair#*:}"
done
chmod +x "$SKILL/scripts/check_copy.py"

cat > "$SKILL/references/kern/README.md" <<'EOF'
# Copy-Kern (generiert)

Diese Dateien und `scripts/check_copy.py` werden aus dem Copy-Kern exportiert
(outreach-plugins, `plugins/outreach/skills/outreach-copy/kern/`, Befehl
`scripts/export-copy-kern.sh`). Hier nicht bearbeiten: Eine Änderung hier wird beim
nächsten Export überschrieben und erzeugt genau den Drift, den der Kern verhindern soll.

Handgepflegt sind nur `SKILL.md`, `scripts/md_to_docx.py` und `assets/`.
EOF

echo "Kern exportiert nach $SKILL"
git -C "$HB" status --short -- "plugins/cold-mail-copy" || true
