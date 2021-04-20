from behave import step, then
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


def find_search_input(browser) -> WebElement:
    return browser.find_element_by_id("gh-ac")


@step('Navigate to eBay')
def step_implementation(context):
    context.browser.get(context.url)


@step('In search bar type "{item}"')
def search_smth(context, item):
    search_input = find_search_input(context.browser)
    search_input.send_keys(str(item))


@step('Click "search" button')
def cleck_the_sirch_btn(context):
    srch_btn = context.browser.find_element_by_xpath("//input[@class = 'btn btn-prim gh-spr']")
    srch_btn.click()



@step('All displayed items are relevant to keyword "{search}"')
def verify_search_result(context, search):
    all_mismatches = get_mismatches_from_current_page(context, search)
    if all_mismatches:
        print(all_mismatches)
        raise ValueError(f'Some items are not {search} related')


def get_mismatches_from_current_page(context, search):
    result_items = context.browser.find_elements_by_xpath("//li[starts-with(@class,'s-item')]//h3")
    mismatches = []                                                # placeholder for bugs
    for each_item in result_items:                                 # iterate through results
        if search.lower() not in each_item.text.lower():           # True or False
            mismatches.append(each_item.text)
    return mismatches


@step('All displayed items on {pages} pages are relevant to keyword "{search}"')
def verify_on_multiple_search_result_pages(context, pages, search):
    max_page = int(pages)
    current_page = 1
    all_mismatches = []
    while current_page <= max_page:
        all_mismatches = all_mismatches + get_mismatches_from_current_page(context, search)
        current_page = click_next_search_result_page(context.browser)
    if all_mismatches:
        print(all_mismatches)
        raise ValueError(f'Some items are not {search} related')


def click_next_search_result_page(browser):
    right_arrow = browser.find_element_by_xpath("//div[@class='s-pagination']//a[@type='next']")
    right_arrow.click()
    current_page_element = browser.find_element_by_xpath("//div[@class='s-pagination']//a[@aria-current='page']")
    page_number = int(current_page_element.text)
    return page_number


@step('In search bar type special characters')
def search_smth(context):
    search_input = find_search_input(context.browser)
    search_input.send_keys("!@#")
    search_input.send_keys("$*&")


@step('All categories displayed')
def verify_search_result(context):
    item = context.browser.find_element_by_xpath("//div[@class='all-categories-left-nav-container']")


@step('In search bar type dress in low and upper case')
def search_smth(context):
    find_search_input(context.browser).send_keys("DResS")


@step('Press Enter using keyboard')
def press_enter_using_keyboard(context):
    find_search_input(context.browser).send_keys(Keys.ENTER)


@step('Click "{link}" element')
def click_header_sell(context, link):
    header_sell_action =\
        context.browser.find_element_by_xpath(f"//*[contains(@class, 'gh') and contains(text(), '{link}')]")
    header_sell_action.click()


@step('List an item bar appears')
def item_bar_appears(context):
    item_bar = context.browser.find_element_by_xpath("//*[contains(@class, 'fake') and @aria-label ='Click on button - List an item']")


@step('User redirected to My ebay security page')
def verification_bar_appears(context):
    varification_bar = context.browser.find_element_by_xpath("//div[@id = 'CentralArea']")


# @step('All displayed items are relevant to keyword "pants"')
# def all_items_relevant_to_pants(context):
#     item = context.browser.find_element_by_xpath("//h3[@class = 's-item__title s-item__title--has-tags' and contains(text(), 'Push Up Fitness Leggings Sport Running Yoga Gym Pants Workout Trousers')]")


@then("Alert popup must be present")
def step_impl(context):
    popup = context.browser.find_element_by_id("gh-eb-Alerts-o")
    assert popup.is_displayed()


@step('Filter by "{chbx_label}" in category "{header}"')
def filter_results(context, chbx_label, header):
    desired_chbx = context.browser.find_elements_by_xpath(f"//li[@class = 'x-refine__main__list '][.//h3[text() = '{header}']]//div[@class = 'x-refine__select__svg']//input[@aria-label='{chbx_label}']")
    if not desired_chbx:
        raise ValueError('No filter by label{} in category {}')
    desired_chbx[0].click()


@step('Apply following filters')
def filters_from_table(context):
    for filter in context.table.rows:
        header = filter['Filter']
        chbx_label = filter['value']

        desired_chbx = context.browser.find_elements_by_xpath(
            f"//li[@class = 'x-refine__main__list '][.//h3[text() = '{header}']]//div[@class = 'x-refine__select__svg']//input[@aria-label='{chbx_label}']")
        if not desired_chbx:
            raise ValueError(f'No filter by label{chbx_label} in category {header}')
        desired_chbx[0].click()


@step('Search for "{item}"')
def search_item (context, item):
    search_inpt = context.browser.find_elements_by_xpath(f"//input[@id = 'gh-ac']")

    # limit = 20
    # while not search_inpt and limit:
    #     sleep(1)
    #     limit -= 1
    #     search_inpt = context.browser.find_elements_by_xpath(f"//input[@id = 'gh-ac']")
    #
    # if not search_inpt:
    #     raise Exception("Item not found")
    # search_inpt[0].send_keys(item)

    search_inpt = WebDriverWait(context.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id = 'gh-ac']")), message='Item is not found')
    search_inpt.send_keys(item)


@step('Validate that all items related to following')
def check_filters(context):
    mismatches = []
    result_items = context.browser.find_elements_by_xpath("//li[contains(@class,'s-item      ')]")

    current_window = context.browser.current_window_handle

    # this dict contains all the filters specified in the scenario
    filters = filters_to_dict(context.table.rows)

    cleared_list = []
    for item in result_items:  # iterate through results
        link = item.find_element_by_xpath("descendant::a").get_attribute("href")
        title = item.find_element_by_xpath("descendant::h3").text
        item_specs = (link, title)
        cleared_list.append(item_specs)

    for link, title in cleared_list[:10]:
        context.browser.execute_script(f'window.open("{link}", "_blank");')

        context.browser.switch_to.window(context.browser.window_handles[-1])

        #validation
        if not all_filters_exist_on_item_page(context.browser, filters):
            mismatches.append((title, link))
        context.browser.close()
        context.browser.switch_to.window(current_window)

    if mismatches:
        print("The following items don't match the filters:")
        print(mismatches)
        raise RuntimeError


def get_element_text_and_sanitize(element):
    text = element.text.lower()
    return re.sub(r'\W+', '', text)


def all_filters_exist_on_item_page(browser, filters) -> bool:
    labels = [get_element_text_and_sanitize(e) for e in browser.find_elements_by_xpath("//div[@class = 'itemAttr']//td[@class = 'attrLabels']")]
    values = [e.text.lower() for e in browser.find_elements_by_xpath(
        "//div[@class = 'itemAttr']//td[@class = 'attrLabels']/following-sibling::td[.//text()][not(contains(@class, 'attrLabels'))]"
    )]

    # this dict has label text as a key, and value text as value
    per_item_specs = dict(zip(labels, values))

    for filter_name, filter_value in filters.items():
        if not (filter_value in per_item_specs[filter_name]):
            return False
    return True


def filters_to_dict(filter_rows):
    result = {}
    for row in filter_rows:
        filter_name = row['Filter'].lower()
        filter_value = row['value'].lower()
        result[filter_name] = filter_value
    return result


# def filter_matches(specs, filter_name, filter_value) -> bool:
#     for label, value in specs.items():
#         # print(f"Finding in {label.text}:{value.text}")
#         # if filter_name in label.text and filter_value.lower() in value.text.lower():
#         if filter_name == label and filter_value in value:
#             return True
#     print(f"could not find filter {filter_name}:{filter_value} in the specs")
#     return False


@step('test one page at "{link}"')
def test_one_item_page(context, link):
    context.browser.get(link)
    result = all_filters_exist_on_item_page(context.browser, filters_to_dict(context.table.rows))
    print(result)
    assert result


