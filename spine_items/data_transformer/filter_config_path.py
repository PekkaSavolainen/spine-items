######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains utilities for filter config paths.

:authors: A. Soininen (VTT)
:date:    2.10.2020
"""
from hashlib import sha1
from pathlib import Path


def filter_config_path(data_dir, specification):
    """
    Constructs an absolute path to transformer's configuration file.

    Args:
        data_dir (str): absolute path to project item's data directory
        specification (DataTransformerSpecification): item's specification

    Returns:
        str: a path to the config file
    """
    hasher = sha1()
    for name, rename in specification.entity_class_name_map().items():
        hasher.update(bytes(name + rename, "utf-8"))
    file_name = "filter_config-" + hasher.hexdigest() + ".json"
    return str(Path(data_dir, file_name))