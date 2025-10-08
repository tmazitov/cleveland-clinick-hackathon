from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser
from .doctor import Doctor

def wait_update(page):
    page.wait_for_timeout(1500)  # Ждём 2 секунды чтобы контент точно прогрузился

class DoctorsProvider:
    
    browser: Browser

    def __init__(self):
        self.pl = sync_playwright().start()
        self.browser = self.pl.chromium.launch(headless=True)

    def get_doctors(self, symptomUUID: str) -> list[Doctor]:
        if not symptomUUID or len(symptomUUID) == 0:
            return []

        page = self.browser.new_page()
        page.goto(f"https://www.clevelandclinicabudhabi.ae/en/find-a-doctor?bySymptoms={symptomUUID}")
        wait_update(page)

        doctors_elements = page.query_selector_all(".DoctorSliderItem")
        if not doctors_elements or len(doctors_elements) == 0:
            return []
        
        return [
            Doctor({
                "name" : elem.query_selector(".DoctorName").inner_text(),
                "role" : elem.query_selector(".DoctorRole").inner_text(),
                "link" : elem.query_selector('a').get_attribute('href'),
                "image" : elem.query_selector(".DoctorImg").query_selector('img').get_attribute('data-src'),
                # "image" : print("image", elem.query_selector(".DoctorImg").inner_html()),
            })
            for elem in doctors_elements 
            if elem.query_selector(".ProfileButtonArea") != None
                and elem.query_selector(".DoctorImg") != None
                and elem.query_selector(".btn-general.btn-blue") != None
                and elem.query_selector(".btn-general.btn-blue").get_attribute("style") == None
        ]

    def close(self) -> None:
        self.browser.close()
        self.pl.stop()
