#!/usr/bin/env python3

import time
from collections import deque

class progress_bar:

	def __init__(self, sizein):
		self.size = sizein

		self.spinny = deque(['|', '/', '-', '\\' ])

	def __len__(self):
		return self.size

	def update_bar(self, length):
		print(self.spinny[0] + " ", end = "")
		tmp = self.spinny.popleft()
		self.spinny.append(tmp)

		if length > self.size:
			raise ValueError('You entered a len > size for the bar')

		for j in range(length):
			print('#', end = "")
		for j in range(self.size - length - 1):
			print('_', end = "")

		time.sleep(0.1)
		print("", end = "\r")

		if length >= self.size - 1:
			print("", end = "\n")

if __name__ == "__main__":
	bar = progress_bar(90)
	for i in range(len(bar)):
		bar.update_bar(i)
		time.sleep(0.1)
