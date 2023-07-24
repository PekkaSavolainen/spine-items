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
"""This module contains functions to upgrade project items in outdated project dictionary."""
from spine_engine.project.exception import ItemsVersionTooHigh

LATEST_PROJECT_DICT_ITEMS_VERSION = 1


def upgrade_items_to_latest(items_dict, old_version):
    """Upgrades the project items in given project dictionary to the latest version.

    Args:
        items_dict (dict): mapping from item name to item dict
        old_version (int): items dict version

    Returns:
        dict: latest version of the items dictionary
    """
    if old_version == LATEST_PROJECT_DICT_ITEMS_VERSION:
        return items_dict
    if old_version > LATEST_PROJECT_DICT_ITEMS_VERSION:
        raise ItemsVersionTooHigh()
