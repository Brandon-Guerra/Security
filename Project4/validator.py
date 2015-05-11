# Command-line driven telephone listing program
#
#Author: Brandon Guerra
#
#
#USAGE:
#
#   Below is a list of commands to interact with the database
#
#   ADD <Person> <Telephone #> - Add a new person to the database
#   DEL <Person> - Remove someone from the database by name
#   DEL <Telephone #> - Remove someone by telephone #
#   LIST - Produce a list of the members of the database
#
import re
import sqlite3
connection = sqlite3.connect('phoneListing.db')

sql = connection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS persons
               (name text, phone text)''')

def addPerson(info):
    """Takes a list with first element name and second element number
       Adds the name and number into the database as new person
    """

    strippedInfo = stripString(info)

    nameAndNumber = getNameAndNumber(info)

    isValidName = validateName(nameAndNumber[0])
    isValidPhoneNumber = validatePhoneNumber(nameAndNumber[1])

    if isValidName and isValidPhoneNumber:
        sql.execute('INSERT INTO persons VALUES (?, ?)', (nameAndNumber[0].strip(), nameAndNumber[1].strip()))
        connection.commit()

        print 'Successfully added ' + nameAndNumber[0] + 'to the database'

    else:
        print 'Invalid name or phone number format'

def listPersons():
    """Lists all persons in the database"""

    print 'Directory'
    sql.execute('SELECT * FROM persons ORDER BY name')
    allRows = sql.fetchall()
    for row in allRows:
        print row[0], row[1]

def deletePerson(info):
    """Takes a list with one element, either a name or number in database
       Removes row from database with matching name or number
    """
    strippedInfo = stripString(info)

    if strippedInfo.isdigit() or strippedInfo[0] == '(' or strippedInfo[0] == '+':
        validPhoneNumber = validatePhoneNumber(info)
        if validPhoneNumber:
            number = (strippedInfo,)
            sql.execute('DELETE FROM persons WHERE phone=?',number)
            connection.commit()

        print 'Successfully deleted ' + strippedInfo + ' from the database'

    else:
        validPerson = validateName(info)
        if validPerson:
            name = (info,)
            sql.execute('DELETE FROM persons WHERE name=?', name)
            connection.commit()

            print 'Successfully deleted ' + info + ' from the database'
        else:
            print 'Invalid name or phone number format'

def validateInput(string):
    """Takes a string an determines if valid command"""

    command, space, data = string.partition(' ')

    match = re.match("ADD$|LIST$|DEL$|help$|q$", command)
    if match:
        return (command, data)

    return ('','')

def runCommand(command):
    """Takes instruction and calls appropriate function"""
    add     = re.match("ADD$", command[0])
    delete  = re.match("DEL$", command[0])
    list    = re.match("LIST$", command[0])

    if add:
        addPerson(command[1])
    if delete:
        deletePerson(command[1])
    if list:
        listPersons()

def validateName(name):
    """Accepts string and returns True if valid phone number
       Else will return false
    """
    pattern = "([A-Z]{1}\'?[A-Z]?[a-z]*\,?)\s?([A-Z]{1}\'?[A-Z]?[a-z]*)?\s?\-?([A-Z]{1}\'?[A-Z]?[a-z]*\.?)?"
    match = re.match(pattern, name)

    if match:
        return True

    return False

def validatePhoneNumber(number):
    """Accepts string and returns True if valid phone number
       Else will return false
    """
    pattern = "\d{5}|(\+?\d{1,3})?\(\d{3}\)\d{3}\-\d{4}|(\+\d{1,3}\s{1}\(\d{2}\)\s{1})?\d{3}\-\d{4}|\d{3}\s{1}\d{3}\s{1}\d{3}\s{1}\d{4}|\d{5}\.\d{5}|\d{3}\s{1}\d{1}\s{1}\d{3}\s{1}\d{3}\s{1}\d{4}"
    match = re.match(pattern, number)

    if match:
        return True
    return False

def stripString(string):
    """Takes string as input and strips all non alphanumeric characters"""
    strippedString = re.sub(r'[^0-9a-zA-Z\'\,\-\(\)]', ' ', string)
    return strippedString

def getNameAndNumber(nameAndNumber):

    pattern = "(\d|\+|\()"
    info = re.split(pattern, nameAndNumber, 1)

    name = info[0]
    number = info[1] + info[2]

    return (name,number)

userQuit = False
commands = ("ADD <Person> <Telephone #> - Add a new person to the database\n"
            "DEL <Person> - Remove someone from the database by name\n"
            "DEL <Telephone #> - Remove someone by telephone #\n"
            "LIST - Produce a list of the members of the database"
            )

print '\n'
print 'Telephone Listing'
print 'Type \'help\' for a list of supported commands or \'q\' to quit'

while not userQuit:

    input = raw_input()

    userCommand = validateInput(input)

    if not userCommand[0] and not userCommand[1]:
        print 'Invalid command'

    elif userCommand[0] == 'help':
        print commands

    elif userCommand[0] == 'q':
        userQuit = True

    else:
        runCommand(userCommand)

connection.close()