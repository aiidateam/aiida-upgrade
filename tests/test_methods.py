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
        ("Dict()", "Dict()"),
        ("Dict(dict={'a': 1})", "Dict({'a': 1})"),
        ("Dict(value={'a': 1})", "Dict(value={'a': 1})"),
        ("List(list=[1, 2, 3])", "List([1, 2, 3])"),
        ("List(value=[1, 2, 3])", "List(value=[1, 2, 3])"),
    ),
)
def test_dict_list_no_keyword(expression, result):
    """Test the ``DictListNoKeywordTransformer`` class."""
    from aiida_upgrade.methods import DictListNoKeywordTransformer

    cst_tree = cst.parse_module(expression)
    assert cst_tree.visit(DictListNoKeywordTransformer()).code == result
