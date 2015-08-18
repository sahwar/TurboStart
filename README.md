# TurboStart
Speeds up heavy application launching significantly under GNU/Linux

This script caches programs and load them into the memory before execution. Hence the programs starts so fast. Effective for heavy programs like,

- Chrome
- Firefox
- Neatbeans
- Eclipse...

> USAGE: turbostart.py [program_path] [binary_file] [user_name] [configurations_directory] [arg1]...[argn]

Example:

> sudo turbostart.py '/usr/lib/firefox' 'firefox' $USER ~/.mozilla 
