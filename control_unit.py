from datapath import DataPath

command_format = 3
memory_format = 1024
stack_head: int = memory_format
stack_pointer: int = memory_format

memory = []
with open("program.o", 'rb') as f:
    for i in range(2048):
        memory.append(int.from_bytes(f.read(4), 'big'))

instr_pointer = 0


def branch_unit(instruction, logger):
    global instr_pointer, stack_pointer
    match instruction:
        case 10:  # Безусловный переход
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - jmp {memory[instr_pointer + 1]} -> IP\n")
            return memory[instr_pointer + 1]

        case 11:  # Переход если не выполняется условие ">"
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifm not {memory[stack_pointer - 1]} > {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] > memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 12:  # Переход если не выполняется условие "<"
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifl not {memory[stack_pointer - 1]} < {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] < memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 13:  # Переход если не выполняется условие "=="
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ife not {memory[stack_pointer - 1]} == {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] == memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 14:  # Переход если не выполняется условие "!="
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifne not {memory[stack_pointer - 1]} != {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] != memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 15:  # Переход если не выполняется условие ">="
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifme not {memory[stack_pointer - 1]} >= {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] >= memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 16:  # Переход если не выполняется условие "<="
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifle not {memory[stack_pointer - 1]} <= {memory[stack_pointer - 2]} -> #ip({memory[instr_pointer + 1]})\n")
            if not (memory[stack_pointer - 1] <= memory[stack_pointer - 2]):
                return memory[instr_pointer + 1]
            return None

        case 17:  # Переход, если вершина стека лежит в диапазоне
            logger.write(
                f"{instr_pointer} - {memory[instr_pointer]} - ifin {memory[stack_pointer - 1]} in [{memory[instr_pointer + 1]}; {memory[instr_pointer + 2]}] -> #ip({memory[stack_pointer - 2]})\n")
            if memory[stack_pointer - 1] in range(memory[instr_pointer + 1], memory[instr_pointer + 2]):
                return memory[stack_pointer - 2]
            return None


with open("log.txt", "w") as log:
    with open("input.txt", "r") as inp:
        with open("output.txt", "w") as out:
            data_path = DataPath(log, out, inp)
            while True:
                match memory[instr_pointer]:
                    case 0:  # Останов
                        log.write(f"{instr_pointer} - {memory[instr_pointer]} - hlt\n")
                        break

                    case 1:  # Берет из памяти, записывает на вершину стека
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - push {memory[memory[instr_pointer + 1]]} -> #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = memory[memory[instr_pointer + 1]]
                        stack_pointer += 1

                    case 2:  # Берет из стека, записывает в память по адресу
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - pull {memory[stack_pointer]} -> #{memory[instr_pointer + 1]}\n")
                        memory[memory[instr_pointer + 1]] = memory[stack_pointer]
                        memory[stack_pointer] = 0

                    case 3 | 4 | 5 | 6 | 7:  # Операции, совершаемые ALU
                        stack_pointer -= 1
                        prom = data_path.alu(memory[stack_pointer], memory[stack_pointer - 1], memory[instr_pointer],
                                             instr_pointer)
                        memory[stack_pointer - 1] = prom
                        memory[stack_pointer] = 0

                    case 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17:  # Команды выполняющиеся в Branch unit
                        new_instr_pointer = branch_unit(memory[instr_pointer], log)
                        if new_instr_pointer is not None:
                            instr_pointer = new_instr_pointer
                            continue

                    case 20:  # Записывает на вершину стека свой операнд
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - pushown {memory[instr_pointer + 1]} -> #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = memory[instr_pointer + 1]
                        stack_pointer += 1

                    case 21:  # Удаляет вершину стека
                        stack_pointer -= 1
                        log.write(
                            f"{instr_pointer} - {memory[instr_pointer]} - del #stack({stack_pointer - stack_head})\n")
                        memory[stack_pointer] = 0

                    case 30:  # Читает число из ввода, записывает на вершину стека
                        input_symbol = data_path.input_mux(True, instr_pointer)
                        if input_symbol is not None:
                            memory[stack_pointer] = input_symbol
                        else:
                            break
                        stack_pointer += 1

                    case 31:  # Читает символ ввода, записывает на вершину стека
                        input_symbol = data_path.input_mux(False, instr_pointer)
                        if input_symbol is not None:
                            memory[stack_pointer] = input_symbol
                        else:
                            break
                        stack_pointer += 1

                    case 32:  # Читает символ из вершины стека, записывает в файл вывода
                        data_path.output_demux(memory[stack_pointer - 1], True, instr_pointer)
                        memory[stack_pointer - 1] = 0
                        stack_pointer -= 1

                    case 33:  # Читает число из вершины стека, записывает в файл вывода
                        data_path.output_demux(memory[stack_pointer - 1], False, instr_pointer)
                        memory[stack_pointer - 1] = 0
                        stack_pointer -= 1

                instr_pointer += command_format
