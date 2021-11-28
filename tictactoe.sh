#!/bin/bash

PLANSZA=("0" "0" "0" "0" "0" "0" "0" "0" "0");
KONIEC="0";
GRACZ="1";
WYBOR_GRACZA=;
LICZBA_TUR=0;
DWOCH_GRACZY=0;

#obok planszy wyswietla sie referencja, zeby wiedziec ktore indeksy sa ktore
function wyswietl {
	echo "             INDEKSY POL"
	echo "===========  ==========="
	echo " ${PLANSZA[0]}" "|" "${PLANSZA[1]}" "|" "${PLANSZA[2]}" "  " "0" "|" "1" "|" "2"
	echo "===========  ==========="
	echo " ${PLANSZA[3]}" "|" "${PLANSZA[4]}" "|" "${PLANSZA[5]}" "  " "3" "|" "4" "|" "5"
	echo "===========  ==========="
	echo " ${PLANSZA[6]}" "|" "${PLANSZA[7]}" "|" "${PLANSZA[8]}" "  " "6" "|" "7" "|" "8"
	echo "===========  ==========="
}


function zmiana_gracza {
	if [ $GRACZ -eq 1 ]; then
		GRACZ="2";
	else
		GRACZ="1";
	fi
}

#save string to jedna linia zapisujaca gracz:pole1:pole2....
function save {
	save_string="";	
	
	save_string=$GRACZ":"$LICZBA_TUR":";
	
	for i in ${PLANSZA[@]}
	do
		save_string+="$i"":";	
	done
	
	echo $save_string > save.txt;

}

#koniec koncow funkcja save zapisuje zawsze ostatnia ture przez zakonczeniem rozgrywki, czy to poprzez zabicie procesu, czy zakonczenie zwyciestwem
function load {

	if [ -s save.txt ]; then

		while [ "1" ]
			save_input=;
		do
			echo "Odnaleziono poprzedni stan gry, czy chcesz go wczytac? (y/n)";
			read save_input;
			
			case $save_input in
			
			"y")
			
				filecontent=`cat save.txt`;
			
				readarray -d : -t my_array <<< "$filecontent"
			
				len=${#my_array[@]}
			
				for ((i=0; i<${len}-1; i++));
				do
					PLANSZA[$i]=${my_array[$i+2]};
				done
				
				GRACZ="${my_array[0]}";
				LICZBA_TUR="${my_array[1]}";
				break
				;;
			
			"n")
			
				echo "Zaczynamy nowa gre";
				break
				;;
			
			*)
			
				echo "Niewlasciwy input";
				continue
				;;
			
			esac
		
		done
		
		
	else
		echo "Brak poprzedniego save'a"
		echo "Zaczynamy nowa gre";
	fi
	
}

function czy_wygral {
	#poziomo
	#czy nie ".", [0,3,6] + 1, [0,3,6] + 2
	for i in {0..6..3}
	do
		if [ ${PLANSZA[$i]} -ne "0" ]; then
			local A=${PLANSZA[$i]}
			if [ ${PLANSZA[$i + 1]} == $A ] && [ ${PLANSZA[$i + 2]} == $A ]; then
				echo "GRACZ: " "$GRACZ" "ZWYCIEZYL";
				KONIEC="1";
				wyswietl;
				break
			else
				continue
			fi
		fi
	done
	#pionowo
	#czy nie ".", [0,1,2] + 3, [0,1,2] + 6
	for i in {0..2}
	do
		if [ ${PLANSZA[$i]} -ne "0" ]; then
			local A=${PLANSZA[$i]}
			if [ ${PLANSZA[$i + 3]} == $A ] && [ ${PLANSZA[$i + 6]} == $A ]; then
				echo "GRACZ: " "$GRACZ" "ZWYCIEZYL";
				KONIEC="1";
				wyswietl;
				break
			else
				continue
			fi
		fi
	done
	#pewnie istnieja bardziej eleganckie rozwiazania
	#na skos
	#czy nie ".", 0, 0 + 4, 0 + 8
	if [ ${PLANSZA[0]} -ne "0" ] && [ ${PLANSZA[4]} -ne "0" ] && [ ${PLANSZA[8]} -ne "0" ]; then
		if [ ${PLANSZA[0]} -eq ${PLANSZA[4]} ] && [ ${PLANSZA[4]} -eq ${PLANSZA[8]} ] && [ ${PLANSZA[0]} -eq ${PLANSZA[8]} ]; then
			echo "GRACZ: " "$GRACZ" "ZWYCIEZYL";
			KONIEC="1";
			wyswietl;
		fi
	fi
	#na skos 2
	#czy nie ".", 2, 4, 6	
	if [ ${PLANSZA[2]} -ne "0" ] && [ ${PLANSZA[4]} -ne "0" ] && [ ${PLANSZA[6]} -ne "0" ]; then
		if [ ${PLANSZA[2]} -eq ${PLANSZA[4]} ] && [ ${PLANSZA[4]} -eq ${PLANSZA[6]} ] && [ ${PLANSZA[2]} -eq ${PLANSZA[6]} ]; then
			echo "GRACZ: " "$GRACZ" "ZWYCIEZYL";
			KONIEC="1";
			wyswietl;
		fi
	fi
}

#HELLO MESSAGE + INSTRUCTIONS
echo "HEJKA, KOLKO I KRZYZYK"
echo "DWAJ GRACZE WYKONUJA RUCHY JEDEN PO DRUGIM. JEDEN Z GRACZY JEST KOLKIEM \"1\" DRUGI KRZYZYKIEM \"2\"."
echo "WYGRYWA TEN Z GRACZY, KTOREMU UDA SIE ULOZYC TRZY SWOJE ZNAKI OBOK SIEBIE (PIONOWO,POZIOMO LUB NA SKOS)."
echo "ABY WYBRAC POLE WPISZ JEGO NUMER I WCISNIJ ENTER."
echo "CTRL+C zeby wyjsc."

#main game loop

load

while [ $KONIEC -eq "0" ]
do
	

	echo "Gracz" "$GRACZ"
	wyswietl

	while [ "1" ] 
	
	do
		read WYBOR_GRACZA;
		if [[ "$WYBOR_GRACZA" =~ ^[0-9]+$ ]] && [ ${PLANSZA[$WYBOR_GRACZA]} == "0" ]; then
			
			case $GRACZ in
			
			"1")
				PLANSZA[$WYBOR_GRACZA]="1"
				break
				;;
			"2")
				PLANSZA[$WYBOR_GRACZA]="2"
				break
				;;
			*)
				echo "Cos zlego sie stalo"
				continue
				;;
			esac
		else
			echo "NIEWLASCIWY RUCH"
			continue
		fi
	done
	czy_wygral
	
	echo "Liczba tur: " $LICZBA_TUR;
	
	if [ $LICZBA_TUR -lt "8" ]; then
		LICZBA_TUR=$((LICZBA_TUR + 1));
	else 
		KONIEC="1";
		echo "BRAK MOZLIWYCH RUCHOW, REMIS"
	fi
	
	if [ $KONIEC -eq "0" ]; then
		zmiana_gracza
		save
	fi
done

