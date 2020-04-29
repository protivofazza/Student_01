print('Урок 1\n\nЗадача 1:')

n = int(input('Введіть значення n: '))
list_01 = []
print('Всі парні значення зі згенерованого списку:')
for i in range(n+1):
    list_01.append(i)
    if i % 2 == 0 and i != 0:
        print(i, '   ', end='')
print(f'\nСгенерований список з {n} елментів, з якого вибирались парні значення:', list_01)


print('\nЗадача 2:')
country_dict = {'Австралія': 'Канберра', 'Італія': 'Рим', 'Germany': 'Berlin', 'Україна': 'Київ'}
country_list = ['Австралія', 'Італія', 'Germany', 'USA', 'ПАР']
for x in country_list:
    if x in country_dict:
        print(country_dict.get(x))


print('\nЗадача 3:')
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)

print('\nЗадача 4:')


def bank(dep_summ, dep_term, percent):
    dep_capitalise = dep_summ
    for x in range(1, dep_term+1):
        dep_capitalise = dep_capitalise*(1 + percent/100)
    return dep_summ + dep_summ*(percent/100)*dep_term, dep_capitalise


res_dep_stand, res_dep_capital = bank(int(input('Введіть розмір депозиту в грн: ')),
                                      int(input('Введіть термін депозиту в роках: ')),
                                      int(input('Введіть відсоткову ставку у відсотках: ')))
print('Сума за звичайною схемою по закінченні депозиту', res_dep_stand, 'грн',
      '\nСума по закінченні депозиту за схемою зі щорічною капіталізацією відсотків', res_dep_capital, 'грн')