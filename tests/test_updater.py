import unittest
from unittest.mock import Mock, patch

import requests

from updater import (
    RELEASES_API,
    _normalize_version_tag,
    _parse_version,
    check_for_update,
)


class VersionParsingTests(unittest.TestCase):
    def test_parses_plain_version(self):
        self.assertEqual(_parse_version("2026.03.17"), (2026, 3, 17))

    def test_parses_v_prefix(self):
        self.assertEqual(_parse_version("v2026.03.17"), (2026, 3, 17))

    def test_parses_stable_release_tag(self):
        self.assertEqual(_parse_version("Stable-v2026.03.17"), (2026, 3, 17))
        self.assertEqual(_normalize_version_tag("Stable-v2026.03.17"), "2026.03.17")

    def test_invalid_tag_is_not_a_version(self):
        self.assertEqual(_parse_version("Stable-preview"), ())


class UpdateCheckTests(unittest.TestCase):
    def _response(self, tag):
        response = Mock()
        response.json.return_value = {
            "tag_name": tag,
            "html_url": "https://github.com/WedoneOfficiel/Wedone-Operate/releases/tag/example",
            "body": "Notes de version",
        }
        response.raise_for_status.return_value = None
        return response

    @patch("updater.requests.get")
    def test_same_stable_tag_is_not_reported_as_an_update(self, get):
        get.return_value = self._response("Stable-v2026.03.17")
        self.assertIsNone(check_for_update())
        get.assert_called_once_with(RELEASES_API, timeout=5)

    @patch("updater.requests.get")
    def test_new_stable_tag_is_reported_with_clean_version(self, get):
        get.return_value = self._response("Stable-v2099.12.31")
        result = check_for_update()
        self.assertIsNotNone(result)
        self.assertEqual(result["version"], "2099.12.31")
        self.assertEqual(result["changelog"], "Notes de version")

    @patch("updater.requests.get")
    def test_invalid_release_tag_is_ignored(self, get):
        get.return_value = self._response("Stable-preview")
        self.assertIsNone(check_for_update())

    @patch("updater.requests.get", side_effect=requests.exceptions.Timeout)
    def test_network_error_is_non_fatal(self, _get):
        self.assertIsNone(check_for_update())


if __name__ == "__main__":
    unittest.main()
