import sys
import getopt

class command_line_flags(object):

	def __init__(self):
		try:
			self.opts, self.args = getopt.getopt(sys.argv[1:], 'd:t:c:')
		except getopt.GetoptError:
			print('Unknown arguments')
			sys.exit(2)

	def get_arguments(self):
		return self.opts
