# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# NOTE! THIS FILE IS COPIED MANUALLY IN OTHER PROVIDERS DELIBERATELY TO AVOID ADDING UNNECESSARY
# DEPENDENCIES BETWEEN PROVIDERS. IF YOU WANT TO ADD CONDITIONAL CODE IN YOUR PROVIDER THAT DEPENDS
# ON AIRFLOW VERSION, PLEASE COPY THIS FILE TO THE ROOT PACKAGE OF YOUR PROVIDER AND IMPORT
# THOSE CONSTANTS FROM IT RATHER THAN IMPORTING THEM FROM ANOTHER PROVIDER OR TEST CODE
#
from __future__ import annotations


def is_version_at_least(base_version: tuple[int, int, int]) -> bool:
    from packaging.version import Version

    from airflow import __version__

    current_version = Version(__version__)
    # Compare the release components only (major.minor.patch), ignoring pre-releases
    return current_version.release >= base_version


AIRFLOW_V_3_0_PLUS: bool = is_version_at_least((3, 0, 0))
AIRFLOW_V_3_1_PLUS: bool = is_version_at_least((3, 1, 0))
AIRFLOW_V_3_2_PLUS: bool = is_version_at_least((3, 2, 0))

# BaseOperator removed from version_compat to avoid circular imports
# Import it directly in files that need it instead

__all__ = [
    "AIRFLOW_V_3_0_PLUS",
    "AIRFLOW_V_3_1_PLUS",
    "AIRFLOW_V_3_2_PLUS",
]
