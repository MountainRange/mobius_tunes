import sys
import getopt

class command_line_flags(object):

	def __init__(self):
		try:
			opts, args = getopt.getopt(sys.argv,"t",["threshold="])
		except getopt.GetoptError:
			print('Unknown arguments')
			sys.exit(2)
		print(opts)
		print(args)
