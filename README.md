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
![image](https://github.com/Lisi4ka59/Lab-3-AK/assets/122356446/af28bc90-594c-4e8e-9915-d305d4cc21c0)

### Control Unit
![image](https://github.com/Lisi4ka59/Lab-3-AK/assets/122356446/22440f2f-90fd-47e4-9af2-665cbf90f59e)


## Тестирование

### Описание работы настроенного CI
Производится проверка форматироания и линтер, затем запускаются тесты, каждый из которых состоит из сборки программы из исходного кода, запуска машины и сверки результата работы машины с эталоном 







