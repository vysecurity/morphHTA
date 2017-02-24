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

