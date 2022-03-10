# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Tests for the transformers for upgrading AiiDA entry points."""
import libcst as cst
import pytest


@pytest.mark.parametrize(
    ("expression", "result"),
    (
        ('DataFactory("structure")', 'DataFactory("core.structure")'),
        ("DataFactory('array.bands')", "DataFactory('core.array.bands')"),
        (
            "CalculationFactory('arithmetic.add')",
            "CalculationFactory('core.arithmetic.add')",
        ),
        ("CalculationFactory('diff-tutorial')", "CalculationFactory('diff-tutorial')"),
        ("CalculationFactory('core.transfer')", "CalculationFactory('core.transfer')"),
    ),
)
def test_factory_core(expression, result):
    """Test the ``FactoryCoreTransformer`` class."""
    from aiida_upgrade.entry_points import FactoryCoreTransformer

    cst_tree = cst.parse_module(expression)
    assert cst_tree.visit(FactoryCoreTransformer()).code == result


@pytest.mark.parametrize(
    ("expression", "result"),
    (
        (
            "types.DataParamType(sub_classes=('aiida.data:remote',))",
            "types.DataParamType(sub_classes=('aiida.data:core.remote',))",
        ),
        (
            'types.DataParamType(sub_classes=("aiida.data:structure",))',
            'types.DataParamType(sub_classes=("aiida.data:core.structure",))',
        ),
    ),
)
def test_full_entry_point(expression, result):
    """Test the ``FullEntryPointTransformer`` class."""
    from aiida_upgrade.entry_points import FullEntryPointTransformer

    cst_tree = cst.parse_module(expression)
    assert cst_tree.visit(FullEntryPointTransformer()).code == result
