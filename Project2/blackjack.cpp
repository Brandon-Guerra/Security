/*******************************************************************************

Blackjack.cpp


This simple blackjack program is used to illustrate buffer overflow
security vulnerabilities.

Written by Brandon Guerra

*******************************************************************************/

#include <iostream>
#include <cstring>
#include <stdlib.h>
#include <time.h>
#include <string>

using namespace std;

bool checkToPlay(const char input);
void dealCards(char hand [], int value []);
char getCardVal(int index);
char getPlayerMove();
string getWinner(int dealer [], char player []);
int hit();
int valFromFace(char face);

int main(int argc, char** argv) {

	srand(time(NULL));
	int randOne = rand() % 10 + 2;
	int randTwo = rand() %  9 + 2;

	char input[2];
	char playerHand [4];
	playerHand[0] = getCardVal(randOne);
	playerHand[1] = getCardVal(randTwo);

	cout << "Let's play blackjack" << endl << "PSA: This is my version of " <<
	"Blackjack so Ace is always 11 and you can only hit" << endl << "once."
	<< " There is also no double down, split, insurance, or surrender." << endl
	<< "Tough Luck." << endl << "Deal hand? (y or n)" << endl;
	cin >> input;

	bool playGame = false;
	char dealerHand [10];

	playGame = checkToPlay(input[0]);

	while(playGame) {

		int dealerVal [10] = {0};
		dealCards(dealerHand, dealerVal);

		cout << endl << "Dealer's Hand: " << dealerHand[0] << endl;
		cout << "Your Hand: " << playerHand[0] 
			 << '|' << playerHand[1] << endl << endl;
		cout << "Hit (h), Stand (s): ";
		char move = getPlayerMove();
		if (move == 's') {
			cout << "Dealer's Hand: " << dealerHand[0] << "|"
			     << dealerHand[1] << endl;
			cout << getWinner(dealerVal, playerHand) << endl;
			playGame = false;
		}

		if(move == 'h') {
			playerHand[2] = getCardVal(hit());
			cout << "Dealer's Hand: " << dealerHand[0] << "|"
				     << dealerHand[1] << endl;
			cout << "Your Hand: " << playerHand[0] << "|" << playerHand[1] << "|"
				 << playerHand[2] << endl << endl;
			cout << getWinner(dealerVal, playerHand) << endl;
			playGame = false;
		}
	}
}

bool checkToPlay(const char input) {

	if(input == 'n') {
		exit(0);
	}
		else {
			return true;
		}
	return true;
}

void dealCards(char hand [], int value []) {

	int randOne = rand() % 10 + 2;
	int randTwo = rand() %  9 + 2;

	value[0] = randOne;
	value[1] = randTwo;
	hand [0] = getCardVal(randOne);
	hand [1] = getCardVal(randTwo);
}

int valFromFace(char face) {

	switch(face) {
		case '2':
			return 2;
		case '3':
			return 3;
		case '4':
			return 4;
		case '5':
			return 5;
		case '6':
			return 6;
		case '7':
			return 7;
		case '8':
			return 8;
		case '9':
			return 9;
		case 'T':
			return 10;
		case 'J':
			return 10;
		case 'Q':
			return 10;
		case 'K':
			return 10;
		case 'A':
			return 11;
	}
}

char getCardVal(int index) {

	int x = rand() % 3;

	switch(index) {
		case 2:
			return '2';
		case 3:
			return '3';
		case 4:
			return '4';
		case 5:
			return '5';
		case 6:
			return '6';
		case 7:
			return '7';
		case 8:
			return '8';
		case 9:
			return '9';
		case 10:
			if(x == 0) {
				return 'J';
			}
			if(x == 1) {
				return 'Q';
			}	
			return 'K';
		case 11:
			return 'A';
	}
}

char getPlayerMove() {

	char move;
	cin >> move;

	if(move != 'h') {
		if(move != 's') {
			cout << "NOPE" << endl;
			exit(0);
		}
		else {
			return 's';
		}
	}
	return 'h';
}

string getWinner(int dealer [], char player []) {

	if(dealer[0] + dealer[1] < 16) {
		if((valFromFace(player[0]) + valFromFace(player[1]) + valFromFace(player[2])) > 21) {
			cout << "You Busted" << endl;
			return "Dealer Wins";
		}
		dealer[2] = hit();
		cout << "Dealer's hand: " << dealer[0] << "|" << dealer[1] << "|"
		<< dealer[2] << endl;
		if(dealer[0] + dealer[1] + dealer[2] > 21) {
			cout << "Dealer Busted" << endl;
			return "You Win";
		}
		if((dealer[0] + dealer[1] + dealer[2]) > (valFromFace(player[0]) + valFromFace(player[1]) +
			valFromFace(player[2]))) {
			return "Dealer Wins";
		}
		else {
			return "You Win";
		}
	}
	else {
		if((valFromFace(player[0]) + valFromFace(player[1]) + valFromFace(player[2])) > 21) {
			cout << "You Busted" << endl;
			return "Dealer Wins";
		}
		if((valFromFace(player[0]) + valFromFace(player[1]) + valFromFace(player[2])) == (dealer[0] + dealer[1]
		    + dealer[2])) {
			return "Push";
		}
		if((dealer[0] + dealer[1]) > (valFromFace(player[0]) + valFromFace(player[1]) + valFromFace(player[2]))) {
			return "Dealer Wins";
		}
		else {
			return "You Win";
		}
	}
}

int hit() {
	return (rand() % 10 + 2);
}