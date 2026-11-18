# 18 November 2026 world news in one image

A make.fun entry: a single 1024×1024 PNG that condenses one day of world news —
**Wednesday, 18 November 2026** — into four panels plus a headline ticker.

The repository ships one asset and one small program:

- `entry.png` — the entry image (1024×1024, RGB, 213,361 bytes,
  sha256 `d44e842b74a3dec01d4e6baf94f143589f5caafa05fd2b70dc05b73a87896e01`).
- `main.py` — standard-library Python 3.13 program that writes that exact image
  to `<output_dir>/entry.png`. It performs no network access.
- `source.svg` — the vector source the PNG was rendered from.
- `LICENSE` — MIT.

## The image

Header: **THE WORLD TODAY — 18 November 2026**.

Four panels, clockwise from top left:

1. **PERU — APEC summit.** Xi greets Trump, with Putin also in attendance.
2. **GULF — Kuwait intercepts.** The first Iranian attack in two months is
   intercepted over Kuwait.
3. **US SENATE — 56–44.** Democrats 56, Republicans 44; Peltola flips Alaska.
4. **MANILA — US–Philippines pact.** A "landmark" trade deal is signed.

Footer ticker, also today: NSA systems outage · House speaker race · Mullin
hearing on flight chaos.

## How to run

The grader runs the program with no arguments and no network, from any working
directory, and expects the image at `/output/entry.png`.

```sh
python3.13 main.py
# OK: wrote /output/entry.png (213361 bytes, sha256=d44e842b…)
```

Output directory resolution:

1. `$MAKEFUN_OUTPUT_DIR`, when set and non-empty;
2. `/output`, otherwise.

The source image is always resolved relative to the script's own directory, so
the current working directory does not matter.

Write to a temporary directory instead of `/output`:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/mf-run1 python3.13 main.py
```

Validate without writing anything (prints the sha256 and exits 0):

```sh
python3.13 main.py --check
# CHECK ok: /path/to/entry.png 213361 bytes sha256=d44e842b… (nothing written)
```

### Guarantees

- Verifies the 8-byte PNG signature (`89 50 4E 47 0D 0A 1A 0A`) before copying.
- Rejects an empty source or one larger than 1,048,576 bytes (1 MiB).
- Creates the output directory if missing; never modifies `entry.png`.
- Prints one summary line; exits `0` on success, `1` with a clear `ERROR:` line
  on stderr otherwise.
- No third-party dependencies, no subprocesses, no network calls.

## Licence

MIT. See [LICENSE](LICENSE). Copyright (c) 2026 coys96.
