# Default guards

Applied in every repo after the contract's own `## Guards`, which can override one with an `allow` bullet. `{plans}`
and `{archive}` are filled from the contract's `## Plans`; their guards are off when it names no directory.

- deny `Bash` `git push\b[^"|;&]*\s(-f|--force\S*)\b` — Never force-push: it rewrites history others may have pulled.
- deny `Bash` `git\s+(reset\s+--hard|clean\s+-\w*f|checkout\s+--\s+\.(\s|"|$)|restore\s+\.(\s|"|$))` — Whole-repo destructive git commands are forbidden; act on named paths and keep the user's uncommitted work.
- ask `Bash` `\b(pip3? install|uv (add|pip install|tool install)|npm (i|install|add)\s+(-\S+\s+)*[^-\s]\S*|pnpm add|yarn add|bun add|brew install|cargo install|go install|gem install|playwright install|claude (plugin|mcp) (install|add))\b` — Nothing is installed without the user's approval.
- ask `Read|Grep|Glob` `{archive}` — The plan archive opens only when the user asks about archived work.
- ask `Bash` `\b(cat|less|more|head|tail|sed|awk|grep|rg|ugrep|bat|ls|find|wc)\b[^|;&]*[\s"'=/]{archive}` — The plan archive opens only when the user asks about archived work; moving a finished plan into it and excluding it from a search need no prompt.
- deny `Read` `^(?!.*"limit").*{plans}/[^/"]+\.md` — Never read a whole plan: read its outline, then one section (`doc-outline`/`doc-section`, or Read with offset and limit).
