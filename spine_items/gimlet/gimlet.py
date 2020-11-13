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
Gimlet class module.

:author: P. Savolainen (VTT)
:date:   15.4.2020
"""

import os
import uuid
from collections import Counter
from PySide2.QtCore import Slot, Qt
from spinetoolbox.project_item.project_item import ProjectItem
from spine_engine.config import GIMLET_WORK_DIR_NAME
from spine_engine.utils.helpers import shorten
from spine_engine.utils.serialization import (
    deserialize_checked_states,
    serialize_checked_states,
    serialize_url,
    deserialize_path,
)
from spine_engine.utils.command_line_arguments import split_cmdline_args
from .item_info import ItemInfo
from .executable_item import ExecutableItem
from .utils import SHELLS
from .commands import UpdateShellCheckBoxCommand, UpdateShellComboboxCommand, UpdatecmdCommand, UpdateWorkDirModeCommand
from ..commands import ChangeItemSelectionCommand, UpdateCmdLineArgsCommand
from ..models import GimletCommandLineArgsModel, InputFileListModel


class Gimlet(ProjectItem):
    """Gimlet class."""

    def __init__(
        self,
        name,
        description,
        x,
        y,
        toolbox,
        project,
        logger,
        use_shell=True,
        shell_index=0,
        cmd="",
        cmd_line_args=None,
        selections=None,
        work_dir_mode=True,
    ):
        """
        Args:
            name (str): Project item name
            description (str): Description
            x (float): Initial X coordinate of item icon
            y (float): Initial Y coordinate of item icon
            toolbox (ToolboxUI): QMainWindow instance
            project (SpineToolboxProject): Project this item belongs to
            logger (LoggerInterface): Logger instance
            use_shell (bool): Use shell flag
            shell_index (int): Selected shell as index
            cmd (str): Command that this Gimlet executes at run time
            cmd_line_args (list, optional): Gimlet command line arguments
            selections (dict, optional): A mapping from file label to boolean 'checked' flag
            work_dir_mode (bool): True uses Gimlet's default work dir, False uses a unique work dir on every execution
        """
        super().__init__(name, description, x, y, project, logger)
        self._toolbox = toolbox
        self._file_model = InputFileListModel(header_label="Available resources")
        self._toolbox_resources = list()  # ProjectItemResources for handling changes in the DAG on Design View
        self.use_shell = use_shell
        self.shell_index = shell_index
        self.cmd = cmd
        if cmd_line_args is None:
            cmd_line_args = []
        self.cmd_line_args = cmd_line_args
        self._cmdline_args_model = GimletCommandLineArgsModel(self)
        self._cmdline_args_model.args_updated.connect(self._push_update_cmd_line_args_command)
        self._populate_cmdline_args_model()
        self._file_model.set_initial_state(selections if selections is not None else dict())
        self._file_model.selected_state_changed.connect(self._push_file_selection_change_to_undo_stack)
        self._work_dir_mode = None
        self.update_work_dir_mode(work_dir_mode)
        self.default_gimlet_work_dir = os.path.join(self.data_dir, GIMLET_WORK_DIR_NAME)

    @staticmethod
    def item_type():
        """See base class."""
        return ItemInfo.item_type()

    @staticmethod
    def item_category():
        """See base class."""
        return ItemInfo.item_category()

    def execution_item(self):
        """Creates project item's execution counterpart."""
        shell = ""
        cmd_list = [self.cmd] + self.cmd_line_args
        if self._active:
            if self._properties_ui.checkBox_shell.isChecked():
                shell = self._properties_ui.comboBox_shell.itemText(self._properties_ui.comboBox_shell.currentIndex())
        else:
            if self.use_shell:
                shell = SHELLS[self.shell_index]
        if self._work_dir_mode:
            work_dir = self.default_gimlet_work_dir
        else:
            app_work_dir = self._toolbox.qsettings().value("appSettings/workDir")
            if not app_work_dir:
                work_dir = None
            else:
                unique_dir_name = shorten(self.name) + "__" + uuid.uuid4().hex + "__toolbox"
                work_dir = os.path.join(app_work_dir, unique_dir_name)
        # Only selected files in properties are sent to the executable item
        selected_files = list()
        for file_item in self._file_model.files:
            if file_item.selected:
                selected_files.append(file_item.label)
        return ExecutableItem(self.name, self._logger, shell, cmd_list, work_dir, selected_files)

    def make_signal_handler_dict(self):
        """Returns a dictionary of all shared signals and their handlers.
        This is to enable simpler connecting and disconnecting."""
        s = super().make_signal_handler_dict()
        s[self._properties_ui.toolButton_gimlet_open_dir.clicked] = lambda checked=False: self.open_directory()
        s[self._properties_ui.checkBox_shell.stateChanged] = self.shell_checkbox_clicked
        s[self._properties_ui.comboBox_shell.activated] = self.shell_combobox_index_changed
        s[self._properties_ui.lineEdit_cmd.editingFinished] = self.cmd_edited
        s[self._properties_ui.radioButton_default.toggled] = self.push_work_dir_mode_cmd
        s[self._properties_ui.toolButton_add_file_path_arg.clicked] = self._add_selected_file_path_args
        s[self._properties_ui.toolButton_remove_arg.clicked] = self._remove_arg
        return s

    def restore_selections(self):
        """Restores selections into shared widgets when this project item is selected."""
        self._properties_ui.label_gimlet_name.setText(self.name)
        if not self._active:
            return
        self._properties_ui.treeView_cmdline_args.setModel(self._cmdline_args_model)
        self._properties_ui.treeView_files.setModel(self._file_model)
        self._properties_ui.checkBox_shell.setChecked(self.use_shell)
        if self.use_shell:
            self._properties_ui.comboBox_shell.setEnabled(True)
        else:
            self._properties_ui.comboBox_shell.setEnabled(False)
        self._properties_ui.comboBox_shell.setCurrentIndex(self.shell_index)
        self._properties_ui.lineEdit_cmd.setText(self.cmd)
        self.update_work_dir_button_state()

    def save_selections(self):
        """Saves selections in shared widgets for this project item into instance variables."""
        self._properties_ui.treeView_files.setModel(None)

    @Slot(int)
    def shell_checkbox_clicked(self, state):
        """Pushes a new shell check box command to undo stack.
        Pushing the command calls the commands redo method.

        Args:
            state (int): New check box state (Qt.CheckState enum)
        """
        use_shell = state == Qt.Checked
        if self.use_shell == use_shell:
            return
        self._toolbox.undo_stack.push(UpdateShellCheckBoxCommand(self, use_shell))

    def toggle_shell_state(self, use_shell):
        """Sets the use shell check box state. Disables shell
        combobox when shell check box is unchecked.

        Args:
            use_shell (bool): New check box state
        """
        self.use_shell = use_shell
        if not self._active:
            return
        # This does not trigger the stateChanged signal.
        self._properties_ui.checkBox_shell.setCheckState(Qt.Checked if use_shell else Qt.Unchecked)
        self._properties_ui.comboBox_shell.setEnabled(bool(use_shell))

    @Slot(int)
    def shell_combobox_index_changed(self, ind):
        """Pushes a shell combobox selection changed command to
        undo stack, which in turn calls set_shell_combobox_index() below.

        Args:
            ind (int): New index in combo box
        """
        if self.shell_index == ind:
            return
        self._toolbox.undo_stack.push(UpdateShellComboboxCommand(self, ind))

    def set_shell_combobox_index(self, ind):
        """Sets new index to shell combobox.

        Args:
            ind (int): New index in shell combo box
        """
        self.shell_index = ind
        if not self._active:
            return
        self._properties_ui.comboBox_shell.setCurrentIndex(ind)

    @Slot()
    def cmd_edited(self):
        """Updates the command instance variable when user has
        finished editing text in the line edit."""
        cmd = self._properties_ui.lineEdit_cmd.text().strip()
        if self.cmd == cmd:
            return
        self._toolbox.undo_stack.push(UpdatecmdCommand(self, cmd))

    def set_command(self, txt):
        self.cmd = txt
        if not self._active:
            return
        self._properties_ui.lineEdit_cmd.setText(txt)

    @Slot(bool)
    def _remove_arg(self, _=False):
        removed_rows = [index.row() for index in self._properties_ui.treeView_cmdline_args.selectedIndexes()]
        cmd_line_args = [arg for row, arg in enumerate(self.cmd_line_args) if row not in removed_rows]
        self._push_update_cmd_line_args_command(cmd_line_args)

    @Slot(bool)
    def _add_selected_file_path_args(self, _=False):
        new_args = [index.data() for index in self._properties_ui.treeView_files.selectedIndexes()]
        self._push_update_cmd_line_args_command(self.cmd_line_args + new_args)

    @Slot(list)
    def _push_update_cmd_line_args_command(self, cmd_line_args):
        if self.cmd_line_args == cmd_line_args:
            return
        self._toolbox.undo_stack.push(UpdateCmdLineArgsCommand(self, cmd_line_args))

    def update_cmd_line_args(self, cmd_line_args):
        """Updates instance cmd line args list and sets the list as text to the line edit widget.

        Args:
            cmd_line_args (list): Tool cmd line args
        """
        self.cmd_line_args = cmd_line_args
        self._populate_cmdline_args_model()

    def _populate_cmdline_args_model(self):
        gimlet_args = self.cmd_line_args
        if self._active:
            pos = self._properties_ui.treeView_cmdline_args.verticalScrollBar().sliderPosition()
        self._cmdline_args_model.reset_model(gimlet_args)
        if self._active:
            self._properties_ui.treeView_cmdline_args.expandAll()
            self._properties_ui.treeView_cmdline_args.verticalScrollBar().setSliderPosition(pos)
            # TODO: self._properties_ui.treeView_cmdline_args.setFocus()

    @Slot(bool, str)
    def _push_file_selection_change_to_undo_stack(self, selected, label):
        """Makes changes to file selection undoable."""
        self._toolbox.undo_stack.push(ChangeItemSelectionCommand(self, selected, label))

    def set_file_selected(self, label, selected):
        """Handles selecting files in Gimlet file list."""
        self._file_model.set_selected(label, selected)

    @Slot(bool)
    def push_work_dir_mode_cmd(self, checked):
        """Pushes a new UpdateWorkDirModeCommand to the undo stack."""
        self._toolbox.undo_stack.push(UpdateWorkDirModeCommand(self, checked))

    def update_work_dir_mode(self, work_dir_mode):
        """Updates work_dir_mode setting.

        Args:
            work_dir_mode (bool): If True, work dir is set to this Gimlet's data dir,
            IF False, a unique work dir is created for every execution.
        """
        if self._work_dir_mode == work_dir_mode:
            return
        self._work_dir_mode = work_dir_mode
        self.update_work_dir_button_state()

    def update_work_dir_button_state(self):
        """Sets the work dir radio button check state according to
        work_dir_mode instance variable."""
        if not self._active:
            return
        self._properties_ui.radioButton_default.blockSignals(True)
        if self._work_dir_mode:
            self._properties_ui.radioButton_default.setChecked(True)
        else:
            self._properties_ui.radioButton_unique.setChecked(True)
        self._properties_ui.radioButton_default.blockSignals(False)

    def _do_handle_dag_changed(self, upstream_resources, downstream_resources):
        """Saves a copy of ProjectItemResources for handling
        changes in the DAG on Design View.

        See also base class.

        Args:
            upstream_resources (list): ProjectItemResources available from upstream
            downstream_resources (list): ProjectItemResources available from downstream
        """
        self._toolbox_resources = upstream_resources + downstream_resources
        self._file_model.update(self._toolbox_resources)
        self._notify_if_duplicate_file_paths()
        # Update cmdline args
        cmd_line_args = self.cmd_line_args.copy()
        for resource in self._toolbox_resources:
            updated_from = resource.metadata.get("updated_from")
            try:
                i = cmd_line_args.index(updated_from)
            except ValueError:
                continue
            cmd_line_args[i] = resource.label
        self.update_cmd_line_args(cmd_line_args)

    def item_dict(self):
        """Returns a dictionary corresponding to this item."""
        d = super().item_dict()
        d["use_shell"] = self.use_shell
        d["shell_index"] = self.shell_index
        d["cmd"] = self.cmd
        d["selections"] = serialize_checked_states(self._file_model.files, self._project.project_dir)
        d["work_dir_mode"] = self._work_dir_mode
        # NOTE: We enclose the arguments in quotes because that preserves the args that have spaces
        cmd_line_args = [f'"{arg}"' for arg in self.cmd_line_args]
        cmd_line_args = split_cmdline_args(" ".join(cmd_line_args))
        d["cmd_line_args"] = [serialize_url(arg, self._project.project_dir) for arg in cmd_line_args]
        return d

    @staticmethod
    def from_dict(name, item_dict, toolbox, project, logger):
        """See base class."""
        description, x, y = ProjectItem.parse_item_dict(item_dict)
        use_shell = item_dict.get("use_shell", True)
        shel_index = item_dict.get("shell_index", 0)
        cmd = item_dict.get("cmd", "")
        selections = deserialize_checked_states(item_dict.get("selections", list()), project.project_dir)
        work_dir_mode = item_dict.get("work_dir_mode", True)
        cmd_line_args = item_dict.get("cmd_line_args", [])
        cmd_line_args = [deserialize_path(arg, project.project_dir) for arg in cmd_line_args]
        return Gimlet(
            name,
            description,
            x,
            y,
            toolbox,
            project,
            logger,
            use_shell,
            shel_index,
            cmd,
            cmd_line_args,
            selections,
            work_dir_mode,
        )

    def notify_destination(self, source_item):
        """See base class."""
        if source_item.item_type() == "Data Connection":
            self._logger.msg.emit(
                f"Link established. Files from <b>{source_item.name}</b> are now available in <b>{self.name}</b>."
            )
            return
        if source_item.item_type() in [
            "Data Store",
            "Data Transformer",
            "Data Connection",
            "Tool",
            "Exporter",
            "Gimlet",
        ]:
            self._logger.msg.emit("Link established")
            return
        super().notify_destination(source_item)

    def _notify_if_duplicate_file_paths(self):
        """Adds a notification if file list contains duplicate entries."""
        labels = list()
        for item in self._file_model.files:
            labels.append(item.label)
        file_counter = Counter(labels)
        duplicates = list()
        for label, count in file_counter.items():
            if count > 1:
                duplicates.append(label)
        if duplicates:
            self.add_notification("Duplicate input files from predecessor items:<br>{}".format("<br>".join(duplicates)))

    def update_name_label(self):
        """Updates the name label in Gimlet properties tab.
        Used only when a project item is renamed."""
        self._properties_ui.label_gimlet_name.setText(self.name)

    @staticmethod
    def default_name_prefix():
        """See base class."""
        return "Gimlet"

    def resources_for_direct_successors(self):
        """Returns resources for direct successors.

        This enables communication of resources between
        project items in the app.

        Returns:
            list: List of ProjectItemResources
        """
        return self._toolbox_resources
