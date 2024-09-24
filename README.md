Munteanu Alexandru-Constantin
331CC

Tema 1 - ASC

Timp de implementare: 25-30 de ore.

Dificultate: Destul de usoara, destul de mult de scris, mi-am pus destul de
multe de probleme legate de sincronizare, deoarece ThreadPoolExecutor imi
rezolva majoritatea cerintelor, dar si din cauza GIL-ului.

La inceput am implementat task_runner folosind ThreadPoolExecutor pentru
a-mi usura munca (mai putin de scris si evit Event sau Condition).

Pentru a citi din csv am folosit pandas, deoarece era deja importat si avea
o metoda destul de usor de folosit pentru a verifica daca o valoare este NaN
sau nu. Pentru a evita un timp de rulare destul de mare, am "parsat" fisierul
si am pus informatia in 2 dictionare pentru a nu cauta mereu in toate liniile
csv-ului de fiecare data. Aceste 2 dictionare (chiar daca pe o rezolvare
neterminata) mi-au scazut timpul de rulare de la 40 de secunde, la 2 secunde
(fara check-ul de pylint).

Tratarea request-urilor se intampla asemanator pentru:
  - Primesc request
  - Creez job nou
  - Trimit in ThreadPool
  - Trimit un mesaj de finalizare
Pentru a reduce cantitatea de cod duplicat, am construit o functie care
primeste ca argument numele altei functii, care va fi trimisa in ThreadPool
in functie de request. De asemenea, am folosit un alt dictionar, "prev_runs"
care va retine rezultatele anterioare pentru states_mean, asa ca, daca se va
apela states_mean de mai multe ori, voi returna direct rezultatul.

  def send_to_threadpool(function_name, need_state = False):

Am folosit "need_state = False" pentru a considera default cazul in care nu mi
se cer informatii despre un anumit stat.

Pentru a contoriza job-urile din ThreadPool, dar si rezultatele date de catre
acesta am folosit future-urile returnate de ThreadPoolExecutor, pe care le-am
stocat intr-un dictionar de forma: {"job_id_number": future}. Atunci cand
introduc un nou future in dictionar folosesc un lock pentru a ma asigura ca
nu exista alte probleme de sincronizare (just to be safe :P). De asemenea,
am folosit un lock pentru counter-ul de job-uri si un lock pentru dictionarul
de raspunsuri. Pentru ultimul, am folosit un lock, deoarece voiam sa fiu
sigur ca o metoda nu va returna raspunsul altei functii, deoarece dictionarul
nu este thread safe.

Replies-urile pentru fiecare request sunt implementate intr-un fisier separat
pentru a nu avea fisiere foarte lungi. Acestea respecta cerinta si dupa
obtinerea rezultatelor folosesc functia writes_to_file pentru a crea un nou
fisier si a scrie rezultatul acolo.

Pentru logging, am construit o clasa noua pentru a actualiza time formatul
in gmt. Pentru RotatingFileHandler, am setat dimensiunea unui fisier log la 3MB.

Pentru testare, mi-am construit un fisier cu cu putine date, pentru a verifica
corectitudinea calculelor, dar si daca output-ul este corect si mi s-a parut
mai usor de vazut pentru un numar de date mic.
Am calculat rezultatele pentru intrebarile puse de mine si le-am pus in
dictionare in interiorul clasei (am vrut sa evit folosirea fisierelor pentru a
simplifica functiile de testare). In acestea am folosit DeepDiff cu
math_epsilon = 0.01, la fel ca in checker, iar pentru assert am folosit
assertTrue(not d, mesaj), unde not d mi-a fost recomandat de pylint,
in locul lui d == {}.

Resurse:

https://ocw.cs.pub.ro/courses/asc/laboratoare/03
https://docs.python.org/3/library/unittest.html
https://docs.python.org/3/library/logging.html
https://www.youtube.com/watch?v=urrfJgHwIJA
https://stackoverflow.com/questions/1521082/what-is-a-good-size-in-bytes-for-a-log-file
