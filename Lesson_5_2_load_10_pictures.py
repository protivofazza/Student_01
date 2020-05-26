from threading import Thread
import requests

num_of_thread = 0


def create_thread(name_thread, daemon):
    def decorator(func):
        def wrapper(link):
            global num_of_thread
            num_of_thread += 1
            t = Thread(target=func, args=(link,), daemon=daemon, name=name_thread + str(num_of_thread))
            t.start()

        return wrapper

    return decorator


@create_thread('Load_picture', False)
def load_link(link):
    global num_of_load
    print('start of load pict')
    response = requests.get(link)
    f = open("Picture_top_50_" + str(num_of_load) + ".jpg", "wb")
    num_of_load += 1
    if response.ok:
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)
    print('end of load pict', num_of_load)


link_list = [
    'https://cdn.photosight.ru/img/7/a54/7044003_xlarge.jpg',
    'https://cdn.photosight.ru/img/9/92e/7044078_xlarge.jpg',
    'https://cdn.photosight.ru/img/8/25f/7044801_xlarge.jpg',
    'https://cdn.photosight.ru/img/c/f79/7043993_xlarge.jpg',
    'https://cdn.photosight.ru/img/0/6da/7043194_xlarge.jpg',
    'https://cdn.photosight.ru/img/9/69f/7043855_xlarge.jpg',
    'https://cdn.photosight.ru/img/e/64c/7044125_xlarge.jpg',
    'https://cdn.photosight.ru/img/b/ca9/7044642_xlarge.jpg',
    'https://cdn.photosight.ru/img/9/10a/7043242_xlarge.jpg',
    'https://cdn.photosight.ru/img/7/362/7043661_xlarge.jpg',
]

print('Start of think_about')

num_of_load = 1
for link_ in link_list:
    load_link(link_)

print('\nEnd of think_about')
