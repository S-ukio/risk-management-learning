#!/usr/bin/env bash
# ============================================================
# Risk Management Learning — build & preview helper
# Usage:
#   ./serve.sh build        # build zh + en and the landing page
#   ./serve.sh zh           # build Chinese only
#   ./serve.sh en           # build English only
#   ./serve.sh serve-zh     # live preview zh at :3000
#   ./serve.sh serve-en     # live preview en at :3001
# ============================================================

set -euo pipefail
cd "$(dirname "$0")"

MDBOOK_BIN="${MDBOOK_BIN:-mdbook}"
if ! command -v "$MDBOOK_BIN" >/dev/null 2>&1 && [ -n "${LOCALAPPDATA:-}" ]; then
  FOUND_MDBOOK=$(find "$LOCALAPPDATA/Microsoft/WinGet/Packages" -iname mdbook.exe 2>/dev/null | head -1)
  [ -n "$FOUND_MDBOOK" ] && MDBOOK_BIN="$FOUND_MDBOOK"
fi
if ! command -v "$MDBOOK_BIN" >/dev/null 2>&1; then
  echo "mdbook not found. Install it first:" >&2
  echo "  winget install Rustlang.mdBook" >&2
  echo "  # or: cargo install mdbook" >&2
  exit 1
fi

restore_zh_config() {
  if [ -f book.toml.zh_bak ]; then
    cp book.toml.zh_bak book.toml
    rm -f book.toml.zh_bak
  fi
}

build_zh() {
  echo "[build] Chinese -> book/zh"
  "$MDBOOK_BIN" build
}

build_en() {
  echo "[build] English -> book/en"
  cp book.toml book.toml.zh_bak
  trap restore_zh_config EXIT
  cp book-en.toml book.toml
  "$MDBOOK_BIN" build
  restore_zh_config
  trap - EXIT
}

build_all() {
  build_zh
  build_en
  cp root-index.html book/index.html
  echo "[done] open book/index.html or run ./serve.sh serve-zh"
}

serve_en() {
  local port="${1:-3001}"
  cp book.toml book.toml.zh_bak
  trap restore_zh_config EXIT
  cp book-en.toml book.toml
  "$MDBOOK_BIN" serve -p "$port"
  restore_zh_config
  trap - EXIT
}

case "${1:-build}" in
  build|all) build_all ;;
  zh) build_zh ;;
  en) build_en ;;
  serve-zh) "$MDBOOK_BIN" serve -p "${2:-3000}" ;;
  serve-en) serve_en "${2:-3001}" ;;
  *)
    echo "Usage: $0 [build|zh|en|serve-zh|serve-en] [port]" >&2
    exit 1
    ;;
esac
