// The Brexit Reset — entry program for make.fun news-image-20261120.
//
// The finished front page lives in this repository as entry.png (drawn by
// build_entry.py). This program is the only thing the competition harness
// runs: it copies that image into the output directory and then proves the
// copy is exact by comparing the two files byte for byte.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only — no dependencies, no network.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The competition gate refuses images over 1 MiB, so refuse to emit one.
const MAX_BYTES = 1024 * 1024;

const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoRoot, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destPath = join(outDir, "entry.png");

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

if (!existsSync(sourcePath)) {
  fail(`source image is missing: ${sourcePath}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePath, destPath);

const original = readFileSync(sourcePath);
const written = readFileSync(destPath);

if (written.length > MAX_BYTES) {
  fail(`output is ${written.length} bytes, over the ${MAX_BYTES} byte limit`);
}

if (!original.equals(written)) {
  fail(`copied file differs from the source (${destPath})`);
}

const digest = createHash("sha256").update(written).digest("hex");
console.log(`wrote ${destPath} (${written.length} bytes, copy verified)`);
console.log(`sha256 ${digest}`);
