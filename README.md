# Skryptowe
Przedmiot jezyki skryptowe

Wiem, będe musiał uprzątnąć to repozytorium.

tictactoe.sh -> bash, wymagania na 5.0.

- gra dwóch graczy,
- zapis "save" do pliku "save.txt" pozwalający na wczyatnie ostatniej tury po restarcie programu (funkcja save wykonuje sie automatycznie po kazdej turze)
format gracz:liczbatur:pole1:pole2....
- możliwa jest gra z komputerem, (funkcja RANDOM)

#Chatbot

Rozwiązania do zadań z ćwiczeń znajdują się w folderze Python_Bot_Excercises.
Nie ma tam nic specjalnie nowego, opierają się głównie na pliku Solutions.pdf

Instrukcje do chatbota, opis jego działania i wykorzystane metody znajdują się w pliku "Instructions.txt"
Bot testowany był na moim serwerze, proszę dać mi znać jeśli czegoś brakuje.

#Phaser3 Game (JS)

Gierka została stworzona na bazie opisanych wymagań:

1. Są dziury, w które można wpaść (kolizja z kolcami znajdującymi się w dziurach)
2. Są rzeczy do zebrania "monety", każda warta 10 punktów, zabicie przeciwnika jest warte 30 punktów.
3. Są przeciwnicy, których można pokonać skacząc im na głowy
4. Jako, że używałem programu Tiled do stworzenia map, to mapy są wczytywane z pliku. Problem pojawił się tylko przy przejściach pomiędzy scenami, bo coś napsułem w kodzie.

Użyte zasoby:
Asset pack from Kenney: 1-Bit Platformer Pack (1.1) under a CC0 licence
https://kenney.nl/assets/bit-platformer-pack

program Tiled:
https://www.mapeditor.org/

Sama gra dostępna jest na moim serverze:
http://www.origin.wojciech.fun/upload_game/Mar0/

Jak i (nieudane) podejścia z przełączaniem scen (niestety są osobno):
http://www.origin.wojciech.fun/upload_game/Mar0_2/ -> scena A
http://www.origin.wojciech.fun/upload_game/Mar0_3/ -> scena B

W tych przypadkach gra się kończy gdy dojdziemy do drzwi na końcu levela. (następuje pauza)

Może kiedyś to naprawię, bo wygląda głównie na problem kompozycji kodu.
