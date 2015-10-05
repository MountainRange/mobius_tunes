#!/usr/bin/env python3

import time
import os
import shutil
from collections import deque

class progress_bar:

	def __init__(self, sizein):
		self.size = sizein
		self.last = 0

		self.spinny = deque(['|', '/', '-', '\\' ])

	def __len__(self):
		return self.size

	def update_bar(self, length):
		length = int(length)
		columns = shutil.get_terminal_size((80, 20))[0]
		#_, columns = os.popen('stty size', 'r').read().split()
		columns = int(columns) -4

		# Go to start of line
		print('', end = "\r")
		# Clear line
		print('\033[J', end = "")

		if columns < 10:
			# We can't output progress on tiny terminals!
			return

		# The amount of space we have to draw in
		numToDraw = columns - 6
		# The amount of 'progress'
		filledAmount = max(1, int(numToDraw * (length / self.size)))
		# The amount of non-progress
		spacedAmount = numToDraw - filledAmount


		print("[" + self.spinny[0] + "] ", end = "")
		tmp = self.spinny.popleft()
		self.spinny.append(tmp)

		if self.last > length:
			print("", end = "\n")
			raise ValueError('Your new bar value decreased!')

		self.last = length

		if length > self.size:
			print("", end = "\n")
			raise ValueError('You entered a len > size for the bar')

		print('[', end = "")
		for j in range(filledAmount - 1):
			print('=', end = "")
		print('>', end = "")


		for j in range(spacedAmount):
			print('-', end = "")
		print(']', end = "")

	def complete(self):
		self.update_bar(self.size)
		print("", end = "\n")
		last = self.size

	def get_value(self):
		return self.last
		

if __name__ == "__main__":
	bar = progress_bar(20)
	for i in range(len(bar) * 10):
		bar.update_bar(int(i / 10.0))
	bar.complete()
