# Troubleshooting

## The plugin does not appear

- Restart the app.
- Run `python3 scripts/validate_plugin.py .` from the plugin root.
- Check that `.codex-plugin/plugin.json` exists.
- Check that the marketplace file contains a `scholarly-research-book` entry.
- Check that the plugin folder was copied to `~/.codex/plugins/scholarly-research-book`.

## Python is missing or too old

Python is only required for the bundled scripts. If you are copying skill folders by hand, you can skip this section.

The scripts need Python 3.10 or newer. On macOS or Linux, run:

```bash
python3 --version
```

On Windows PowerShell, run:

```powershell
py --version
```

If the command is missing or reports an older version, install a current Python release and make sure the launcher is in `PATH`.

## Install fails with a permission error

Run `./install.sh --dry-run` or `.\install.ps1 --dry-run` to see the paths before writing. The installer needs write access to the plugin destination and marketplace JSON. If you pass `--dest` or `--marketplace`, check those paths first.

## Marketplace JSON cannot be parsed

The installer backs up the existing marketplace file with a timestamped `.backup-*` suffix, then creates a fresh marketplace file. Compare the backup with the new file before deleting anything.

## Package creation fails

`scripts/package_plugin.py` writes the zip to the current directory by default. If that directory is read-only, pass `--out` with a writable path:

```bash
python3 scripts/package_plugin.py --root . --out dist/scholarly-research-book-plugin.zip
```

## A script option is unclear

Run the script with `--help`. The common commands and write behavior are also documented in [`docs/SCRIPTS.md`](SCRIPTS.md).

## A skill is not being selected automatically

Skill activation depends heavily on the `description` field. If automatic selection misses, name the skill directly:

```text
Use claim-evidence-ledger on this chapter draft.
```

## Too many skills appear

Install only the core set as direct skills, or use the plugin and name the specific skill you want.

## The agent invents citations

Use `citation-integrity-auditor` and require unverified citation details to stay marked as unverified instead of being filled from memory.

## The prose becomes generic

Use `scholarly-prose-editor` in style-preserving mode and provide a paragraph that represents the voice you want.
