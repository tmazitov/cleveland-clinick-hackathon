from .doctor import Doctor
from playwright.async_api import async_playwright

pt = None
browser = None

async def setup_scrapper():
    global pt, browser
    pt = await async_playwright().start()
    browser = await pt.chromium.launch(headless=True)

async def close_scrapper():
    global pt, browser
    await browser.close()
    await pt.stop()

async def get_doctors(symptomUUID: str) -> list[Doctor]:
    if not symptomUUID:
        return []

    page = await browser.new_page()
    await page.goto(f"https://www.clevelandclinicabudhabi.ae/en/find-a-doctor?bySymptoms={symptomUUID}")
    await page.wait_for_timeout(2000)

    doctors_elements = await page.query_selector_all(".DoctorSliderItem")
    if not doctors_elements:
        print("info : no doctors")
        return []

    doctors = []
    for elem in doctors_elements:
        if (
                await elem.query_selector(".ProfileButtonArea") is not None and
                await elem.query_selector(".DoctorImg") is not None and
                await elem.query_selector(".btn-general.btn-blue") is not None and
                await( await elem.query_selector(".btn-general.btn-blue")).get_attribute("style") is None
        ):
            doctor = Doctor({
                "name": await (await elem.query_selector(".DoctorName")).inner_text(),
                "role": await (await elem.query_selector(".DoctorRole")).inner_text(),
                "link": await (await elem.query_selector('a')).get_attribute('href'),
                "image": await (
                    await (await elem.query_selector(".DoctorImg")).query_selector('img')).get_attribute(
                    'data-src'),
            })
            doctors.append(doctor)
    return doctors