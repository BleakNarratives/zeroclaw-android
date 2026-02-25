#!/bin/bash
# consolidate.sh
# Run this in Termux to pull everything into one place on device storage.
# BleakNarratives / zeroclaw-android session 2026-02-25

set -e

DEST="/storage/emulated/0/zeroclaw-android"
VERTICAL="$HOME/vertical-ai"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  zeroclaw-android CONSOLIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Ensure destination exists
mkdir -p "$DEST"/{bin,docs,bridge,personas/keys,logs}

# 2. Copy the binary
echo "[1/6] Copying zeroclaw binary..."
cp "$HOME/zeroclaw/target/release/zeroclaw" "$DEST/bin/zeroclaw"
chmod +x "$DEST/bin/zeroclaw"
echo "      ✓ $DEST/bin/zeroclaw ($(du -sh $DEST/bin/zeroclaw | cut -f1))"

# 3. Copy cargo build config (the secret sauce)
echo "[2/6] Copying build config..."
cp -r "$HOME/zeroclaw/.cargo" "$DEST/"
echo "      ✓ .cargo/config.toml"

# 4. Copy repo docs
echo "[3/6] Copying repo docs..."
for f in README.md LORE.md LICENSE WORKFLOW_LOG.md zeroclaw-integration.json; do
  [ -f "$DEST/$f" ] && cp "$DEST/$f" "$DEST/docs/" || true
done
echo "      ✓ docs/"

# 5. Copy vertical-ai bridge files if they exist
echo "[4/6] Copying bridge scripts..."
[ -f "$VERTICAL/nostr_to_telegram.py" ] && \
  cp "$VERTICAL/nostr_to_telegram.py" "$DEST/bridge/" && \
  echo "      ✓ nostr_to_telegram.py" || \
  echo "      - nostr_to_telegram.py not found yet (create from WORKFLOW_LOG)"

[ -f "$VERTICAL/code-city/zeroclaw_events.js" ] && \
  cp "$VERTICAL/code-city/zeroclaw_events.js" "$DEST/bridge/" && \
  echo "      ✓ zeroclaw_events.js" || \
  echo "      - zeroclaw_events.js not found yet (create from WORKFLOW_LOG)"

# 6. Copy persona keys if they exist
echo "[5/6] Copying persona keys..."
if [ -d "$VERTICAL/personas/keys" ]; then
  cp -r "$VERTICAL/personas/keys/"* "$DEST/personas/keys/" 2>/dev/null || true
  echo "      ✓ persona keypairs"
else
  echo "      - No persona keys yet. Run keygen from WORKFLOW_LOG."
fi

# 7. Write a session manifest
echo "[6/6] Writing session manifest..."
cat > "$DEST/SESSION.md" << EOF
# Session Manifest
**Date:** $(date)
**Binary:** zeroclaw v0.1.7 (aarch64-android, native)
**Build timestamp:** 2026-02-25T04:11:47-06:00
**Repo:** https://github.com/BleakNarratives/zeroclaw-android

## Files
- \`bin/zeroclaw\` — the binary
- \`.cargo/config.toml\` — build config (mold linker + memory flags)
- \`docs/\` — README, LORE, workflow log, integration JSON
- \`bridge/\` — Nostr→Telegram + Code City event bridge scripts
- \`personas/keys/\` — persona Nostr keypairs

## Next Steps
1. Post zeroclaw-android repo to Nostr, r/nostr, r/termux, HN
2. Create Telegram channel
3. Wire up: zeroclaw subscribe | swarm_parser.py | boardroom.py
4. Set personas live on Nostr
5. Connect Code City event bridge
6. First paid session demo
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DONE. Everything consolidated to:"
echo "  $DEST"
echo ""
echo "  Contents:"
find "$DEST" -type f | sort | sed 's|'"$DEST"'/|  |'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
