from selenium.webdriver.common.by import By

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver

    def get_zone_load(self, zone_id):
        selector = f"#zone-{zone_id} .load"
        elem = self.driver.find_element(By.CSS_SELECTOR, selector)
        return float(elem.text.strip())

    def get_zone_status(self, zone_id):
        selector = f"#zone-{zone_id} .status"
        elem = self.driver.find_element(By.CSS_SELECTOR, selector)
        return elem.text.strip(), elem.get_attribute("class")
