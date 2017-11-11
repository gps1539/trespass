#!/usr/bin/env python3
import sys
import os
import re
import getopt
import gpgme
import io
import numpy as np
import argparse
import pyperclip
import string
from random import *

version = "0.7.1"

# initialize gpg
c = gpgme.Context()

# set directory to user's home (should work for Linux, Mac and Windows)
os.chdir(os.path.expanduser("~"))
if os.path.exists('.trespass')==False:
	os.mkdir('.trespass')
os.chdir(os.path.expanduser('.trespass'))

# command line options and help
parser = argparse.ArgumentParser()
parser.add_argument("--accounts", help="list all accounts",action="store_true")
parser.add_argument("--add", nargs='+', help="add an account, username and password")
parser.add_argument("--add_random", nargs='+', help="add an account username with random password")
parser.add_argument("--debug", help="show debug info",action="store_true")
parser.add_argument("--export",  help="export unencrypted acc and user npy files",action="store_true" )
parser.add_argument("--hidepass", help="place password in paste buffer",action="store_true")
parser.add_argument("--init", nargs='+', help="initialize with two gpg keys. (keys can be created with gpg2 --gen-key)")
parser.add_argument("--load", help="load acc & user files from ~.trepass/",action="store_true")
parser.add_argument("--remove", help="remove an account")
parser.add_argument("--showuser", help="show the username for an account")
parser.add_argument("--showpass", help="show the password for a user",action="store_true")
parser.add_argument("--version", help="print the version and exit",action="store_true")

args = parser.parse_args()

if (len(sys.argv)) < 2:
	parser.print_usage()

if args.add:
	if len(args.add)!=3:
		print('account, username and password are required with --add')
		sys.exit(1)

if args.add_random:
	if len(args.add_random)!=2:
		print('account, and username are required with --add-random')
		sys.exit(1)

if args.init:
	if len(args.init)!=2:
		print('please provide two gpg keys with --init')
		sys.exit(1)

if args.init:
	k1=str(args.init[0])
	key1={1:k1}
	np.save('key1.npy', key1)
	print(key1[1])
	k2=str(args.init[1])
	key2={1:k2}
	np.save('key2.npy', key2)
	print(key2[1])
	sys.exit(1)

if args.version:
	print('version ' + version)
	sys.exit(1)

# check if gpg keys exist
if os.path.exists('key1.npy')==False:
	print('Please initialize with --init <gpg-key UUID>')
else:
	keys1 = np.load('key1.npy').item()
	recipient= c.get_key(str(keys1[1]))

if os.path.exists('key2.npy')==False:
	print('Please initialize with --init <gpg-key UUID>')
else:
	keys2 = np.load('key2.npy').item()
	recipient2= c.get_key(str(keys2[1]))

# call --load option on command line
if args.load:
	if os.path.exists('acc.npy')==False:
		print("Please copy acc.npy to .trespass in your home directory")
		sys.exit(1)
	else:
		with open('acc.npy', 'rb') as input_file:
			with open('acc.npy.gpg', 'wb') as output_file:
				c.encrypt([recipient], 0, input_file, output_file)
	if os.path.exists('user.npy')==False:
		print("Please copy user.npy to .trespass in your home directory")
		sys.exit(1)
	else:
		with open('user.npy', 'rb') as input_file:
			with open('user.npy.gpg', 'wb') as output_file:
				c.encrypt([recipient2], 0, input_file, output_file)

if os.path.exists('acc.npy.gpg')==False:
	acc={}
	np.save('acc.npy', acc)
else:
	with open('acc.npy.gpg', 'rb') as input_file:
		with open('acc.npy', 'wb') as output_file:
			c.decrypt(input_file, output_file)
	acc=np.load('acc.npy').item()
	os.remove('acc.npy')
if os.path.exists('user.npy.gpg')==False:
	user={}
	np.save('user.npy', acc)
else:
	with open('user.npy.gpg', 'rb') as input_file:
		with open('user.npy', 'wb') as output_file:
			c.decrypt(input_file, output_file)
	user=np.load('user.npy').item()
	os.remove('user.npy')

# function to add username and password for an account
def inputtoacc(account, username, password):
	accuser=(id(account, username))
	acc.update({accuser:username})
	np.save('acc.npy', acc)
	with open('acc.npy', 'rb') as input_file:
		with open('acc.npy.gpg', 'wb') as output_file:
			c.encrypt([recipient], 0, input_file, output_file)	
	print(accuser)
	user.update({accuser:password})
	np.save('user.npy', user)
	with open('user.npy', 'rb') as input_file:
		with open('user.npy.gpg', 'wb') as output_file:
			c.encrypt([recipient2], 0, input_file, output_file)
	os.remove('acc.npy')
	os.remove('user.npy')

# function to add username and password for an account
def randomtoacc(account, username):
	characters = string.ascii_letters + string.punctuation  + string.digits
	password =  "".join(choice(characters) for x in range(randint(8, 16)))
	print(password)
	accuser=(id(account, username))
	acc.update({accuser:username})
	np.save('acc.npy', acc)
	with open('acc.npy', 'rb') as input_file:
		with open('acc.npy.gpg', 'wb') as output_file:
			c.encrypt([recipient], 0, input_file, output_file)	
	print(accuser)
	user.update({accuser:password})
	np.save('user.npy', user)
	with open('user.npy', 'rb') as input_file:
		with open('user.npy.gpg', 'wb') as output_file:
			c.encrypt([recipient2], 0, input_file, output_file)
	os.remove('acc.npy')
	os.remove('user.npy')

# function to create account:id
def id(account, username):
	a=0
	for c in account+username:
		a+=(ord(c))	
	accuser=((account) + ":" + str(a))
	return (accuser)

# function to remove an account     
def removeacc(account):
	if account in acc:
		del acc[account]
		np.save('acc.npy', acc)
		with open('acc.npy', 'rb') as input_file:
			with open('acc.npy.gpg', 'wb') as output_file:
				c.encrypt([recipient], 0, input_file, output_file)
		os.remove('acc.npy')				
	if account in user:
		del user[account]
		np.save('user.npy', user)
		with open('user.npy', 'rb') as input_file:
			with open('user.npy.gpg', 'wb') as output_file:
				c.encrypt([recipient2], 0, input_file, output_file)
		os.remove('user.npy')
	return

# if --add option on command line
if args.add:
	account=str(args.add[0])
	username=str(args.add[1])
	password=str(args.add[2])
	inputtoacc(account,username,password)

# if --add_random option on command line
if args.add_random:
	account=str(args.add_random[0])
	username=str(args.add_random[1])
	randomtoacc(account,username)

# if --delete option on command line      
if args.remove:
	account=str(args.remove)
	removeacc(account)
	sys.exit(1)

# if --accounts option on command line      
if args.accounts:
	for key in sorted(acc.keys()):
		print(key)
	sys.exit(1)

# if --showuser option on command line      
if args.showuser:
	account=str(args.showuser)
	if account in acc:	
		print(acc[account])
	else:
		print('Error no account "' + (account) + '"')	
		sys.exit(1)

# if --showpass option on command line
if args.showpass:
	if account in acc:
		print(user[account])

# if --hidepass option on command line
if args.hidepass:
	if account in acc:
		pyperclip.copy(user[account])

# if --export option on command line
if args.export:
	with open('acc.npy.gpg', 'rb') as input_file:
		with open('acc.npy', 'wb') as output_file:
			c.decrypt(input_file, output_file)
	acc=np.load('acc.npy').item()
	with open('user.npy.gpg', 'rb') as input_file:
		with open('user.npy', 'wb') as output_file:
			c.decrypt(input_file, output_file)
	acc=np.load('user.npy').item()
	print('exported')

# if --dedug option on command line
if args.debug:
	print(recipient)
	print(recipient2)
	print(acc)
	print(user)
