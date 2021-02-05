######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
QWidget that is used to create or edit Tool specifications.
In the former case it is presented empty, but in the latter it
is filled with all the information from the specification being edited.

:author: M. Marin (KTH), P. Savolainen (VTT)
:date:   12.4.2018
"""

import os
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QWidget, QStatusBar, QInputDialog, QFileDialog, QFileIconProvider, QMessageBox
from PySide2.QtCore import Slot, Qt, QFileInfo
from spinetoolbox.config import STATUSBAR_SS, TREEVIEW_HEADER_SS
from spinetoolbox.helpers import busy_effect, open_url
from spine_engine.utils.command_line_arguments import split_cmdline_args
from ..item_info import ItemInfo
from ..tool_specifications import TOOL_TYPES, REQUIRED_KEYS
from .custom_menus import AddIncludesPopupMenu


class ToolSpecificationWidget(QWidget):
    def __init__(self, toolbox, specification=None):
        """A widget to query user's preferences for a new tool specification.

        Args:
            toolbox (ToolboxUI): QMainWindow instance
            specification (ToolSpecification): If given, the form is pre-filled with this specification
        """
        from ..ui.tool_specification_form import Ui_Form  # pylint: disable=import-outside-toplevel

        super().__init__(parent=toolbox, f=Qt.Window)  # Inherit stylesheet from ToolboxUI
        # Setup UI from Qt Designer file
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.widget_main_program.setVisible(False)
        self.ui.textEdit_main_program.setStyleSheet(
            "QTextEdit {background-color: #19232D; border: 1px solid #32414B; color: #F0F0F0; border-radius: 2px;}"
        )
        # Class attributes
        self._toolbox = toolbox
        self._project = self._toolbox.project()
        self._original_specification = specification
        # init models
        self.sourcefiles_model = QStandardItemModel()
        self.inputfiles_model = QStandardItemModel()
        self.inputfiles_opt_model = QStandardItemModel()
        self.outputfiles_model = QStandardItemModel()
        # Add status bar to form
        self.statusbar = QStatusBar(self)
        self.statusbar.setFixedHeight(20)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setStyleSheet(STATUSBAR_SS)
        self.ui.horizontalLayout_statusbar_placeholder.addWidget(self.statusbar)
        # init ui
        self.ui.treeView_sourcefiles.setModel(self.sourcefiles_model)
        self.ui.treeView_inputfiles.setModel(self.inputfiles_model)
        self.ui.treeView_inputfiles_opt.setModel(self.inputfiles_opt_model)
        self.ui.treeView_outputfiles.setModel(self.outputfiles_model)
        self.ui.treeView_sourcefiles.setStyleSheet(TREEVIEW_HEADER_SS)
        self.ui.treeView_inputfiles.setStyleSheet(TREEVIEW_HEADER_SS)
        self.ui.treeView_inputfiles_opt.setStyleSheet(TREEVIEW_HEADER_SS)
        self.ui.treeView_outputfiles.setStyleSheet(TREEVIEW_HEADER_SS)
        self.ui.comboBox_tooltype.addItem("Select type...")
        self.ui.comboBox_tooltype.addItems(TOOL_TYPES)
        # if a specification is given, fill the form with data from it
        if specification is not None:
            self.ui.lineEdit_name.setText(specification.name)
            check_state = Qt.Checked if specification.execute_in_work else Qt.Unchecked
            self.ui.checkBox_execute_in_work.setCheckState(check_state)
            self.ui.textEdit_description.setPlainText(specification.description)
            self.ui.lineEdit_args.setText(" ".join(specification.cmdline_args))
            tool_types = [x.lower() for x in TOOL_TYPES]
            index = tool_types.index(specification.tooltype) + 1
            self.ui.comboBox_tooltype.setCurrentIndex(index)
        # Init lists
        self.sourcefiles = list(specification.includes) if specification else list()
        # Get first item from sourcefiles list as the main program file
        try:
            self.main_program_file = self.sourcefiles.pop(0)
        except IndexError:
            self.main_program_file = ""
        self.inputfiles = list(specification.inputfiles) if specification else list()
        self.inputfiles_opt = list(specification.inputfiles_opt) if specification else list()
        self.outputfiles = list(specification.outputfiles) if specification else list()
        self.program_path = specification.path if specification else None
        self.definition = dict(item_type=ItemInfo.item_type())
        # Populate lists (this will also create headers)
        self.populate_sourcefile_list(self.sourcefiles)
        self.populate_inputfiles_list(self.inputfiles)
        self.populate_inputfiles_opt_list(self.inputfiles_opt)
        self.populate_outputfiles_list(self.outputfiles)
        self.ui.lineEdit_name.setFocus()
        # Add includes popup menu
        self.add_source_files_popup_menu = AddIncludesPopupMenu(self)
        self.ui.toolButton_add_source_files.setMenu(self.add_source_files_popup_menu)
        self.ui.toolButton_add_source_files.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        self.ui.toolButton_add_source_files.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        self.connect_signals()
        if self.program_path is not None:  # It's None if the path does not exist
            self.set_main_program_file(os.path.join(self.program_path, self.main_program_file))

    def connect_signals(self):
        """Connect signals to slots."""
        self.ui.toolButton_add_source_files.clicked.connect(self.show_add_source_files_dialog)
        self.ui.toolButton_add_source_dirs.clicked.connect(self.show_add_source_dirs_dialog)
        self.ui.lineEdit_main_program.file_dropped.connect(self.set_main_program_file)
        self.ui.lineEdit_main_program.textChanged.connect(self.validate_main_program_file)
        self.ui.textEdit_main_program.document().modificationChanged.connect(
            self.ui.toolButton_save_main_program.setEnabled
        )
        self.ui.treeView_sourcefiles.files_dropped.connect(self.add_dropped_includes)
        self.ui.treeView_sourcefiles.doubleClicked.connect(self.open_includes_file)
        self.ui.toolButton_new_main_program.clicked.connect(self.new_main_program_file)
        self.ui.toolButton_browse_main_program.clicked.connect(self.browse_main_program_file)
        self.ui.toolButton_save_main_program.clicked.connect(self.save_main_program_file)
        self.ui.toolButton_minus_source_files.clicked.connect(self.remove_source_files)
        self.ui.toolButton_plus_inputfiles.clicked.connect(self.add_inputfiles)
        self.ui.toolButton_minus_inputfiles.clicked.connect(self.remove_inputfiles)
        self.ui.toolButton_plus_inputfiles_opt.clicked.connect(self.add_inputfiles_opt)
        self.ui.toolButton_minus_inputfiles_opt.clicked.connect(self.remove_inputfiles_opt)
        self.ui.toolButton_plus_outputfiles.clicked.connect(self.add_outputfiles)
        self.ui.toolButton_minus_outputfiles.clicked.connect(self.remove_outputfiles)
        self.ui.pushButton_ok.clicked.connect(self.handle_ok_clicked)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        # Enable removing items from QTreeViews by pressing the Delete key
        self.ui.treeView_sourcefiles.del_key_pressed.connect(self.remove_source_files_with_del)
        self.ui.treeView_inputfiles.del_key_pressed.connect(self.remove_inputfiles_with_del)
        self.ui.treeView_inputfiles_opt.del_key_pressed.connect(self.remove_inputfiles_opt_with_del)
        self.ui.treeView_outputfiles.del_key_pressed.connect(self.remove_outputfiles_with_del)

    def populate_sourcefile_list(self, items):
        """List source files in QTreeView.
        If items is None or empty list, model is cleared.
        """
        self.sourcefiles_model.clear()
        self.sourcefiles_model.setHorizontalHeaderItem(0, QStandardItem("Additional source files"))  # Add header
        if items is not None:
            for item in items:
                qitem = QStandardItem(item)
                qitem.setFlags(~Qt.ItemIsEditable)
                qitem.setData(QFileIconProvider().icon(QFileInfo(item)), Qt.DecorationRole)
                self.sourcefiles_model.appendRow(qitem)

    def populate_inputfiles_list(self, items):
        """List input files in QTreeView.
        If items is None or empty list, model is cleared.
        """
        self.inputfiles_model.clear()
        self.inputfiles_model.setHorizontalHeaderItem(0, QStandardItem("Input files"))  # Add header
        if items is not None:
            for item in items:
                qitem = QStandardItem(item)
                qitem.setData(QFileIconProvider().icon(QFileInfo(item)), Qt.DecorationRole)
                self.inputfiles_model.appendRow(qitem)

    def populate_inputfiles_opt_list(self, items):
        """List optional input files in QTreeView.
        If items is None or empty list, model is cleared.
        """
        self.inputfiles_opt_model.clear()
        self.inputfiles_opt_model.setHorizontalHeaderItem(0, QStandardItem("Optional input files"))  # Add header
        if items is not None:
            for item in items:
                qitem = QStandardItem(item)
                qitem.setData(QFileIconProvider().icon(QFileInfo(item)), Qt.DecorationRole)
                self.inputfiles_opt_model.appendRow(qitem)

    def populate_outputfiles_list(self, items):
        """List output files in QTreeView.
        If items is None or empty list, model is cleared.
        """
        self.outputfiles_model.clear()
        self.outputfiles_model.setHorizontalHeaderItem(0, QStandardItem("Output files"))  # Add header
        if items is not None:
            for item in items:
                qitem = QStandardItem(item)
                qitem.setData(QFileIconProvider().icon(QFileInfo(item)), Qt.DecorationRole)
                self.outputfiles_model.appendRow(qitem)

    @Slot(bool)
    def browse_main_program_file(self, checked=False):
        """Open file browser where user can select the path of the main program file."""
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getOpenFileName(
            self, "Select existing main program file", self._project.project_dir, "*.*"
        )
        file_path = answer[0]
        if not file_path:  # Cancel button clicked
            return
        self.set_main_program_file(file_path)

    @Slot("QString")
    def set_main_program_file(self, file_path):
        """Set main program file and folder path."""
        self.ui.lineEdit_main_program.setText(file_path)

    @Slot(str)
    def validate_main_program_file(self, file_path):
        folder_path = os.path.split(file_path)[0]
        self.program_path = os.path.abspath(folder_path)
        # Update UI
        self.ui.label_mainpath.setText(self.program_path)
        if not os.path.isfile(file_path):
            self.show_status_bar_msg("Main program file is not valid")
            self.ui.widget_main_program.setVisible(False)
            return
        self.ui.widget_main_program.setVisible(True)
        # Load main program file into text edit
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            self.ui.textEdit_main_program.setPlainText(text)
        except IOError as e:
            self.show_status_bar_msg(e)

    @Slot(bool)
    def save_main_program_file(self, _=False):
        """Saves main program file."""
        main_program = self.ui.lineEdit_main_program.text().strip()
        try:
            with open(main_program, "w") as file:
                file.write(self.ui.textEdit_main_program.toPlainText())
            self.ui.textEdit_main_program.document().setModified(False)
            self.show_status_bar_msg(f"Main program file '{os.path.basename(main_program)}' saved successfully")
        except IOError as e:
            self.show_status_bar_msg(e)

    @Slot(bool)
    def new_main_program_file(self, _=False):
        """Creates a new blank main program file. Let's user decide the file name and path.
         Alternative version using only one getSaveFileName dialog.
         """
        # noinspection PyCallByClass
        answer = QFileDialog.getSaveFileName(self, "Create new main program file", self._project.project_dir)
        file_path = answer[0]
        if not file_path:  # Cancel button clicked
            return
        # Remove file if it exists. getSaveFileName has asked confirmation for us.
        try:
            os.remove(file_path)
        except OSError:
            pass
        try:
            with open(file_path, "w"):
                pass
        except OSError:
            msg = "Please check directory permissions."
            # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
            QMessageBox.information(self, "Creating file failed", msg)
            return
        self.set_main_program_file(file_path)

    @Slot()
    def new_source_file(self):
        """Let user create a new source file for this tool specification."""
        path = self.program_path if self.program_path else self._project.project_dir
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        dir_path = QFileDialog.getSaveFileName(self, "Create source file", path, "*.*")
        file_path = dir_path[0]
        if file_path == "":  # Cancel button clicked
            return
        # create file. NOTE: getSaveFileName does the 'check for existence' for us
        open(file_path, "w").close()
        self.add_single_include(file_path)

    @Slot(bool)
    def show_add_source_files_dialog(self, checked=False):
        """Let user select source files for this tool specification."""
        path = self.program_path if self.program_path else self._project.project_dir
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getOpenFileNames(self, "Add source file", path, "*.*")
        file_paths = answer[0]
        if not file_paths:  # Cancel button clicked
            return
        for path in file_paths:
            if not self.add_single_include(path):
                continue

    @Slot(bool)
    def show_add_source_dirs_dialog(self, checked=False):
        """Let user select a source directory for this tool specification.
        All files and sub-directories will be added to the source files.
        """
        path = self.program_path if self.program_path else self._project.project_dir
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getExistingDirectory(self, "Select a directory to add to source files", path)
        file_paths = list()
        for root, _, files in os.walk(answer):
            for file in files:
                file_paths.append(os.path.abspath(os.path.join(root, file)))
        for path in file_paths:
            if not self.add_single_include(path):
                continue

    @Slot("QVariant")
    def add_dropped_includes(self, file_paths):
        """Adds dropped file paths to Source files list."""
        for path in file_paths:
            if not self.add_single_include(path):
                continue

    def add_single_include(self, path):
        """Add file path to Source files list."""
        dirname, file_pattern = os.path.split(path)
        # logging.debug("program path:{0}".format(self.program_path))
        # logging.debug("{0}, {1}".format(dirname, file_pattern))
        if not self.program_path:
            self.program_path = dirname
            self.ui.label_mainpath.setText(self.program_path)
            path_to_add = file_pattern
        else:
            # check if path is a descendant of main dir.
            common_prefix = os.path.commonprefix([os.path.abspath(self.program_path), os.path.abspath(path)])
            # logging.debug("common_prefix:{0}".format(common_prefix))
            if common_prefix != self.program_path:
                self.show_status_bar_msg(
                    "Source file {0}'s location is invalid " "(should be in main directory)".format(file_pattern)
                )
                return False
            path_to_add = os.path.relpath(path, self.program_path)
        if self.sourcefiles_model.findItems(path_to_add):
            self.show_status_bar_msg("Source file {0} already included".format(path_to_add))
            return False
        qitem = QStandardItem(path_to_add)
        qitem.setFlags(~Qt.ItemIsEditable)
        qitem.setData(QFileIconProvider().icon(QFileInfo(path_to_add)), Qt.DecorationRole)
        self.sourcefiles_model.appendRow(qitem)
        return True

    @busy_effect
    @Slot("QModelIndex")
    def open_includes_file(self, index):
        """Open source file in default program."""
        if not index:
            return
        if not index.isValid():
            self._toolbox.msg_error.emit("Selected index not valid")
            return
        includes_file = self.sourcefiles_model.itemFromIndex(index).text()
        _, ext = os.path.splitext(includes_file)
        if ext in [".bat", ".exe"]:
            self._toolbox.msg_warning.emit(
                "Sorry, opening files with extension <b>{0}</b> not implemented. "
                "Please open the file manually.".format(ext)
            )
            return
        url = "file:///" + os.path.join(self.program_path, includes_file)
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        res = open_url(url)
        if not res:
            self._toolbox.msg_error.emit("Failed to open file: <b>{0}</b>".format(includes_file))

    @Slot()
    def remove_source_files_with_del(self):
        """Support for deleting items with the Delete key."""
        self.remove_source_files()

    @Slot(bool)
    def remove_source_files(self, checked=False):
        """Remove selected source files from include list.
        Do not remove anything if there are no items selected.
        """
        indexes = self.ui.treeView_sourcefiles.selectedIndexes()
        if not indexes:  # Nothing selected
            self.show_status_bar_msg("Please select the source files to remove")
        else:
            rows = [ind.row() for ind in indexes]
            rows.sort(reverse=True)
            for row in rows:
                self.sourcefiles_model.removeRow(row)
            if self.sourcefiles_model.rowCount() == 0:
                if self.ui.lineEdit_main_program.text().strip() == "":
                    self.program_path = None
                    self.ui.label_mainpath.clear()
            self.show_status_bar_msg("Selected source files removed")

    @Slot(bool)
    def add_inputfiles(self, checked=False):
        """Let user select input files for this tool specification."""
        msg = (
            "Add an input file or a directory required by your program. Wildcards "
            "<b>are not</b> supported.<br/><br/>"
            "Examples:<br/>"
            "<b>data.csv</b> -> File is copied to the same work directory as the main program.<br/>"
            "<b>input/data.csv</b> -> Creates subdirectory /input to work directory and "
            "copies file data.csv there.<br/>"
            "<b>output/</b> -> Creates an empty directory into the work directory.<br/><br/>"
        )
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QInputDialog.getText(self, "Add input item", msg, flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        file_name = answer[0]
        if not file_name:  # Cancel button clicked
            return
        qitem = QStandardItem(file_name)
        qitem.setData(QFileIconProvider().icon(QFileInfo(file_name)), Qt.DecorationRole)
        self.inputfiles_model.appendRow(qitem)

    @Slot()
    def remove_inputfiles_with_del(self):
        """Support for deleting items with the Delete key."""
        self.remove_inputfiles()

    @Slot(bool)
    def remove_inputfiles(self, checked=False):
        """Remove selected input files from list.
        Do not remove anything if there are no items selected.
        """
        indexes = self.ui.treeView_inputfiles.selectedIndexes()
        if not indexes:  # Nothing selected
            self.show_status_bar_msg("Please select the input files to remove")
        else:
            rows = [ind.row() for ind in indexes]
            rows.sort(reverse=True)
            for row in rows:
                self.inputfiles_model.removeRow(row)
            self.show_status_bar_msg("Selected input files removed")

    @Slot(bool)
    def add_inputfiles_opt(self, checked=False):
        """Let user select optional input files for this tool specification."""
        msg = (
            "Add optional input files that may be utilized by your program. <br/>"
            "Wildcards are supported.<br/><br/>"
            "Examples:<br/>"
            "<b>data.csv</b> -> If found, file is copied to the same work directory as the main program.<br/>"
            "<b>*.csv</b> -> All found CSV files are copied to the same work directory as the main program.<br/>"
            "<b>input/data_?.dat</b> -> All found files matching the pattern 'data_?.dat' will be copied to <br/>"
            "input/ subdirectory under the same work directory as the main program.<br/><br/>"
        )
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QInputDialog.getText(
            self, "Add optional input item", msg, flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint
        )
        file_name = answer[0]
        if not file_name:  # Cancel button clicked
            return
        qitem = QStandardItem(file_name)
        qitem.setData(QFileIconProvider().icon(QFileInfo(file_name)), Qt.DecorationRole)
        self.inputfiles_opt_model.appendRow(qitem)

    @Slot()
    def remove_inputfiles_opt_with_del(self):
        """Support for deleting items with the Delete key."""
        self.remove_inputfiles_opt()

    @Slot(bool)
    def remove_inputfiles_opt(self, checked=False):
        """Remove selected optional input files from list.
        Do not remove anything if there are no items selected.
        """
        indexes = self.ui.treeView_inputfiles_opt.selectedIndexes()
        if not indexes:  # Nothing selected
            self.show_status_bar_msg("Please select the optional input files to remove")
        else:
            rows = [ind.row() for ind in indexes]
            rows.sort(reverse=True)
            for row in rows:
                self.inputfiles_opt_model.removeRow(row)
            self.show_status_bar_msg("Selected optional input files removed")

    @Slot(bool)
    def add_outputfiles(self, checked=False):
        """Let user select output files for this tool specification."""
        msg = (
            "Add output files that will be archived into the Tool results directory after the <br/>"
            "Tool specification has finished execution. Wildcards are supported.<br/><br/>"
            "Examples:<br/>"
            "<b>results.csv</b> -> File is copied from work directory into results.<br/> "
            "<b>*.csv</b> -> All CSV files will copied into results.<br/> "
            "<b>output/*.gdx</b> -> All GDX files from the work subdirectory /output will be copied into <br/>"
            "results /output subdirectory.<br/><br/>"
        )
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QInputDialog.getText(self, "Add output item", msg, flags=Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        file_name = answer[0]
        if not file_name:  # Cancel button clicked
            return
        qitem = QStandardItem(file_name)
        qitem.setData(QFileIconProvider().icon(QFileInfo(file_name)), Qt.DecorationRole)
        self.outputfiles_model.appendRow(qitem)

    @Slot()
    def remove_outputfiles_with_del(self):
        """Support for deleting items with the Delete key."""
        self.remove_outputfiles()

    @Slot(bool)
    def remove_outputfiles(self, checked=False):
        """Remove selected output files from list.
        Do not remove anything if there are no items selected.
        """
        indexes = self.ui.treeView_outputfiles.selectedIndexes()
        if not indexes:  # Nothing selected
            self.show_status_bar_msg("Please select the output files to remove")
        else:
            rows = [ind.row() for ind in indexes]
            rows.sort(reverse=True)
            for row in rows:
                self.outputfiles_model.removeRow(row)
            self.show_status_bar_msg("Selected output files removed")

    @Slot()
    def handle_ok_clicked(self):
        """Checks that everything is valid, creates Tool spec definition dictionary and adds Tool spec to project."""
        # Check that tool type is selected
        if self.ui.comboBox_tooltype.currentIndex() == 0:
            self.show_status_bar_msg("Tool type not selected")
            return
        self.definition["name"] = self.ui.lineEdit_name.text()
        self.definition["description"] = self.ui.textEdit_description.toPlainText()
        self.definition["tooltype"] = self.ui.comboBox_tooltype.currentText().lower()
        flags = Qt.MatchContains
        # Check that path of main program file is valid before saving it
        main_program = self.ui.lineEdit_main_program.text().strip()
        if not os.path.isfile(main_program):
            self.show_status_bar_msg("Main program file is not valid")
            return
        # Fix for issue #241
        folder_path, file_path = os.path.split(main_program)
        self.program_path = os.path.abspath(folder_path)
        self.ui.label_mainpath.setText(self.program_path)
        self.definition["execute_in_work"] = self.ui.checkBox_execute_in_work.isChecked()
        self.definition["includes"] = [file_path]
        self.definition["includes"] += [i.text() for i in self.sourcefiles_model.findItems("", flags)]
        self.definition["inputfiles"] = [i.text() for i in self.inputfiles_model.findItems("", flags)]
        self.definition["inputfiles_opt"] = [i.text() for i in self.inputfiles_opt_model.findItems("", flags)]
        self.definition["outputfiles"] = [i.text() for i in self.outputfiles_model.findItems("", flags)]
        # Strip whitespace from args before saving it to JSON
        self.definition["cmdline_args"] = split_cmdline_args(self.ui.lineEdit_args.text())
        for k in REQUIRED_KEYS:
            if not self.definition[k]:
                self.show_status_bar_msg(f"{k} missing")
                return
        # Create new Tool specification
        if self.call_add_tool_specification():
            self.close()

    def _make_tool_specification(self):
        """Returns a ToolSpecification from current form settings.

        Returns:
            ToolSpecification
        """
        self.definition["includes_main_path"] = self.program_path.replace(os.sep, "/")
        tool = self._toolbox.load_specification(self.definition)
        if not tool:
            self.show_status_bar_msg("Adding Tool specification failed")
        return tool

    def call_add_tool_specification(self):
        """Adds or updates Tool specification according to user's selections.
        If the name is the same as an existing tool specification, it is updated and
        auto-saved to the definition file. (User is editing an existing
        tool specification.) If the name is not in the tool specification model, creates
        a new tool specification and offers to save the definition file. (User is
        creating a new tool specification from scratch or spawning from an existing one).
        """
        new_spec = self._make_tool_specification()
        if not new_spec:
            return False
        if self._original_specification is not None and new_spec.is_equivalent(self._original_specification):
            # Nothing changed
            return True
        if self._original_specification is None or self.definition["name"] != self._original_specification.name:
            # The user is creating a new spec, either from scratch (no original spec)
            # or by changing the name of an existing one
            self._toolbox.add_specification(new_spec)
        else:
            # The user is modifying an existing spec, while conserving the name
            new_spec.definition_file_path = self._original_specification.definition_file_path
            self._toolbox.update_specification(new_spec)
        return True

    def keyPressEvent(self, e):
        """Close Setup form when escape key is pressed.

        Args:
            e (QKeyEvent): Received key press event.
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event=None):
        """Handle close window.

        Args:
            event (QEvent): Closing event if 'X' is clicked.
        """
        if event:
            event.accept()

    def show_status_bar_msg(self, msg):
        word_count = len(msg.split(" "))
        mspw = 60000 / 140  # Assume people can read ~140 words per minute
        duration = mspw * word_count
        self.statusbar.showMessage(msg, duration)
