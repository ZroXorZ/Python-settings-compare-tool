# Copyright 2015 Zachary Navarro
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Script that compares 2 Device settings reports.
This script is looking for differences in the 2 reports in an effort to
identify specific changes to default settings that have been made since
the time of startup.
"""

import os
import sys
import csv

class CSV(object):
	"""A CSV file processed to an array of strings"""
	
	def __init__(self, file):
		self.array = self.read_csv(file)
		
	def read_csv(self, file):
		array = []
		f = open(file)
		cr = csv.reader(f)
		for row in cr:
			array.append(row)
		f.close()
		return array
		
def quit():
	sys.exit()
	
def clear():
	os.system("cls")
	
def check_for_csv():
	count = 0
	curr_path = []
	for root, dir, file in os.walk("./"):
		for filename in file:
			if root == "./" and filename.endswith("csv"):
				count += 1
				curr_path.append(os.path.join(root, filename))
			else:
				continue
				
	if count < 2:
		clear()
		print("Error: 2 files needed to compare.  Not Enough found in")
		print("the current directory.")
		input("\n\nPress the Enter Key to quit...")
		quit()
	elif count > 2:
		clear()
		print("Error: 2 files needed to compare.  Found more than 2 files")
		print("in the current directory.")
		input("\n\nPress the Enter Key to quit...")
		quit()
	else:
		objs = []
		for path in curr_path:
			objs.append(CSV(path))
		return objs
		
def compare(array1, array2):
	index = 0
	for list in array1:
		while list[2] != array2[index][2]:
			index += 1
		if list == array2[index]:
			continue
		else:
			find_diff(list, array2[index], array1, array2)
			
def find_diff(list1, list2, array1, array2):
	index = 0
	while index < 120:
		if list1[index] == list2[index]:
			index += 1
		else:
			text_file = open("differences.txt", "a")
			text_file.write("Difference Found: " + str(list1[2]) +
			                " - " + str(array1[0][index]) + " = " +
							str(list1[index]) + " / " + str(list2[2]) +
							" - " + str(array2[0][index]) + " = " +
							str(list2[index]) + "\n")
			text_file.close()
			index += 1
			
def print_diff():
	if os.path.isfile("differences.txt"):
		print ("Differneces found - log generated:\n\n")
		text_file = open("differences.txt", "r")
		for line in text_file:
			print (line)
		text_file.close()
	else:
		print ("No differences were found.  Original settings intact.")
		
def main():
	objs = []
	clear()
	print ("Checking CSV files, please wait...\n")
	objs = check_for_csv()
	compare(objs[0].array, objs[1].array)
	print_diff()
	input("\n\nPress the Enter Key to quit...")
	
if __name__ == "__main__":
	main()
