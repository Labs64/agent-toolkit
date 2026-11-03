#!/usr/bin/env bash
# Fails when a file in the repository looks like it names something internal:
# a host or ticket key outside the public allow-lists, a personal path or an
# e-mail address. Everything in this repository is published.
#
# The rules match by shape and list only what is public, so the script itself
# names nothing internal. Patterns that only a list of names can catch come
# from CHECK_PUBLIC_EXTRA, one extended regex per line, which CI reads from a
# secret.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# Public hosts that may appear; any other labs64 host fails.
public_hosts='(www\.)?labs64\.(com|de|io)|github\.com/Labs64'

# Ticket-like tokens that are placeholders or standard names, not tickets.
public_keys='PROJ-[0-9]+|(UTF|ISO|SHA|AES|RFC|CVE|TLS|HTTP)-[0-9]+'

checks=(
  # hosts under a labs64 domain
  '[a-z0-9.-]*labs64\.[a-z]{2,}'
  # ticket keys
  '[A-Z][A-Z0-9]+-[0-9]+'
  # personal home directories
  '/Users/[A-Za-z]'
  '/home/[A-Za-z]'
  # e-mail addresses
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
  # hosts of a hosted Jira or Confluence site
  '[a-z0-9-]+\.atlassian\.net'
)

allowed="$public_hosts|$public_keys|example\.atlassian\.net|@example\.(com|org)|noreply@"

if [ -n "${CHECK_PUBLIC_EXTRA:-}" ]; then
  while IFS= read -r p; do
    [ -n "$p" ] && checks+=("$p")
  done <<< "$CHECK_PUBLIC_EXTRA"
fi

found=0
for p in "${checks[@]}"; do
  # Drop the allowed tokens from each match, and report what is left.
  if git grep --untracked -nIoE "$p" -- ':!LICENSE' ':!scripts/check-public.sh' \
      | grep -vE "^[^:]+:[0-9]+:($allowed)$"; then
    found=1
  fi
done

if [ "$found" -ne 0 ]; then
  echo "check-public: the matches above must not be published" >&2
  exit 1
fi
