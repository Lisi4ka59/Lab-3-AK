# Лабораторная работа #3 АК
***
#### Начинкин Михаил P3206
Базовый Вариант: `alg | stack | neum | hw | instr | binary | stream | port | pstr | prob2 | cache`


## Язык программирования
***
* Алгоритмический язык программирования, синтаксис похож на синтаксис C.
* Каждое выражение должно заканчиваться space или enter. 
* Поддерживаются математические выражения.
* Стратегия вычисления: передача параметров через глобальную область видимости всех переменных
* Все переменные объявляются в глобальной зоне видимости 
Статическая типизация, существует 3 типа данных:
* целое число
* символ, в памяти хранится как число в кодировке ОС
* строка, ссылка на последовательность символов, первое из которых - число, означающее количество символов в строке

### BNF

```BNF
<program> ::= <statements> "};"
<statements> ::= <statements> <statement>
    | ""

<statement> ::= <assignment>
    | <while>
    | <if>
    | <input>
    | <output>

<NAME> ::= <small letter> <letters and digits>
<STR> ::=  <small letters or digits or _ or ! or ? or , or .>
<CHAR> ::= <small letter or digit or _ or ! or ? or , or .>
<NUMBER> ::= <integer number>

<operation> ::= <NAME> <operand> <NAME>
    | <NAME> <operand> <NUMBER>
    | <NUMBER> <operand> <NAME>
    |<NUMBER> <operand> <NUMBER>

<operand> ::= "+"
    | "-"
    | "*"
    | "/"
    | "%"

<assignment> ::= <NAME> "=" <NUMBER>
    | <NAME> "=" <operation>
    | <NAME> "=" <NAME>
    | <NAME> "=" <STR>
    | <NAME> "=" <CHAR>

<while> ::= "While" "(" <condition> ")" "{" <statements> "}"

<if> ::= "If" "(" <condition> ")" "{" <statements> "}"

<condition> ::= <NAME> <comparison> <NUMBER>
    | <NUMBER> <comparison> <NAME>
    | <NUMBER> <comparison> <NUMBER>
    | <NAME> <comparison> <NAME>

<comparison> ::= "<"
    | ">"
    | "=="
    | "!="
    | "<="
    | ">="

<input> ::= "InputC" "(" <NAME> ")"
    | "Input" "(" <NAME> ")"
    | "InputI" "(" <NAME> ")"

<output> ::= "Print" "(" <NAME> ")"
    | "PrintI" "(" <NAME> ")"
    | "PrintC" "(" <NAME> ")"
```
* Функции используются только встроенные:
*  Input:
  * Input:
    * Считывание строки до символа переноса строки
  * InputI:
    * Считывание одного числа в переменную
  * InputC:
    * Считывание одного символа в переменную
*  Print:
  * Print:
    * Выводит строковую переменную 
  * PrintI:
    * Выводит числовую переменную 
  * PrintC:
    * Выводит символьную переменную 
* Цикл `while` и условный переход `if` в качестве аргумента принимают `condition`
  * `condition` проверяет на равенство или неравенство две переменные или переменную и число или два числа, поддерживаемые сравнения:
    * `==, !=, >, <, <=, >=`
  * `break` или `else` не предусмотрены
* Поддерживаются математические выражения, поддерживаемые операции:
  * `+, -, *, /, %`
* Литералы:
  * Целые числа
  * Строки 
  * Символы 

## Организация памяти

Модель памяти: `neum` -  архитектура Фон Неймана
Инструкция занимает 3 ячейки памяти: 1 инструкция и 2 аргумента
Каждая ячейка памяти может хранить целое 64 битное число
Адресом является целое число
Программист может изменять любое значение ячейки памяти, в том числе аргумента команды, это можно использовать для реализации указателей

### Модель  памяти

| Address | Instruction      |
|---------|------------------|
| 0       | instruction/data |
| 1       | instruction/data |
| ...     |
| 2048    | instruction/data |

* ячейки `0-511` используются для команд и их аргументов
* ячейки `512-1023` используется для данных
* ячейки `1024-2048` используется для стека
Распределение памяти от 0-1023 не фиксировано и задается компилятором

Целочисленные переменные хранятся каждая в своей ячейке памяти
Символы
Строки

Так как инструкция занимает 3 ячейки, то счетчик комманд всегда переключается на 3 ячейки вперед, кроме команд ветвления.

### Pегистры

* Специализированные: `IP`, `SP`
* РОН нет, вместо них используется стек

## Система команд


| Операнд   | Описание                                                                            |
|-----------|-------------------------------------------------------------------------------------|
| `hlt`     | Остановка                                                                           |
| `push`    | Берет из памяти, записывает на вершину стека                                        |
| `pull`    | Берет из стека, записывает в память по адресу                                       |
| `add`     | Складывает два верхних значения в стеке                                             |
| `sub`     | Вычитает из верхнего значения стека следующее значение стека                        |
| `mult`    | Умножает верхнее значение стека и следующее значение стека                          |
| `div`     | Производит целочисленное деление верхнего значения стека на следующее значение стека|
| `mod`     | Находит остаток от деления значения на вершине стека и следующего значения стека    |
| `jmp`     | Безусловный переход                                                                 |
| `ifm not` | Переход если не выполняется условие ">"                                             |
| `ifl not` | Переход если не выполняется условие "<"                                             |
| `ife not` | Переход если не выполняется условие "=="                                            |
| `ifne not`| Переход если не выполняется условие "!="                                            |
| `ifme not`| Переход если не выполняется условие ">="                                            |
| `ifle not`| Переход если не выполняется условие "<="                                            |
| `ifin`    | Переход если вершина стека находится в диапазоне                                    |
| `pushown` | Записывает на вершину стека свой операнд                                            |
| `del`     | Удаляет вершину стека                                                               |
| `inpint`  | Читает число из ввода, записывает на вершину стека                                  |
| `inp`     | Читает символ ввода, записывает на вершину стека                                    |
| `out`     | Читает символ из вершины стека, записывает в файл вывода                            |
| `outint`  | Читает число из вершины стека, записывает в файл вывода                             |

 
### Кодирование инструкций

Программа загружается в машину из двоичного файла, в котором инструкции представлены также, как в памяти

## Транслятор 

Транслятор запускается командой python3 main.py, аргументы не требуются
Программа считывается из консоли
Скомпилированный машинный код в бинарном виде записывается в файл program.o


## Модель процессора

### Datapath
![image](https://github.com/user-attachments/assets/c80cd330-7154-4733-abaf-ae2004685b8f)

### Control Unit
![image](https://github.com/user-attachments/assets/caca6b54-ce60-49cd-8c8b-2da6d1478852)


## Тестирование

### Краткое описание разработанных тестов
Производится запуск транслятора и машины с определенными входными данными, затем результат выполнения машины и ее логи сравниваются с эталонами 

### Описание работы настроенного CI
Производится проверка форматироания и линтер, затем запускаются тесты, каждый из которых состоит из сборки программы из исходного кода, запуска машины и сверки результата работы машины с эталоном 

### Реализация алгоритмов

Для алгоритмов реализованы golden-тесты:
* [Hello](tests/Hello)
* [Cat](tests/Cat)
* [Hello User](tests/Hello_user_name)
* [Prob2](tests/Fibonnachi)


### Prob2

#### Код программы:

```
a=1
b=1
prom=0
While(a<4000000){
    mod=a%2
    If(mod==0){
        prom=prom+a
    }
    c=a+b
    b=a
    a=c
}
PrintI(prom)
};
```

#### Машинный код
```
20 1 0 2 512 0 20 1 0 2 513 0 20 0 0 2 514 0 20 4000000 0 1 512 0 12 99 0 21 0 0 
21 0 0 20 2 0 1 512 0 7 0 0 2 515 0 20 0 0 1 515 0 13 72 0 21 0 0 21 0 0 
1 512 0 1 514 0 3 0 0 2 514 0 1 513 0 1 512 0 3 0 0 2 516 0 1 512 0 2 513 0 
1 516 0 2 512 0 10 18 0 1 514 0 33 0 0 0 0 0 
```

#### Лог выполнения машины
```
0 - 20 - pushown 1 -> #stack(0)
3 - 2 - pull 1 -> #512
6 - 20 - pushown 1 -> #stack(0)
9 - 2 - pull 1 -> #513
12 - 20 - pushown 0 -> #stack(0)
15 - 2 - pull 0 -> #514
18 - 20 - pushown 4000000 -> #stack(0)
21 - 1 - push 1 -> #stack(1)
24 - 12 - ifl not 1 < 4000000 -> #ip(99)
27 - 21 - del #stack(1)
30 - 21 - del #stack(0)
33 - 20 - pushown 2 -> #stack(0)
36 - 1 - push 1 -> #stack(1)
39 - 7 - mod 1 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(0)
48 - 1 - push 1 -> #stack(1)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 1 -> #stack(2)
75 - 1 - push 1 -> #stack(3)
78 - 3 - add 1 + 1
81 - 2 - pull 2 -> #516
84 - 1 - push 1 -> #stack(2)
87 - 2 - pull 1 -> #513
90 - 1 - push 2 -> #stack(2)
93 - 2 - pull 2 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(2)
21 - 1 - push 2 -> #stack(3)
24 - 12 - ifl not 2 < 4000000 -> #ip(99)
27 - 21 - del #stack(3)
30 - 21 - del #stack(2)
33 - 20 - pushown 2 -> #stack(2)
36 - 1 - push 2 -> #stack(3)
39 - 7 - mod 2 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(2)
48 - 1 - push 0 -> #stack(3)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(3)
57 - 21 - del #stack(2)
60 - 1 - push 2 -> #stack(2)
63 - 1 - push 0 -> #stack(3)
66 - 3 - add 0 + 2
69 - 2 - pull 2 -> #514
72 - 1 - push 1 -> #stack(2)
75 - 1 - push 2 -> #stack(3)
78 - 3 - add 2 + 1
81 - 2 - pull 3 -> #516
84 - 1 - push 2 -> #stack(2)
87 - 2 - pull 2 -> #513
90 - 1 - push 3 -> #stack(2)
93 - 2 - pull 3 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(2)
21 - 1 - push 3 -> #stack(3)
24 - 12 - ifl not 3 < 4000000 -> #ip(99)
27 - 21 - del #stack(3)
30 - 21 - del #stack(2)
33 - 20 - pushown 2 -> #stack(2)
36 - 1 - push 3 -> #stack(3)
39 - 7 - mod 3 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(2)
48 - 1 - push 1 -> #stack(3)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 2 -> #stack(4)
75 - 1 - push 3 -> #stack(5)
78 - 3 - add 3 + 2
81 - 2 - pull 5 -> #516
84 - 1 - push 3 -> #stack(4)
87 - 2 - pull 3 -> #513
90 - 1 - push 5 -> #stack(4)
93 - 2 - pull 5 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(4)
21 - 1 - push 5 -> #stack(5)
24 - 12 - ifl not 5 < 4000000 -> #ip(99)
27 - 21 - del #stack(5)
30 - 21 - del #stack(4)
33 - 20 - pushown 2 -> #stack(4)
36 - 1 - push 5 -> #stack(5)
39 - 7 - mod 5 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(4)
48 - 1 - push 1 -> #stack(5)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 3 -> #stack(6)
75 - 1 - push 5 -> #stack(7)
78 - 3 - add 5 + 3
81 - 2 - pull 8 -> #516
84 - 1 - push 5 -> #stack(6)
87 - 2 - pull 5 -> #513
90 - 1 - push 8 -> #stack(6)
93 - 2 - pull 8 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(6)
21 - 1 - push 8 -> #stack(7)
24 - 12 - ifl not 8 < 4000000 -> #ip(99)
27 - 21 - del #stack(7)
30 - 21 - del #stack(6)
33 - 20 - pushown 2 -> #stack(6)
36 - 1 - push 8 -> #stack(7)
39 - 7 - mod 8 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(6)
48 - 1 - push 0 -> #stack(7)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(7)
57 - 21 - del #stack(6)
60 - 1 - push 8 -> #stack(6)
63 - 1 - push 2 -> #stack(7)
66 - 3 - add 2 + 8
69 - 2 - pull 10 -> #514
72 - 1 - push 5 -> #stack(6)
75 - 1 - push 8 -> #stack(7)
78 - 3 - add 8 + 5
81 - 2 - pull 13 -> #516
84 - 1 - push 8 -> #stack(6)
87 - 2 - pull 8 -> #513
90 - 1 - push 13 -> #stack(6)
93 - 2 - pull 13 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(6)
21 - 1 - push 13 -> #stack(7)
24 - 12 - ifl not 13 < 4000000 -> #ip(99)
27 - 21 - del #stack(7)
30 - 21 - del #stack(6)
33 - 20 - pushown 2 -> #stack(6)
36 - 1 - push 13 -> #stack(7)
39 - 7 - mod 13 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(6)
48 - 1 - push 1 -> #stack(7)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 8 -> #stack(8)
75 - 1 - push 13 -> #stack(9)
78 - 3 - add 13 + 8
81 - 2 - pull 21 -> #516
84 - 1 - push 13 -> #stack(8)
87 - 2 - pull 13 -> #513
90 - 1 - push 21 -> #stack(8)
93 - 2 - pull 21 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(8)
21 - 1 - push 21 -> #stack(9)
24 - 12 - ifl not 21 < 4000000 -> #ip(99)
27 - 21 - del #stack(9)
30 - 21 - del #stack(8)
33 - 20 - pushown 2 -> #stack(8)
36 - 1 - push 21 -> #stack(9)
39 - 7 - mod 21 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(8)
48 - 1 - push 1 -> #stack(9)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 13 -> #stack(10)
75 - 1 - push 21 -> #stack(11)
78 - 3 - add 21 + 13
81 - 2 - pull 34 -> #516
84 - 1 - push 21 -> #stack(10)
87 - 2 - pull 21 -> #513
90 - 1 - push 34 -> #stack(10)
93 - 2 - pull 34 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(10)
21 - 1 - push 34 -> #stack(11)
24 - 12 - ifl not 34 < 4000000 -> #ip(99)
27 - 21 - del #stack(11)
30 - 21 - del #stack(10)
33 - 20 - pushown 2 -> #stack(10)
36 - 1 - push 34 -> #stack(11)
39 - 7 - mod 34 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(10)
48 - 1 - push 0 -> #stack(11)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(11)
57 - 21 - del #stack(10)
60 - 1 - push 34 -> #stack(10)
63 - 1 - push 10 -> #stack(11)
66 - 3 - add 10 + 34
69 - 2 - pull 44 -> #514
72 - 1 - push 21 -> #stack(10)
75 - 1 - push 34 -> #stack(11)
78 - 3 - add 34 + 21
81 - 2 - pull 55 -> #516
84 - 1 - push 34 -> #stack(10)
87 - 2 - pull 34 -> #513
90 - 1 - push 55 -> #stack(10)
93 - 2 - pull 55 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(10)
21 - 1 - push 55 -> #stack(11)
24 - 12 - ifl not 55 < 4000000 -> #ip(99)
27 - 21 - del #stack(11)
30 - 21 - del #stack(10)
33 - 20 - pushown 2 -> #stack(10)
36 - 1 - push 55 -> #stack(11)
39 - 7 - mod 55 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(10)
48 - 1 - push 1 -> #stack(11)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 34 -> #stack(12)
75 - 1 - push 55 -> #stack(13)
78 - 3 - add 55 + 34
81 - 2 - pull 89 -> #516
84 - 1 - push 55 -> #stack(12)
87 - 2 - pull 55 -> #513
90 - 1 - push 89 -> #stack(12)
93 - 2 - pull 89 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(12)
21 - 1 - push 89 -> #stack(13)
24 - 12 - ifl not 89 < 4000000 -> #ip(99)
27 - 21 - del #stack(13)
30 - 21 - del #stack(12)
33 - 20 - pushown 2 -> #stack(12)
36 - 1 - push 89 -> #stack(13)
39 - 7 - mod 89 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(12)
48 - 1 - push 1 -> #stack(13)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 55 -> #stack(14)
75 - 1 - push 89 -> #stack(15)
78 - 3 - add 89 + 55
81 - 2 - pull 144 -> #516
84 - 1 - push 89 -> #stack(14)
87 - 2 - pull 89 -> #513
90 - 1 - push 144 -> #stack(14)
93 - 2 - pull 144 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(14)
21 - 1 - push 144 -> #stack(15)
24 - 12 - ifl not 144 < 4000000 -> #ip(99)
27 - 21 - del #stack(15)
30 - 21 - del #stack(14)
33 - 20 - pushown 2 -> #stack(14)
36 - 1 - push 144 -> #stack(15)
39 - 7 - mod 144 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(14)
48 - 1 - push 0 -> #stack(15)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(15)
57 - 21 - del #stack(14)
60 - 1 - push 144 -> #stack(14)
63 - 1 - push 44 -> #stack(15)
66 - 3 - add 44 + 144
69 - 2 - pull 188 -> #514
72 - 1 - push 89 -> #stack(14)
75 - 1 - push 144 -> #stack(15)
78 - 3 - add 144 + 89
81 - 2 - pull 233 -> #516
84 - 1 - push 144 -> #stack(14)
87 - 2 - pull 144 -> #513
90 - 1 - push 233 -> #stack(14)
93 - 2 - pull 233 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(14)
21 - 1 - push 233 -> #stack(15)
24 - 12 - ifl not 233 < 4000000 -> #ip(99)
27 - 21 - del #stack(15)
30 - 21 - del #stack(14)
33 - 20 - pushown 2 -> #stack(14)
36 - 1 - push 233 -> #stack(15)
39 - 7 - mod 233 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(14)
48 - 1 - push 1 -> #stack(15)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 144 -> #stack(16)
75 - 1 - push 233 -> #stack(17)
78 - 3 - add 233 + 144
81 - 2 - pull 377 -> #516
84 - 1 - push 233 -> #stack(16)
87 - 2 - pull 233 -> #513
90 - 1 - push 377 -> #stack(16)
93 - 2 - pull 377 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(16)
21 - 1 - push 377 -> #stack(17)
24 - 12 - ifl not 377 < 4000000 -> #ip(99)
27 - 21 - del #stack(17)
30 - 21 - del #stack(16)
33 - 20 - pushown 2 -> #stack(16)
36 - 1 - push 377 -> #stack(17)
39 - 7 - mod 377 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(16)
48 - 1 - push 1 -> #stack(17)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 233 -> #stack(18)
75 - 1 - push 377 -> #stack(19)
78 - 3 - add 377 + 233
81 - 2 - pull 610 -> #516
84 - 1 - push 377 -> #stack(18)
87 - 2 - pull 377 -> #513
90 - 1 - push 610 -> #stack(18)
93 - 2 - pull 610 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(18)
21 - 1 - push 610 -> #stack(19)
24 - 12 - ifl not 610 < 4000000 -> #ip(99)
27 - 21 - del #stack(19)
30 - 21 - del #stack(18)
33 - 20 - pushown 2 -> #stack(18)
36 - 1 - push 610 -> #stack(19)
39 - 7 - mod 610 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(18)
48 - 1 - push 0 -> #stack(19)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(19)
57 - 21 - del #stack(18)
60 - 1 - push 610 -> #stack(18)
63 - 1 - push 188 -> #stack(19)
66 - 3 - add 188 + 610
69 - 2 - pull 798 -> #514
72 - 1 - push 377 -> #stack(18)
75 - 1 - push 610 -> #stack(19)
78 - 3 - add 610 + 377
81 - 2 - pull 987 -> #516
84 - 1 - push 610 -> #stack(18)
87 - 2 - pull 610 -> #513
90 - 1 - push 987 -> #stack(18)
93 - 2 - pull 987 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(18)
21 - 1 - push 987 -> #stack(19)
24 - 12 - ifl not 987 < 4000000 -> #ip(99)
27 - 21 - del #stack(19)
30 - 21 - del #stack(18)
33 - 20 - pushown 2 -> #stack(18)
36 - 1 - push 987 -> #stack(19)
39 - 7 - mod 987 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(18)
48 - 1 - push 1 -> #stack(19)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 610 -> #stack(20)
75 - 1 - push 987 -> #stack(21)
78 - 3 - add 987 + 610
81 - 2 - pull 1597 -> #516
84 - 1 - push 987 -> #stack(20)
87 - 2 - pull 987 -> #513
90 - 1 - push 1597 -> #stack(20)
93 - 2 - pull 1597 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(20)
21 - 1 - push 1597 -> #stack(21)
24 - 12 - ifl not 1597 < 4000000 -> #ip(99)
27 - 21 - del #stack(21)
30 - 21 - del #stack(20)
33 - 20 - pushown 2 -> #stack(20)
36 - 1 - push 1597 -> #stack(21)
39 - 7 - mod 1597 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(20)
48 - 1 - push 1 -> #stack(21)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 987 -> #stack(22)
75 - 1 - push 1597 -> #stack(23)
78 - 3 - add 1597 + 987
81 - 2 - pull 2584 -> #516
84 - 1 - push 1597 -> #stack(22)
87 - 2 - pull 1597 -> #513
90 - 1 - push 2584 -> #stack(22)
93 - 2 - pull 2584 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(22)
21 - 1 - push 2584 -> #stack(23)
24 - 12 - ifl not 2584 < 4000000 -> #ip(99)
27 - 21 - del #stack(23)
30 - 21 - del #stack(22)
33 - 20 - pushown 2 -> #stack(22)
36 - 1 - push 2584 -> #stack(23)
39 - 7 - mod 2584 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(22)
48 - 1 - push 0 -> #stack(23)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(23)
57 - 21 - del #stack(22)
60 - 1 - push 2584 -> #stack(22)
63 - 1 - push 798 -> #stack(23)
66 - 3 - add 798 + 2584
69 - 2 - pull 3382 -> #514
72 - 1 - push 1597 -> #stack(22)
75 - 1 - push 2584 -> #stack(23)
78 - 3 - add 2584 + 1597
81 - 2 - pull 4181 -> #516
84 - 1 - push 2584 -> #stack(22)
87 - 2 - pull 2584 -> #513
90 - 1 - push 4181 -> #stack(22)
93 - 2 - pull 4181 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(22)
21 - 1 - push 4181 -> #stack(23)
24 - 12 - ifl not 4181 < 4000000 -> #ip(99)
27 - 21 - del #stack(23)
30 - 21 - del #stack(22)
33 - 20 - pushown 2 -> #stack(22)
36 - 1 - push 4181 -> #stack(23)
39 - 7 - mod 4181 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(22)
48 - 1 - push 1 -> #stack(23)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 2584 -> #stack(24)
75 - 1 - push 4181 -> #stack(25)
78 - 3 - add 4181 + 2584
81 - 2 - pull 6765 -> #516
84 - 1 - push 4181 -> #stack(24)
87 - 2 - pull 4181 -> #513
90 - 1 - push 6765 -> #stack(24)
93 - 2 - pull 6765 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(24)
21 - 1 - push 6765 -> #stack(25)
24 - 12 - ifl not 6765 < 4000000 -> #ip(99)
27 - 21 - del #stack(25)
30 - 21 - del #stack(24)
33 - 20 - pushown 2 -> #stack(24)
36 - 1 - push 6765 -> #stack(25)
39 - 7 - mod 6765 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(24)
48 - 1 - push 1 -> #stack(25)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 4181 -> #stack(26)
75 - 1 - push 6765 -> #stack(27)
78 - 3 - add 6765 + 4181
81 - 2 - pull 10946 -> #516
84 - 1 - push 6765 -> #stack(26)
87 - 2 - pull 6765 -> #513
90 - 1 - push 10946 -> #stack(26)
93 - 2 - pull 10946 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(26)
21 - 1 - push 10946 -> #stack(27)
24 - 12 - ifl not 10946 < 4000000 -> #ip(99)
27 - 21 - del #stack(27)
30 - 21 - del #stack(26)
33 - 20 - pushown 2 -> #stack(26)
36 - 1 - push 10946 -> #stack(27)
39 - 7 - mod 10946 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(26)
48 - 1 - push 0 -> #stack(27)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(27)
57 - 21 - del #stack(26)
60 - 1 - push 10946 -> #stack(26)
63 - 1 - push 3382 -> #stack(27)
66 - 3 - add 3382 + 10946
69 - 2 - pull 14328 -> #514
72 - 1 - push 6765 -> #stack(26)
75 - 1 - push 10946 -> #stack(27)
78 - 3 - add 10946 + 6765
81 - 2 - pull 17711 -> #516
84 - 1 - push 10946 -> #stack(26)
87 - 2 - pull 10946 -> #513
90 - 1 - push 17711 -> #stack(26)
93 - 2 - pull 17711 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(26)
21 - 1 - push 17711 -> #stack(27)
24 - 12 - ifl not 17711 < 4000000 -> #ip(99)
27 - 21 - del #stack(27)
30 - 21 - del #stack(26)
33 - 20 - pushown 2 -> #stack(26)
36 - 1 - push 17711 -> #stack(27)
39 - 7 - mod 17711 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(26)
48 - 1 - push 1 -> #stack(27)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 10946 -> #stack(28)
75 - 1 - push 17711 -> #stack(29)
78 - 3 - add 17711 + 10946
81 - 2 - pull 28657 -> #516
84 - 1 - push 17711 -> #stack(28)
87 - 2 - pull 17711 -> #513
90 - 1 - push 28657 -> #stack(28)
93 - 2 - pull 28657 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(28)
21 - 1 - push 28657 -> #stack(29)
24 - 12 - ifl not 28657 < 4000000 -> #ip(99)
27 - 21 - del #stack(29)
30 - 21 - del #stack(28)
33 - 20 - pushown 2 -> #stack(28)
36 - 1 - push 28657 -> #stack(29)
39 - 7 - mod 28657 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(28)
48 - 1 - push 1 -> #stack(29)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 17711 -> #stack(30)
75 - 1 - push 28657 -> #stack(31)
78 - 3 - add 28657 + 17711
81 - 2 - pull 46368 -> #516
84 - 1 - push 28657 -> #stack(30)
87 - 2 - pull 28657 -> #513
90 - 1 - push 46368 -> #stack(30)
93 - 2 - pull 46368 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(30)
21 - 1 - push 46368 -> #stack(31)
24 - 12 - ifl not 46368 < 4000000 -> #ip(99)
27 - 21 - del #stack(31)
30 - 21 - del #stack(30)
33 - 20 - pushown 2 -> #stack(30)
36 - 1 - push 46368 -> #stack(31)
39 - 7 - mod 46368 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(30)
48 - 1 - push 0 -> #stack(31)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(31)
57 - 21 - del #stack(30)
60 - 1 - push 46368 -> #stack(30)
63 - 1 - push 14328 -> #stack(31)
66 - 3 - add 14328 + 46368
69 - 2 - pull 60696 -> #514
72 - 1 - push 28657 -> #stack(30)
75 - 1 - push 46368 -> #stack(31)
78 - 3 - add 46368 + 28657
81 - 2 - pull 75025 -> #516
84 - 1 - push 46368 -> #stack(30)
87 - 2 - pull 46368 -> #513
90 - 1 - push 75025 -> #stack(30)
93 - 2 - pull 75025 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(30)
21 - 1 - push 75025 -> #stack(31)
24 - 12 - ifl not 75025 < 4000000 -> #ip(99)
27 - 21 - del #stack(31)
30 - 21 - del #stack(30)
33 - 20 - pushown 2 -> #stack(30)
36 - 1 - push 75025 -> #stack(31)
39 - 7 - mod 75025 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(30)
48 - 1 - push 1 -> #stack(31)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 46368 -> #stack(32)
75 - 1 - push 75025 -> #stack(33)
78 - 3 - add 75025 + 46368
81 - 2 - pull 121393 -> #516
84 - 1 - push 75025 -> #stack(32)
87 - 2 - pull 75025 -> #513
90 - 1 - push 121393 -> #stack(32)
93 - 2 - pull 121393 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(32)
21 - 1 - push 121393 -> #stack(33)
24 - 12 - ifl not 121393 < 4000000 -> #ip(99)
27 - 21 - del #stack(33)
30 - 21 - del #stack(32)
33 - 20 - pushown 2 -> #stack(32)
36 - 1 - push 121393 -> #stack(33)
39 - 7 - mod 121393 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(32)
48 - 1 - push 1 -> #stack(33)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 75025 -> #stack(34)
75 - 1 - push 121393 -> #stack(35)
78 - 3 - add 121393 + 75025
81 - 2 - pull 196418 -> #516
84 - 1 - push 121393 -> #stack(34)
87 - 2 - pull 121393 -> #513
90 - 1 - push 196418 -> #stack(34)
93 - 2 - pull 196418 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(34)
21 - 1 - push 196418 -> #stack(35)
24 - 12 - ifl not 196418 < 4000000 -> #ip(99)
27 - 21 - del #stack(35)
30 - 21 - del #stack(34)
33 - 20 - pushown 2 -> #stack(34)
36 - 1 - push 196418 -> #stack(35)
39 - 7 - mod 196418 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(34)
48 - 1 - push 0 -> #stack(35)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(35)
57 - 21 - del #stack(34)
60 - 1 - push 196418 -> #stack(34)
63 - 1 - push 60696 -> #stack(35)
66 - 3 - add 60696 + 196418
69 - 2 - pull 257114 -> #514
72 - 1 - push 121393 -> #stack(34)
75 - 1 - push 196418 -> #stack(35)
78 - 3 - add 196418 + 121393
81 - 2 - pull 317811 -> #516
84 - 1 - push 196418 -> #stack(34)
87 - 2 - pull 196418 -> #513
90 - 1 - push 317811 -> #stack(34)
93 - 2 - pull 317811 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(34)
21 - 1 - push 317811 -> #stack(35)
24 - 12 - ifl not 317811 < 4000000 -> #ip(99)
27 - 21 - del #stack(35)
30 - 21 - del #stack(34)
33 - 20 - pushown 2 -> #stack(34)
36 - 1 - push 317811 -> #stack(35)
39 - 7 - mod 317811 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(34)
48 - 1 - push 1 -> #stack(35)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 196418 -> #stack(36)
75 - 1 - push 317811 -> #stack(37)
78 - 3 - add 317811 + 196418
81 - 2 - pull 514229 -> #516
84 - 1 - push 317811 -> #stack(36)
87 - 2 - pull 317811 -> #513
90 - 1 - push 514229 -> #stack(36)
93 - 2 - pull 514229 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(36)
21 - 1 - push 514229 -> #stack(37)
24 - 12 - ifl not 514229 < 4000000 -> #ip(99)
27 - 21 - del #stack(37)
30 - 21 - del #stack(36)
33 - 20 - pushown 2 -> #stack(36)
36 - 1 - push 514229 -> #stack(37)
39 - 7 - mod 514229 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(36)
48 - 1 - push 1 -> #stack(37)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 317811 -> #stack(38)
75 - 1 - push 514229 -> #stack(39)
78 - 3 - add 514229 + 317811
81 - 2 - pull 832040 -> #516
84 - 1 - push 514229 -> #stack(38)
87 - 2 - pull 514229 -> #513
90 - 1 - push 832040 -> #stack(38)
93 - 2 - pull 832040 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(38)
21 - 1 - push 832040 -> #stack(39)
24 - 12 - ifl not 832040 < 4000000 -> #ip(99)
27 - 21 - del #stack(39)
30 - 21 - del #stack(38)
33 - 20 - pushown 2 -> #stack(38)
36 - 1 - push 832040 -> #stack(39)
39 - 7 - mod 832040 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(38)
48 - 1 - push 0 -> #stack(39)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(39)
57 - 21 - del #stack(38)
60 - 1 - push 832040 -> #stack(38)
63 - 1 - push 257114 -> #stack(39)
66 - 3 - add 257114 + 832040
69 - 2 - pull 1089154 -> #514
72 - 1 - push 514229 -> #stack(38)
75 - 1 - push 832040 -> #stack(39)
78 - 3 - add 832040 + 514229
81 - 2 - pull 1346269 -> #516
84 - 1 - push 832040 -> #stack(38)
87 - 2 - pull 832040 -> #513
90 - 1 - push 1346269 -> #stack(38)
93 - 2 - pull 1346269 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(38)
21 - 1 - push 1346269 -> #stack(39)
24 - 12 - ifl not 1346269 < 4000000 -> #ip(99)
27 - 21 - del #stack(39)
30 - 21 - del #stack(38)
33 - 20 - pushown 2 -> #stack(38)
36 - 1 - push 1346269 -> #stack(39)
39 - 7 - mod 1346269 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(38)
48 - 1 - push 1 -> #stack(39)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 832040 -> #stack(40)
75 - 1 - push 1346269 -> #stack(41)
78 - 3 - add 1346269 + 832040
81 - 2 - pull 2178309 -> #516
84 - 1 - push 1346269 -> #stack(40)
87 - 2 - pull 1346269 -> #513
90 - 1 - push 2178309 -> #stack(40)
93 - 2 - pull 2178309 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(40)
21 - 1 - push 2178309 -> #stack(41)
24 - 12 - ifl not 2178309 < 4000000 -> #ip(99)
27 - 21 - del #stack(41)
30 - 21 - del #stack(40)
33 - 20 - pushown 2 -> #stack(40)
36 - 1 - push 2178309 -> #stack(41)
39 - 7 - mod 2178309 % 2
42 - 2 - pull 1 -> #515
45 - 20 - pushown 0 -> #stack(40)
48 - 1 - push 1 -> #stack(41)
51 - 13 - ife not 1 == 0 -> #ip(72)
72 - 1 - push 1346269 -> #stack(42)
75 - 1 - push 2178309 -> #stack(43)
78 - 3 - add 2178309 + 1346269
81 - 2 - pull 3524578 -> #516
84 - 1 - push 2178309 -> #stack(42)
87 - 2 - pull 2178309 -> #513
90 - 1 - push 3524578 -> #stack(42)
93 - 2 - pull 3524578 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(42)
21 - 1 - push 3524578 -> #stack(43)
24 - 12 - ifl not 3524578 < 4000000 -> #ip(99)
27 - 21 - del #stack(43)
30 - 21 - del #stack(42)
33 - 20 - pushown 2 -> #stack(42)
36 - 1 - push 3524578 -> #stack(43)
39 - 7 - mod 3524578 % 2
42 - 2 - pull 0 -> #515
45 - 20 - pushown 0 -> #stack(42)
48 - 1 - push 0 -> #stack(43)
51 - 13 - ife not 0 == 0 -> #ip(72)
54 - 21 - del #stack(43)
57 - 21 - del #stack(42)
60 - 1 - push 3524578 -> #stack(42)
63 - 1 - push 1089154 -> #stack(43)
66 - 3 - add 1089154 + 3524578
69 - 2 - pull 4613732 -> #514
72 - 1 - push 2178309 -> #stack(42)
75 - 1 - push 3524578 -> #stack(43)
78 - 3 - add 3524578 + 2178309
81 - 2 - pull 5702887 -> #516
84 - 1 - push 3524578 -> #stack(42)
87 - 2 - pull 3524578 -> #513
90 - 1 - push 5702887 -> #stack(42)
93 - 2 - pull 5702887 -> #512
96 - 10 - jmp 18 -> IP
18 - 20 - pushown 4000000 -> #stack(42)
21 - 1 - push 5702887 -> #stack(43)
24 - 12 - ifl not 5702887 < 4000000 -> #ip(99)
99 - 1 - push 4613732 -> #stack(44)
102 - 33 - outint 4613732
105 - 0 - hlt
```

#### Результат выполнения программы
```
4613732
```

### Аналитика

```
|           Full name          | alg             | loc | bytes   | instr | exec_instr | tick |                                       variant                                     |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Начинкин Михаил Анатольевич  | prob2           | 14  | 864     | 36    | 750        | -    |  alg | stack | neum | hw | instr | binary | stream | port | pstr | prob2 | cache  |
| Начинкин Михаил Анатольевич  | cat             | 4   | 648     | 27    | 636        | -    |  alg | stack | neum | hw | instr | binary | stream | port | pstr | prob2 | cache  |
| Начинкин Михаил Анатольевич  | hello           | 2   | 1080    | 45    | 200        | -    |  alg | stack | neum | hw | instr | binary | stream | port | pstr | prob2 | cache  |
| Начинкин Михаил Анатольевич  | hello_user_name | 8   | 3480    | 145   | 578        | -    |  alg | stack | neum | hw | instr | binary | stream | port | pstr | prob2 | cache  |
```
