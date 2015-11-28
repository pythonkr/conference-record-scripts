#!/usr/bin/env python
# coding=utf-8

import glob
import unittest
import re
import os

from create_cover_image import create_cover_image

def list_videos(root_dir):
    containers = glob.glob(root_dir + "*_day")
    for container in containers:
        video_files = glob.glob(container + "/*.mp4")
        for video_file in video_files:
            i = extract_name(video_file)
            # print " ".join([v for v in i.values() if v is not None])
            new_filename = "%s_%s_%s.jpg" % ( i["day"], i["seq"], i["room"])
            new_cover_path = os.path.join(root_dir, "cover_dir", new_filename)
            img = create_cover_image(
                    i["date"],
                    i["session_name"].decode("utf8"),
                    i["speaker"].decode("utf8"))
            img.save(new_cover_path, quality=99)

def extract_name(filename):
    f = os.path.basename(filename)
    ret = {}
    ret["filename"] = f
    if f.startswith("0"):
        ret["day"] = "1st"
        ret["date"] = "2015/08/29"
        # day1
        regex = r"""(?P<seq>[0-9]{2})-
            (?P<room>[ABC]{1})_
            (?P<session_name>[^[]+)_
            (\[(?P<speaker>[^[]+)]_)?
            \[(?P<time_info>[^\]]+)].mp4"""
    else:
        ret["day"] = "2nd"
        ret["date"] = "2015/08/30"
        # day2
        regex = r"""(?P<room>[ABC]{1})_
            (?P<seq>[0-9]{2})_
            (?P<session_name>[^[]+)_
            (\[(?P<speaker>[^[]+)]_)?
            \[(?P<time_info>[^\]]+)].mp4"""
    m = re.match(regex, f, re.X)
    ret["room"] = m.group('room')
    ret["seq"] = m.group('seq')
    ret["speaker"] = m.group('speaker')
    if m.group('speaker') is None:
        ret["speaker"] = ""
    ret["session_name"] = m.group('session_name')
    ret["time_info"] = m.group('time_info')
    return ret


class TestExtractName(unittest.TestCase):
    def test_extract_name_day2_lt(self):
        test_name = """/data/PyCon2015/2st_day/A_09_라이트닝 토크_[둘째날 A트랙 20150830].mp4"""
        info = extract_name(test_name)
        self.assertEqual(info["filename"], "A_09_라이트닝 토크_[둘째날 A트랙 20150830].mp4")
        self.assertEqual(info["room"], "A")
        self.assertEqual(info["seq"], "09")
        self.assertEqual(info["session_name"], "라이트닝 토크")
        self.assertEqual(info["time_info"], "둘째날 A트랙 20150830")

    def test_extract_name_day2(self):
        test_name = "C_01_Python and test _[배권한]_[둘째날 C트랙 20150830].mp4"
        info = extract_name(test_name)
        self.assertEqual(info["filename"], test_name)
        self.assertEqual(info["room"], "C")
        self.assertEqual(info["seq"], "01")
        self.assertEqual(info["session_name"], "Python and test ")
        self.assertEqual(info["speaker"], "배권한")
        self.assertEqual(info["time_info"], "둘째날 C트랙 20150830")

    def test_extract_name_day1(self):
        test_name = "05-B_유연한 모바일 게임 운영을 위한 Git 기반 패치 시스템_[오영택]_[첫째날 B트랙 20150830].mp4"
        info = extract_name(test_name)
        self.assertEqual(info["filename"], test_name)
        self.assertEqual(info["room"], "B")
        self.assertEqual(info["seq"], "05")
        self.assertEqual(info["speaker"], "오영택")
        self.assertEqual(info["session_name"], "유연한 모바일 게임 운영을 위한 Git 기반 패치 시스템")
        self.assertEqual(info["time_info"], "첫째날 B트랙 20150830")

if __name__ == '__main__':
    list_videos("/data/PyCon2015/")
