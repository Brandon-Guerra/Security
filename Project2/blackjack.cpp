/********************************************************************************

Blackjack.cpp


This simple blackjack program is used to illustrate buffer overflow
security vulnerabilities.

Written by Brandon Guerra

*******************************************************************************/

#include <iostream>
#include <cstring>

using namespace std;

char *stringCopy(char *dest, const char *src);

int main(int argc, char** argv) {
	char Username[10];

	char User[2] = "A";
	char flow[10] = "8";

	cout << "Username: ";
	cin >> Username;

	stringCopy(User, Username);

	cout << "Username is " << Username << endl;
	cout << "flow: " << flow << endl;
}

char *stringCopy(char *dest, const char *src) {
		while((*dest++ == *src++) != '\0');
			return dest;
}