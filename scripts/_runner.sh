# shellcheck shell=bash
# Resolve how to run the ai-scheme CLI. Sourced by the other scripts so that
# there is one answer to "which ai-scheme is this?" per checkout.
#
# Not executable on purpose: it has no behaviour of its own.

ai_scheme_run() {
  if command -v ai-scheme >/dev/null 2>&1; then
    ai-scheme "$@"
  elif [ -f pyproject.toml ] && grep -q '^name = "ai-scheme"' pyproject.toml; then
    uv run ai-scheme "$@"
  else
    # Pinning this to a released version is #6; until then it tracks the
    # default branch, which is what `ai-scheme update` would fetch anyway.
    uvx --from git+https://github.com/matheme-justyn/ai-scheme ai-scheme "$@"
  fi
}
