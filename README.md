# resources
## bug fixes
https://docs.google.com/spreadsheets/d/1L9fpa-3Z1NzuXxwXZK0tIzjGgcxKG6c84HR0kPAkEBM/edit?gid=0#gid=0

# setup
personal information should be input into config folder's python files

personal statements and writing should be put into modules/scaffolding/user_statements.yaml

these are used to answer questions about years of experience, and also to classify whether or not you should be applying to a job. It will err on the side of applying, but make sure you are clear about which jobs you would accept, and what skills/degrees you have. Feel free to also clearly state anything that would completely prevent you from working a job.

# AI Scaffolding
modules/scaffolding holds all the AI scaffolding stuff that interacts with the initial bit of this project that we pulled.

AIClient.py class is just something I made that is nicer to use, but will probably remake another class for the larger text generative functions that we will need.

## oracle
this answers all of the AI-based questions

## current state
as most of the long form personal questions seem very rare (or nonexistent) for easy apply applications, the current bot just goes onto easy apply, and with the relevant 