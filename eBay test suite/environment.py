from selenium import webdriver
import re



def before_all(context):
    context.url = 'https://www.ebay.com/'


def before_scenario(context, feature):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(5)


def after_step(context, step):
    if step.status == 'failed':
        step_name = re.sub('[^a-zA-Z0-9]', '', step.name)
        print(step_name)
        context.browser.save_screenshot(f"{step_name}.png")


def after_scenario(context, feature):
    context.browser.close()
    context.browser.quit()
