morphHTA
========

<img src="example.png">

Usage: 
```
usage: morph-hta.py [-h] [--in <input_file>] [--out <output_file>]
                    [--maxstrlen <default: 1000>] [--maxvarlen <default: 40>]
                    [--maxnumsplit <default: 10>]

optional arguments:
  -h, --help            show this help message and exit
  --in <input_file>     File to input Cobalt Strike PowerShell HTA
  --out <output_file>   File to output the morphed HTA to
  --maxstrlen <default: 1000>
                        Max length of randomly generated strings
  --maxvarlen <default: 40>
                        Max length of randomly generated variable names
  --maxnumsplit <default: 10>
                        Max number of times values should be split in chr
                        obfuscation
```

Examples:
=========
```
/morphHTA# python morph-hta.py
﻿███╗   ███╗ ██████╗ ██████╗ ██████╗ ██╗  ██╗      ██╗  ██╗████████╗ █████╗
████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║  ██║      ██║  ██║╚══██╔══╝██╔══██╗
██╔████╔██║██║   ██║██████╔╝██████╔╝███████║█████╗███████║   ██║   ███████║
██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║╚════╝██╔══██║   ██║   ██╔══██║
██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║      ██║  ██║   ██║   ██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝      ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝

Morphing Evil.HTA from Cobalt Strike
Author: Vincent Yiu (@vysec, @vysecurity)


[*] morphHTA initiated
[+] Writing payload to morph.hta
[+] Payload written
```


Max variable name length and randomly generated string length reduced to reduce overall size of HTA output:

`/morphHTA# python morph-hta.py --maxstrlen 4 --maxvarlen 4`


Max split in chr() obfuscation, this reduces the number of additions we do to reduce length:

`/morphHTA# python morph-hta.py --maxnumsplit 4`


Change input file and output files:

`/morphHTA# python morph-hta.py --in advert.hta --out advert-morph.hta`


VirusTotal Example 
==================

<b><i>I suggest not uploading to VT</i></b>:

<img src="virustotal.png">