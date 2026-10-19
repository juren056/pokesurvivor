"""Build only the Wiki for Cloudflare Pages Git deployments."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


# The exporter pins the commit that actually changed the game source. A shallow
# checkout can otherwise misidentify a later Wiki-only commit as that source.
shallow = subprocess.check_output(
    ['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT, text=True
).strip()
if shallow == 'true':
    run('git', 'fetch', '--unshallow', 'origin')

run('node', 'wiki/export-data.cjs')
run(sys.executable, 'wiki/build.py')
run(sys.executable, 'wiki/check.py')
run(sys.executable, 'wiki/agent_check.py')
run(sys.executable, 'wiki/v4_check.py')
run('node', 'wiki/analytics_check.cjs')
