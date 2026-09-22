import asyncio

import pygame

pygame.init()  # Kors forst av allt, innan nagot annat projektimport, eftersom
                # pygbags WASM-bygge av pygame inte har alla attribut (t.ex.
                # .event/.init sjalv) tillgangliga forran har.

from menu import menu


async def main():
    await menu()


asyncio.run(main())
