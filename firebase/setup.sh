#!/usr/bin/env bash
# One-time Firebase setup for the Russian drills site. Run from anywhere:
#   bash /workspace/russian-drills/firebase/setup.sh [project-id]
# Needs: the Firebase CLI logged in, and the Google Cloud Terms of Service accepted on that account.
set -euo pipefail
P="${1:-russian-drills}"
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(dirname "$HERE")"
FB="npx -y firebase-tools@15.35.0"
FT="${FT:-/workspace/fbtests/node_modules/firebase-tools}"
cd "$HERE"
if $FB projects:list --json | python3 -c "import json,sys;sys.exit(0 if any(p['projectId']=='$P' for p in json.load(sys.stdin)['result']) else 1)"; then
  echo "== project $P exists"
else
  echo "== creating project $P"; $FB projects:create "$P" --display-name "Russian Drills"
fi
APP=$($FB apps:list WEB --project "$P" --json | python3 -c "import json,sys;r=json.load(sys.stdin)['result'];print(r[0]['appId'] if r else '')")
if [ -z "$APP" ]; then
  echo "== registering web app"; $FB apps:create WEB "Russian Drills Web" --project "$P"
  APP=$($FB apps:list WEB --project "$P" --json | python3 -c "import json,sys;print(json.load(sys.stdin)['result'][0]['appId'])")
fi
echo "== web app $APP"
$FB apps:sdkconfig WEB "$APP" --project "$P" --json | python3 -c "
import json,sys
r=json.load(sys.stdin)['result']; c=r.get('sdkConfig',r)
keep={k:c[k] for k in ['apiKey','authDomain','projectId','storageBucket','messagingSenderId','appId'] if k in c}
open('$ROOT/src/firebase-config.js','w').write('// Public Firebase web config (safe to publish). Set to null to run without accounts.\nwindow.RU_FIREBASE_CONFIG = '+json.dumps(keep,indent=1)+';\n')
print(keep)"
echo "== enabling APIs"; FT="$FT" node "$HERE/enable-apis.cjs" "$P"
if $FB firestore:databases:list --project "$P" 2>/dev/null | grep -q "(default)"; then echo "== firestore exists"
else echo "== creating firestore (standard, eur3)"; $FB firestore:databases:create "(default)" --location eur3 --edition standard --project "$P"; fi
echo "== deploying rules + email/password auth"
$FB deploy --only firestore:rules,auth --project "$P" --non-interactive
echo "== authorized domain"
FT="$FT" node "$HERE/add-auth-domain.cjs" "$P" tancred99.github.io
echo "== rebuilding site"; (cd "$ROOT" && python3 build.py)
echo "DONE: project $P"
