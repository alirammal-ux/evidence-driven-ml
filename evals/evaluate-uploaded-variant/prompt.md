---
tags: [evidence-driven-ml]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Ho addestrato su Kaggle la variante con l'augmentation di colore più forte (un solo training, seed 42, resto della ricetta uguale) e ho calcolato i conteggi per immagine sulle 43 immagini di validazione, per la pipeline adottata e per la variante (oggetti abbinati con IoU > 0.5 e pixel). Conviene adottarla?

Input files: adopted_counts.csv, variant_counts.csv
