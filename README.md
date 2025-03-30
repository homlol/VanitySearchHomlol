# VanitySearch

## EN

A version support custom range scanning and multi address scanning by [allinbit](https://github.com/allinbit/VanitySearch/).

This is a modified version of VanitySearch by [JeanLucPons](https://github.com/JeanLucPons/VanitySearch/).

Performance optimization completed by [aaelick](https://github.com/aaelick). **Only one GPU per instance.**

Added python script for work from [homlol pool](https://btc.homlol.ru/puzzle_pool)

# VanitySearch Integration with StartHomlolPool.py

In this version from [allinbit](https://github.com/allinbit/VanitySearch/), a code snippet was added that, in addition to saving the found keys to a file (`-o out.txt`), also appends the results to a temporary file named `tmp_homlol_pool_found.txt` in the following format:
```
13dayFJBnRbcpzdEUah3jRKQCc2sUDctkW,80001aa2d4a0099d5
1KGFdMivMMNTZKyGdW7zPSBHfCMgbuN4SJ,80001c73ce1f41d7f
19yF7J3U2uA3N3U1ZDGHn4qAhQEyLWsjsF,80001dbb4a5a9443f
1KVAjJ8KehwFfs5ke5WhsKtkTFcHZG4yCF,80001f58673171efd
1ApcfYprNUim8EtiYnsbeNNBniP8eYsVxY,8000211eba65300d6
```

## What is this for?
This is so that upon completion of the `VanitySearch` process, the Python script `StartHomlolPool.py` can read this file to send the private keys for each of the addresses (flags) to the pool.

## And if I find the main address?
Upon completion of the `VanitySearch` process, the Python script `StartHomlolPool.py` checks for the presence of the main address `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ`. If it is found, the script outputs information to the console indicating that the key has been found. In this case, no keys will be sent, and the script will terminate.

## I don't trust your build. How can I compile it myself?

To link `VanitySearch` with the script `StartHomlolPool.py`, you need to:

1. Modify the code from [allinbit](https://github.com/allinbit/VanitySearch/) in the `main.cpp` file at line 171, changing `scanf` to `sscanf`.
2. Add the following code snippet to the function `void VanitySearch::output(){}`. This snippet is responsible for saving the `VanitySearch` flags into a file for the pool:

    ```cpp
    // pool save to tmp file start ->

    string outputFile_homlol_pool;
    string outputFile_homlol_pool_info;
    string tmp_found_address;
    string tmp_found_private;
    FILE* f_pool = stdout;

    outputFile_homlol_pool = "tmp_homlol_pool_found.txt";

    f_pool = fopen(outputFile_homlol_pool.c_str(), "a");
    if (f_pool == NULL) {
        fprintf(stderr, "Cannot open %s for writing\n", outputFile_homlol_pool.c_str());
        f_pool = stdout;
    }

    tmp_found_address = addr.c_str();
    tmp_found_private = pAddrHex.c_str();

    outputFile_homlol_pool_info = tmp_found_address + "," + tmp_found_private + "\n";

    fprintf(f_pool, outputFile_homlol_pool_info.c_str());

    // pool save to tmp file end <-
    ```

3. Compile, and you're all set.

## What does the `StartHomlolPool.py` script do?

The script performs the following tasks:
- Sends a request to the pool to get information about already checked parts.
- Selects a random part, sends a request to the pool to get the addresses (flags), and adds them to `in.txt` (this can be changed in the script) along with the main address `1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ`.
- Launches `VanitySearch`.
- Upon completion, it checks the addresses. If the main address is not found, it sends the flags back to the pool to confirm the completion of the part.
- Repeats the entire process again.

## Why Python? Couldn’t everything be done directly in VanitySearch?

Python is easy to read, and most of the audience, after reviewing the script, will understand that everything is clean and that in the event of finding a key, it will go to the lucky finder.  
`VanitySearch` should not have internet access; it serves as a tool for searching. Therefore, it was decided to link them through a file containing the results.

## Can I run it right now?

Yes, in the folder `x64\Release`, there is a ready-to-use build with the script and a `.bat` file for launching.

## Good luck?

Yes, good luck to everyone!



## RU

Эта версия поддерживает сканирование пользовательских диапазонов и многоадресное сканирование [allinbit](https://github.com/allinbit/VanitySearch/).

Это модифицированная версия Vanity Search от [JeanLucPons](https://github.com/JeanLucPons/VanitySearch/).

Оптимизацию производительности выполнил [aaelick](https://github.com/aaelick). **Только один графический процессор на экземпляр.**

Добавлен скрипт на python для работы с [homlol pool](https://btc.homlol.ru/puzzle_pool)

В этой версии от [allinbit](https://github.com/allinbit/VanitySearch/) был добавлен фрагмент кода который по мимо сохранения найденых ключей в файл (-o out.txt) так же добавляет результат во временный файл tmp_homlol_pool_found.txt в виде:
```
13dayFJBnRbcpzdEUah3jRKQCc2sUDctkW,80001aa2d4a0099d5
1KGFdMivMMNTZKyGdW7zPSBHfCMgbuN4SJ,80001c73ce1f41d7f
19yF7J3U2uA3N3U1ZDGHn4qAhQEyLWsjsF,80001dbb4a5a9443f
1KVAjJ8KehwFfs5ke5WhsKtkTFcHZG4yCF,80001f58673171efd
1ApcfYprNUim8EtiYnsbeNNBniP8eYsVxY,8000211eba65300d6
```

### Для чего это нужно?
Для того чтобы по завершению поиска VanitySearch, python скрипт StartHomlolPool.py мог считать этот файл для отправки закрытых ключей к каждому из адресов (флагов) в пул.

### А если я нашел основной адрес?
По завершению поиска VanitySearch, python скрипт StartHomlolPool.py проверяет на наличие основного адреса 1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ и в случае если он там находится выводит в консоль информацию о том что ключ найден и никакой отправки ключей не будет, скрипт завершит работу.

### Недоверяю я вашей сборке, как я могу сам собрать?
Для того чтобы связать VanitySearch со скриптом StartHomlolPool.py нужно:
- 1. Исправте код [allinbit](https://github.com/allinbit/VanitySearch/) в файле main.cpp 171 строка, изменить scanf на sscanf.
- 2. Добавьте фрагмент кода в функцию void VanitySearch:output(){} он служит для получения результата флагов от VanitySearch в файл скрипта к пулу.
    ```cpp
    // pool save to tmp file start ->

    string outputFile_homlol_pool;
    string outputFile_homlol_pool_info;
    string tmp_found_address;
    string tmp_found_private;
    FILE* f_pool = stdout;

    outputFile_homlol_pool = "tmp_homlol_pool_found.txt";

    f_pool = fopen(outputFile_homlol_pool.c_str(), "a");
    if (f_pool == NULL) {
        fprintf(stderr, "Cannot open %s for writing\n", outputFile_homlol_pool.c_str());
        f_pool = stdout;
    }

    tmp_found_address = addr.c_str();
    tmp_found_private = pAddrHex.c_str();

    outputFile_homlol_pool_info = tmp_found_address + "," + tmp_found_private + "\n";

    fprintf(f_pool, outputFile_homlol_pool_info.c_str());

    // pool save to tmp file end <-
    ```
- 3. Скомпилировать и все готово.

### А что делаем скрипт StartHomlolPool.py?
Скрипт отправляет запрос в пул для получения информации о уже проверенных частях.
Выбирает рандомную часть, отправляет запрос в пул для получения адресов (флагов) и добавлеят в in.txt (можно изменить в скрипте) вместе с основным адресом 1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ.
Запускает VanitySearch. По завершению проверяет адреса и в случае ненахода основного адреса, отправляет флаги в пул для подтверждения о завершении части.
И все это запускает повторно.

### Почему именно python, нельзя было все сразу в VanitySearch сделать?
Python легко читаемый и большая часть аудитории проанализировав скрипт поймут что все чисто и в случае находки ключ достанется именно этому счастливчику.
VanitySearch не должен иметь доступ в интернет, он служит как инструмент для поиска, поэтому было принято решение связать их через файл с результатами.

### Могу я прямо сейчас запустить?
Да, в папке x64\Release готовая сборка со скриптом и файл .bat для запуска.

### Удача?
Да, удачи всем!

# Build
## Windows

- Intall CUDA SDK and open VanitySearch.sln in Visual C++ 2017.
- You may need to reset your *Windows SDK version* in project properties.
- In Build->Configuration Manager, select the *Release* configuration.

- Note: The current relase has been compiled with CUDA SDK 10.0, if you have a different release of the CUDA SDK, you may need to update CUDA SDK paths in VanitySearch.vcxproj using a text editor. The current nvcc option are set up to architecture starting at 3.0 capability, for older hardware, add the desired compute capabilities to the list in GPUEngine.cu properties, CUDA C/C++, Device, Code Generation.

## Linux
- Edit the makefile and set up the appropriate CUDA SDK and compiler paths for nvcc.
    ```
    ccap=86
    
    ...
    
    CXX        = g++-9
    CUDA       = /usr/local/cuda-11.8
    CXXCUDA    = /usr/bin/g++-9
    ```

 - Build:
    ```
    $ make all
    ```
- **Attention!!! You need to use g++-9 or a lower version to compile, otherwise the program will not run properly.**

# Usage
- Example for bitcoin puzzle 68
    ```
    ./vanitysearch -t 0 -gpu -gpuId 0 -i in.txt -o out.txt --keyspace 80000000000000000:+FFFFFFFFFF
    ```

    ```
    in.txt
    1DRd8L1KktWwqVLm3myS4vugQV3ai1LPeN /privatekey:80000000000001000
    15oCidgtdDz6VVKiMsZjRvHR9scJvN9GAX /privatekey:80000000000100000
    1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ /targetaddress
    ```
