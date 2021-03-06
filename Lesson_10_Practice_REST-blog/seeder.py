import random
from models import Tag, Author, Post
import schemas

TAGS = ('Альбер-Парк', 'Спа', 'Монца', 'Монако', 'Нюрбурринг', 'Сільверстоун', 'Судзука', 'Сахір', 'Інтерлагос')
AUTHORS = (
    ('Марк', 'Веббер'), ('Люіс', 'Хемілтон'), ('Ніко', 'Розберг'), ('Себастьян', 'Феттель'),
    ('Чарлі', 'Уайтінг'), ('Пол', 'Хендри'), ('Даніель', 'Ріккярдо'), ('Шарль', 'Леклер'),
    ('Кімі', 'Ряйкконен'), ('Серхіо', 'Перес'), ('Ленс', 'Стролл'), ('Вальтері', 'Боттас'),
    ('Ромен', 'Гросжан'), ('Кевін', 'Магнуссен'), ('Ніко', 'Хюлькенберг'), ('Карлос', 'Сайнс'),
    ('Пьер', 'Гаслі'), ('Феліппе', 'Масса'), ('Міхаєль', 'Шумахер'), ('Міка', 'Хаккінен'),
    ('Фернандо', 'Алонсо')
)

POSTS = (('Гран-прі та Кубок конструкторів',
          'Чемпіонат світу у класі «Формула-1» відбувається щороку і складається з Гран-прі, або етапів, '
          'які проводяться на спеціально побудованих трасах, або підготовлених вулицях міста. Наприкінці '
          'сезону, за підсумками всіх гонок визначається переможець чемпіонату. У Формулі-1 змагаються '
          'як окремі пілоти, так і команди. Пілот-переможець отримує титул чемпіона світу, а команда-'
          'переможець отримує Кубок конструкторів.'),
         ('Боліди',
          'Команди учасники змагань Формули-1 використовують гоночні автомобілі («боліди») власного '
          'виробництва. Тому для кожної команди вкрай важливо мати не лише швидкого і стабільного пілота '
          'та гарну стратегію, але й надзвичайно сильний конструкторський відділ. Наразі боліди Формули-1 '
          'розвивають швидкість до 360 км/год (хоча в останні роки FIA намагалась зменшити швидкість, '
          'впроваджуючи нові технічні правила), та здатні витримувати у поворотах перевантаження до 5 g. '
          'Кількість обертів двигуна обмежена до 15 000 об/хв.'),
         ('Географія перегонів',
          'Слід зазначити, що за всі роки свого існування Формула-1 постійно змінювалася. Історично основним '
          'центром розвитку Формули-1 є Європа. Більшість баз та дослідницьких центрів команд розташовано на '
          'цьому континенті. Однак, сфера спорту значно розширилася в останні роки і дедалі більше число '
          'Гран-прі проводяться на інших континентах.'),
         ('Фінансові особливості',
          'Щорічними витрати у Формулі 1 оцінюються у мільярди доларів США, а економічний ефект від проведення '
          'змагань є значним. Вартість проектування та будівництва проміжного рівня автомобілів складає близько '
          '$ 120 млн. Крім того, фінансові та політичні баталії у цьому спорті широко висвітлюються у ЗМІ. Однак, '
          'з 2000 року, після безперервного зростання витрат, декілька команд, у тому числі команди виробників '
          'автомобілів збанкрутували або були викуплені іншими компаніями.'),
         ('Інновації в Ф-1',
          'Оскільки кожна команда будує болід самостійно, то завдяки дуже високій конкуренції в перегонах '
          'Формула-1 постійно народжуються оригінальні конструкторські ідеї та рішення, які призводять до '
          'швидкого прогресу як самих болідів, так і звичайних дорожніх авто. Найвідомішим прикладом впровадження '
          'у серійному виробництві технології, розробленої для Формули-1, є антипробуксувальна система. Вперше '
          'цю систему було використано у 1990 році командою «Феррарі». Після заборони її в Формулі-1 у 1994 році, '
          'автовиробники почали впроваджувати систему на серійних автомобілях.\n'),
         ('Телетрансляції',
          'Формула-1 має глобальну телевізійну аудиторію близько 527 млн глядачів[3], що робить цей спорт '
          'найпопулярнішим міжнародним змаганням у світі. Власником всіх телевізійних прав на показ змагання '
          'є компанія Formula One Group.'),
         ('Організація змагального вікенду',
          "Гран-прі Формули-1 охоплює вихідні і починається з вільних заїздів, що проводяться протягом трьох сесій, "
          "кваліфікації, яка відбувається в суботу, та самих перегонів, які проводиться у неділю. Зазвичай, дві сесії "
          "вільних заїздів (тривалістю по 1,5 години) проводяться в п'ятницю, одна (тривалістю 1 годину) — у суботу, "
          "перед кваліфікацією.'"),
         ('Нарахування очків та пілоти команди',
          'У разі хвороби або інших поважних причин третій пілот може замінити у кваліфікації й перегонах одного з '
          'основних пілотів команди, але третій пілот може бути допущений до перегонів тільки якщо він брав участь у '
          'кваліфікаційних заїздах. Очки, набрані запасним пілотом в гонці, будуть нараховані на його особистий '
          'рахунок у чемпіонаті світу; у боротьбі за Кубок конструкторів ці очки будуть додані до рахунку команди, '
          'якщо б за неї виступав основний пілот. Протягом сезону за одну команду можуть виступати, набираючи для '
          'себе і для неї очки, до 4 пілотів.'),
         ('Кваліфікаційні сесії',
          'Протягом більшої частини історії цього виду спорту, кваліфікаційні сесія мало чим відрізнялася від '
          'вільних заїздів. Кілька років тому це була годинна сесія під час якої пілоти могли проїхати одне швидке '
          'коло. Найшвидше коло йде в залік. На стартовому полі перед перегонами пілоти розташовувалися згідно з '
          'результатами, показаними під час кваліфікації. На відміну від багатьох інших гонок, в сучасній Формулі-1 '
          'за перемогу в кваліфікації додаткових очок не дають.'),
         ('«Нокаут»',
          "Теперішній формат кваліфікації, відомий також як «нокаут», був прийнятий в сезоні 2006 року. Кваліфікація "
          "«нокаут» поділяється на три частини (періоди, або тури). У першому періоді дозволяється виїзд всіх машин. "
          "П'ять найповільніших не беруть участь у подальшій кваліфікації, результати 15-ти найкращих не враховуються. "
          "У другому періоді дозволяється виїзд решти 15-ти машин. П'ять найповільніших із них не братимуть участь у "
          "подальшій кваліфікації, результати 10-ти найкращих надалі не враховуються. У третьому і останньому періоді "
          "решта десять машин розігрують між собою десять перших місць на старті перегонів. Ця процедура "
          "застосовується за участі 20-ти машин, якщо ж їх 22, то в першому й другому кваліфікаційному періоді "
          "вибуває по шість машин. Якщо, на думку стюардів, гонщик навмисно зупинився на трасі або створив перешкоди "
          "іншому гонщику, то його результат анулюється."),
         ('Прогрівочне коло',
          "Перегони починаються з прогрівочного кола, щоб пілоти могли прогріти гуму і гальма на своїх болідах. "
          "Також прогрівочне коло дозволяє пілотам перевірити стан траси та їх боліду. Обгони на прогрівочному колі "
          "заборонені. Перед ним і після його закінчення боліди шикуються на стартовому полі (стартовій решітці) "
          "згідно з результатами кваліфікації. Якщо старт було відкладено, прогрівочне коло повторюють, а дистанцію "
          "перегонів скорочують на одне коло. Після його закінчення боліди знову шикуються на стартовій решітці і "
          "після сигналу світлофора починають перегони в змагальному режимі."),
         ('Старт',
          "П'ять червоних вогнів на світлофорі засвічуються по черзі з інтервалом в одну секунду, потім всі вони "
          "одночасно згасають після невизначеного часу (як правило, менш ніж за 3 секунди), щоб сигналізувати про "
          "початок перегонів. Старт може бути скасовано, якщо водій який заглух на стартовому полі, подав про це "
          "сигнал, піднявши руку. У цьому випадку здійснюється рестарт перегонів, але вже без участі пілота, що "
          "його викликав.")
         )


def add_tags():
    for tag in TAGS:
        tag = {"tag_name": tag}
        if not Tag.objects.filter(**tag):
            tag = schemas.TagSchema().load(tag)
            print('tag =', tag)
            Tag.objects.create(**tag).save()


def add_authors():
    for author in AUTHORS:
        author = {"name": author[0], "surname": author[1]}
        if not Author.objects.filter(**author):
            author = schemas.AuthorSchema().load(author)
            print("author =", author)
            Author.objects.create(**author).save()


def add_posts():
    tags_list = Tag.objects
    authors_list = Author.objects
    for post in POSTS:
        data_dict = {}

        author = authors_list[random.randint(0, len(authors_list) - 1)]
        author.num_of_publications += 1
        author.save()
        data_dict['author'] = str(author.id)

        data_dict['title'] = post[0]
        data_dict['body'] = post[1]

        tags_num = random.randint(1, 3)
        tags_in_post = []
        while tags_num >= 1:
            tag = tags_list[random.randint(0, len(tags_list) - 1)]
            if tag not in tags_in_post:
                tags_in_post.append(str(tag.id))
                tags_num -= 1
        data_dict['tag'] = tags_in_post
        print("data_dict =", data_dict)

        post_in_db = schemas.PostSchema().load(data_dict)
        Post.objects.create(**post_in_db).save()


if __name__ == '__main__':
    add_tags()
    add_authors()
    add_posts()
    # Tag.objects.delete()
    # Author.objects.delete()
    # Post.objects.delete()
