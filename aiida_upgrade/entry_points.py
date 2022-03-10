# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Transformers for upgrading AiiDA entry points."""
import re

import libcst as cst

# Maps of deprecated entry points that require `core.` prefix in `aiida-core>=2.0`
DEPRECATED_ENTRY_POINTS_MAPPING = {
    "aiida.calculations": ["arithmetic.add", "templatereplacer"],
    "aiida.data": [
        "array",
        "array.bands",
        "array.kpoints",
        "array.projection",
        "array.trajectory",
        "array.xy",
        "base",
        "bool",
        "cif",
        "code",
        "dict",
        "float",
        "folder",
        "int",
        "list",
        "numeric",
        "orbital",
        "remote",
        "remote.stash",
        "remote.stash.folder",
        "singlefile",
        "str",
        "structure",
        "upf",
    ],
    "aiida.tools.dbimporters": [
        "cod",
        "icsd",
        "materialsproject",
        "mpds",
        "mpod",
        "nninc",
        "oqmd",
        "pcod",
        "tcod",
    ],
    "aiida.tools.data.orbitals": ["orbital", "realhydrogen"],
    "aiida.parsers": ["arithmetic.add", "templatereplacer.doubler"],
    "aiida.schedulers": ["direct", "lsf", "pbspro", "sge", "slurm", "torque"],
    "aiida.transports": ["local", "ssh"],
    "aiida.workflows": ["arithmetic.multiply_add", "arithmetic.add_multiply"],
    "aiida.groups": [],
}

FACTORY_MAPPING = {
    "CalculationFactory": "aiida.calculations",
    "DataFactory": "aiida.data",
    "GroupFactory": "aiida.groups",
    "ParserFactory": "aiida.parsers",
    "SchedulerFactory": "aiida.schedulers",
    "TransportFactory": "aiida.transports",
    "DbImporterFactory": "aiida.tools.dbimporters",
    "OrbitalFactory": "aiida.tools.data.orbitals",
    "WorkflowFactory": "aiida.workflows",
}


class FactoryCoreTransformer(cst.CSTTransformer):
    """Transformer that adds the ``core.`` prefix to deprecated aiida-core v1 entry points."""

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:

        try:
            function = original_node.func.value

            if function in FACTORY_MAPPING.keys():

                entry_point = original_node.args[0].value.value
                string_quote = entry_point[0]
                entry_point = entry_point.strip(string_quote)

                if (
                    entry_point
                    in DEPRECATED_ENTRY_POINTS_MAPPING[FACTORY_MAPPING[function]]
                ):
                    return updated_node.with_changes(
                        args=[
                            original_node.args[0].with_changes(
                                value=original_node.args[0].value.with_changes(
                                    value=f"{string_quote}core.{entry_point}{string_quote}"
                                )
                            )
                        ]
                    )
        except (AttributeError, TypeError):
            return original_node

        return original_node


class FullEntryPointTransformer(cst.CSTTransformer):
    """Transformer that adds the ``core.`` prefix to aiida-core v1 full entry point strings."""

    def leave_SimpleString(
        self, original_node: cst.SimpleString, updated_node: cst.SimpleString
    ) -> cst.SimpleString:

        if "aiida." not in original_node.value:
            return original_node

        for entry_group, entry_points in DEPRECATED_ENTRY_POINTS_MAPPING.items():

            option_string = "|".join(entry_points)

            match = re.match(
                rf"(['|\"]){entry_group}:({option_string})[',\"]", original_node.value
            )

            if match is not None:
                string_quote = match.groups()[0]
                entry_point = match.groups()[1]
                return updated_node.with_changes(
                    value=f"{string_quote}{entry_group}:core.{entry_point}{string_quote}"
                )

        return original_node
