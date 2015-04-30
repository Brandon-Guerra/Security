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
import sqlite3
connection = sqlite3.connect('phoneListing.db')

sql = connection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS persons
               (name text, phone text)''')

userQuit = False
commands = ("ADD <Person> <Telephone #> - Add a new person to the database\n"
            "DEL <Person> - Remove someone from the database by name\n"
            "DEL <Telephone #> - Remove someone by telephone #\n"
            "LIST - Produce a list of the members of the database\n"
            )
userCommand = []

def addPerson(info):
    sql.execute('INSERT INTO persons VALUES (?, ?)', info)
    connection.commit()

    print 'Successfully added ' + info[0] + ' to the database'

def listPersons():
    sql.execute('SELECT * FROM persons ORDER BY name')
    allRows = sql.fetchall()
    for row in allRows:
        print row[0], row[1]

print '\n'
print 'Telephone Listing'
print 'Type \'help\' for a list of supported commands'

while not userQuit:

    userCommand= []

    input = raw_input()

    if input == 'help':
        print commands

    userCommand = input.split()

    if userCommand[0] == 'ADD':
        userCommand.pop(0)
        addPerson(userCommand)

    if userCommand[0] == 'LIST':
        listPersons()