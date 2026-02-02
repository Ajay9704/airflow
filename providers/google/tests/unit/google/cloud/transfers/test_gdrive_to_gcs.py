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
from __future__ import annotations

import os
from unittest import mock

from airflow.providers.google.cloud.transfers.gdrive_to_gcs import GoogleDriveToGCSOperator

FOLDER_ID = os.environ.get("GCP_GDRIVE_FOLDER_ID", "abcd1234")
DRIVE_ID = os.environ.get("GCP_GDRIVE_DRIVE_ID", "abcd1234")
FILE_NAME = os.environ.get("GCP_GDRIVE_TO_GCS_FILE_NAME", "gdrive_to_gcs_file.txt")
BUCKET = os.environ.get("GCP_GDRIVE_TO_GCS_BUCKET", "gdrive-to-gcs-bucket")
OBJECT = "prefix/test.txt"
GCP_CONN_ID = "google_cloud_default"
IMPERSONATION_CHAIN = ["ACCOUNT_1", "ACCOUNT_2", "ACCOUNT_3"]


class TestGoogleDriveToGCSOperator:
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GCSHook")
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GoogleDriveHook")
    def test_execute_with_unwrap_single_true(self, mock_gdrive_hook, mock_gcs_hook):
        context = {}
        op = GoogleDriveToGCSOperator(
            task_id="test_task",
            folder_id=FOLDER_ID,
            file_name=FILE_NAME,
            drive_id=DRIVE_ID,
            bucket_name=BUCKET,
            object_name=OBJECT,
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
            unwrap_single=True,
        )
        meta = {"id": "123xyz"}
        mock_gdrive_hook.return_value.get_file_id.return_value = meta

        result = op.execute(context)
        mock_gdrive_hook.return_value.get_file_id.assert_called_once_with(
            folder_id=FOLDER_ID, file_name=FILE_NAME, drive_id=DRIVE_ID
        )

        mock_gdrive_hook.return_value.download_file.assert_called_once_with(
            file_id=meta["id"], file_handle=mock.ANY
        )

        mock_gcs_hook.return_value.provide_file_and_upload.assert_called_once_with(
            bucket_name=BUCKET, object_name=OBJECT
        )

        # Assert single string is returned when unwrap_single=True (default)
        assert result == f"gs://{BUCKET}/{OBJECT}"
        assert op.dry_run() is None
    
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GCSHook")
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GoogleDriveHook")
    def test_execute_with_unwrap_single_false(self, mock_gdrive_hook, mock_gcs_hook):
        context = {}
        op = GoogleDriveToGCSOperator(
            task_id="test_task",
            folder_id=FOLDER_ID,
            file_name=FILE_NAME,
            drive_id=DRIVE_ID,
            bucket_name=BUCKET,
            object_name=OBJECT,
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
            unwrap_single=False,
        )
        meta = {"id": "123xyz"}
        mock_gdrive_hook.return_value.get_file_id.return_value = meta

        result = op.execute(context)
        mock_gdrive_hook.return_value.get_file_id.assert_called_once_with(
            folder_id=FOLDER_ID, file_name=FILE_NAME, drive_id=DRIVE_ID
        )

        mock_gdrive_hook.return_value.download_file.assert_called_once_with(
            file_id=meta["id"], file_handle=mock.ANY
        )

        mock_gcs_hook.return_value.provide_file_and_upload.assert_called_once_with(
            bucket_name=BUCKET, object_name=OBJECT
        )

        # Assert list is returned when unwrap_single=False
        assert result == [f"gs://{BUCKET}/{OBJECT}"]
        
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GCSHook")
    @mock.patch("airflow.providers.google.cloud.transfers.gdrive_to_gcs.GoogleDriveHook")
    def test_execute_with_unwrap_single_default(self, mock_gdrive_hook, mock_gcs_hook):
        context = {}
        op = GoogleDriveToGCSOperator(
            task_id="test_task",
            folder_id=FOLDER_ID,
            file_name=FILE_NAME,
            drive_id=DRIVE_ID,
            bucket_name=BUCKET,
            object_name=OBJECT,
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
            # unwrap_single not specified, should default to True with warning
        )
        meta = {"id": "123xyz"}
        mock_gdrive_hook.return_value.get_file_id.return_value = meta

        result = op.execute(context)
        mock_gdrive_hook.return_value.get_file_id.assert_called_once_with(
            folder_id=FOLDER_ID, file_name=FILE_NAME, drive_id=DRIVE_ID
        )

        mock_gdrive_hook.return_value.download_file.assert_called_once_with(
            file_id=meta["id"], file_handle=mock.ANY
        )

        mock_gcs_hook.return_value.provide_file_and_upload.assert_called_once_with(
            bucket_name=BUCKET, object_name=OBJECT
        )

        # Assert single string is returned when unwrap_single defaults to True
        assert result == f"gs://{BUCKET}/{OBJECT}"
