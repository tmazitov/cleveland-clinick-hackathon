from playwright.sync_api import sync_playwright
import json


# https://www.clevelandclinicabudhabi.ae/en/forms/request-appointment-callback

def wait_update(page):
    page.wait_for_timeout(1500)  # Ждём 2 секунды чтобы контент точно прогрузился

def extract_A_Z(page):
    sorting_area = page.query_selector(".SortingArea, .sorting-area, .sort-area")
    if not sorting_area:
        raise Exception("No element with class 'SortingArea' found")
    
    links = sorting_area.query_selector_all("a")
    return links

# def extract_doctors(browser, symptomUUID):
#     if not symptomUUID or len(symptomUUID) == 0:
#         return []

#     page = browser.new_page()
#     page.goto(f"https://www.clevelandclinicabudhabi.ae/en/find-a-doctor?bySymptoms={symptomUUID}")
#     wait_update(page)

#     doctors_elements = page.query_selector_all(".DoctorSliderItem")
#     if not doctors_elements or len(doctors_elements) == 0:
#         return []
    
#     return [
#         {
#             "name" : elem.query_selector(".DoctorName").inner_text(),
#             "role" : elem.query_selector(".DoctorRole").inner_text(),
#             "image" : f"www.clevelandclinicabudhabi.ae/${elem.query_selector('img').get_attribute('src')}",
#         }
#         for elem in doctors_elements
#     ]

def extract_symptoms(browser, page):
    slick_track = page.query_selector(".DoctorSymptomsSlider")
    if not slick_track:
        raise Exception("No element with class 'DoctorSymptomsSlider' found")
    
    links = slick_track.query_selector_all("a")
    return [
        {
            "name": link.inner_text(),
            "value": link.get_attribute("data-value"),
        }
        for link in links
    ]

    # filtered_links = []
    # for link in links_values:
    #     doctors = extract_doctors(browser, link["value"])
    #     if not doctors or len(doctors) == 0:
    #         continue
    #     link["doctors"] = doctors
    #     filtered_links.append(link)

    # return filtered_links 

def save_symptoms_to_file(symptoms, filename="symptoms.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(symptoms, file, ensure_ascii=False, indent=4)

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False чтобы видеть браузер
        page = browser.new_page()
        page.goto("https://www.clevelandclinicabudhabi.ae/en/find-a-doctor")
        wait_update(page)

        print("info : connected to the main page")
        print("info : scrapper starts")

        symtoms_button = page.query_selector(f'[data-key="Symptoms"]')
        if not symtoms_button:
            raise Exception("No 'symptoms button'")

        symtoms_button.click()
        wait_update(page)
    

        links:list = extract_A_Z(page)
        if not links or len(links) == 0:
            raise Exception("No links found in SortingArea")
        
        symptoms = []
        letters = [chr(i) for i in range(65, 88)]  # List of capital letters (A-W)

        for letter in letters:
            links:list = extract_A_Z(page)
            if not links or len(links) == 0:
                raise Exception("No links found in SortingArea")
            print("info : found links: ", len(links))
            link = next((l for l in links if l.inner_text() == letter), None)
            if not link:
                print(f"info : no link for letter '{letter}'")
                continue
            
            link.click()
            print(f"info : waiting for page update for letter '{letter}'")
            wait_update(page)

            symptom_links = extract_symptoms(browser, page)
            if not symptom_links or len(symptom_links) == 0:
                continue

            text = link.inner_text()
            print(f"info : {text}: extracted {len(symptom_links)} symptoms:")
            print(f"info : symptoms collected {len(symptoms)}")

            symptoms.extend(symptom_links)

        save_symptoms_to_file(symptoms)

        browser.close()

if __name__ == "__main__":
    scrape()
