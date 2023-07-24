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
"""This module contains Data Connection's Spine-Engine item as well as support utilities."""
from functools import cached_property
from spine_engine.project.project_item_wrapper import ProjectItemWrapper
from .output_resources import file_paths_to_resources, urls_to_resources


class DataConnectionWrapper(ProjectItemWrapper):
    """Spine Engine wrapper over Data Connection item."""

    @cached_property
    def _file_paths(self):
        """Data files and file references."""
        return self._item.all_file_paths()

    def _output_resources_forward(self):
        """See base class."""
        file_resources = file_paths_to_resources(self._name, )
        url_resources = urls_to_resources()
        return file_resources + url_resources
