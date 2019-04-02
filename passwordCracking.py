import hashlib
import os
from os import listdir
from os.path import isfile, join

print('Program Started')

commonPasswordsPath = '10-million-password-list-top-100000.txt'
commonPasswordsFile = open(commonPasswordsPath, 'r')
commonPasswordFileLines = commonPasswordsFile.readlines()

hashedPasswordsPath = 'Password Dump/formspring/formspring.txt'
hashedPasswordsFile = open(hashedPasswordsPath, 'r')
hashedPasswordsFileLines = hashedPasswordsFile.readlines()

linkedInPasswordsPath = 'Password Dump/linkedin/SHA1.txt'
linkedInPasswordFile = open(linkedInPasswordsPath, 'r')
linkedInPasswordsFileLines = linkedInPasswordFile.readlines()

yahooPasswordsPath = 'Password Dump/yahoo/password.txt'
yahooPasswordFile = open(yahooPasswordsPath, 'r')
yahooPasswordsFileLines = yahooPasswordFile.readlines()

formspringAnswers = open('formspringAnswers.txt', 'w')
linkedinAnswers = open('linkedinAnswers.txt', 'w')
yahooAnswers = open('yahooAnswers.txt', 'w')

sha256CommonPasswords = []
sha1CommonPasswords = []
modifiedLinkedInPasswords = []

formspringPasswordDictionary = {}
linkedinPasswordDictionary = {}

def removeFirstChars():
	for password in linkedInPasswordsFileLines:
		modifiedLinkedInPasswords.append(password[5:].rstrip())


def sha1HashAndSort(Passwords):
	for ind, password in enumerate(Passwords):
		#if ind % 1000 == 0:
			#print password
		modified = hashlib.sha1(password.rstrip()).hexdigest()
		sha1CommonPasswords.append(modified[5:])
		data  = {
			'hashedPassword' : modified,
			'password' : password.rstrip()
		}

		linkedinPasswordDictionary[modified[5:]] = data 
	sha1CommonPasswords.sort()
	print('sorted')


def sha256hashAndSort(Passwords): 
	for ind, password in enumerate(Passwords):
		if ind % 1000 == 0:
			print (str(float(ind)/float(len(Passwords))*100) + '%')
		salt = 0
		while salt < 100:
			sha256CommonPasswords.append(hashlib.sha256(str(salt) + password.rstrip()).hexdigest() + '\n')

			data =  {
				'salt' : salt,
				'password' : password,
				'hashedPassword' : hashlib.sha256(str(salt) + password.rstrip()).hexdigest()
			}

			formspringPasswordDictionary[hashlib.sha256(str(salt) + password.rstrip()).hexdigest()] = data
			salt = salt + 1
	sha256CommonPasswords.sort()
	print('sorted')


def findMatches(sorted1, sorted2):
	iterator1 = 0
	iterator2 = 0
	matches = {}
	matchList = []

	while (iterator1 < len(sorted1) and iterator2 < len(sorted2)):
		if sorted1[iterator1] == sorted2[iterator2]:
			matches[iterator1] = iterator2
			matchList.append(sorted2[iterator2])
			iterator1 = iterator1 + 1
			iterator2 = iterator2 + 1
		else: 
			if sorted1[iterator1] < sorted2[iterator2]:
				iterator1 = iterator1 + 1
			else:
				if sorted1[iterator1] > sorted2[iterator2]:
					iterator2 = iterator2 + 1

	print('Matches: ', len(matches.keys()), iterator1)

	return matchList



def crackYahoo():
	results = []

	for ind, line in enumerate(yahooPasswordsFileLines):
		if line.rstrip() == 'user_id   :  user_name  : clear_passwd : passwd':
			answers = yahooPasswordsFileLines[ind+2 : ind+32]
			for answer in answers:
				colonCount = 0
				for i in range(1, len(answer)+1):
					if answer[i-1:i] == ':':
						colonCount = colonCount + 1
					if colonCount == 2:
						results.append(answer[i:].rstrip())
						break

			return results

def yahooStart():
	for ind, line in enumerate(yahooPasswordsFileLines):
		if line.rstrip() == 'user_id   :  user_name  : clear_passwd : passwd':
			return (ind+2)	


#crackYahoo()

hashedPasswordsFileLines.sort()
sha256hashAndSort(commonPasswordFileLines)


removeFirstChars()
modifiedLinkedInPasswords.sort()
sha1HashAndSort(commonPasswordFileLines)



formspringMatches = findMatches(hashedPasswordsFileLines, sha256CommonPasswords)
linkedInMatches = findMatches(modifiedLinkedInPasswords, sha1CommonPasswords)[:30]
yahooMatches = crackYahoo()


for match in formspringMatches:
	plainText = formspringPasswordDictionary[match[0: 64]]['password']
	hashed = formspringPasswordDictionary[match[0: 64]]['hashedPassword']
	formspringAnswers.write(hashed + ' ' + plainText)
	#print ('Salt: ', formspringPasswordDictionary[match[0: 64]]['salt'], formspringPasswordDictionary[match[0: 64]]['password'])
	#print ('Password: ', linkedinPasswordDictionary[match]['password'])




for match in linkedInMatches:
	plainText = linkedinPasswordDictionary[match]['password']
	hashed = linkedinPasswordDictionary[match]['hashedPassword']
	linkedinAnswers.write(hashed.rstrip() + ' ' + plainText.rstrip() + '\n')
	


i = yahooStart()
for match in yahooMatches:
	yahooAnswers.write(yahooPasswordsFileLines[i].rstrip() + ' ' + match + '\n')
	i = i + 1


formspringAnswers.close()
linkedinAnswers.close()
yahooAnswers.close()
print ('Cracked')