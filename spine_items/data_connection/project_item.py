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
"""This module contains Data Connection's project item."""
import logging
import shutil

from spine_engine.project.project_item import ProjectItem
from spine_engine.utils.helpers import fails_if_virtual
from spine_engine.utils.serialization import deserialize_path, serialize_path


logger = logging.getLogger(__name__)


class DataConnection(ProjectItem):
    """A Data Connection project item."""

    def __init__(self, description, file_references=None, url_references=None, url_credentials=None):
        """
        Args:
            description (str): item's description
            file_references (list of Path, optional): a list of file paths
            url_references (list of str, optional): a list of URLs
            url_credentials (dict, optional): mapping URLs to tuples (username, password)
        """
        super().__init__(description)
        self._file_references = file_references if file_references is not None else []
        self._url_references = url_references if url_references is not None else []
        self._url_credentials = url_credentials if url_credentials is not None else {}

    def all_file_paths(self):
        """Combines file references and data files.

        Returns:
            list of Path: file paths
        """
        file_paths = list(self._file_references)
        if not self.is_memory_only:
            file_paths += [entry for entry in self._data_dir.iterdir() if entry.is_file()]
        return file_paths

    @fails_if_virtual
    def add_data_file(self, paths):
        """Copies file to data directory.

        Args:
            paths (Iterable of Path): paths to add
        """
        for file_path in paths:
            logger.info("Copying file {} to data dir.", file_path.name, extra={"item": self})
            try:
                shutil.copy(file_path, self.data_dir)
            except OSError:
                logger.error("[OSError] Copying failed", extra={"item": self})

    def add_file_references(self, paths):
        """Adds multiple file paths to reference list.

        Args:
            paths (Iterable of Path): paths to add
        """
        new_paths = []
        existing_references = (reference for reference in self._file_references if reference.isfile())
        for path in paths:
            if not path.isfile():
                continue
            if any(path == ref for ref in existing_references):
                logger.warning("Reference to file already exists", path.name)
            else:
                new_paths.append(path.resolve())
        if not new_paths:
            return
        self._file_references += new_paths

    def add_database_references(self, urls):
        """Adds multiple database URLs to reference list.

        Args:
            urls (Iterable of str): URLs to add
        """
        self._url_references += urls

    @classmethod
    def item_type(cls):
        """See base class."""
        return "Data Connection"

    def to_dict(self):
        """See base class."""
        item_dict = super().to_dict()
        item_dict["file_references"] = [serialize_path(ref, self._project.project_dir) for ref in self._file_references]
        item_dict["db_references"] = self._url_references
        item_dict["db_credentials"] = self._url_credentials
        return item_dict

    @staticmethod
    def item_dict_local_entries():
        """See base class."""
        return [("db_credentials",)]

    @staticmethod
    def _init_args_from_dict(item_dict, project_dir, specifications):
        """See base class."""
        kwargs = super()._init_args_from_dict(item_dict, project_dir, specifications)
        file_references = item_dict.get("file_references", []) or item_dict.get("references", [])
        kwargs["file_references"] = [deserialize_path(r, project_dir) for r in file_references]
        kwargs["url_references"] = item_dict.get("db_references", [])
        kwargs["url_credentials"] = item_dict.get("db_credentials", {})
        return kwargs
