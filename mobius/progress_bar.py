#!/usr/bin/env python3

import time
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
		for j in range(length - 1):
			print('=', end = "")
		print('>', end = "")


		# Edge case for start
		if length == 0:
			length += 1
		for j in range(self.size - length - 1):
			print('-', end = "")
		print(']', end = "")

		time.sleep(0.1)
		print("", end = "\r")

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
