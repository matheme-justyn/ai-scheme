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
    # Run the release this project was applied from, not whatever the default
    # branch happens to be today. The tag is recorded in provenance.json by
    # the lifecycle command that applied it.
    tag=""
    if [ -f .scheme/provenance.json ]; then
      tag="$(python3 -c 'import json,sys; print(json.load(open(".scheme/provenance.json")).get("tag") or "")' 2>/dev/null || true)"
    fi
    if [ -n "$tag" ]; then
      uvx --from "git+https://github.com/matheme-justyn/ai-scheme@${tag}" ai-scheme "$@"
    else
      uvx --from git+https://github.com/matheme-justyn/ai-scheme ai-scheme "$@"
    fi
  fi
}
