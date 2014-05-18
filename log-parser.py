#!/usr/bin/python
from xml.etree import ElementTree
import argparse
import sys

def extract_depths(diveSamples):
  assert diveSamples.tag.endswith('DiveSamples')
  depths = []
  for diveSample in diveSamples:
    for child in diveSample:
      if child.tag.endswith('Depth'):
        depths.append(float(child.text))

  return depths

def parse_args():
  parser = argparse.ArgumentParser(description='Extract dive log data into a .srt file')
  parser.add_argument('--xml_log_file', '-f', required=True, dest='logFile')
  return parser.parse_args()

def main():
  args = parse_args()
  
  root = ElementTree.parse(args.logFile).getroot()
  depths = extract_depths(root[13])
  print depths

if __name__ == "__main__":
    main()
    