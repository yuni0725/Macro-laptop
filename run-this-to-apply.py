import tracemalloc
import asyncio

tracemalloc.start()

from playwright.async_api import async_playwright

from playwright_version import run_apply_script


async def main():
    async with async_playwright() as p:
        # print(await run_apply_script("31203", "0725", 9, False))
        await run_apply_script("30104", "1124", 10, False)


if __name__ == "__main__":
    asyncio.run(main())
