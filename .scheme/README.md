# `.scheme/`

This directory holds the skeleton layer's configuration. There is one file that
matters, `config.yml`, and Copier rewrites it on every update -- edit it by
hand only when you know what you are changing, then run:

```bash
ai-scheme config validate
```

## You may have two configuration files

If this project also uses the mechanism layer (`ai-zpd`), there is a second
file, `config.toml`, at the repository root. They are not duplicates and
neither reads the other.

| File | Layer | What it configures |
| --- | --- | --- |
| `.scheme/config.yml` | Skeleton (`ai-scheme`) | What the repository is like: identity, language profiles, branching, release phase, collaboration mode, visibility, optional features |
| `config.toml` | Mechanism (`ai-zpd`) | What the agent tooling does: module selection, OpenCode settings, service capabilities |

Keys that appear in both are independent. There is no fallback from one to the
other, and no command in this layer parses `config.toml`.

Full explanation, including why this is two files rather than one:
[`docs/config-boundary.md`](../docs/config-boundary.md).
