# -*- coding: utf-8 -*-
import unittest

from drupan.site import Site
from drupan.config import Config
from drupan.deployment.s3cf import Deploy


class TestS3cf(unittest.TestCase):
    def setUp(self):
        self.site = Site()
        self.config = Config()
        cfg = {
            "options": {
                "s3cf": {
                    "bucket": "asdf",
                    "md5path": "asdf",
                    "redirects": "asdf",
                    "site_url": "asdf",
                    "skip_upload": "asdf",
                    "aws_access_key": "asdf",
                    "aws_secret_key": "asdf",
                    "cloudfront_id": "asdf",
                },
                "writer": {
                    "directory": "asdf",
                }
            }
        }
        self.config.from_dict(cfg)

    def test_compare_md5s_not_found(self):
        """should add key to changed"""
        s3cf = Deploy(self.site, self.config)
        s3cf.new_md5s["foo"] = 1
        s3cf.compare_md5s()
        self.assertEquals(s3cf.changed[0], "foo")

    def test_compare_md5s_changed(self):
        """should add key to changed"""
        s3cf = Deploy(self.site, self.config)
        s3cf.new_md5s["foo"] = 1
        s3cf.old_md5s["foo"] = 2
        s3cf.compare_md5s()
        self.assertEquals(s3cf.changed[0], "foo")

    def test_compare_md5s_no_change(self):
        """should add key to changed"""
        s3cf = Deploy(self.site, self.config)
        s3cf.new_md5s["foo"] = 1
        s3cf.old_md5s["foo"] = 1
        s3cf.compare_md5s()
        self.assertEquals(len(s3cf.changed), 0)

    def test_should_upload_skip(self):
        """should skip uploading"""
        s3cf = Deploy(self.site, self.config)
        s3cf.skip_upload = ["/foo/foo.html", "bar"]
        s3cf.changed = ["/foo/foo.html"]
        self.assertFalse(s3cf.should_upload)

    def test_should_upload(self):
        """should_upload should return True"""
        s3cf = Deploy(self.site, self.config)
        s3cf.skip_upload = ["foo", "bar"]
        s3cf.changed = ["asdf/foo", "bazbaz/zap"]
        self.assertTrue(s3cf.should_upload)