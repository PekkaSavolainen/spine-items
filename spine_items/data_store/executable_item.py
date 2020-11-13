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
Contains Data Store's executable item as well as support utilities.

:authors: A. Soininen (VTT)
:date:   1.4.2020
"""

from spine_engine.project_item.executable_item_base import ExecutableItemBase
from spine_engine.project_item.project_item_resource import ProjectItemResource
from spine_engine.utils.serialization import deserialize_path
from .item_info import ItemInfo
from .utils import convert_to_sqlalchemy_url, make_label


class ExecutableItem(ExecutableItemBase):
    def __init__(self, name, url, logger):
        """
        Args:
            name (str): item's name
            url (str): database's URL
            logger (LoggerInterface): a logger
        """
        super().__init__(name, logger)
        self._url = url

    @staticmethod
    def item_type():
        """Returns the data store executable's type identifier string."""
        return ItemInfo.item_type()

    def _output_resources_backward(self):
        """See base class."""
        return self._output_resources_forward()

    def _output_resources_forward(self):
        """See base class."""
        if not self._url:
            return list()
        metadata = {"label": make_label(self.name)}
        resource = ProjectItemResource(self, "database", url=str(self._url), metadata=metadata)
        return [resource]

    @classmethod
    def from_dict(cls, item_dict, name, project_dir, app_settings, specifications, logger):
        """See base class."""
        if item_dict["url"]["dialect"] == "sqlite":
            item_dict["url"]["database"] = deserialize_path(item_dict["url"]["database"], project_dir)
        url = convert_to_sqlalchemy_url(item_dict["url"], name, logger, log_errors=True)
        return cls(name, url, logger)
