#!/usr/bin/env python
import fnmatch
import os
from codecs import open

import pypandoc
import yara

rules_dir = 'apkid/rules/'
compiled_rules_path = "%srules.yarc" % rules_dir

print "[*] Converting Markdown README to reStructuredText ..."
rst = pypandoc.convert_file('README.md', 'rst')
with open('README.rst', 'w+', encoding='utf-8') as f:
    f.write(rst)
print "[*] Finished converting to README.rst (%s bytes)" % len(rst)

yara_files = {}
for root, dirnames, filenames in os.walk(rules_dir):
    for filename in fnmatch.filter(filenames, '*.yara'):
        path = os.path.join(root, filename)
        yara_files[path] = path

# print yara_files
rules = yara.compile(filepaths=yara_files)
print "[*] Compiling %d Yara rules ..." % len(yara_files)
rules.save(compiled_rules_path)
print "[*] Saved rules to %s" % compiled_rules_path

# print "[*] Registering ..."
# os.system("python setup.py register")

# print "[*] Cleaning up ..."
# os.remove('README.rst')

print "[*] Done."
