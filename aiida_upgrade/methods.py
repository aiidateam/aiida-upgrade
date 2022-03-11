# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Transformers for upgrading AiiDA methods."""
import libcst as cst
from libcst import matchers


class DictListNoKeywordTransformer(cst.CSTTransformer):
    """Remove ``dict`` and ``list`` keywords from constructors of ``Dict`` and ``List`` nodes."""

    dict_constructor = matchers.Name("Dict")
    list_constructor = matchers.Name("List")

    dict_keyword = matchers.Name("dict")
    list_keyword = matchers.Name("list")

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:

        if matchers.matches(
            original_node.func, self.dict_constructor | self.list_constructor
        ):

            # Empty `Dict` or `List` constructor
            if len(original_node.args) == 0:
                return original_node
            # `Dict` or `List` constructor without keyword
            elif original_node.args[0].keyword is None:
                return original_node
            # `Dict` or `List` constructor with `dict` or `list` keyword
            elif matchers.matches(
                original_node.args[0].keyword, self.dict_keyword | self.list_keyword
            ):
                arguments = list(updated_node.args)
                arguments[0] = updated_node.args[0].with_changes(
                    equal=cst.MaybeSentinel.DEFAULT, keyword=None
                )
                return updated_node.with_changes(args=arguments)

        return original_node
