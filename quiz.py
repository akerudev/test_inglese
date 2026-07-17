#!/usr/bin/env python3
"""Quiz CLI a scelta multipla basato su domande.json + soluzioni.json."""

import json
import random
import argparse
from pathlib import Path

BASE = Path(__file__).parent


def carica():
    domande = json.loads((BASE / "domande.json").read_text(encoding="utf-8"))["domande"]
    soluzioni = json.loads((BASE / "soluzioni.json").read_text(encoding="utf-8"))["soluzioni"]
    chiavi = {s["id"]: s for s in soluzioni}
    return domande, chiavi


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-n", type=int, default=10, help="numero di domande")
    p.add_argument("--paniere", type=int, choices=[1, 2], help="filtra per paniere")
    p.add_argument("--capitolo", type=int, help="filtra per capitolo")
    args = p.parse_args()

    domande, chiavi = carica()
    if args.paniere:
        domande = [q for q in domande if q["paniere"] == args.paniere]
    if args.capitolo:
        domande = [q for q in domande if q["capitolo"] == args.capitolo]
    if not domande:
        print("Nessuna domanda con questi filtri.")
        return

    test = random.sample(domande, min(args.n, len(domande)))
    punti, errori = 0, []

    for i, q in enumerate(test, 1):
        print(f"\n[{i}/{len(test)}] {q['domanda']}")
        for lettera, testo in q["opzioni"].items():
            print(f"  {lettera}) {testo}")
        risposta = input("> ").strip().upper()[:1]
        corretta = chiavi[q["id"]]["risposta"]
        if risposta == corretta:
            punti += 1
            print("✅ Corretto")
        else:
            print(f"❌ Sbagliato — risposta esatta: {corretta}) {chiavi[q['id']]['testo_risposta']}")
            errori.append(q)

    print(f"\nPunteggio: {punti}/{len(test)} ({punti / len(test):.0%})")
    if errori:
        print("\nDa ripassare:")
        for q in errori:
            print(f"  - cap. {q['capitolo']} · {q['sezione']}: {q['domanda'][:70]}")


if __name__ == "__main__":
    main()
