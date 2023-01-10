# BrainHunt
    BrainHunt - это реализация инструмента brainflayer на языке Python. это простой и одновременно функциональный инструмент. 
    Функционал расширен если смотреть на источник. Программы производить хеширование в 2х алгоритмах (SHA256, Keccak-256)
    После хеширования полученный хеш является private key, из полученного ключа создаются все возможные адреса биткоинаи 30 альткоинов а также адрес ethereum.
    после генерации все хеши прогоняются через фильтры на совпадения, если найдено совпадение то повторная проверка происходит на сервере с блокчайнами.

## Предварительные установки
    для работы программы требуется Python 3.9.
    ```python:
    pip install -r requirements.txt
    ```
    если mmh3 у вас не устанавливается, вы пожете взять уже скомпилированный модуль и установить его:
    pip install mmh3
    https://pypi.org/project/mmh3/#files
    https://files.pythonhosted.org/packages/f4/aa/8a820c4253ea8d5b51fc141aa012abb9595d5529bc7057ccb21f6d023d78/mmh3-3.0.0-cp39-cp39-win_amd64.whl
    pip install mmh3-3.0.0-cp39-cp39-win_amd64.whl


## Создание базы BloomFilter:
    для создания блюм фитьтров вам необходим список файлов с адресами:
    скачать его можно ![Database Dumps](https://blockchair.com/dumps#database)
    или если у вас платная подписка, вы получите их с наших серверов
    если вы качаете с публичных ресурсов:
    Если вы скачиваете файлы адресов по вышеуказаной ссылке, то перед использование файлов их надо отредактировать.
    Для редактирования рекомендую EMEDITOR
    ```python:
    winndows:
    python create-bloom.py <IN File> <OUT File>
    linux:
    python3 create-bloom.py <IN File> <OUT File>
    ```
    IN File - Файл с адресами построчно (один адрес на одну строку)
    OUT File - Файл BloomFilter, в процесе конвертации и фильтрации адресов в него добавляются данные.

    если вы качаете с наших серверов то вам ничего делать не нужно.

## Описание параметров программы
    -th - количество ядер для обработки данных
    -dbbtc - база BloomFilter созданная из адресов BTC (на текущий момент BTC и альткоины)
    -dbeth - база BloomFilter созданная из адресов ETH
    -dbalt - база BloomFilter созданная из адресов альткоинов (это будет в процессе...)
    -bal - проверка баланса, если в BloomFilter найдено совпадение
    -telegram - отправка сообщения вам в telegram при совпадении.
    -id - если вы запускаете несколько копий программы (что в полне обоснованно) то для сохнанения положения вам потребуется ID процесса.
    -desc - описание машины на которой запускается процесса
    -save - указание времени сохраниея положения поиска в секундах
    -in - выходящий файл (для ревизии BrainHunt)
    -minout - ограничение вывода фразы на экран
    -word - начать последовательное хеширование с указанного слова. Если хотите указать фразу, укажите ее в ковычках "I love LIFE" (для ревизии BrainHunt-SEQ)
    -wordstop - указывает сколько циклов хеширования нужно прокрутить (для ревизии BrainHunt-SEQ)
    -raw - возможность подавать HEX адреса которые будут восприниматся программой как приватный ключ. ключи подаются генератором (для ревизии BrainHunt-EX, BrainHunt Classic)
    -raw1 - возможность подавать HEX адреса которые будут восприниматся программой как приватный ключ и с помощью делителя -div производится постоянное деление (либо ограниченое количеством раз -wordstop)
    -raw2 - возможность подавать HEX адреса которые будут восприниматся программой как приватный ключ он как в режиме майнинга производит постоянное перехеширование (также присудствует ограничение -wordstop)

    ```python:
    winndows:
    python -B BrainHunt.py -th 3 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -in dictionaries/10-million-combos.txt -bal -telegram -desc home -save 10
    linux:
    python3 -B BrainHunt.py -th 3 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -in dictionaries/10-million-combos.txt -bal -telegram -desc home -save 10
    winndows:
    mp64.exe -i 1:7 -q 2 ?l?l?l?l?l?l?l | python BrainHunt_EX.py -th 3 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -bal -telegram -desc home -save 10
    linux:
    mp64.bin -i 1:7 -q 2 ?l?l?l?l?l?l?l | python3 BrainHunt_EX.py -th 3 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -bal -telegram -desc home -save 10
    winndows:
    python BrainHunt_SEQ.py -th 1 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -bal -telegram -word genesis -desc home -save 10
    linux:
    python3 BrainHunt_SEQ.py -th 1 -id 0 -dbbtc BF/all.bf -dbeth BF/eth.bf -bal -telegram -word genesis -desc home -save 10
    ```

##Общее описание
    Программа работает с мультиядерностью, за счет чего повышается скорость работы.
    одновременное хеширование из 2х хешей (sha256, Keccak-256) (получение приватного ключа)
    получение из приватного ключа всех возможных комбинаций адреса (uncompress, compress, sigwit)
    программа проверяет баланс при включении параметра включение баланса

##PS
    в программу добаылены куча генераторов, которые решат все ваши потребности.
    
## И так давайте остановимся на каждой программе подробнее:
    BrainHunt - Красcическая реализация всем известная. Дополнительные функции это 
    BrainHunt EX - 
    BrainHunt SEQ - 
