import asyncio
from playwright.async_api import async_playwright

async def scrape_quotes():
    total = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()

        for seed in range(28, 38):
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            await page.goto(url)
            await page.wait_for_selector("#table")
            cells = await page.query_selector_all("#table td")

            for cell in cells:
                try:
                    text = await cell.inner_text()
                    total += int(text.strip())
                except ValueError:
                    continue  # skip non-integer cells

        await browser.close()
    return total

if __name__ == "__main__":
    total_sum = asyncio.run(scrape_quotes())
    print(f"Total sum of all numbers: {total_sum}")
