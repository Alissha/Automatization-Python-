import unittest
from Md import *

class TestLS(unittest.TestCase):
    def setUp(self):
        self.ls = LS()
        self.tm = TimeMode.UNIX
        
    def test_get_path(self):
        result = self.ls.get_path(Mode.SCRIPT_PATH)
        self.assertEqual(result, "/home/al/Desktop/mod1/")
        
    def test_get_content_list(self):
        result = self.ls.get_content_list(self.ls.get_path(Mode.SCRIPT_PATH))
        expected = "['Md.py', '__pycache__', 'report.csv', 'report.txt', '28.txt', 'report.html', 'F', 'TestLS.py', 'report.json']"
        self.assertTrue(result, expected)
        
    def test_get_file_list(self):
        result = self.ls.get_file_list(self.ls.get_path((Mode.SCRIPT_PATH)))
        expected = "['Md.py', '__pycache__', 'report.csv', 'report.txt', '28.txt', 'report.html', 'F', 'TestLS.py', 'report.json']"
        self.assertTrue(result, expected)
        
    def test_get_file_info(self):
        result = self.ls.get_file_info("/home/al/Desktop/mod1/Md.py", self.tm)
        expected = "[{'name': '/home/al/Desktop/mod1/Md.py', 'time': 1656315134.2804286, 'size': 5891, 'hash': '4d88ae8502afd63fda62ca5b5c85db1f'}, {'name': '/home/al/Desktop/mod1/report.csv', 'time': 1656282917.4404285, 'size': 772, 'hash': '49e9df90a2ba2ba6f9e007679aa0dd17'}, {'name': '/home/al/Desktop/mod1/report.txt', 'time': 1656315169.7504287, 'size': 256, 'hash': '0d7f731a840adcd4128049011bdb1934'}, {'name': '/home/al/Desktop/mod1/28.txt', 'time': 1656016853.832884, 'size': 7739, 'hash': '37610af5f719c26e4e11d2326ef97991'}, {'name': '/home/al/Desktop/mod1/report.html', 'time': 1656283192.8704286, 'size': 3277, 'hash': 'bb72b3e079fd91994c0e8d6a7ad1ddf6'}, {'name': '/home/al/Desktop/mod1/TestLS.py', 'time': 1656313118.6804285, 'size': 3288, 'hash': '8903295dd6b911ca8937bc29fd4fe920'}, {'name': '/home/al/Desktop/mod1/report.json', 'time': 1656282912.5304286, 'size': 781, 'hash': 'dc7004986cb869cf614b9b69681da293'}]"
        self.assertTrue(result, expected)
        
    def test_get_directory_info(self):
        result = self.ls.get_directory_info("/home/al/Desktop/mod1",  self.tm)
        expected = "[{'name': '/home/al/Desktop/mod1/__pycache__', 'time': 1656310874.7604287, 'size': 4096, 'hash': '93b4d6963bcb7c413f58262e8b411751'}, {'name': '/home/al/Desktop/mod1/F', 'time': 1656314644.4804287, 'size': 4096, 'hash': 'd41d8cd98f00b204e9800998ecf8427e'}]"
        self.assertTrue(result, expected)
        
if __name__ == '__main__':
    unittest.main()