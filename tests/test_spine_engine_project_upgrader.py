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
"""Unit tests for spine_engine.project.project_upgrader module.

These tests test project.json upgrades up to and including version 10.
They are here and not in spine_engine because project.json upgrades up to version 10 depend on spine_items.
"""

import importlib
import json
from unittest import mock
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from spine_engine.project.project_upgrader import is_valid, upgrade
from spine_engine.project.exception import ProjectUpgradeFailed

LATEST_SPINE_ITEMS_DEPENDENT_PROJECT_VERSION = 10


class TestIsValid(unittest.TestCase):
    def test_is_valid_v1(self):
        """Tests is_valid for a version 1 project dictionary."""
        p = make_v1_project_dict()
        try:
            is_valid(p, 1)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v1 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["objects"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 1)

    def test_is_valid_v2(self):
        """Tests is_valid for a version 2 project dictionary."""
        p = make_v2_project_dict()
        try:
            is_valid(p, 2)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v2 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 3)

    def test_is_valid_v3(self):
        """Tests is_valid for a version 3 project dictionary."""
        p = make_v3_project_dict()
        try:
            is_valid(p, 3)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v3 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 3)

    def test_is_valid_v4(self):
        """Tests is_valid for a version 4 project dictionary."""
        p = make_v4_project_dict()
        try:
            is_valid(p, 4)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v4 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 4)

    def test_is_valid_v5(self):
        """Tests is_valid for a version 5 project dictionary."""
        p = make_v5_project_dict()
        try:
            is_valid(p, 5)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v5 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 5)

    def test_is_valid_v9(self):
        p = make_v9_project_dict()
        try:
            is_valid(p, 9)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v9 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 9)

    def test_is_valid_v10(self):
        p = make_v10_project_dict()
        try:
            is_valid(p, 10)
        except ProjectUpgradeFailed:
            self.fail("is_valid should not throw")
        # Test that an invalid v10 project dict is not valid
        p = dict()
        p["project"] = dict()
        p["items"] = dict()
        self.assertRaises(ProjectUpgradeFailed, is_valid, p, 10)


class TestUpgrade(unittest.TestCase):
    def setUp(self):
        self._items_module = importlib.import_module("spine_items")

    def test_upgrade_v1_to_v2(self):
        proj_v1 = make_v1_project_dict()
        try:
            is_valid(proj_v1, 1)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', 2
            ):
                # Upgrade to version 2
                proj_v2, old_version, new_version = upgrade(proj_v1, project_dir, self._items_module)
                self.assertEqual(old_version, 1)
                self.assertEqual(new_version, 2)
                try:
                    is_valid(proj_v2, 2)
                except ProjectUpgradeFailed:
                    self.fail("upgraded project is not valid")
                # Check that items were transferred successfully by checking that item names are found in new
                # 'items' dict and that they contain a dict
                v1_items = proj_v1["objects"]
                v2_items = proj_v2["items"]
                # v1 project items categorized under an item_type dict which were inside an 'objects' dict
                for item_category in v1_items.keys():
                    for name in v1_items[item_category]:
                        self.assertTrue(name in v2_items.keys())
                        self.assertIsInstance(v2_items[name], dict)

    def test_upgrade_v2_to_v3(self):
        proj_v2 = make_v2_project_dict()
        try:
            is_valid(proj_v2, 2)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', 3
            ):
                os.mkdir(os.path.join(project_dir, "tool_specs"))  # Make /tool_specs dir
                # Make temp preprocessing_tool.json tool spec file
                spec_file_path = os.path.join(project_dir, "tool_specs", "preprocessing_tool.json")
                with open(spec_file_path, "w", encoding="utf-8") as tmp_spec_file:
                    tmp_spec_file.write("hello")
                    # Upgrade to version 3
                    proj_v3, old_version, new_version = upgrade(proj_v2, project_dir, self._items_module)
                    self.assertEqual(old_version, 2)
                    self.assertEqual(new_version, 3)
                    try:
                        is_valid(proj_v3, 3)
                    except ProjectUpgradeFailed:
                        self.fail("upgraded project is not valid")
                    # Check that items were transferred successfully by checking that item names are found in new
                    # 'items' dict and that they contain a dict
                    v2_items = proj_v2["items"]
                    v3_items = proj_v3["items"]
                    for name in v2_items.keys():
                        self.assertTrue(name in v3_items.keys())
                        self.assertIsInstance(v3_items[name], dict)

    def test_upgrade_v3_to_v4(self):
        proj_v3 = make_v3_project_dict()
        try:
            is_valid(proj_v3, 3)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', 4
            ):
                os.mkdir(os.path.join(project_dir, "tool_specs"))  # Make /tool_specs dir
                # Make temp preprocessing_tool.json tool spec file
                spec_file_path = os.path.join(project_dir, "tool_specs", "preprocessing_tool.json")
                with open(spec_file_path, "w", encoding="utf-8") as tmp_spec_file:
                    tmp_spec_file.write("hello")
                    # Upgrade to version 4
                    proj_v4, old_version, new_version = upgrade(proj_v3, project_dir, self._items_module)
                    self.assertEqual(old_version, 3)
                    self.assertEqual(new_version, 4)
                    try:
                        is_valid(proj_v4, 4)
                    except ProjectUpgradeFailed:
                        self.fail("upgraded project is not valid")
                    # Check that items were transferred successfully by checking that item names are found in new
                    # 'items' dict and that they contain a dict
                    v3_items = proj_v3["items"]
                    v4_items = proj_v4["items"]
                    for name in v3_items.keys():
                        self.assertTrue(name in v4_items.keys())
                        self.assertIsInstance(v4_items[name], dict)

    def test_upgrade_v4_to_v5(self):
        proj_v4 = make_v4_project_dict()
        try:
            is_valid(proj_v4, 4)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', 5
            ):
                os.mkdir(os.path.join(project_dir, "tool_specs"))  # Make /tool_specs dir
                # Make temp preprocessing_tool.json tool spec file
                spec_file_path = os.path.join(project_dir, "tool_specs", "preprocessing_tool.json")
                with open(spec_file_path, "w", encoding="utf-8") as tmp_spec_file:
                    tmp_spec_file.write("hello")
                    # Upgrade to version 5
                    proj_v5, old_version, new_version = upgrade(proj_v4, project_dir, self._items_module)
                    self.assertEqual(old_version, 4)
                    self.assertEqual(new_version, 5)
                    try:
                        is_valid(proj_v5, 5)
                    except ProjectUpgradeFailed:
                        self.fail("upgraded project is not valid")
                    # Check that items were transferred successfully by checking that item names are found in new
                    # 'items' dict and that they contain a dict. Combiners should be gone in v5
                    v4_items = proj_v4["items"]
                    # Make a list of Combiner names
                    combiners = list()
                    for name, d in v4_items.items():
                        if d["type"] == "Combiner":
                            combiners.append(name)
                    v5_items = proj_v5["items"]
                    for name in v4_items.keys():
                        if name in combiners:
                            # v5 should not have Combiners anymore
                            self.assertFalse(name in v5_items.keys())
                        else:
                            self.assertTrue(name in v5_items.keys())
                            self.assertIsInstance(v5_items[name], dict)

    def test_upgrade_v9_to_v10(self):
        proj_v9 = make_v9_project_dict()
        try:
            is_valid(proj_v9, 9)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', 10
            ):
                os.mkdir(os.path.join(project_dir, "tool_specs"))  # Make /tool_specs dir
                # Make temp preprocessing_tool.json tool spec file
                spec_file_path = os.path.join(project_dir, "tool_specs", "preprocessing_tool.json")
                with open(spec_file_path, "w", encoding="utf-8") as tmp_spec_file:
                    tmp_spec_file.write("hello")
                    # Upgrade to version 10
                    proj_v10, old_version, new_version = upgrade(proj_v9, project_dir, self._items_module)
                    self.assertEqual(old_version, 9)
                    self.assertEqual(new_version, 10)
                    try:
                        is_valid(proj_v10, 10)
                    except ProjectUpgradeFailed:
                        self.fail("upgraded project is not valid")
                    v10_items = proj_v10["items"]
                    # Make a list of Gimlet and GdxExporter names in v9
                    names = list()
                    for name, d in proj_v9["items"].items():
                        if d["type"] in ["Gimlet", "GdxExporter"]:
                            names.append(name)
                    self.assertEqual(4, len(names))  # Old should have 3 Gimlets, 1 GdxExporter
                    # Check that connections have been removed
                    for conn in proj_v10["project"]["connections"]:
                        for name in names:
                            self.assertTrue(name not in conn["from"] and name not in conn["to"])
                    # Check that gimlet and GdxExporter dicts are gone from items
                    for item_name in v10_items.keys():
                        self.assertTrue(item_name not in names)
                    # Check number of connections
                    self.assertEqual(8, len(proj_v9["project"]["connections"]))
                    self.assertEqual(1, len(proj_v10["project"]["connections"]))

    def test_upgrade_v1_to_latest(self):
        proj_v1 = make_v1_project_dict()
        try:
            is_valid(proj_v1, 1)
        except ProjectUpgradeFailed:
            self.fail("original project isn't valid")
        with TemporaryDirectory() as project_dir:
            specification_dir = Path(project_dir, "Specs")
            specification_dir.mkdir()
            tool_specification_path = specification_dir / "python_tool_spec.json"
            tool_specification = {
                "item_type": "Tool"
            }
            with open(tool_specification_path, "w") as tool_specification_file:
                json.dump(tool_specification, tool_specification_file)
            with mock.patch(
                'spine_engine.project.project_upgrader.LATEST_PROJECT_VERSION', LATEST_SPINE_ITEMS_DEPENDENT_PROJECT_VERSION
            ):
                os.mkdir(os.path.join(project_dir, "tool_specs"))  # Make /tool_specs dir
                # Make temp preprocessing_tool.json tool spec file
                spec_file_path = os.path.join(project_dir, "tool_specs", "preprocessing_tool.json")
                with open(spec_file_path, "w", encoding="utf-8") as tmp_spec_file:
                    tmp_spec_file.write("hello")
                    # Upgrade to latest version
                    proj_latest, old_version, new_version = upgrade(proj_v1, project_dir, self._items_module)
                    self.assertEqual(old_version, 1)
                    self.assertEqual(new_version, LATEST_SPINE_ITEMS_DEPENDENT_PROJECT_VERSION)
                    try:
                        is_valid(proj_latest, LATEST_SPINE_ITEMS_DEPENDENT_PROJECT_VERSION)
                    except ProjectUpgradeFailed:
                        self.fail("upgraded project is not valid")
                    # Check that items were transferred successfully by checking that item names are found in new
                    # 'items' dict and that they contain a dict. Combiners should be gone in v5
                    v1_items = proj_v1["objects"]
                    latest_items = proj_latest["items"]
                    # v1 project items were categorized under a <item_type> dict which were inside an 'objects' dict
                    for item_category in v1_items.keys():
                        for name in v1_items[item_category]:
                            self.assertIn(name, latest_items)
                            self.assertIsInstance(latest_items[name], dict)
                            self.assertTrue(latest_items[name]["type"] == item_category[:-1])


def make_v1_project_dict():
    return _get_project_dict(1)


def make_v2_project_dict():
    return _get_project_dict(2)


def make_v3_project_dict():
    return _get_project_dict(3)


def make_v4_project_dict():
    return _get_project_dict(4)


def make_v5_project_dict():
    return _get_project_dict(5)


def make_v9_project_dict():
    return _get_project_dict(9)


def make_v10_project_dict():
    return _get_project_dict(10)


def _get_project_dict(v):
    """Returns a project dict read from a file according to given version."""
    project_json_versions_dir = os.path.join(str(Path(__file__).parent), "test_resources", "project_json_versions")
    f_name = "proj_v" + str(v) + ".json"  # e.g. proj_v1.json
    with open(os.path.join(project_json_versions_dir, f_name), "r") as fh:
        project_dict = json.load(fh)
    return project_dict
