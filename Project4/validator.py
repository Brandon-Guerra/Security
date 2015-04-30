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

userQuit = False
commands = ("ADD <Person> <Telephone #> - Add a new person to the database\n"
            "DEL <Person> - Remove someone from the database by name\n"
            "DEL <Telephone #> - Remove someone by telephone #\n"
            "LIST - Produce a list of the members of the database\n"
            )

print '\n'
print 'Telephone Listing'
print 'Type \'help\' for a list of supported commands'

while not userQuit:

    command = raw_input()

    if command == 'help':
        print commands
