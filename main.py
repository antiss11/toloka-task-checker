from browserFunctions import BrowserCore, VkActions
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


VK_LOGIN = ""
VK_PASSWORD = ""


TOLOKA_PAGE = "https://toloka.yandex.ru/"
TOLOKA_XPATH_LOGIN_BUTTON = "//span[@class='button__label']"
VK_LOGIN_BUTTON = "//span[@class='passp-social-block__list-item-icon passp-social-block__list-item-icon_vk']"
TOLOKA_PAGE_TASKS = "https://toloka.yandex.ru/tasks"
TASK_TEXT = "//div[@class='snippet__title']"
TASK_CSS = ".snippet"
TASKS_FILE = 'tasks'
ALARM_FILE = "alarm.wav"


def play_sound(path, count):
    pygame.init()
    sound = pygame.mixer.Sound(path)
    for i in range(count):
        sound.play(count - 1)


def load_tasklist(file_name):
    path = os.path.join(os.getcwd(), file_name)
    with open(path) as f:
        task_list = f.readlines()
        return [str.rstrip() for str in task_list]


class Log:
    def __call__(self, msg):
        time_now = time.strftime("%H:%M:%S_%d/%m")
        if len(msg) > 50:
            msg = msg[0:50] + "..."
        print("[{}] {:>20}".format(time_now, msg))


class TolokaChecker(BrowserCore):
    def __init__(self, *options):
        BrowserCore.__init__(self, *options)
        self.log = Log()

    def login(self):
        BrowserCore.get_page(self, TOLOKA_PAGE)
        BrowserCore.waiting(self, elem_class="promo-body")
        BrowserCore.find_element(self, xpath=TOLOKA_XPATH_LOGIN_BUTTON).click()
        BrowserCore.find_element(self, xpath=VK_LOGIN_BUTTON).click()
        BrowserCore.switch_window(self, 1)
        VkActions.vk_popup_login(self, VK_LOGIN, VK_PASSWORD)
        BrowserCore.switch_window(self, 0)
        BrowserCore.waiting(self, elem_class="snippet__title")
        self.log('Успешный логин')

    def get_task_title(self, task):
        return task.find_element_by_css_selector(".snippet__title").text

    def find_tasks(self):
        BrowserCore.get_page(self, TOLOKA_PAGE_TASKS)
        BrowserCore.waiting(self, xpath=TASK_TEXT)
        tasks = BrowserCore.find_element(self, css=TASK_CSS, all=True)
        task_list = load_tasklist(TASKS_FILE)
        for task in tasks:
            task_title = self.get_task_title(task)
            if task_title in task_list:
                self.log(task_title)
                play_sound(ALARM_FILE, 3)
                if input("Продолжить? (y/n)").lower() == "y" or "":
                    return True
                else:
                    return False
        return True


if __name__ == "__main__":
    browser = TolokaChecker("--log-level=3", "--headless")
    browser.login()
    while browser.find_tasks():
        time.sleep(50)
