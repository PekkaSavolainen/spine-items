######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################
"""Functions for deserialization of items and specifications."""
from .tool.tool_specifications import make_specification


def project_item_from_dict(item_dict, name, specifications):
    """Deserializes project item from dictionary.

    Args:
        item_dict (dict): serialized project item
        name (str): name of item
        specifications (dict): mapping from item type to list of specifications available for that item type

    Returns:
        ProjectItem: deserialized project item

    Raises:
        UnrecognizedProjectItemType: raised when item dictionary contains unrecognized item type
        SpecificationNotFound: raised when specifications does not contain expected specification
    """
    item_type = item_dict["type"]


def specification_from_dict(item_type, specification_dict):
    """Deserializes project item specification from dictionary.

    Args:
        item_type (str): type of project item that is compatible with the specification
        specification_dict (dict): serialized specification

    Returns:
        ProjectItemSpecification: deserialized specification
    """
    constructor = {"Tool": make_specification}[item_type]
    return constructor(specification_dict)
