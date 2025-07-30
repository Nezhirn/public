import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Основные разделы и их подстраницы с соответствующими папками
sections_and_urls = {
    "Радиаторные терморегуляторы и клапаны": {
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany": None,
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/termostaticeskie-elementy-radiatornyx-termoregulyatorov": "Термостатические элементы радиаторных терморегуляторов",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/radiatornye-klapany": "Радиаторные клапаны",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/komplekty-termoregulyatorov-dlya-sistem-otopleniya": "Комплекты терморегуляторов для систем отопления",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/komnatnye-termostaty": "Комнатные термостаты",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/prisoedinitelno-reguliruyushchie-garnitury": "Присоединительно-регулирующие гарнитуры",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/garnitury-dlya-niznego-podklyuceniya": "Гарнитуры для нижнего подключения",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/zaporno-prisoedinitelnye-radiatornye-klapany": "Запорно-присоединительные радиаторные клапаны",
        "https://ridan.ru/catalog/thermal-automation/radiatornye-termoregulyatory-i-klapany/fitingi-dlya-prisoedineniya-truboprovodov-i-dopolnitelnye-prinadleznosti": "Фитинги для присоединения трубопроводов и дополнительные принадлежности"
    },
    "Балансировочные клапаны для систем тепло- и холодоснабжения": {
        "https://ridan.ru/catalog/thermal-automation/balansirovochnye-klapany-dlya-sistem-teplo-i-kholodosnabzheniya": None,
        "https://ridan.ru/catalog/thermal-automation/balansirovochnye-klapany-dlya-sistem-teplo-i-kholodosnabzheniya/avtomaticeskie-balansirovocnye-klapany": "Автоматические балансировочные клапаны",
        "https://ridan.ru/catalog/thermal-automation/balansirovochnye-klapany-dlya-sistem-teplo-i-kholodosnabzheniya/rucnye-balansirovocnye-klapany": "Ручные балансировочные клапаны",
        "https://ridan.ru/catalog/thermal-automation/balansirovochnye-klapany-dlya-sistem-teplo-i-kholodosnabzheniya/fitingi-prisoedinitelnye": "Фитинги присоединительные",
        "https://ridan.ru/catalog/thermal-automation/balansirovochnye-klapany-dlya-sistem-teplo-i-kholodosnabzheniya/dopolnitelnye-prinadlezhnosti": "Дополнительные принадлежности"
    },
    "Регуляторы температуры и давления прямого действия": {
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya": None,
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/reguliruyushchie-klapany-dlya-regulyatorov-davleniya-perepada-davleniya-raskhoda-i-temperatury-bolshoy-serii": "Регулирующие клапаны для регуляторов давления, перепада давления, расхода и температуры большой серии",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-perepada-davleniya": "Регуляторы перепада давления",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-davleniya-do-sebya-regulyator-podpora": "Регуляторы давления «до себя» (регулятор подпора)",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-davleniya-posle-sebya": "Регуляторы давления «после себя»",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-perepuska": "Регуляторы перепуска",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-temperatury-kombinirovannye": "Регуляторы температуры комбинированные",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/prinadleznosti-k-gidravliceskim-regulyatoram-ridan": "Принадлежности к гидравлическим регуляторам Ридан",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-ograniciteli-rasxoda": "Регуляторы – ограничители расхода (архив)",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-perepada-davleniya-s-avtomaticeskim-ograniceniem-rasxoda": "Регуляторы перепада давления с автоматическим ограничением расхода (архив)",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/pilotnye-regulyatory-davleniya-dlya-sistem-teplosnabzheniya": "Пилотные регуляторы давления для систем теплоснабжения (архив)",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/regulyatory-temperatury-monoblochnye": "Регуляторы температуры моноблочные (архив)",
        "https://ridan.ru/catalog/thermal-automation/regulyatory-temperatury-i-davleniya-pryamogo-deistviya/intellektualnye-privody-dlya-gidravliceskix-regulyatorov": "Интеллектуальные приводы для гидравлических регуляторов (архив)"
    },
    "Клапаны и электроприводы": {
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody": None,
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/klapany-reguliruyushhie-sedelnye": "Клапаны регулирующие седельные",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/privody-dlya-reguliruyushhix-klapanov": "Приводы для регулирующих клапанов",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/povorotnye-reguliruyushhie-klapany-i-elektroprivody-k-nim": "Поворотные регулирующие клапаны и электроприводы к ним",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/klapany-sarovye-dvuxpozicionnye": "Клапаны шаровые двухпозиционные",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/klapany-reguliruyushhie-kombinirovannye": "Клапаны регулирующие комбинированные",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/klapany-i-elektroprivody-dlya-avtomatizacii-mestnyx-ventilyacionnyx-ustanovok": "Клапаны и электроприводы для автоматизации местных вентиляционных установок",
        "https://ridan.ru/catalog/thermal-automation/klapany-i-elektroprivody/aksessuary-dlya-reguliruyushhix-klapanov": "Аксессуары для регулирующих клапанов"
    },
    "Пластинчатые теплообменники": {
        "https://ridan.ru/catalog/thermal-automation/plastinchatye-teploobmenniki": None,
        "https://ridan.ru/catalog/thermal-automation/plastinchatye-teploobmenniki/odnoxodovye-payanye-plastincatye-teploobmenniki": "Одноходовые паяные пластинчатые теплообменники",
        "https://ridan.ru/catalog/thermal-automation/plastinchatye-teploobmenniki/dvuxxodovye-payanye-plastincatye-teploobmenniki": "Двухходовые паяные пластинчатые теплообменники"
    },
    "Контроллеры и диспетчеризация": {
        "https://ridan.ru/catalog/thermal-automation/kontrollery-i-dispetcerizaciya": None,
        "https://ridan.ru/catalog/thermal-automation/kontrollery-i-dispetcerizaciya/controllery-serii-ecl": "Контроллеры серии ECL",
        "https://ridan.ru/catalog/thermal-automation/kontrollery-i-dispetcerizaciya/datciki-temperatury-ecl": "Датчики и реле для контроллеров ECL",
        "https://ridan.ru/catalog/thermal-automation/kontrollery-i-dispetcerizaciya/dispetcerizaciya": "Диспетчеризация"
    },
    "Насосные станции" : {
        "https://ridan.ru/catalog/thermal-automation/nasosnye-stancii": None
    },
    "Блочные тепловые пункты": {
        "https://ridan.ru/catalog/thermal-automation/blocnye-teplovye-punkty": None
    },
    "Блочные холодильные узлы": {
        "https://ridan.ru/catalog/thermal-automation/blochnie-holodilnie-uzly": None
    },
    "Коллекторы и распределительные узлы": {
        "https://ridan.ru/catalog/thermal-automation/kollektory-i-raspredelitelnye-uzly": None,
        "https://ridan.ru/catalog/thermal-automation/kollektory-i-raspredelitelnye-uzly/uzly-raspredelitelnyie-etaznyie-tdu-r": "Узлы распределительные этажные для систем отопления TDU-R Ридан",
        "https://ridan.ru/catalog/thermal-automation/kollektory-i-raspredelitelnye-uzly/kvartirnye-stancii-sks": "Квартирные станции ШКС Ридан",
        "https://ridan.ru/catalog/thermal-automation/kollektory-i-raspredelitelnye-uzly/kollektory-raspredelitelnye": "Коллекторы распределительные"
    },
    "Шкафы автоматизации, диспетчеризации и учета": {
        "https://ridan.ru/catalog/thermal-automation/skafy-avtomatizacii": None
    },
    "Учёт тепловой энергии": {
        "https://ridan.ru/catalog/thermal-automation/ucyot-teplovoi-energii": None,
        "https://ridan.ru/catalog/thermal-automation/ucyot-teplovoi-energii/raspredeliteli-indiv": "Распределители INDIV",
        "https://ridan.ru/catalog/thermal-automation/ucyot-teplovoi-energii/kvartirnye-pribory-ucyota": "Квартирные приборы учёта",
        "https://ridan.ru/catalog/thermal-automation/ucyot-teplovoi-energii/kommerceskii-obshhedomovoi-ucet-teplovoi-energii": "Коммерческий (Общедомовой) учет тепловой энергии"
    },
    "Трубопроводная арматура": {
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura": None,
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/stalnye-zaporno-reguliruyushhie-krany": "Стальные краны запорно-регулирующие Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/stalnye-krany-sarovye-zapornye": "Стальные краны шаровые запорные Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/privod-elektriceskii-amv-dlia-sarovyx-kranov-rjip-premium": "Привод электрический АМВ для шаровых кранов RJIP Premium (раздел в разработке)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/cugunnye-krany-sarovye-ridan": "Краны шаровые чугунные Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/latunnye-krany-sarovye-zapornye": "Латунные краны шаровые запорные Ридан (код 065B82xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/latunnye-krany-sarovye-zapornye-ridan-kod-065b83xxr": "Латунные краны шаровые запорные Ридан (код 065B83xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/nerzhaveyushchie-krany-sarovye-zapornye": "Нержавеющие краны шаровые запорные Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/diskovye-zatvory": "Затворы дисковые Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/latunnye-obratnye-klapany": "Латунные обратные клапаны Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/chugunnie-klapany-obratnye": "Чугунные обратные клапаны/затворы Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/nerzaveyushhie-obratnye-klapany": "Нержавеющие обратные клапаны Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/cugunnye-filtry-setcatye": "Фильтры сетчатые Ридан ФСФ",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/latunnie-filtry-setcatye": "Латунные фильтры сетчатые Ридан (код 065B82xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/latunnye-filtry-setcatye-ridan-kod-065b83xxr": "Латунные фильтры сетчатые Ридан (код 065B83xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/nerzaveyushhie-filtry-setcatye": "Нержавеющие фильтры сетчатые Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/vozdukhootvodchiki": "Воздухоотводчики Airvent-R Ридан (код 06582xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/vozduxootvodciki-airvent-r-ridan-kod-06583xxr": "Воздухоотводчики Airvent-R Ридан (код 06583xxR)",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/osevye-silfonnye-kompensatory": "Компенсаторы осевые сильфонные Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/regulyatory-davlenya-ridan": "Регуляторы давления Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/redukcionnye-klapany": "Клапаны редукционные Ридан",
        "https://ridan.ru/catalog/thermal-automation/truboprovodnaya-armatura/gibkie-vstavki": "Гибкие вставки"
    },
    "Узлы регулирования приточных установок": {
        "https://ridan.ru/catalog/thermal-automation/uzly-regulirovaniya-pritocnyx-ustanovok": None,
        "https://ridan.ru/catalog/thermal-automation/uzly-regulirovaniya-pritocnyx-ustanovok/uzly-teplosnabzeniya-s-3-xodovymi-klapanami": "Узлы теплоснабжения с 3-ходовыми клапанами",
        "https://ridan.ru/catalog/thermal-automation/uzly-regulirovaniya-pritocnyx-ustanovok/uzly-xolodosnabzeniya-s-3-xodovymi-klapanami": "Узлы холодоснабжения с 3-ходовыми клапанами"
    },
    "Преобразователи частоты": {
        "https://ridan.ru/catalog/thermal-automation/preobrazovateli-castoty": None
    },
    "Компоненты горелок": {
        "https://ridan.ru/catalog/thermal-automation/komponenty-gorelok": None
    }

}
# Заголовки HTTP-запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# Функция для создания папок для разделов и подстраниц
def create_directory_for_url(section_name, subfolder_name=None, base_directory="C:/Users/Andrew/Downloads/Выгрузка"):
    # Папка для основного раздела
    section_path = os.path.join(base_directory, section_name)
    os.makedirs(section_path, exist_ok=True)
    
    # Если для подстраницы нужно создать подпапку
    if subfolder_name:
        folder_path = os.path.join(section_path, subfolder_name)
        os.makedirs(folder_path, exist_ok=True)
    else:
        folder_path = section_path
    
    return folder_path

# Функция для загрузки и сохранения изображений
def download_image(img_url, title=None, folder=""):
    # Если заголовок отсутствует, используем имя файла из URL
    if not title:
        filename = os.path.basename(img_url)
    else:
        # Фильтруем недопустимые символы в заголовке и используем его в имени файла
        filename = "".join(c for c in title if c.isalnum() or c in (' ', '.', '_')).rstrip() + ".jpg"
    
    # Полный путь для сохранения файла
    filepath = os.path.join(folder, filename)
    
    # Загружаем изображение
    img_data = requests.get(img_url).content
    with open(filepath, "wb") as handler:
        handler.write(img_data)
    print(f"Изображение сохранено: {filepath}")

# Проходим по каждому разделу и его подстраницам
for section_name, urls_and_folders in sections_and_urls.items():
    print(f"Обрабатывается раздел: {section_name}")
    
    # Проходим по каждому URL в разделе
    for url, subfolder_name in urls_and_folders.items():
        print(f"Обрабатывается URL: {url} для раздела {section_name}")
        
        # Создаем директорию для текущего URL: основная папка + подпапка (если есть)
        save_directory = create_directory_for_url(section_name, subfolder_name)
        
        # Получаем содержимое страницы
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Проверим, загрузилось ли что-то
        if response.status_code == 200:
            print("Страница успешно загружена")
        else:
            print("Не удалось загрузить страницу")
            continue

        # Находим все теги <img> и проверяем, содержат ли они изображения из директории /files/
        images = soup.find_all("img")

        # Проверим, сколько изображений было найдено
        print(f"Найдено {len(images)} изображений")

        # Скачиваем изображения
        for img in images:
            img_url = img.get("src")
            if img_url and "/files/" in img_url:  # Проверяем, что ссылка ведет в директорию files
                # Делаем URL абсолютным, если он относительный
                img_url = urljoin(url, img_url)
                
                # Попытаемся найти заголовок <h3>
                title = None
                h_tag = img.find_previous("h3")
                if h_tag:
                    title = h_tag.text.strip()
                
                print(f"Найдено изображение: {img_url}, заголовок: {title if title else 'Без названия'}")
                download_image(img_url, title, folder=save_directory)
            else:
                print("Изображение не из директории /files/")
