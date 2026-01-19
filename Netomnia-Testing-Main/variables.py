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

# SUPPORTED CODES
CLOSURE_CODES = {"TST003", "CBT003", "CBT004", "CBT001","H&D147", "MBR001", "JNT001", "JNT004", "TST002"}
BLOCKAGE_CODES = {"H&D125", "H&D126"}

# LOGIN PAGE
LOGIN_BUTTON = "//button[@class='bp5-button bp5-intent-primary bp5-large']"

# PROJECT MODULE
PROJECT_LINK_XPATH = "//a[@href='/ProjectModule/Map']//button[@type='button']"

# LAYER BUILD
HAMBURGER_BUTTON = "//button[contains(@class,'floatingSidebarButtonNoTabs')]"
LAYERS_TAB = "//button[contains(., 'Layers')]"
BUILD_LAYER_LABEL = "//label[normalize-space()='Build']"

# FEATURE SECTION
FEATURES_TAB = "//button[contains(., 'Features')]"
FEATURE_ID_INPUT = "//input[@placeholder='Feature ID']"

# FEATURE ID INVALID
FEATURE_ID_INVALID = "//span[contains(text(),'no data found, verify that the feature and id exis')]"

# CLEAR SEARCH BUTTON
CLEAR_SEARCH_BUTTON = "//button[contains(., 'Clear Search')]"

# DROPDOWN
ABS_XPATH = "/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/main[1]/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]/input[1]"

# CATEGORIES
CLOSURE_OPTION = "//div[@class='ant-select-item-option-content' and normalize-space()='closure']"
BLOCKAGE_OPTION = "//div[@class='ant-select-item-option-content'][normalize-space()='blockage']"

# EYE ICON
EYE_BUTTON = "//span[@aria-label='eye' or @aria-describedby]"

# BUILD STATUS
BUILD_STATUS = "//span[normalize-space()='Build Status']/ancestor::tr/td//span"

# SIEBEL REFERENCE & WHEREABOUTS
SHOW_MORE_BTN = "//div[@id='bp5-tab-panel_undefined_RecordDetails']//span[@class='bp5-button-text'][normalize-space()='Show More']"
SIEBEL_REF_VALUE = "//th[.//span[normalize-space()='Siebel Reference']]/following-sibling::td//span[normalize-space()]"
WHEREABOUTS_VALUE = "//th[.//span[normalize-space()='Whereabouts']]/following-sibling::td//span[normalize-space()]"

# POWER METER BLOCK
POWER_BLOCK = "//*[contains(normalize-space(.),'POWER_METER')]/ancestor::div[contains(@class,'ant-collapse-item')]"
POWER_HEADER = ".//div[contains(@class,'ant-collapse-header')]"
POWER_IMAGES = ".//div[contains(@class,'ant-collapse-content-active')]//img"

# CLOSURE MEDIA DOWNLOAD
SHOW_MORE_DROP = "//button[.//span[normalize-space()='Show more']]"
CARDS_PATH = "//div[contains(@class,'filePreviewCard')]"
IMAGE_PATH = ".//img[contains(@class,'ant-image-img')]"
DOC_PATH = ".//button[contains(@class,'ant-dropdown-trigger')]"
LINKS_XPATH = (
    "//div[contains(@class,'ant-dropdown') and not(contains(@style,'display: none'))]"
    "//a[contains(@href,'http')]"
)

# OTDR BLOCK
OTDR_BLOCK_PATH = (
    "//*[contains(@class,'ant-collapse-item')]"
    "[.//span[contains(normalize-space(),'File (OTDR)')]]"
)

OTDR_HEADER = ".//div[contains(@class,'ant-collapse-header')]"

PDF_CARDS = (
    ".//div[contains(@class,'filePreviewCard')]"
    "[.//i[contains(@class,'bi-filetype-pdf')]]"
)