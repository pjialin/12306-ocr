import asyncio

from web import Web


def main():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(Web().run())
    loop.run_forever()


if __name__ == '__main__':
    main()
