# -*- coding: utf-8 -*-
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

################################################################################
## Form generated from reading UI file 'tool_specification_form.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from spinetoolbox.widgets.custom_qlineedits import CustomQLineEdit
from spinetoolbox.widgets.custom_qtreeview import CustomTreeView
from spinetoolbox.widgets.custom_qtreeview import SourcesTreeView
from spine_items.tool.widgets.main_program_text_edit import MainProgramTextEdit

from spine_items import resources_icons_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.ApplicationModal)
        Form.resize(600, 997)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(Form)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy1)
        self.lineEdit_name.setMinimumSize(QSize(220, 24))
        self.lineEdit_name.setMaximumSize(QSize(5000, 24))
        self.lineEdit_name.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit_name)

        self.comboBox_tooltype = QComboBox(Form)
        self.comboBox_tooltype.setObjectName(u"comboBox_tooltype")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_tooltype.sizePolicy().hasHeightForWidth())
        self.comboBox_tooltype.setSizePolicy(sizePolicy2)
        self.comboBox_tooltype.setMinimumSize(QSize(180, 24))
        self.comboBox_tooltype.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout.addWidget(self.comboBox_tooltype)


        self.verticalLayout_11.addLayout(self.horizontalLayout)

        self.textEdit_description = QTextEdit(Form)
        self.textEdit_description.setObjectName(u"textEdit_description")
        self.textEdit_description.setMaximumSize(QSize(16777215, 80))
        self.textEdit_description.setFocusPolicy(Qt.StrongFocus)
        self.textEdit_description.setTabChangesFocus(True)

        self.verticalLayout_11.addWidget(self.textEdit_description)

        self.checkBox_execute_in_work = QCheckBox(Form)
        self.checkBox_execute_in_work.setObjectName(u"checkBox_execute_in_work")
        self.checkBox_execute_in_work.setChecked(True)

        self.verticalLayout_11.addWidget(self.checkBox_execute_in_work)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit_main_program = CustomQLineEdit(Form)
        self.lineEdit_main_program.setObjectName(u"lineEdit_main_program")
        self.lineEdit_main_program.setClearButtonEnabled(True)

        self.horizontalLayout_6.addWidget(self.lineEdit_main_program)

        self.toolButton_new_main_program = QToolButton(Form)
        self.toolButton_new_main_program.setObjectName(u"toolButton_new_main_program")
        self.toolButton_new_main_program.setMaximumSize(QSize(22, 22))
        icon = QIcon()
        icon.addFile(u":/icons/file.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_new_main_program.setIcon(icon)
        self.toolButton_new_main_program.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout_6.addWidget(self.toolButton_new_main_program)

        self.toolButton_browse_main_program = QToolButton(Form)
        self.toolButton_browse_main_program.setObjectName(u"toolButton_browse_main_program")
        icon1 = QIcon()
        icon1.addFile(u":/icons/folder-open-solid.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_browse_main_program.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.toolButton_browse_main_program)


        self.verticalLayout_11.addLayout(self.horizontalLayout_6)


        self.verticalLayout_5.addLayout(self.verticalLayout_11)

        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(6)
        self.widget_main_program = QWidget(self.splitter)
        self.widget_main_program.setObjectName(u"widget_main_program")
        self.verticalLayout_2 = QVBoxLayout(self.widget_main_program)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEdit_main_program = MainProgramTextEdit(self.widget_main_program)
        self.textEdit_main_program.setObjectName(u"textEdit_main_program")
        self.textEdit_main_program.setEnabled(True)

        self.verticalLayout_2.addWidget(self.textEdit_main_program)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 2, -1, 2)
        self.label = QLabel(self.widget_main_program)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)

        self.horizontalLayout_7.addWidget(self.label)

        self.label_mainpath = QLabel(self.widget_main_program)
        self.label_mainpath.setObjectName(u"label_mainpath")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_mainpath.sizePolicy().hasHeightForWidth())
        self.label_mainpath.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_mainpath.setFont(font1)

        self.horizontalLayout_7.addWidget(self.label_mainpath)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.toolButton_save_main_program = QToolButton(self.widget_main_program)
        self.toolButton_save_main_program.setObjectName(u"toolButton_save_main_program")
        self.toolButton_save_main_program.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_save_main_program.setIcon(icon2)

        self.horizontalLayout_7.addWidget(self.toolButton_save_main_program)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.splitter.addWidget(self.widget_main_program)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.treeView_sourcefiles = SourcesTreeView(self.widget_2)
        self.treeView_sourcefiles.setObjectName(u"treeView_sourcefiles")
        sizePolicy3.setHeightForWidth(self.treeView_sourcefiles.sizePolicy().hasHeightForWidth())
        self.treeView_sourcefiles.setSizePolicy(sizePolicy3)
        self.treeView_sourcefiles.setMaximumSize(QSize(16777215, 200))
        font2 = QFont()
        font2.setPointSize(10)
        self.treeView_sourcefiles.setFont(font2)
        self.treeView_sourcefiles.setFocusPolicy(Qt.StrongFocus)
        self.treeView_sourcefiles.setAcceptDrops(True)
        self.treeView_sourcefiles.setLineWidth(1)
        self.treeView_sourcefiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView_sourcefiles.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.treeView_sourcefiles.setIndentation(5)

        self.verticalLayout_3.addWidget(self.treeView_sourcefiles)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButton_add_source_files = QToolButton(self.widget_2)
        self.toolButton_add_source_files.setObjectName(u"toolButton_add_source_files")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.toolButton_add_source_files.sizePolicy().hasHeightForWidth())
        self.toolButton_add_source_files.setSizePolicy(sizePolicy4)
        self.toolButton_add_source_files.setMinimumSize(QSize(22, 22))
        self.toolButton_add_source_files.setMaximumSize(QSize(22, 22))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        font3.setWeight(75)
        self.toolButton_add_source_files.setFont(font3)
        icon3 = QIcon()
        icon3.addFile(u":/icons/file-link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_add_source_files.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.toolButton_add_source_files)

        self.toolButton_add_source_dirs = QToolButton(self.widget_2)
        self.toolButton_add_source_dirs.setObjectName(u"toolButton_add_source_dirs")
        self.toolButton_add_source_dirs.setMinimumSize(QSize(22, 22))
        self.toolButton_add_source_dirs.setMaximumSize(QSize(22, 22))
        icon4 = QIcon()
        icon4.addFile(u":/icons/folder-link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_add_source_dirs.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.toolButton_add_source_dirs)

        self.toolButton_minus_source_files = QToolButton(self.widget_2)
        self.toolButton_minus_source_files.setObjectName(u"toolButton_minus_source_files")
        sizePolicy4.setHeightForWidth(self.toolButton_minus_source_files.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_source_files.setSizePolicy(sizePolicy4)
        self.toolButton_minus_source_files.setMinimumSize(QSize(22, 22))
        self.toolButton_minus_source_files.setMaximumSize(QSize(22, 22))
        self.toolButton_minus_source_files.setFont(font3)
        icon5 = QIcon()
        icon5.addFile(u":/icons/trash-alt.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_minus_source_files.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.toolButton_minus_source_files)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_15)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 1, 0, 1, 1)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setSpacing(6)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.treeView_inputfiles_opt = CustomTreeView(self.widget_2)
        self.treeView_inputfiles_opt.setObjectName(u"treeView_inputfiles_opt")
        self.treeView_inputfiles_opt.setMaximumSize(QSize(16777215, 500))
        self.treeView_inputfiles_opt.setFont(font2)
        self.treeView_inputfiles_opt.setFocusPolicy(Qt.StrongFocus)
        self.treeView_inputfiles_opt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView_inputfiles_opt.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.treeView_inputfiles_opt.setIndentation(5)

        self.verticalLayout_15.addWidget(self.treeView_inputfiles_opt)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButton_plus_inputfiles_opt = QToolButton(self.widget_2)
        self.toolButton_plus_inputfiles_opt.setObjectName(u"toolButton_plus_inputfiles_opt")
        sizePolicy4.setHeightForWidth(self.toolButton_plus_inputfiles_opt.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_inputfiles_opt.setSizePolicy(sizePolicy4)
        self.toolButton_plus_inputfiles_opt.setMinimumSize(QSize(22, 22))
        self.toolButton_plus_inputfiles_opt.setMaximumSize(QSize(22, 22))
        self.toolButton_plus_inputfiles_opt.setFont(font3)
        self.toolButton_plus_inputfiles_opt.setIcon(icon3)

        self.horizontalLayout_5.addWidget(self.toolButton_plus_inputfiles_opt)

        self.toolButton_minus_inputfiles_opt = QToolButton(self.widget_2)
        self.toolButton_minus_inputfiles_opt.setObjectName(u"toolButton_minus_inputfiles_opt")
        sizePolicy4.setHeightForWidth(self.toolButton_minus_inputfiles_opt.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_inputfiles_opt.setSizePolicy(sizePolicy4)
        self.toolButton_minus_inputfiles_opt.setMinimumSize(QSize(22, 22))
        self.toolButton_minus_inputfiles_opt.setMaximumSize(QSize(22, 22))
        self.toolButton_minus_inputfiles_opt.setFont(font3)
        self.toolButton_minus_inputfiles_opt.setIcon(icon5)

        self.horizontalLayout_5.addWidget(self.toolButton_minus_inputfiles_opt)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)


        self.verticalLayout_15.addLayout(self.horizontalLayout_5)


        self.gridLayout_3.addLayout(self.verticalLayout_15, 2, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeView_inputfiles = CustomTreeView(self.widget_2)
        self.treeView_inputfiles.setObjectName(u"treeView_inputfiles")
        sizePolicy3.setHeightForWidth(self.treeView_inputfiles.sizePolicy().hasHeightForWidth())
        self.treeView_inputfiles.setSizePolicy(sizePolicy3)
        self.treeView_inputfiles.setMaximumSize(QSize(16777215, 500))
        self.treeView_inputfiles.setFont(font2)
        self.treeView_inputfiles.setFocusPolicy(Qt.StrongFocus)
        self.treeView_inputfiles.setLineWidth(1)
        self.treeView_inputfiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView_inputfiles.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.treeView_inputfiles.setIndentation(5)
        self.treeView_inputfiles.setUniformRowHeights(False)

        self.verticalLayout_4.addWidget(self.treeView_inputfiles)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.toolButton_plus_inputfiles = QToolButton(self.widget_2)
        self.toolButton_plus_inputfiles.setObjectName(u"toolButton_plus_inputfiles")
        sizePolicy4.setHeightForWidth(self.toolButton_plus_inputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_inputfiles.setSizePolicy(sizePolicy4)
        self.toolButton_plus_inputfiles.setMinimumSize(QSize(22, 22))
        self.toolButton_plus_inputfiles.setMaximumSize(QSize(22, 22))
        self.toolButton_plus_inputfiles.setFont(font3)
        self.toolButton_plus_inputfiles.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.toolButton_plus_inputfiles)

        self.toolButton_minus_inputfiles = QToolButton(self.widget_2)
        self.toolButton_minus_inputfiles.setObjectName(u"toolButton_minus_inputfiles")
        sizePolicy4.setHeightForWidth(self.toolButton_minus_inputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_inputfiles.setSizePolicy(sizePolicy4)
        self.toolButton_minus_inputfiles.setMinimumSize(QSize(22, 22))
        self.toolButton_minus_inputfiles.setMaximumSize(QSize(22, 22))
        self.toolButton_minus_inputfiles.setFont(font3)
        self.toolButton_minus_inputfiles.setIcon(icon5)

        self.horizontalLayout_4.addWidget(self.toolButton_minus_inputfiles)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 1, 1, 1)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.treeView_outputfiles = CustomTreeView(self.widget_2)
        self.treeView_outputfiles.setObjectName(u"treeView_outputfiles")
        self.treeView_outputfiles.setMaximumSize(QSize(16777215, 500))
        self.treeView_outputfiles.setFont(font2)
        self.treeView_outputfiles.setFocusPolicy(Qt.WheelFocus)
        self.treeView_outputfiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView_outputfiles.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.treeView_outputfiles.setIndentation(5)

        self.verticalLayout_16.addWidget(self.treeView_outputfiles)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolButton_plus_outputfiles = QToolButton(self.widget_2)
        self.toolButton_plus_outputfiles.setObjectName(u"toolButton_plus_outputfiles")
        sizePolicy4.setHeightForWidth(self.toolButton_plus_outputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_outputfiles.setSizePolicy(sizePolicy4)
        self.toolButton_plus_outputfiles.setMinimumSize(QSize(22, 22))
        self.toolButton_plus_outputfiles.setMaximumSize(QSize(22, 22))
        self.toolButton_plus_outputfiles.setFont(font3)
        self.toolButton_plus_outputfiles.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.toolButton_plus_outputfiles)

        self.toolButton_minus_outputfiles = QToolButton(self.widget_2)
        self.toolButton_minus_outputfiles.setObjectName(u"toolButton_minus_outputfiles")
        sizePolicy4.setHeightForWidth(self.toolButton_minus_outputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_outputfiles.setSizePolicy(sizePolicy4)
        self.toolButton_minus_outputfiles.setMinimumSize(QSize(22, 22))
        self.toolButton_minus_outputfiles.setMaximumSize(QSize(22, 22))
        self.toolButton_minus_outputfiles.setFont(font3)
        self.toolButton_minus_outputfiles.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.toolButton_minus_outputfiles)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_13)


        self.verticalLayout_16.addLayout(self.horizontalLayout_3)


        self.gridLayout_3.addLayout(self.verticalLayout_16, 2, 1, 1, 1)

        self.lineEdit_args = QLineEdit(self.widget_2)
        self.lineEdit_args.setObjectName(u"lineEdit_args")
        sizePolicy1.setHeightForWidth(self.lineEdit_args.sizePolicy().hasHeightForWidth())
        self.lineEdit_args.setSizePolicy(sizePolicy1)
        self.lineEdit_args.setMinimumSize(QSize(220, 24))
        self.lineEdit_args.setMaximumSize(QSize(5000, 24))
        self.lineEdit_args.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_args, 0, 0, 1, 2)

        self.splitter.addWidget(self.widget_2)

        self.verticalLayout_5.addWidget(self.splitter)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.pushButton_ok = QPushButton(Form)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_8.addWidget(self.pushButton_ok)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.pushButton_cancel = QPushButton(Form)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_8.addWidget(self.pushButton_cancel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.horizontalLayout_statusbar_placeholder = QHBoxLayout()
        self.horizontalLayout_statusbar_placeholder.setObjectName(u"horizontalLayout_statusbar_placeholder")
        self.widget_invisible_dummy = QWidget(Form)
        self.widget_invisible_dummy.setObjectName(u"widget_invisible_dummy")

        self.horizontalLayout_statusbar_placeholder.addWidget(self.widget_invisible_dummy)


        self.verticalLayout_6.addLayout(self.horizontalLayout_statusbar_placeholder)

        QWidget.setTabOrder(self.pushButton_ok, self.pushButton_cancel)

        self.retranslateUi(Form)

        self.pushButton_ok.setDefault(True)
        self.pushButton_cancel.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Tool Specification editor", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_name.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Tool specification name (required)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("Form", u"Type name here...", None))
#if QT_CONFIG(tooltip)
        self.comboBox_tooltype.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Tool specification type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_tooltype.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.textEdit_description.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Tool specification description (optional)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_description.setPlaceholderText(QCoreApplication.translate("Form", u"Type description here...", None))
#if QT_CONFIG(tooltip)
        self.checkBox_execute_in_work.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>If checked, Tool specification is executed in a work directory (default).</p><p>If unchecked, Tool specification is executed in main program file directory.</p><p>It is recommended to uncheck this for <span style=\" font-weight:600;\">Executable</span> Tool specifications.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_execute_in_work.setText(QCoreApplication.translate("Form", u"Execute in work directory", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_main_program.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Main program file that is used to launch the Tool specification (required)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_main_program.setPlaceholderText(QCoreApplication.translate("Form", u"Type path of main program file here...", None))
#if QT_CONFIG(tooltip)
        self.toolButton_new_main_program.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Create new main program file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_browse_main_program.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select existing main program file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_browse_main_program.setText(QCoreApplication.translate("Form", u"...", None))
        self.textEdit_main_program.setPlaceholderText(QCoreApplication.translate("Form", u"Create main program file here...", None))
        self.label.setText(QCoreApplication.translate("Form", u"Main program directory", None))
        self.label_mainpath.setText("")
#if QT_CONFIG(tooltip)
        self.toolButton_save_main_program.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Save</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_save_main_program.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.treeView_sourcefiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Other source files and/or directories (in addition to the main program file) <span style=\" font-weight:600;\">required</span> by the program.</p><p><span style=\" font-weight:600;\">Tip</span>: You can Drag &amp; Drop files and/or directories here from File Explorer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_add_source_files.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Add source code <span style=\" font-weight:600;\">files</span> that your program requires in order to run.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_add_source_files.setText("")
#if QT_CONFIG(tooltip)
        self.toolButton_add_source_dirs.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Add source code <span style=\" font-weight:600;\">directory</span> and all its contents.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_minus_source_files.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Remove selected item(s)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_minus_source_files.setText("")
#if QT_CONFIG(tooltip)
        self.treeView_inputfiles_opt.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Optional</span> data files for the program.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_plus_inputfiles_opt.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Add optional input filenames and/or directories.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_plus_inputfiles_opt.setText("")
#if QT_CONFIG(tooltip)
        self.toolButton_minus_inputfiles_opt.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Remove selected item(s)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_minus_inputfiles_opt.setText("")
#if QT_CONFIG(tooltip)
        self.treeView_inputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Required</span> data files for the program.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_plus_inputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Add input filenames and/or directories required by the program. Examples:</p><p>'data.csv'</p><p>'input/data.csv'</p><p>'input/'</p><p>'output/'</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_plus_inputfiles.setText("")
#if QT_CONFIG(tooltip)
        self.toolButton_minus_inputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Remove selected item(s)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_minus_inputfiles.setText("")
#if QT_CONFIG(tooltip)
        self.treeView_outputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Output files that may be used by other project items downstream. These files will be archived into a results directory after execution.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.toolButton_plus_outputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Add output filenames produced by your program that are saved to results after execution.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_plus_outputfiles.setText("")
#if QT_CONFIG(tooltip)
        self.toolButton_minus_outputfiles.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Remove selected item(s)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_minus_outputfiles.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_args.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Command line arguments (space-delimited) for the main program (optional). Use '@@' tags to refer to input files or URLs, see the User Guide for details.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_args.setPlaceholderText(QCoreApplication.translate("Form", u"Type command line arguments here...", None))
        self.pushButton_ok.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

