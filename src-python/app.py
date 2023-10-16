from asyncio import run, sleep
from translater import YouDictTranslater


async def main():
    ts = YouDictTranslater()
    while True:
        text = input()
        if not text:
            continue
        text = text.strip()
        if text == "EXIT":
            break
        else:
            while True:
                try:
                    result = await ts.send_word(text)
                    r = ts.decode_result(result)
                    print(r)
                    break
                except ValueError as e:
                    print(e)
                    await sleep(1)
                    continue

if __name__ == "__main__":
    run(main())
