#!/usr/bin/python
#
# Copyright 2024 Kaggle Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

import pprint
import re  # noqa: F401

import six


class DatasetColumn(object):
    """
    Attributes:
      column_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    column_types = {"order": "float", "name": "str", "type": "str", "original_type": "str", "description": "str"}

    attribute_map = {
        "order": "order",
        "name": "name",
        "type": "type",
        "original_type": "originalType",
        "description": "description",
    }

    def __init__(self, order=None, name=None, type=None, original_type=None, description=None):  # noqa: E501
        """DatasetColumn - a model defined in Swagger"""  # noqa: E501

        self._order = None
        self._name = None
        self._type = None
        self._original_type = None
        self._description = None
        self.discriminator = None

        if order is not None:
            self.order = order
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if original_type is not None:
            self.original_type = original_type
        if description is not None:
            self.description = description

    @property
    def order(self):
        """Gets the order of this DatasetColumn.  # noqa: E501.

        The order that the column comes in, 0-based. (The first column is 0,
        second is 1, etc.)  # noqa: E501

        :return: The order of this DatasetColumn.  # noqa: E501
        :rtype: float
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this DatasetColumn.

        The order that the column comes in, 0-based. (The first column is 0,
        second is 1, etc.)  # noqa: E501

        :param order: The order of this DatasetColumn.  # noqa: E501
        :type: float
        """

        self._order = order

    @property
    def name(self):
        """Gets the name of this DatasetColumn.  # noqa: E501.

        The column name  # noqa: E501

        :return: The name of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DatasetColumn.

        The column name  # noqa: E501

        :param name: The name of this DatasetColumn.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this DatasetColumn.  # noqa: E501.

        The type of all of the fields in the column. Please see the data
        types on
        https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata
         # noqa: E501

        :return: The type of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DatasetColumn.

        The type of all of the fields in the column. Please see the data
        types on
        https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata
         # noqa: E501

        :param type: The type of this DatasetColumn.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def original_type(self):
        """Gets the original_type of this DatasetColumn.  # noqa: E501.

        Used to store the original type of the column, which will be converted to Kaggle's types. For example, an `originalType` of `\"integer\"` would convert to a `type` of `\"numeric\"`  # noqa: E501

        :return: The original_type of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._original_type

    @original_type.setter
    def original_type(self, original_type):
        """Sets the original_type of this DatasetColumn.

        Used to store the original type of the column, which will be converted to Kaggle's types. For example, an `originalType` of `\"integer\"` would convert to a `type` of `\"numeric\"`  # noqa: E501

        :param original_type: The original_type of this DatasetColumn.  # noqa: E501
        :type: str
        """

        self._original_type = original_type

    @property
    def description(self):
        """Gets the description of this DatasetColumn.  # noqa: E501.

        The description of the column  # noqa: E501

        :return: The description of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DatasetColumn.

        The description of the column  # noqa: E501

        :param description: The description of this DatasetColumn. # noqa:
            E501
        :type: str
        """

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict."""
        result = {}

        for attr, _ in six.iteritems(self.column_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], "to_dict") else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal."""
        if not isinstance(other, DatasetColumn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal."""
        return not self == other
