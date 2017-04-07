# trespass
A secure password keeper written in python using gpg to protect account/user and user/password key value stores.

The code aims to be secure and requires the password for 2 gpg keys before a user password can be revealed. 

trespass --help
usage: trespass [-h] [--accounts] [--add ADD [ADD ...]]
                [--add_random ADD_RANDOM [ADD_RANDOM ...]] [--debug]
                [--export] [--hidepass] [--init INIT [INIT ...]] [--load]
                [--remove REMOVE] [--showuser SHOWUSER] [--showpass]

optional arguments:
  -h, --help            show this help message and exit
  --accounts            list all accounts
  --add ADD [ADD ...]   add an account, username and password
  --add_random ADD_RANDOM [ADD_RANDOM ...]
                        add an account username with random password
  --debug               show debug info
  --export              export unencrypted acc and user npy files
  --hidepass            place password in paste buffer
  --init INIT [INIT ...]
                        initialize with two gpg keys
  --load                load acc & user files from ~.trepass/
  --remove REMOVE       remove an account
  --showuser SHOWUSER   show the username for an account
  --showpass            show the password for a user

To initialize 2 gpg keys need to be provided. They can be created via gpg2 --full-generate-key

trespass --init key1 key2

To add accounts
trespass --add accountname username password

To add accounts and create a random password
trespass -add_random accountname username

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
