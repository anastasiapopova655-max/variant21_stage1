# Вариант 21 — Этап 1: REPL

Минимальный прототип эмулятора UNIX-подобной командной оболочки.
Реализован в виде графического интерфейса на Python/Tkinter.

## Реализовано

- GUI-интерфейс;
- заголовок окна с именем VFS: `VFS: default`;
- простой парсер: команда и аргументы разделяются по пробелам;
- команды-заглушки `ls` и `cd`;
- команда `exit`;
- обработка пустого ввода и неизвестных команд;
- интерактивный диалог с отображением ввода и вывода.

## Структура

```text
variant21_stage1/
├── src/
│   └── main.py
├── tests/
│   └── test_stage1.py
├── run.sh
├── README.md
└── .gitignore
```

## Запуск

Требуется Python 3 и Tkinter.

```bash
./run.sh
```

или:

```bash
python3 src/main.py
```

## Тесты

```bash
python3 -m pytest
```

## Примеры для демонстрации

```text
$ ls
ls:

$ ls folder file.txt
ls: folder file.txt

$ cd home
cd: home

$ hello
error: unknown command 'hello'

$ 
error: empty command

$ exit
Выход из эмулятора.
```

На этапе 1 `ls` и `cd` являются заглушками: они пока не работают с
реальной виртуальной файловой системой. Логика VFS появится на этапе 3.
