from selenium.webdriver.common.by import By


def smart_find_element(driver, keywords, tag="*"):
    xpath_conditions = []
    for key in keywords:
        x = key.lower()
        xpath_conditions.append(
            f"contains(translate(.//text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{x}')"
        )
        xpath_conditions.append(
            f"contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{x}')"
        )
        xpath_conditions.append(
            f"contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{x}')"
        )
        xpath_conditions.append(
            f"contains(translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{x}')"
        )
        xpath_conditions.append(
            f"contains(translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{x}')"
        )

    xpath = f"//{tag}[{' or '.join(xpath_conditions)}]"

    try:
        return driver.find_element(By.XPATH, xpath)
    except:
        return None


# LOGIN PAGE
LOGIN_BUTTON = "//button[@class='bp5-button bp5-intent-primary bp5-large']"

# PROJECT MODULE
PROJECT_LINK_XPATH = "//a[@href='/ProjectModule/Map']//button[@type='button']"

# LAYER BUILD
HAMBURGER_BUTTON = "//button[contains(@class,'floatingSidebarButtonNoTabs')]"
LAYERS_TAB = "//button[contains(., 'Layers')]"
BUILD_LAYER_LABEL = "//label[normalize-space()='Build']"

# POWER METER BLOCK
POWER_BLOCK = "//*[contains(normalize-space(.),'POWER_METER')]/ancestor::div[contains(@class,'ant-collapse-item')]"
POWER_HEADER = ".//div[contains(@class,'ant-collapse-header')]"
POWER_IMAGES = ".//div[contains(@class,'ant-collapse-content-active')]//img"

# FEATURE SECTION
FEATURES_TAB = "//button[contains(., 'Features')]"
FEATURE_ID_INPUT = "//input[@placeholder='Feature ID']"
FEATURE_SEARCH = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/main[1]/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/span[1]/span[1]/span[1]/button[1]/span[1]/span[1]/*[name()='svg'][1]"

# DROPDOWN
DROPDOWN_INPUT = "//div[contains(@class,'ant-select-selector')]"
INDEX_XPATH = "(//div[@class='ant-select ant-select-outlined css-kbg4zp ant-select-single ant-select-show-arrow'])[2]"
ABS_XPATH = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/main[1]/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]/input[1]"
FEATURE_TYPE_DROPDOWN = "//div[contains(@class,'ant-select-selector')]"
FEATURES_PANEL = "//div[contains(@class,'ant-drawer-body')]"


# CATEGORIES
CLOSURE_OPTION = "//div[@class='ant-select-item-option-content' and normalize-space()='closure']"
BLOCKAGE_OPTION = "//div[@class='ant-select-item-option-content'][normalize-space()='blockage']"

# SIEBEL REFERENCE & WHEREABOUTS
SHOW_MORE_BTN = "//div[@id='bp5-tab-panel_undefined_RecordDetails']//span[@class='bp5-button-text'][normalize-space()='Show More']"
SIEBEL_REF_VALUE = "//th[.//span[normalize-space()='Siebel Reference']]/following-sibling::td//span[normalize-space()]"
WHEREABOUTS_VALUE = "//th[.//span[normalize-space()='Whereabouts']]/following-sibling::td//span[normalize-space()]"

# EYE ICON
EYE_BUTTON = "//span[@aria-label='eye' or @aria-describedby]"

# BUILD STATUS
BUILD_STATUS = "//span[normalize-space()='Build Status']/ancestor::tr/td//span"

# MEDIA CARDS
CARDS_PATH = ".//div[contains(@class,'filePreviewCard')]"

# DOCUMENT MENU
DOC_PATH = ".//button[contains(@class,'ant-dropdown-trigger')]"

# DOWNLOAD LINK
DOWNLOAD_PATH = "//li[contains(@class,'ant-dropdown-menu-item')]//a[@download]"
SELECT_DROPDOWN_SELECTOR = (
    "//span[contains(@class,'ant-select-selection-item')]"
)

# FEATURE ID INVALID

FEATURE_ID_INVALID = "//span[contains(text(),'no data found, verify that the feature and id exis')]"

ANT_SELECT_CONTAINER = "//div[contains(@class,'ant-select-container')]"