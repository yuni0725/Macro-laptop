import tracemalloc
import asyncio

tracemalloc.start()

from playwright.async_api import async_playwright

from playwright_version import run_apply_script


async def main():
    async with async_playwright() as p:
        print(await run_apply_script("31203", "0725", 10, True))
        print(await run_apply_script("30104", "1124", 9, True))


if __name__ == "__main__":
    asyncio.run(main())
