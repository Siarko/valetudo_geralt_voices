# DREAME Vacuum Robot Geralt of Rivia voice pack

This is a Polish language voice pack - sound like Geralt of Rivia.
Because of that, rest of this description is Polish.

--

Głosy zostały wygenerowane przy pomocy [Minimax TTS](https://platform.minimax.io/docs/api-reference/speech-t2a-http)

Paczkę testowałem na robocie Dreame X40 ultra, ale te paczki są dość uniwersalne i powinny zadziałać na większości wspieranych przez valetudo robotów.

## Wgrywanie gotowej paczki

Jeżeli nie chcesz nic modyfikować i po prostu wgrać gotową paczkę - zobacz sekcję [Wgrywanie paczki](#uploading_pack)

Kolejne sekcje wyjaśniają wszystkie skrypty i będą pomocne jeżeli chcesz utworzyć swoją paczkę albo zmodyfikować tą.

## Wymagania (modyfikowanie/generowanie głosu)

- python3 (do uruchamiania skryptów)
    - pakiety w requirements.txt
- ffmpeg - konwersja mp3 -> ogg
- mplayer - jeżeli chcesz samodzielnie mapować głosy

## Mapowanie głosów

Żeby wygenerować głosy, najpierw pobrałem angielską paczkę dźwiękową bezpośrednio z robota.
Następnie za pomocą skryptu, przeszedłem przez wszystkie >400 nagrań i zrobiłem ludzki STT.

Do tego celu wykorzystałem skrypt sound_mapping/mapper.sh
Przyjmuje on dwa parametry:
- Ścieżka do katalogu z nagraniami
- Numer nagrania od którego zaczynamy mapowanie

Skrypt sortuje katalog z nagraniami, każde nagranie musi mieć nazwę składającą się z liczby i rozszerzenie .ogg. Inne pliki są ignorowane.
Następnie w pętli przechodzi przez wszystkie pliki, odtwarza jeden po drugim za pomocą `mplayer` i udostępnia prompt do wpisywania usłyszanego tekstu.
Spektrum autyzmu jest pomocne w wykonaniu takiego mapowania przy większej ilości plików...

Naciśnięcie <ESC> odtwarza plik jeszcze raz. <ENTER> akceptuje i przechodzi do kolejnego nagrania.
Strzałka w górę/dół wywołuje poprzednio zapisany tekst. Strzałki lewo/prawo poruszają kursor. Trzeba uważać żeby nie używać ctrl+strzałki bo wstawia 
to escape sequence w tekst - nie naprawiałem tego.

Skrypt wpisuje kolejne teksty do pliku `output.csv`.

## Tworzenie listy tekstów

Do wygenerowanego wcześniej pliku `output.csv`, dorzuciłem kolumnę `text_geralt_pl` - w niej znalazły się teksty które będzie wypowiadał Geralt.
Okazuje się że większość robotów Dreame wykorzystuje tylko pierwsze 200 tekstów - zupełnie jakbym nie musiał mapować wszystkich..

Stąd:
- `en_sound_map.csv` - oryginalnie zmapowany plik
- `pl_sound_map_geralt.csv` - tylko pierwsze 200 tekstów z dodanymi już tekstami Geralta. Może nie są najlepsze ale za to jako takie

## Generowanie głosów

Do generowania głosu Geralta wykorzystałem API MiniMax. Jest płatne ale za 100k "kredytów" (cokolwiek to znaczy), zapłaciłem 5 USD. A wygenerowanie wszystkich tekstów zużyło ~2k - więc tanio.
Wszystkie skrypty używają zmiennej środowiskowej `MINIMAX_API_KEY`.

Wszystkie narzędzia do generowania głosu są w `sound_generation`.

Katalog `minimax_audio` zawiera:
- `uploader.py` - Do wgrywania głosu na serwer minimax w celu późniejszego utworzenia modelu głosu. Ja pociąłem różne teksty Geralta z gry i wrzuciłem to na serwe. Można by to zrobić curlem ale ja zrobiłem tak.
- `clone.py` - Prośba do api aby utworzyć model głosu na podstawie wgranego pliku. Też można by curlem.
- `tts.py` - Tworzenie plików dźwiękowych z użyciem konkretnego głosu. Użycie bez argumentów pokazuje help. Ten plik robi najwięcej, dostaje tekst i zapisuje plik z dźwiękiem. Jest wywoływany przez inny skrypt.

`uploader` i `clone` używają zależności takich jak `requests` więc dobrze zainstalować sobie venv z podanych zależności `requirements.txt` - `pip install -r requirements.txt`.

### Najważniejsze skrypty w tym katalogu

`bulk_generate.py` - Przyjmuje plik csv, wywołuje skrypt `generate_voice.sh` dla każdego entry w pliku.

Użycie: `python bulk_generate.py ../sound_mapping/pl_sound_map_geralt.csv text_geralt_pl`
Gdzie pierwszy argument to ścieżka do pliku csv z tekstami a drugi to nazwa kolumny z polskimi tekstami których używamy. Nazwa pliku zawsze musi znajdować się w kolumnie `file`.

--

`generate_voice.sh` - Tak naprawdę tylko wywołuje `tts.py` z określonymi parametrami. Jest wywoływany przez `bulk_generate.py`. Wypluwa pliki mp3 do `sound_generation/output_audio/`.

--

`bulk_convert.sh` - Przekonwertowuje wszystkie pliki mp3 z `sound_generation/output_audio` na pliki ogg i zapisuje je w `sound_generation/output_audio_ogg`

## Tworzenie paczki

Jeżeli mamy już gotowe pliki ogg w `sound_generation/output_audio_ogg` to wystarczy wywołać `generate_pack.sh sound_generation/output_audio_ogg`.
Skrypt utworzy paczkę `pack_{timestamp}.tar.gz` w obecnym katalogu i wypluje na konsolę hash **MD5**.

## Wgrywanie paczki do robota <a name="uploading_pack"></a>

Jeżeli chcesz wgrać gotową paczkę z tego repo to pobierz plik `pack_geralt.tar.gz`.
Hash MD5 dla niej to `bab82bab3d1f78963238f2d0507113db`.

Ostatnie co należy zrobić żeby wgrać paczkę to wystawić plik w sieci lokalnej, tak żeby robot mógł ją pobrać. Ja używam pythona w katalogu z paczką `python3 -m http.server 8080`
To utworzy serwer http na obecnym hoście z którego można pobrać plik paczki (nie tylko paczki, tak naprawdę udostępni cały obecny katalog ale cii).

Aby zmienić paczkę w valetudo wchodzimy w `Options -> Robot -> System Options`. Tutaj jest sekcja **Voice packs** i jej użyjemy do wgrania paczki.
W polu URL podajemy adres pod którym można pobrać paczkę. Jeżeli używamy serwera http w pythonie to: `http://{ADRES IP HOSTA}:8080/{NAZWA PACZKI}` - uzupełniamy adres ip i nazwę wygenerowanej paczki.

W polu Language Code możemy podać cokolwiek, ja użyłem **GERALT**.

W polu HASH podajemy hash paczki - tutaj z readme dla gotowej paczki lub wypluty przez skrypt `generate_pack.sh`.

Wgrana paczka zadziała od razu, nie trzeba restartować robota (Przynajmniej w valetudo <= 2026.02.0)
