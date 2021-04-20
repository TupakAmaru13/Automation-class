from behave import then, when


@when('Navigate to Amazon')
def open_amazon_link(context):
    context.browser.get('https://www.amazon.com/b/ref=s9_acss_bw_cg_SP21L0D6_4a1_w?ie=UTF8&node=9538491011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-10&pf_rd_r=4Q0MCJ2R8XW2NVAMXBWK&pf_rd_t=101&pf_rd_p=f2050b75-d118-4437-ae42-d65eb3c068d8&pf_rd_i=7141123011&nocache=1618171138803/')


@then('Check all "{super_category}" deal buttons')
def check_super_category(context, super_category):
    deal_list = []

    # collect the labels for the buttons to test
    for a in context.browser.find_elements_by_xpath(f'//div[div/div/img[contains(@alt, "{super_category}")]]/following-sibling::div/div/div/a'):
        category = a.get_attribute("aria-label")
        deal_list.append(category)
    print(f"For {super_category} will check the following categories: {deal_list}")

    # iterate over the list of labels, find each button, click on it, test the page it leads to
    for category in deal_list:
        a = context.browser.find_element_by_xpath(f'//div[div/div/img[contains(@alt, "{super_category}")]]/following-sibling::div/div/div/a[@aria-label = "{category}"]')
        a.click()
        # on category page
        assert_category_is_present(context, super_category, category)
        click_back(context)


def click_back(context):
    context.browser.execute_script("window.history.go(-1)")


def assert_category_is_present(context, super_category, category):
    search_element = context.browser.find_element_by_xpath(f"//div[@id = 'departments']//ul/li/span[@class = 'a-list-item'][not (a)]")
    department_name = search_element.text.lower()
    if not (category.lower() in department_name and super_category.lower() in department_name):
        raise RuntimeError(f"Can't find {super_category} {category}")
