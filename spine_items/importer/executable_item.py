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
Contains Importer's executable item as well as support utilities.

:authors: A. Soininen (VTT)
:date:   1.4.2020
"""
import os
import pathlib
from PySide2.QtCore import QObject, QEventLoop, Signal, Slot, QThread
from spine_engine.spine_io.gdx_utils import find_gams_directory
from spine_engine.project_item.executable_item_base import ExecutableItemBase
from spine_engine.utils.helpers import shorten
from spine_engine.utils.serialization import deserialize_checked_states
from .importer_worker import ImporterWorker
from .item_info import ItemInfo
from ..utils import labelled_resource_filepaths


class ExecutableItem(ExecutableItemBase, QObject):

    importing_finished = Signal()
    """Emitted after import thread has finished."""

    def __init__(self, name, mapping, selected_files, logs_dir, gams_path, cancel_on_error, logger):
        """
        Args:
            name (str): Importer's name
            mapping (dict): import mapping
            selected_files (list): selected_files
            logs_dir (str): path to the directory where logs should be stored
            gams_path (str): path to system's GAMS executable or empty string for the default path
            cancel_on_error (bool): if True, revert changes on error and quit
            logger (LoggerInterface): a logger
        """
        ExecutableItemBase.__init__(self, name, logger)
        QObject.__init__(self)
        self._mapping = mapping
        self._selected_files = selected_files
        self._logs_dir = logs_dir
        self._gams_path = gams_path
        self._cancel_on_error = cancel_on_error
        self._resources_from_downstream = list()
        self._worker = None
        self._worker_thread = None
        self._worker_succeeded = None
        self._loop = None

    @staticmethod
    def item_type():
        """Returns ImporterExecutable's type identifier string."""
        return ItemInfo.item_type()

    def stop_execution(self):
        """Stops execution."""
        super().stop_execution()
        if self._loop:
            if self._loop.isRunning():
                self._loop.exit(-1)
            self._loop = None
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait()
            self._worker_thread = None

    def _execute_backward(self, resources):
        """See base class."""
        self._resources_from_downstream = resources.copy()
        return True

    def _execute_forward(self, resources):
        """See base class."""
        if not self._mapping:
            return True
        labelled_filepaths = labelled_resource_filepaths(resources)
        source_filepaths = list()
        for label in self._selected_files:
            filepath = labelled_filepaths.get(label)
            if filepath is not None:
                source_filepaths.append(filepath)
        source_settings = {"GdxConnector": {"gams_directory": self._gams_system_directory()}}
        self._destroy_current_worker()
        self._loop = QEventLoop()
        self._worker = ImporterWorker(
            source_filepaths,
            self._mapping,
            source_settings,
            [r.url for r in self._resources_from_downstream if r.type_ == "database"],
            self._logs_dir,
            self._cancel_on_error,
            self._logger,
        )
        self._worker_thread = QThread()
        self._worker.moveToThread(self._worker_thread)
        self._worker.import_finished.connect(self._handle_worker_finished)
        self._worker.import_finished.connect(self._loop.quit)
        self._worker_thread.started.connect(self._worker.do_work)
        self._worker_thread.start()
        loop_retval = self._loop.exec_()
        if loop_retval:
            # If retval is not 0, loop exited with nonzero return value. Should happen when
            # user stops execution
            self._logger.msg_error.emit(f"Importer {self.name} stopped")
            self._worker_succeeded = -1
            return self._worker_succeeded
        if not self._worker_succeeded:
            self._logger.msg_error.emit(f"Executing Importer {self.name} failed")
        else:
            self._logger.msg_success.emit(f"Executing Importer {self.name} finished")
        return self._worker_succeeded

    @Slot(int)
    def _handle_worker_finished(self, exit_code):
        self._worker_succeeded = exit_code == 0
        self._destroy_current_worker()

    def _destroy_current_worker(self):
        """Runs before starting execution and after worker finishes.
        Destroys current worker and quits thread if present.
        """
        if self._loop:
            self._loop.deleteLater()
            self._loop = None
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait()
            self._worker_thread = None

    def _gams_system_directory(self):
        """Returns GAMS system path or None if GAMS default is to be used."""
        path = self._gams_path
        if not path:
            path = find_gams_directory()
        if path is not None and os.path.isfile(path):
            path = os.path.dirname(path)
        return path

    @classmethod
    def from_dict(cls, item_dict, name, project_dir, app_settings, specifications, logger):
        """See base class."""
        specification_name = item_dict["specification"]
        specification = ExecutableItemBase._get_specification(
            name, ItemInfo.item_type(), specification_name, specifications, logger
        )
        mapping = specification.mapping if specification else {}
        file_selection = item_dict.get("file_selection")
        file_selection = deserialize_checked_states(file_selection, project_dir)
        selected_files = [filepath for filepath, selected in file_selection.items() if selected]
        data_dir = pathlib.Path(project_dir, ".spinetoolbox", "items", shorten(name))
        logs_dir = os.path.join(data_dir, "logs")
        gams_path = app_settings.value("appSettings/gamsPath", defaultValue=None)
        cancel_on_error = item_dict["cancel_on_error"]
        return cls(name, mapping, selected_files, logs_dir, gams_path, cancel_on_error, logger)
