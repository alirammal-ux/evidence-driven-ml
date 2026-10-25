---
tags: [evidence-driven-ml]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Il mio modello di segmentazione di nuclei si è fermato a F1 di oggetto 0.80 in validazione (43 immagini, abbinamento con IoU > 0.5); sulle immagini di training, con la stessa pipeline, fa 0.82. Ti allego gli errori per immagine sulla validazione. Cosa faccio adesso per migliorarlo?

Input files: val_errors.csv
