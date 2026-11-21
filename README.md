# The Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/cunong05/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/cunong05/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An open passport spread from the Republic of Talveria — a Mediterranean island
country that does not exist. Left page: the data page of Elena Mara Meridian,
born 14 March 1988 in Port Meridian, passport TAL 0048217, issued 2 June 2024
by the Ministry of the Sea, with a portrait and a machine-readable zone whose
check digits are computed, not typed. Right page: the visa page, with entry
stamps from Marseille (12 Sep 2024), Tunis (3 Nov 2024) and Valletta
(19 Jan 2025) — all after the date of issue, in order — a single-entry visa
from the Republic of Caldonia, and the condition that tells you what kind of
place Talveria is: valid for travel by sea only, because Talveria has no
airport, and a harbour tax of 12 shells is payable on arrival.

The spread is drawn by `draw.py` (Python + Pillow, deterministic — same run,
same bytes) and `main.ts` copies the resulting `entry.png` to
`/output/entry.png`.

## How to run

```sh
node main.ts
```

The program copies `entry.png` to `/output/entry.png` (set `MAKEFUN_OUTPUT_DIR` to change the destination). It checks the spread first — real PNG, exactly 1024×1024, at most 1 MiB — and confirms the copy byte for byte, so repeated runs always produce the same file.

To redraw the spread from scratch:

```sh
python3 draw.py
```

<sub>Entered on [make.fun](https://make.fun/?ref=4w89k05q&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
