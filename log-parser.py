#!/usr/bin/python
from xml.etree import ElementTree
import argparse
from datetime import datetime
from datetime import timedelta

XML_SCHEMA = '{http://schemas.datacontract.org/2004/07/Suunto.Diving.Dal}'
INPUT_TIME_FORMAT = '%H:%M:%S.%f'
OUTPUT_TIME_FORMAT = '%H:%M:%S,%f'

def main():
  args = parse_args()
  root = ElementTree.parse(args.logFile).getroot()
  depths = extract_depths(root.find(XML_SCHEMA + 'DiveSamples'))
  sampleFreq = extract_sample_freq(root)
  print depths
  print sampleFreq
  write_srt(args.logFile + '.srt', depths, datetime.strptime('00:00:00.005', INPUT_TIME_FORMAT), sampleFreq)

def parse_args():
  parser = argparse.ArgumentParser(description='Extract dive log data into a .srt file')
  parser.add_argument('--xml_log_file', '-f', required=True, dest='logFile')
  parser.add_argument('--dive_start_timestamp', '-s', required=True, dest='startTime')
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
  
def write_srt(fileName, depths, startTime, sampleFreq):
  srtFile = open(fileName, 'w')
  index = 1
  time = startTime
  for depth in depths:
    endTime = time + timedelta(seconds=sampleFreq)
    srtFile.write(build_srt_stanza(index, time, endTime, str(depth)))
    srtFile.write(2 * '\r\n')
    time = endTime 
    index = index + 1
  srtFile.close()
  
def build_srt_stanza(index, startTime, endTime, value):
  stanza = []
  stanza.append(str(index))
  stanza.append(startTime.strftime(OUTPUT_TIME_FORMAT) + ' --> ' + endTime.strftime(OUTPUT_TIME_FORMAT))
  stanza.append(value)
  return '\r\n'.join(stanza)
  
if __name__ == "__main__":
    main()
    