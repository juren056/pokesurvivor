# Git deployment configuration

Repository: https://github.com/juren056/pokesurvivor

Cloudflare Pages project: `pokemonsurvivorwiki`. Production branch: `main`.

- Repository root: `/`.
- Framework: None.
- Build command: `python3 wiki/ci_build.py`.
- Output directory: `wiki/dist`.
- The builder uses Python 3.12+ and Node 18+; no third-party build dependencies.

The CI entry restores Git history when the checkout is shallow, exports the source snapshot, generates the Wiki, validates its final HTML/sitemap and checks analytics consent behavior. A failed command exits nonzero and blocks that build.

Update the Wiki's source/content/assets and push the reviewed commit to `main`. Cloudflare then builds and releases the output to the existing custom domains. Do not publish the original repository root as the Wiki. Production DNS, SSL, www redirect and Pages-hostname Bulk Redirects remain configured in the Cloudflare account. No Cloudflare API token belongs in this repository.

The initial connection and first successful Git-built deployment must be verified separately in the live release record; this configuration file alone is not proof that automatic deployment ran.
