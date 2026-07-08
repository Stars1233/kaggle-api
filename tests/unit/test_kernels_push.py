# coding=utf-8
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from kaggle.api.kaggle_api_extended import KaggleApi


class TestKernelsPush(unittest.TestCase):

    def setUp(self):
        self.api = KaggleApi.__new__(KaggleApi)
        self.api.config_values = {"username": "testuser"}
        self.api.valid_push_language_types = ["python", "r", "julia", "rmarkdown"]
        self.api.valid_push_kernel_types = ["script", "notebook"]
        self.api.valid_push_pinning_types = ["original", "latest"]
        self.api.KERNEL_METADATA_FILE = "kernel-metadata.json"

    @patch.object(KaggleApi, "build_kaggle_client")
    def test_kernels_push_utf8_behavior(self, mock_client):
        # Setup mock client response
        mock_kaggle = MagicMock()
        mock_response = MagicMock()
        mock_response.error = None
        mock_response.invalidTags = []
        mock_response.invalidDatasetSources = []
        mock_response.invalidCompetitionSources = []
        mock_response.invalidKernelSources = []
        mock_response.versionNumber = 1
        mock_response.url = "https://www.kaggle.com/testuser/test-kernel"
        mock_kaggle.kernels.kernels_api_client.save_kernel.return_value = mock_response
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_kaggle)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)

        # Content with non-ASCII characters to trigger UnicodeDecodeError if opened as ANSI
        unicode_content = (
            'print("\U0001f44b")\n'
            'print("R\u00e9sum\u00e9")\n'
            'print("\u3053\u3093\u306b\u3061\u306f")\n'
            'print("\u0928\u092e\u0938\u094d\u0924\u0947")\n'
        )

        metadata_dict = {
            "id": "testuser/test-kernel",
            "title": "Test Kernel Title",
            "code_file": "script.py",
            "language": "python",
            "kernel_type": "script",
            "is_private": True,
            "enable_gpu": False,
            "enable_tpu": False,
            "enable_internet": True,
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": [],
            "model_sources": [],
        }

        # Create actual temporary directory and files to test real filesystem behavior
        with tempfile.TemporaryDirectory() as tmpdir:
            meta_file_path = os.path.join(tmpdir, "kernel-metadata.json")
            code_file_path = os.path.join(tmpdir, "script.py")

            # Write UTF-8 metadata (which can also contain unicode characters in title)
            metadata_dict["title"] = "Test R\u00e9sum\u00e9 Title \U0001f44b"
            with open(meta_file_path, "w", encoding="utf-8") as f:
                json.dump(metadata_dict, f)

            # Write UTF-8 script code
            with open(code_file_path, "w", encoding="utf-8") as f:
                f.write(unicode_content)

            # Run kernels_push on the temporary directory, forcing preferred encoding to be cp1252
            # to verify that explicit utf-8 encoding is used regardless of the system locale.
            try:
                with patch("locale.getpreferredencoding", return_value="cp1252"):
                    self.api.kernels_push(tmpdir)
            except Exception as e:
                self.fail(f"kernels_push raised an unexpected exception: {e}")

            # Verify that save_kernel was called with the correctly read request body
            mock_kaggle.kernels.kernels_api_client.save_kernel.assert_called_once()
            call_args = mock_kaggle.kernels.kernels_api_client.save_kernel.call_args
            request = call_args[0][0]

            self.assertEqual(request.new_title, "Test R\u00e9sum\u00e9 Title \U0001f44b")
            self.assertEqual(request.text, unicode_content)


if __name__ == "__main__":
    unittest.main()
