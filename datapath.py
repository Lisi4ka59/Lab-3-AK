class DataPath:
    log = None
    output = None
    input = None

    def __init__(self, log, output, input):
        self.log = log
        self.output = output
        self.input = input

    def alu(self, stack_top, stack_next, instruction, instr_pointer):
        match instruction:
            case 3:  # Складывает два верхних значения в стеке
                self.log.write(
                    f"{instr_pointer} - {instruction} - add {stack_top} + {stack_next}\n")
                return stack_next + stack_top

            case 4:  # Вычитает из верхнего значения стека следующее значение стека
                self.log.write(
                    f"{instr_pointer} - {instruction} - sub {stack_top} - {stack_next}\n")
                return stack_top - stack_next

            case 5:  # Умножает верхнее значение стека и следующее значение стека
                self.log.write(
                    f"{instr_pointer} - {instruction} - mult {stack_top} * {stack_next}\n")
                return stack_top * stack_next

            case 6:  # Производит целочисленное деление верхнего значения стека на следующее значение стека
                self.log.write(
                    f"{instr_pointer} - {instruction} - div {stack_top} // {stack_next}\n")
                return stack_top // stack_next

            case 7:  # Находит остаток от деления значения на вершине стека и следующего значения стека
                self.log.write(
                    f"{instr_pointer} - {instruction} - mod {stack_top} % {stack_next}\n")
                return stack_top % stack_next

    def input_mux(self, is_numeric, instr_pointer):
        input_symbol = self.input.read(1)
        if is_numeric:  # Читает число из ввода, записывает на вершину стека
            self.log.write(
                f"{instr_pointer} - 30 - inpint {str(input_symbol)} \n")
            if input_symbol:
                symbol = int(input_symbol)
            else:
                self.log.write("Program terminated because of end of input\n")
                return None
            return symbol
        else:
            self.log.write(
                f"{instr_pointer} - 31 - inp {str(input_symbol)} \n")
            if input_symbol:
                symbol = ord(input_symbol)
            else:
                self.log.write("Program terminated because of end of input\n")
                return None
            return symbol

    def output_demux(self, symbol, is_number, instr_pointer):
        if is_number:  # Читает символ из вершины стека, записывает в файл вывода
            self.log.write(
                f"{instr_pointer} - 32 - out {chr(symbol)}\n")
            self.output.write(chr(symbol))
        else:  # Читает число из вершины стека, записывает в файл вывода
            self.log.write(
                f"{instr_pointer} - 33 - outint {str(symbol)}\n")
            self.output.write(str(symbol))
