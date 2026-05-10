#!/usr/bin/env python3
"""Print the three-level SVPWM table 7 state-vector standard.

The script has no third-party dependencies. It is intended for agents that need
to compare a Simulink state-vector table against the PDF-derived standard.
"""

from __future__ import annotations

import argparse
import json


TABLE7 = {
    "I": {
        "1": "onn oon ooo poo ooo oon onn",
        "2": "oon ooo poo ppo poo ooo oon",
        "3": "onn oon pon poo pon oon onn",
        "4": "oon pon poo ppo poo pon oon",
        "5": "onn pnn pon poo pon pnn onn",
        "6": "oon pon ppn ppo ppn pon oon",
    },
    "II": {
        "1": "oon ooo opo ppo opo ooo oon",
        "2": "non oon ooo opo ooo oon non",
        "3": "oon opn opo ppo opo opn oon",
        "4": "non oon opn opo opn oon non",
        "5": "oon opn ppn ppo ppn opn oon",
        "6": "non npn opn opo opn npn non",
    },
    "III": {
        "1": "non noo ooo opo ooo noo non",
        "2": "noo ooo opo opp opo ooo noo",
        "3": "non noo npo opo npo noo non",
        "4": "noo npo opo opp opo npo noo",
        "5": "non npn npo opo npo npn non",
        "6": "noo npo npp opp npp npo noo",
    },
    "IV": {
        "1": "noo ooo oop opp oop ooo noo",
        "2": "nno noo ooo oop ooo noo nno",
        "3": "noo nop oop opp oop nop noo",
        "4": "nno noo nop oop nop noo nno",
        "5": "noo nop npp opp npp nop noo",
        "6": "nno nnp nop oop nop nnp nno",
    },
    "V": {
        "1": "nno ono ooo oop ooo ono nno",
        "2": "ono ooo oop pop oop ooo ono",
        "3": "nno ono onp oop onp ono nno",
        "4": "ono onp oop pop oop onp ono",
        "5": "nno nnp onp oop onp nnp nno",
        "6": "ono onp pnp pop pnp onp ono",
    },
    "VI": {
        "1": "ono ooo poo pop poo ooo ono",
        "2": "onn ono ooo poo ooo ono onn",
        "3": "ono pno poo pop poo pno ono",
        "4": "onn ono pno poo pno ono onn",
        "5": "ono pno pnp pop pnp pno ono",
        "6": "onn pnn pno poo pno pnn onn",
    },
}

ENCODING = {"n": 0, "o": 1, "p": 2}


def encode_triplet(token: str) -> list[int]:
    return [ENCODING[ch] for ch in token]


def build_encoded_table() -> dict[str, dict[str, list[list[int]]]]:
    return {
        sector: {
            small: [encode_triplet(token) for token in sequence.split()]
            for small, sequence in small_sectors.items()
        }
        for sector, small_sectors in TABLE7.items()
    }


def print_markdown() -> None:
    encoded = build_encoded_table()
    for sector, small_sectors in encoded.items():
        print(f"## {sector}")
        for small, vectors in small_sectors.items():
            first_four = vectors[:4]
            print(f"- {sector}{small}: first4={first_four}, sequence={vectors}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    encoded = build_encoded_table()
    if args.format == "json":
        print(json.dumps(encoded, indent=2, sort_keys=True))
    else:
        print_markdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
