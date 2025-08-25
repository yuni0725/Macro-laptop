from playwright.async_api import async_playwright
from datetime import datetime, date
from urllib.parse import urljoin
import asyncio

URL = "http://mysangsan.cafe24.com/dms/regi/login.php"

# Setting time
today = date.today()
login_time = datetime(today.year, today.month, today.day, 6, 28, 30)  # 6시 28분 30초
submit_time = datetime(today.year, today.month, today.day, 6, 29, 0)  # 6시 29분


async def login(page, student_id, password):
    # ID
    # Use locator to be more specific about which text input to fill
    await page.locator('input[type="text"]').first.fill(student_id)

    # Password
    await page.locator('input[type="password"]').first.fill(password)

    # Security code
    codes = await page.query_selector_all("b")
    code_list = [await code.inner_text() for code in codes]
    code = "".join(code_list[2:])

    # The security code is the second text input on the page
    security_code_input = page.locator('input[type="text"]').nth(1)
    await security_code_input.fill(code)

    await security_code_input.press("Enter")
    print("Login Succeeded!")


async def agree(page):
    await page.click("#agr1_y")
    await page.click("#agr2_y")
    await page.click('input[type="button"][value="확인"]')
    await page.wait_for_load_state("networkidle")
    print("Agree Succeeded!")


async def apply_access(page):
    # Navigate to the apply page directly using the link
    apply_link = await page.query_selector(
        "body > table:nth-child(3) > tbody > tr > td > table > tbody > tr > td > ul > li:nth-child(4) > ul > li:nth-child(3) > a"
    )
    if apply_link:
        href = await apply_link.get_attribute("href")
        absolute_url = urljoin(page.url, href)
        await page.goto(absolute_url)
        print("Apply Access Succeeded!")
    else:
        print("Could not find the apply link.")


async def apply(page, laptop_number):
    await page.reload()
    if laptop_number < 10:
        await page.select_option(
            'select[name="sel_roomseq"]', value=f"0{laptop_number}"
        )
    else:
        await page.select_option('select[name="sel_roomseq"]', value=f"{laptop_number}")
    await page.fill('textarea[name="sel_content"]', ".")

    # A Future is like a placeholder for a result that will arrive later.
    dialog_future = asyncio.get_running_loop().create_future()

    # Set up the event listener for the dialog *before* clicking the button.
    async def handle_dialog(dialog):
        message = dialog.message
        print(f"Dialog message: {message}")
        await dialog.accept()

        # Check if the future is already resolved to avoid errors.
        if dialog_future.done():
            return

        # Any dialog means failure, so we set the message as the result.
        dialog_future.set_result(message)

    page.once("dialog", handle_dialog)

    # The click must happen AFTER the listener is set up.
    await page.click('input[type="button"][value="저장"]')

    # Now, wait for the handle_dialog function to fill our placeholder.
    # I've added a 5-second timeout. If no dialog appears, it's a success.
    try:
        # Wait for a dialog to appear.
        failure_message = await asyncio.wait_for(dialog_future, timeout=5)
        print(f"Dialog appeared with message: {failure_message}")

        if "이미" in failure_message:
            return {
                "status": "error",
                "message": f"{laptop_number} is already taken by someone else",
            }  # A dialog appeared, so, it's success.
        else:
            return {
                "status": "error",
                "message": failure_message,
            }  # A dialog appeared, so it's a failure.

    except asyncio.TimeoutError:
        print("No dialog appeared within 5 seconds, assuming success.")
        return {"status": "success"}  # No dialog appeared, so it's a success.


async def run_apply_script(student_id, password, laptop_number, headless=False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        await page.goto(URL)

        await page.wait_for_load_state("networkidle")
        # Login
        await login(page, student_id, password)

        # Wait for the page to fully load after the first login
        await page.wait_for_load_state("networkidle")

        # The user confirmed a second login is required to proceed.
        print("Performing second login as required...")
        await login(page, student_id, password)
        await page.wait_for_load_state("networkidle")

        # --- DEBUGGING STEP ---
        print(f"Current URL after login attempts: {page.url}")
        # --- END DEBUGGING STEP ---

        await agree(page)

        await apply_access(page)

        try:
            # Check for a specific element that indicates the application is not yet open
            await page.wait_for_selector(
                "body > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > b > font",
                timeout=1000,
            )
            return {"status": "error", "message": "page not open"}
        except:
            # If the element is not found, it means the application is open
            applied = await apply(page, laptop_number)
            if applied.get("status") == "success":
                return {"status": "success", "message": "applied"}
            else:
                return applied
