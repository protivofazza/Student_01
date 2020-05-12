class StackList:
    """Проста реалізація класу структури даних Стек за допомогою стандартного типу колекцій Пайтон List. Серед переваг -
    простота реалізації за допомогою вбудованої структури.
    Серед недоліків - проблема швидкості роботи програми при помітному збільшенні наповненості стеку даними"""

    def __init__(self):
        self.stack_list = []

    def input_data(self):
        self.stack_list.append(input('Введіть дані для зберігання: '))

    def place_in(self, data_in):
        self.stack_list.append(data_in)

    def take_out(self):
        try:
            self.stack_list.pop()
        except IndexError:
            print('Stack is empty. Recovery operation is not possible...')

    def stack_demo(self):
        print(*self.stack_list)


stack_01 = StackList()
stack_01.input_data()
stack_01.input_data()
stack_01.input_data()
stack_01.place_in(12)
stack_01.stack_demo()
stack_01.take_out()
stack_01.take_out()
stack_01.stack_demo()


from collections import deque


class StackDeque:
    """
    Реалізація класу структури даних Стек за допомогою імпортованої структури даних deque. Серед переваг -
    методи .append() і .рор() працюють помітно швидше за ті ж методи структури List при випадках, коли блоки пам'яті
    для зберігання наступних комірок стеку виявляються заповнені.
    Серед недоліків - проблема швидкості роботи програми при операціях отримання даних по індексу. Хоча для Стеку це не
    актуально.
    """

    def __init__(self):
        self.stack_list = deque()

    def input_data(self):
        self.stack_list.append(input('Введіть дані для зберігання: '))

    def place_in(self, data_in):
        self.stack_list.append(data_in)

    def take_out(self):
        try:
            self.stack_list.pop()
        except IndexError:
            print('Stack is empty. Recovery operation is not possible...')

    def stack_demo(self):
        print(*self.stack_list)


stack_02 = StackDeque()
stack_02.input_data()
stack_02.input_data()
stack_02.input_data()
stack_02.place_in(12)
stack_02.stack_demo()
stack_02.take_out()
stack_02.take_out()
stack_02.stack_demo()
stack_02.take_out()
stack_02.take_out()
stack_02.take_out()
stack_02.stack_demo()


class Queue:
    """
    Реалізація класу структури даних Черга за допомогою імпортованої структури даних deque. Серед переваг -
    методи .append() і .popleft() працюють помітно швидше за аналогічні методи структури List.
    """

    def __init__(self):
        self.stack_list = deque()

    def input_data(self):
        self.stack_list.append(input('Введіть дані для зберігання: '))

    def place_in(self, data_in):
        self.stack_list.append(data_in)

    def take_out(self):
        try:
            self.stack_list.popleft()
        except IndexError:
            print('Stack is empty. Recovery operation is not possible...')

    def stack_demo(self):
        print(*self.stack_list)


queue_01 = Queue()
queue_01.input_data()
queue_01.input_data()
queue_01.input_data()
queue_01.place_in(12)
queue_01.stack_demo()
queue_01.take_out()
queue_01.take_out()
queue_01.stack_demo()
queue_01.take_out()
queue_01.take_out()
queue_01.take_out()
queue_01.stack_demo()

