// Entry program for post-x-promote-make-your-own-bounty-01 (Node 22,
// standard library only). It reads POST.json from the repository root,
// validates that it names one real X post, and writes the same JSON to
// /output/POST.json, where the gate reads it. The entry is the post itself:
// one post of our own on X quoting make.fun's make-your-own-bounty post,
// with a photo of its own attached and the play code in its text.
// Nothing this program writes about the post is scored.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Deterministic: the same POST.json always produces the same output bytes.
// No network, no wall clock, no files outside the repository.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// A real post address, as X's Share button gives it:
// https://x.com/<handle>/status/<digits> (twitter.com also passes).
// The gate itself refuses a placeholder address at grading time, so this
// program copies POST.json through as it stands and lets the gate judge
// it; its job is only to prove the file is a well-formed JSON object
// naming one URL string.

function fail(message: string): never {
  console.error(`POST.json rejected: ${message}`);
  process.exit(1);
}

const raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');

let parsed: unknown;
try {
  parsed = JSON.parse(raw);
} catch (err) {
  fail(`not valid JSON (${(err as Error).message})`);
}

if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  fail('must be a JSON object, not an array or a scalar');
}

const record = parsed as Record<string, unknown>;
const keys = Object.keys(record);
if (keys.length !== 1 || keys[0] !== 'url') {
  fail('must hold exactly one field, "url"');
}
const url = record.url;
if (typeof url !== 'string' || url.length === 0) {
  fail('must carry a "url" string naming the post');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, 'POST.json'), JSON.stringify({ url }) + '\n');
