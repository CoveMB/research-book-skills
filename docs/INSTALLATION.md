# Installation guide

This package can be installed as a local plugin or used as a portable collection of skill folders.

## Requirements

If you use this package as a collection of skill folders, you do not need Python.

Python 3.10 or newer is only required when you run the bundled install, validation, or packaging scripts. No pip packages are required. The scripts use the Python standard library.

- macOS and Linux installs use Bash through `./install.sh`.
- Windows installs use PowerShell through `.\install.ps1`.
- A local plugin install needs write access to the plugin destination and marketplace JSON.

## Option A: Install as a local plugin

### macOS / Linux

```bash
cd research-book-plugin
./install.sh
```

### Windows PowerShell

```powershell
cd research-book-plugin
.\install.ps1
```

The installer:

1. validates `.codex-plugin/plugin.json`,
2. validates every `skills/*/SKILL.md`,
3. copies the plugin to `~/.codex/plugins/scholarly-research-book`,
4. creates or updates `~/.agents/plugins/marketplace.json`,
5. adds the marketplace entry for this plugin.

Restart the app after installation.

Preview the install first if you want to check paths before writing files:

```bash
./install.sh --dry-run
```

More script details are in [`docs/SCRIPTS.md`](SCRIPTS.md).

## Option B: Manual personal marketplace install

1. Copy this folder to:

```text
~/.codex/plugins/scholarly-research-book
```

2. Create or update:

```text
~/.agents/plugins/marketplace.json
```

3. Add an entry like:

```json
{
  "name": "local-personal-plugins",
  "interface": {
    "displayName": "Local Personal Plugins"
  },
  "plugins": [
    {
      "name": "scholarly-research-book",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/scholarly-research-book"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

4. Restart the app and look for the plugin in the plugin directory.

## Option C: Direct local skill install

Some agent environments read skills directly from a skills folder. Copy the folders under `skills/` into that environment's skill directory.

A common target for direct user skills is:

```text
~/.agents/skills
```

Example:

```bash
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/
```

## Option D: ChatGPT Skills upload

Some skill-upload interfaces expect one skill bundle at a time. This package is mainly a multi-skill plugin. If your workspace requires one skill per upload, zip an individual folder under `skills/<skill-name>/` and upload that zip. See `docs/SKILL_INDEX.md` to choose the core skills first.

## Validate after install

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
```

For a full local package check, run:

```bash
./validate.sh
```

See [`docs/SCRIPTS.md`](SCRIPTS.md) for the full script list and dependency notes.

## Uninstall

Remove the copied plugin folder:

```bash
rm -rf ~/.codex/plugins/scholarly-research-book
```

Then remove the `scholarly-research-book` entry from `~/.agents/plugins/marketplace.json`.
