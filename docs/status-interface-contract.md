# The status interface contract

An agent driving this layer runs one command first and does what it says. It
does not decide for itself whether a project needs adopting or updating, and it
does not read version files to compare them.

    ai-scheme status --json

Deliberately not called an "install" document: the mechanism layer has its own
`.opencode/INSTALL.md`, which is about how capabilities get installed into a
project. This file is about how an agent calls the skeleton layer's lifecycle
interface. See ADR 0007.

## The contract

1. Run `ai-scheme status --json` in the project.
2. Read `state` and `next_command`.
3. Run `next_command`. Every lifecycle command produces a plan first; apply it
   only after the plan has been seen.
4. Never infer a state from the filesystem, from `.template-version`, from a
   `VERSION` file, or from anything else. If `status` cannot answer, it says so
   -- that is not an invitation to guess.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | The question was answered. **Any** state, including one that needs work. |
| 1 | The answer is no. `status` does not use this; sibling commands do. |
| 2 | The question could not be answered: not a git repository, unreadable answers file, a failure the caller has to fix. |

"An update is available" is a `0` with `state: update`. It is not an error, and
the old "exit 1 means there are updates" convention is not used anywhere here.

## The payload

| Field | Meaning |
| --- | --- |
| `state` | One of the states below |
| `reason` | Why that state, in words, naming what was **not** checked |
| `next_command` | The command to run, or `null` when there is nothing to do |
| `current_version` | The template version recorded in `.scheme/config.yml`, or `null` |
| `target_version` | The template version this `ai-scheme` would apply |
| `drift` | Paths that differ from the template, `[]`, or `"unknown"` |
| `policy_drift` | Repository settings that differ, `[]`, or `"unknown"` |
| `mechanism_config_detected` | Whether a root `config.toml` exists. Detection only -- this layer never reads it (ADR 0008) |

`"unknown"` is a real answer and must not be read as "none". It means the check
could not run -- the template could not be fetched, or GitHub was not reachable.
A caller that treats `"unknown"` as `[]` is claiming something nobody verified.

## The states

| `state` | When | `next_command` |
| --- | --- | --- |
| `create` | The target does not exist, or is an empty directory | `ai-scheme create --plan` |
| `adopt` | An existing project with no `.scheme/config.yml` | `ai-scheme adopt --plan` |
| `migrate` | No answers file, but the previous layout's `.template-version` or `.scaffolding/` is there | `ai-scheme adopt --plan` |
| `update` | The recorded version is behind the template | `ai-scheme update --plan` |
| `drifted` | Version matches, template-owned files were changed locally | `ai-scheme update --plan` |
| `policy-only-update` | Version and files match, repository settings do not | `ai-scheme settings apply --plan` |
| `current` | Everything that could be checked matches | `null` |

Precedence, when more than one could apply: `create`, then `migrate`, then
`adopt`, then `update`, then `drifted`, then `policy-only-update`, then
`current`. `update` outranks `drifted` because the update is what will have to
merge the drift; `drift` stays in the payload either way, so a caller that
cares can look before running anything.

The legacy `.template-version` sentinel is read in the `migrate` state and
nowhere else. It is never written, and it never takes part in a version
comparison.

## Determinism

Two runs against an unchanged project produce byte-identical output. If you
need a run that cannot reach the network, pass `--no-render`: drift comes back
as `"unknown"` rather than as a guess.
