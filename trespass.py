#!/usr/bin/env python3
import sys
import os
import re
import getopt
import gpgme
import io
import numpy as np
import argparse

# initialize gpg
c = gpgme.Context()

# set directory to user's home (should work for Linux, Mac and Windows)
os.chdir(os.path.expanduser("~"))
if os.path.exists('.trespass')==False:
	os.mkdir('.trespass')
os.chdir(os.path.expanduser('.trespass'))

# command line options and help
parser = argparse.ArgumentParser()
parser.add_argument("--init", nargs='+', help="initialize with two gpg keys")
parser.add_argument("--add", nargs='+', help="add an account, username and password")
parser.add_argument("--remove", help="remove an account")
parser.add_argument("--accounts", help="list all accounts",action="store_true")
parser.add_argument("--showuser", help="show the username for an account")
parser.add_argument("--showpass", help="show the password for a user")
parser.add_argument("--debug", help="show debug info",action="store_true")

#parser.add_argument("--portfolio", help="choose a portfolio")
args = parser.parse_args()

if args.add:
	if len(args.add)!=3:
		print('account, username and password are required with --add')
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

if os.path.exists('key1.npy')==False:
	print('Please initialize with --init <gpg-key>')
else:
	keys1 = np.load('key1.npy').item()
	recipient= c.get_key(str(keys1[1]))

if os.path.exists('key2.npy')==False:
	print('Please initialize with --init <gpg-key>')
else:
	keys2 = np.load('key2.npy').item()
	recipient2= c.get_key(str(keys2[1]))

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

# call inputtoacc if --add option on command line
if args.add:
	account=str(args.add[0])
	username=str(args.add[1])
	password=str(args.add[2])
	inputtoacc(account,username,password)

# call removeacc if --delete option on command line      
if args.remove:
	account=str(args.remove)
	removeacc(account)
	sys.exit(1)

# if --accounts option on command line      
if args.accounts:
	for key in acc.keys():
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

# call --showpass option on command line
if args.showpass:
	username=str(args.showpass)
	if account in acc:
		print(user[account])


# call --dedug option on command line
if args.debug:
	print(recipient)
	print(recipient2)
	print(acc)
	print(user)

# polite exit if no acc in dictionary and --added not used
if len(acc)==0:
	print('Please input account with --add')
	sys.exit(1)
