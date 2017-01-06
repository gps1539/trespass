# trespass
A secure password keeper written in python using gpg to protect account/user and user/password key value stores.

The code aims to be secure and requires the password for 2 gpg keys before a user password can be revealed. 

I wrote this to learn python, so expect bugs. Feedback and suggestions welcome.

trespass.py --help
usage: trespass.py [-h] [--init INIT [INIT ...]] [--add ADD [ADD ...]]
                   [--remove REMOVE] [--accounts] [--showuser SHOWUSER]
                   [--showpass SHOWPASS [SHOWPASS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --init INIT [INIT ...]
                        initialize with gpg key
  --add ADD [ADD ...]   add an account, username and password
  --remove REMOVE       remove an account
  --accounts            list all accounts
  --showuser SHOWUSER   show the username for an account
  --showpass SHOWPASS [SHOWPASS ...]
                        show the password for a user/account

To initialize 2 gpg keys need to be provided. They can be created via gpg2 --full-generate-key

trespass --init key1 key2

To add accounts
trespass --add accountname username password

To remove accounts
trespass --remove 

To show user for an account
trespass.py --showuser accountname

To show the password for the account/user
trespass.py --showpass accountname username

Files are written a .trespass/ directory in users home directory.

The code is dependent on gpg2 and numpy and several python modules. It has been tested on Linux only.

Expect bugs so don't use as your only password keeper.
