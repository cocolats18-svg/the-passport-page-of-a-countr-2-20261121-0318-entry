// Passport spread entry for 21 November 2026 (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// the output directory the grader gives it, deterministically.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

// The image itself is committed in this repository as entry.png (1024x1024,
// an invented passport spread for the Republic of Velmora, drawn locally
// with Pillow by gen_passport.py: data page with a drawn portrait and a
// machine-readable zone, visa page with stamps from Kessarin, Valdris and
// Dravenhold, all dated after the passport's 12 JUN 2025 issue date).
// Copying it, byte for byte, is the whole program: no network, no
// randomness, so two runs write identical bytes.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
