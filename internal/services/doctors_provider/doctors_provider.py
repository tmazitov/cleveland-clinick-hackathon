from .doctor import Doctor
from playwright.async_api import async_playwright

pt = None
browser = None

async def setup_scrapper():
    global pt, browser, context
    pt = await async_playwright().start()
    browser = await pt.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="Asia/Dubai",
        viewport={"width": 1366, "height": 900},
    )

    await context.route("**/*", lambda r: (
        r.abort() if r.request.resource_type in {"image", "font", "media"} else r.continue_()
    ))

async def close_scrapper():
    global pt, browser, context
    await browser.close()
    await pt.stop()

async def get_doctors(symptomUUID: str, retry: bool = False) -> list[Doctor]:
    if not symptomUUID:
        return []

    page = await context.new_page()

    try:
        response = await page.goto(f"https://www.clevelandclinicabudhabi.ae/en/find-a-doctor?bySymptoms={symptomUUID}", timeout=10000)
        if response.status >= 400:
            print(f"error: bad response status code {response.status}, retrying...")
            await page.close()
            if not retry:
                return await get_doctors(symptomUUID, retry=True)
            return []
        await page.wait_for_timeout(2000)
    except TimeoutError:
        print("error: timeout error, retrying...")
        await page.close()
        if not retry:
            return []
        return await get_doctors(symptomUUID, retry=True)
    except Exception as e:
        print("error: unknown error:", e)
        await page.close()
        if not retry:
            return []
        return await get_doctors(symptomUUID, retry=True)

    doctors_elements = await page.query_selector_all(".DoctorSliderItem")
    if not doctors_elements:
        print("info : no doctors")
        await page.close()
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
    await page.close()
    return doctors