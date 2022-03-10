# aiida-upgrade

[![PyPI][pypi-badge]][pypi-link]

**In Development!**

A tool to aide upgrades of plugins to new aiida-core versions

## Usage

To use the command line tool, it is recommended to install via [pipx](https://pypa.github.io/pipx/):

```console
$ pipx install aiida-upgrade
```

Once installed, you can simply run `aiida-upgrade` on any `PATH`, which can be a single file or a directory:

```console
$ aiida-upgrade --help
Usage: aiida-upgrade [OPTIONS] PATH

  The command line interface of aiida-upgrade.

Options:
  --help  Show this message and exit.
```

In case `PATH` is a directory, `aiida-upgrade` will recursively update all `.py` files inside that directory.

## Supported migrations

Currently, `aiida-upgrade` performs the following code refactoring:

* Look for deprecated `aiida-core` entry points loaded by plugin factories and add the `core.` prefix, see [the corresponding section in the plugin migration guide](https://github.com/aiidateam/aiida-core/wiki/AiiDA-2.0-plugin-migration-guide#entry-points).
* Similarly, find and correct full deprecated entry point strings e.g. `'aiida.data:structure'`.

Migration steps that are not (yet) supported are:

* Adding the `core.` prefix in shell scripts.
* [Update `'name'` to `'label'` when querying for a `Computer` with the `QueryBuilder`](https://github.com/aiidateam/aiida-core/wiki/AiiDA-2.0-plugin-migration-guide#querybuilder).
* Small changes in the API of [Transport](https://github.com/aiidateam/aiida-core/wiki/AiiDA-2.0-plugin-migration-guide#transport-plugins) and [Scheduler](https://github.com/aiidateam/aiida-core/wiki/AiiDA-2.0-plugin-migration-guide#schedulers) plugins.
* [Removal of the `PluginTestCase` class.](https://github.com/aiidateam/aiida-core/wiki/AiiDA-2.0-plugin-migration-guide#unit-tests)

If you find any problems with the current refactoring, or any migration steps that are missing, please let us know by opening an issue.

[pypi-badge]: https://img.shields.io/pypi/v/aiida_upgrade.svg
[pypi-link]: https://pypi.org/project/aiida_upgrade
