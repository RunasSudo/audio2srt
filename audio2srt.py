#!/usr/bin/python3
#    audio2srt - Generate automatic subtitles from an audio file using PocketSphinx
#    Copyright © 2015  RunasSudo (Yingtong Li)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http:#www.gnu.org/licenses/>.

import argparse
import fileinput
import re
import subprocess
import sys

subnum = 1
words = []
inSentence = False
def processLine(line):
	global subnum, words, inSentence
	
	bits = line.split(' ')
	
	if bits[0] == '<s>':
		inSentence = True
	else:
		if not inSentence:
			return
		
		if bits[0] == '</s>':
			i = 0
			while i < len(words):
				subtitle = None
				if len(words) - i + 1 < 14: # If fewer than 14 words remaining, put them on one line
					subtitle = words[i:]
					i = len(words)
				else:
					subtitle = words[i:i+10]
					i += 10
				
				output.write('{}\n'.format(subnum))
				output.write('{} --> {}\n'.format(secondsToTime(subtitle[0]['startTime']), secondsToTime(subtitle[-1]['endTime'])))
				output.write('{}\n'.format(joinWords(subtitle)))
				output.write('\n')
				
				subnum += 1
			
			words.clear()
			inSentence = False
		else:
			if bits[0][0] != '<' and bits[0][0] != '[':
				words.append({'text': re.sub('\(.*?\)', '', bits[0]), 'startTime': bits[1], 'endTime': bits[2]})
	
	output.flush()

def secondsToTime(sec):
	sec = float(sec)
	hours = int(sec // 3600)
	minutes = int((sec % 3600) // 60)
	seconds = int((sec % 60) // 1)
	msecs = int((sec % 1) // 0.001)
	return '{:}:{:02}:{:02},{:03}'.format(hours, minutes, seconds, msecs)

def joinWords(words):
	text = '';
	for word in words:
		if text != '':
			text += ' '
		text += word['text']
	return text

parser = argparse.ArgumentParser(description='Generate a transcript from an audio file using pocketsphinx.')
parser.add_argument('--inputwav', '-i', metavar='FILE', help='16kHz 16-bit mono audio file')
parser.add_argument('--inputtext', '-t', metavar='FILE', help='filename containing previously computed pocketsphinx (-time yes) output')
parser.add_argument('--output', '-o', metavar='FILE', help='filename to save srt output to')
parser.add_argument('args', help='arguments to pass to pocketsphinx', nargs=argparse.REMAINDER)

args = parser.parse_args()

if '--' in args.args:
	args.args.remove('--')

output = sys.stdout
if args.output and args.output != '-':
	output = open(args.output, 'w')

if args.inputwav:
	sphinxargs = ['pocketsphinx_continuous', '-infile', args.inputwav, '-time', 'yes']
	sphinxargs.extend(args.args)
	proc = subprocess.Popen(sphinxargs, stdout=subprocess.PIPE, universal_newlines=True)
	for line in proc.stdout:
		processLine(line)
elif args.inputtext:
	for line in fileinput.input(args.inputtext):
		processLine(line)
