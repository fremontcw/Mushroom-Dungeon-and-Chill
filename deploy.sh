#!/usr/bin/env bash
# Deploy lofi_claude to the Pi: local check first, then copy, install the service, restart.
# Reads PI_HOST / PI_USER / PI_AUDIO from deploy.env (see deploy.env.example).
set -euo pipefail
cd "$(dirname "$0")"
source deploy.env
AUDIO_FLAG=$([ "${PI_AUDIO:-0}" = "1" ] && echo "" || echo "--silent")
.venv/bin/python lofi_claude/test_scene_renders.py 2>/dev/null | tail -1 | grep -qx ok || { echo "local check failed"; exit 1; }
ssh "$PI_USER@$PI_HOST" 'mkdir -p ~/lofi_claude && rm -f ~/lofi_claude/*.py'
scp -rq lofi_claude "$PI_USER@$PI_HOST:~/"
sed "s/PI_USER/$PI_USER/g; s/AUDIO_FLAG/$AUDIO_FLAG/" lofi_claude/lofi-claude.service | ssh "$PI_USER@$PI_HOST" 'cat > /tmp/lofi-claude.service && sudo mv /tmp/lofi-claude.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now lofi-claude && sudo systemctl restart lofi-claude && sleep 4 && systemctl is-active lofi-claude'
