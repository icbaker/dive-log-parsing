#!/usr/bin/python
from xml.etree import ElementTree
import argparse
import sys

XML_SCHEMA = '{http://schemas.datacontract.org/2004/07/Suunto.Diving.Dal}'

def main():
  args = parse_args()
  root = ElementTree.parse(args.logFile).getroot()
  depths = extract_depths(root.find(XML_SCHEMA + 'DiveSamples'))
  sampleFreq = extract_sample_freq(root)
  print depths
  print sampleFreq

def parse_args():
  parser = argparse.ArgumentParser(description='Extract dive log data into a .srt file')
  parser.add_argument('--xml_log_file', '-f', required=True, dest='logFile')
  return parser.parse_args()

def extract_depths(diveSamples):
  assert diveSamples.tag.endswith('DiveSamples')
  depths = []
  for diveSample in diveSamples:
    for child in diveSample:
      if child.tag.endswith('Depth'):
        depths.append(float(child.text))
  return depths
  
def extract_sample_freq(root):
  return int(root.find(XML_SCHEMA + 'SampleInterval').text)

if __name__ == "__main__":
    main()
    