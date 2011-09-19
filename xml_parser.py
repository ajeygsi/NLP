#!/usr/bin/env python

from xml.etree import ElementTree as ET

def main():
	pass

if __name__ == "__main__":
	main()

file = open("TestCase1.xml")
data = file.read()
element = ET.XML(data)

for subelement in element:
    print subelement.attrib['id'], subelement.text
