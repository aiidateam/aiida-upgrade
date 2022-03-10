from pathlib import Path

import libcst as cst

from .entry_points import FactoryCoreTransformer, FullEntryPointTransformer
from .methods import DictListNoKeywordTransformer


def migrate_path(path: Path):
    """Recursively migrate ``.py``, ``.rst`` and ``.md`` files in ``path`` ``aiida-core`` v2.0"""

    if path.is_dir():
        for sub_path in path.iterdir():
            migrate_path(sub_path)

    elif path.suffix == ".py":
        with path.open("r") as handle:
            cst_tree = cst.parse_module(handle.read())

        cst_tree = cst_tree.visit(FactoryCoreTransformer())
        cst_tree = cst_tree.visit(FullEntryPointTransformer())
        cst_tree = cst_tree.visit(DictListNoKeywordTransformer())

        with path.open("w") as handle:
            handle.write(cst_tree.code)
