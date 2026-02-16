#!/usr/bin/env bash
set -u

URLS_FILE="${1:-urls.txt}"
TTS_MODEL="${TTS_MODEL:-edge}"

: > failed-urls.log

while IFS= read -r url || [[ -n "$url" ]]; do
  url="${url%$'\r'}"         # handle Windows line endings
  [[ -z "$url" ]] && continue
  [[ "$url" =~ ^# ]] && continue

  echo "Processing: $url"
  if ! make diyfire-podcast URL="$url" TTS="$TTS_MODEL" </dev/null; then
    echo "$url" >> failed-urls.log
  fi
  sleep 2
done < "$URLS_FILE"

echo "Done."