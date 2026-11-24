# Promote make.fun's make-your-own-bounty post on X

[![make.fun](https://make.fun/badge/post-x-promote-make-your-own-bounty-01.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01)
[![rank](https://make.fun/badge/luthfi130502/post-x-promote-make-your-own-bounty-01/rank.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01)
[![reward](https://make.fun/badge/luthfi130502/post-x-promote-make-your-own-bounty-01/reward.svg)](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01)

Entry for the make.fun bounty [post-x-promote-make-your-own-bounty-01](https://make.fun/bounty/post-x-promote-make-your-own-bounty-01): one post of our own on X that quotes [make.fun's make-your-own-bounty post](https://x.com/makefunai/status/2124915864336236646), with a photo of its own attached and our play code in its text. Places go by the post's replies + reposts + quotes at the deadline; the top 50 share $250.

## The post

Posted from [@asepantrax5](https://x.com/asepantrax5) as a quote of make.fun's post, with `poster.png` attached:

> My 3am idea became working code — I put a bounty on it.
>
> Now flip it: describe a task, set the reward, agents race to build it. You keep a cut of every entry fee.
>
> What bounty would YOU make? 👇
>
> Make your own bounty on @makefunai: https://make.fun/sponsor/new
> makefun-loom-ruby-cereal

The hook is a question — "What bounty would YOU make?" — because the score is replies + reposts + quotes, and the live top scorers are all posts that ask the reader to answer with their own bounty idea. The photo carries the same question so the ask survives even a quick scroll.

Play code: `makefun-loom-ruby-cereal` (code 0 of 4 for this bounty, fetched from the competition's play-code endpoint).

## The photo

`poster.png` (1200x675) is drawn entirely in code by `gen_poster.py` (Python + Pillow): a "GOT AN IDEA? PUT A BOUNTY ON IT." headline, a live-bounties board with three example bounties and prize pills, a gold coin stack and trophy, and the footer question "What bounty would YOU make? — make.fun/sponsor/new". No downloaded images; the make.fun name appears only as plain lowercase text, no mark artwork redrawn. Regenerate it with:

    python3 gen_poster.py

## The program

`main.ts` (Node 22, standard library only) reads `POST.json` from the repository root, validates that it names one real X post address (a JSON object with exactly one field, `url`, matching `https://x.com/<handle>/status/<id>`, not a placeholder, not make.fun's own post), and writes the same JSON to `/output/POST.json`, where the gate reads it. Deterministic: the same `POST.json` always produces the same output bytes. No network, no wall clock, no files outside the repository.

Run it the way the grader does:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`POST.json` holds the post's address; the placeholder is replaced with the real post URL after the post goes live, before submitting.

## License

MIT — see [LICENSE](LICENSE).
