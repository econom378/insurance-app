# insurance-app

## Popis:
Tento projekt byl vytvořen v rámci certifikace webového developmentu (studijní projekt) tj. nejedná se o projekt předaný zákazníkovi (projekt neobsahuje další části jako unit testy, aplikační testy, propracovanější readme.md).

Projekt zajišťuje správu fiktivní pojišťovny. Celý je rozdělen na několik hlavních částí - pojištěnci, pojištění, pojistné události, generování reportů, registrace nového uživatele a přihlášení stávajícího uživatele.
Registrační a loginovacé formulář je validován jak na straně webového prohlížeče, tak i na straně serveru.
Výpis pojištěnců, pojištění a událostí je realizován prostřednictvím stránkování po 10 záznamech.
Přidávání nových pojištění a pojistných událostí je možné jen po rozkliknutí detailu příslušného pojištěnce.


Jednotlivý uživatelé mají přiřazena práva prostřednictvím administračního rozhraní. Pro účely ukázky byli vytvořeni 2 uživatelé:

username: user1     password: 123Xx456      může číst, přidávat záznamy, editovat záznamy a mazat záznamy

username: user2     password: 123Xx456      může číst a přidávat záznamy


## Instalace
Po stažení a otevření v IDE je pro spuštění nezbytné mít nainstalováno:

django 

python 3.10+

xhtml2pdf        - pro generování reportů *.pdf
