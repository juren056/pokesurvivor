# Git deployment configuration

Repository: https://github.com/juren056/pokesurvivor

Cloudflare Pages project: `pokemonsurvivorwiki`. Production branch: `main`.

- Repository root: `wiki`.
- Framework: None.
- Build command: `python3 ci_build.py`.
- Output directory: `dist` (relative to the `wiki` root).
- The builder uses Python 3.12+ and Node 18+; no third-party build dependencies.

The CI entry restores Git history when the checkout is shallow, exports the source snapshot, generates the Wiki, validates its final HTML/sitemap and checks analytics consent behavior. A failed command exits nonzero and blocks that build.

Update the Wiki's source/content/assets and push the reviewed commit to `main`. Cloudflare then builds and releases the output to the existing custom domains. Do not publish the original repository root as the Wiki. Production DNS, SSL, www redirect and Pages-hostname Bulk Redirects remain configured in the Cloudflare account. No Cloudflare API token belongs in this repository.

Git connection and automatic production deployments were enabled in the existing Pages project. The first Git build of commit 9a9ee733a0959bbacb96a021fcf3ec6c3b690aef succeeded as deployment b6443081-89f7-4606-a8a0-2ab2a2408208. Its logs passed all Wiki gates and pinned the original game source b297089. A root-directory adjustment scopes Cloudflare function discovery to wiki, avoiding the unrelated original Firebase functions directory. The follow-up documentation push is used to verify the repository webhook and final settings.
