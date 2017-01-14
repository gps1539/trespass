# trespass
A secure password keeper written in python using gpg to protect account/user and user/password key value stores.

The code aims to be secure and requires the password for 2 gpg keys before a user password can be revealed. 

trespass --help
usage: trespass [-h] [--init INIT [INIT ...]] [--add ADD [ADD ...]]
                   [--remove REMOVE] [--accounts] [--showuser SHOWUSER]
                   [--showpass SHOWPASS] [--hidepass HIDEPASS] [--load]
                   [--export] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --init INIT [INIT ...]
                        initialize with two gpg keys
  --add ADD [ADD ...]   add an account, username and password
  --remove REMOVE       remove an account
  --accounts            list all accounts
  --showuser SHOWUSER   show the username for an account
  --showpass SHOWPASS   show the password for a user
  --hidepass HIDEPASS   put password in paste buffer
  --load                load acc & user files from ~.trepass/
  --export              export unencrypted acc and user npy files
  --debug               show debug info

To initialize 2 gpg keys need to be provided. They can be created via gpg2 --full-generate-key

trespass --init key1 key2

To add accounts
trespass --add accountname username password

To remove accounts
trespass --remove 

To show user for an account
trespass --showuser accountname

To show the password for the account/user
trespass --showuser accountname --showpass username

To hide the password and add to paste buffer
trespass --showuser accountname --hidepass username

To load unencrypted files from another client, copy the files to the .trespass/ directory in your home directory and then
trespass --load

Note. running without the --load option will delete the unencrypted files, you will have to recopy them to the ~.trespass/ directory

To export unencrypted files so they can be loaded on another client
trespass --export
Copy acc.npt and user.npy to another directory before rerunning trespass otherwise they will be deleted

Note. The npg files are not encrypted, please delete them after loading on other clients.

Files are written a .trespass/ directory in users home directory.

The code is dependent on gpg2 and numpy and several python modules. It has been tested on Linux only.

Expect bugs so don't use as your only password keeper.
