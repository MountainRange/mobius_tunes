import sys
import getopt

class command_line_flags(object):

	def __init__(self):
		try:
			self.opts, self.args = getopt.getopt(sys.argv[1:],'d:')
		except getopt.GetoptError:
			print('Unknown arguments')
			sys.exit(2)
		# print(getopt.getopt(sys.argv[1:],"d:"))

	def get_directory(self):
		if len(self.opts) > 0:
			return self.opts[0][1]
		return 0
