# Beispiel-Sequenz in der Form von DealSupply

So steht eine Sequenz in DealSupply: jede Mail beginnt mit `{{ai.hallo}}`, Step 1 trägt `{{ai.intro}}`,
unter der Grußformel steht nur `{{accountSignature}}`, der Abschied trägt `{{ai.routing}}` als eigenen
Absatz. Karte C mit dem festen zweiten Satz. Die Datei besteht
`python3 -I kern/check_copy.py references/beispiel-sequenz.md --dealsupply` ohne Fehler und ist die
Vorlage für das Format der Prüfdatei. Im Blueprint steht derselbe Text als `body` je Step, mit `\n`
statt der Zeilenumbrüche (vollständiger Blueprint: `beispiel-blueprint.md`).

## Step 1: Entry Mail

Betreff: kurze Frage

{{ai.hallo}}

{{ai.intro}}

Deswegen war ich so frei und habe dir einen kompletten Entwurf für eine neue Startseite erstellt, inklusive eingebauter Online-Terminbuchung.

Ich bin gerade noch an den letzten Feinheiten dran.

Wäre es in Ordnung, wenn ich es dir morgen zusende? Völlig unverbindlich natürlich.


Viele Grüße
{{accountSignature}}

Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.

## Step 2: Erinnerung

Betreff: (leer)

{{ai.hallo}}

du hast sicher viel um die Ohren, ich wollte nur sichergehen, dass meine Mail bei dir angekommen ist.

Ein kurzes Ja reicht mir.


Viele Grüße
{{accountSignature}}

## Step 3: Neuer Winkel mit Social Proof

Betreff: (leer)

{{ai.hallo}}

ich habe die Website einer Zahnarztpraxis in Stuttgart neu aufgesetzt, danach haben sich ihre Online-Terminanfragen in vier Monaten verdreifacht.

Wäre es in Ordnung, wenn ich dir morgen den Entwurf zusende? Völlig unverbindlich natürlich.


Viele Grüße
{{accountSignature}}

Falls das gerade kein Thema für dich ist, gib mir kurz Bescheid.

## Step 4: Abschied mit Routing-Absatz

Betreff: (leer)

{{ai.hallo}}

da ich bisher nichts gehört habe, gehe ich davon aus, dass es gerade nicht passt. Das ist absolut in Ordnung.

{{ai.routing}}


Viele Grüße
{{accountSignature}}
