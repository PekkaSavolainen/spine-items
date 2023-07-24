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
"""Standard project item package for Spine Toolbox."""
from .version import __version__


def _project_item_classes():
    """Returns project item classes in this package.

    Returns:
        dict: mapping from item type to project item class
    """
    from .data_connection.project_item import DataConnection
    from .data_store.project_item import DataStore
    from .tool.project_item import Tool
    from .view.project_item import View

    classes = {}
    for item_class in (DataConnection, DataStore, Tool, View):
        classes[item_class.item_type()] = item_class
    return classes


PROJECT_ITEM_CLASSES = _project_item_classes()
from .project_item_upgrader import (
    LATEST_PROJECT_DICT_ITEMS_VERSION,
    upgrade_items_to_latest,
)

from .deserialization import specification_from_dict
