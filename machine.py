command_format = 3
memory_format = 1024
stack_head: int = memory_format
stack_pointer: int = memory_format

memory = []
with open("program.o", 'rb') as f:
    for i in range(2048):
        memory.append(int.from_bytes(f.read(4), 'big'))

instr_pointer = 0

with open("log.txt", "w") as log:
    with open("input.txt", "r") as inp:
        with open("output.txt", "w") as out:
            while True:
                match memory[instr_pointer]:
                    case 0:  # Останов
                        log.write(f"{instr_pointer} - {memory[instr_pointer]} - hlt\n")
                        break

                    case 1:  # Берет из памяти, записывает на вершину стека
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - push {memory[memory[instr_pointer + 1]]} -> \
                            #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = memory[memory[instr_pointer + 1]]
                        stack_pointer += 1

                    case 2:  # Берет из стека, записывает в память по адресу
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - pull {memory[stack_pointer]} -> \
                            #{memory[instr_pointer + 1]}\n")
                        memory[memory[instr_pointer + 1]] = memory[stack_pointer]
                        memory[stack_pointer] = 0

                    case 3:  # Складывает два верхних значения в стеке
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - add {memory[stack_pointer]} + \
                            {memory[stack_pointer - 1]} -> #stack({stack_pointer - 1 - stack_head})\n")
                        memory[stack_pointer - 1] = memory[stack_pointer] + memory[stack_pointer - 1]
                        memory[stack_pointer] = 0

                    case 4:  # Вычитает из верхнего значения стека следующее значение стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - sub {memory[stack_pointer]} - \
                            {memory[stack_pointer - 1]} -> #stack({stack_pointer - 1 - stack_head})\n")
                        memory[stack_pointer - 1] = memory[stack_pointer] - memory[stack_pointer - 1]
                        memory[stack_pointer] = 0

                    case 5:  # Умножает верхнее значение стека и следующее значение стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - mult {memory[stack_pointer]} * \
                            {memory[stack_pointer - 1]} -> #stack({stack_pointer - 1 - stack_head})\n")
                        memory[stack_pointer - 1] = memory[stack_pointer] * memory[stack_pointer - 1]
                        memory[stack_pointer] = 0

                    case 6:  # Производит целочисленное деление верхнего значения стека на следующее значение стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - div {memory[stack_pointer]} // \
                            {memory[stack_pointer - 1]} -> #stack({stack_pointer - 1 - stack_head})\n")
                        memory[stack_pointer - 1] = memory[stack_pointer] // memory[stack_pointer - 1]
                        memory[stack_pointer] = 0

                    case 7:  # Находит остаток от деления значения на вершине стека и следующего значения стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - mod {memory[stack_pointer]} % \
                            {memory[stack_pointer - 1]} -> #stack({stack_pointer - 1 - stack_head})\n")
                        memory[stack_pointer - 1] = memory[stack_pointer] % memory[stack_pointer - 1]
                        memory[stack_pointer] = 0

                    case 10:  # Безусловный переход
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - jmp {memory[instr_pointer + 1]} -> IP\n")
                        instr_pointer = memory[instr_pointer + 1]
                        continue

                    case 11:  # Переход если не выполняется условие ">"
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ifm not {memory[stack_pointer - 1]} > \
                            {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] > memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 12:  # Переход если не выполняется условие "<"
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ifl not {memory[stack_pointer - 1]} < \
                            {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] < memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 13:  # Переход если не выполняется условие "=="
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ife not {memory[stack_pointer - 1]} \
                            == {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] == memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 14:  # Переход если не выполняется условие "!="
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ifne not {memory[stack_pointer - 1]} \
                            != {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] != memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 15:  # Переход если не выполняется условие ">="
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ifme not {memory[stack_pointer - 1]} \
                            >= {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] >= memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 16:  # Переход если не выполняется условие "<="
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - ifle not {memory[stack_pointer - 1]} \
                            <= {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
                        if not (memory[stack_pointer - 1] <= memory[stack_pointer - 2]):
                            instr_pointer = memory[instr_pointer + 1]
                            continue

                    case 20:  # Записывает на вершину стека свой операнд
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - pushown {memory[instr_pointer + 1]} \
                            -> #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = memory[instr_pointer + 1]
                        stack_pointer += 1

                    case 21:  # Удаляет вершину стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - del #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = 0

                    case 30:  # Читает число из ввода, записывает на вершину стека
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - inpint {memory[instr_pointer + 1]} \
                            -> #stack({stack_pointer - stack_head})\n")
                        input_symbol = inp.read(1)
                        if input_symbol:
                            memory[stack_pointer] = int(input_symbol)
                        else:
                            log.write("Program terminated because of end of input\n")
                            break
                        stack_pointer += 1

                    case 31:  # Читает символ ввода, записывает на вершину стека
                        input_symbol = inp.read(1)
                        log.write(f"{instr_pointer} - {memory[instr_pointer]} - inp \
                        {input_symbol} -> #stack({stack_pointer - stack_head})\n")
                        if input_symbol:
                            input_symbol = ord(input_symbol)
                            memory[stack_pointer] = input_symbol
                        else:
                            log.write("Program terminated because of end of input\n")
                            break
                        stack_pointer += 1

                    case 32:  # Читает символ из вершины стека, записывает в файл вывода
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - out {chr(memory[stack_pointer - 1])} \
                            -> #stack({stack_pointer - stack_head})\n")
                        out.write(chr(memory[stack_pointer - 1]))
                        memory[stack_pointer - 1] = 0
                        stack_pointer -= 1

                    case 33:  # Читает число из вершины стека, записывает в файл вывода
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - outint {str(memory[stack_pointer - 1])} \
                            -> #stack({stack_pointer - stack_head})\n")
                        out.write(str(memory[stack_pointer - 1]))
                        memory[stack_pointer - 1] = 0
                        stack_pointer -= 1

                instr_pointer += command_format
                
