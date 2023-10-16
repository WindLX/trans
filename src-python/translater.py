from time import time
from typing import Any
from json import loads as json_loads
from base64 import urlsafe_b64decode

from config import *

from aiohttp import ClientSession
from pydantic import BaseModel
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class DetailedResult(BaseModel):
    part: list[str]
    form: list[str]
    more: list[str]

    def __str__(self) -> str:
        return f"""<ul>
        <li><strong>释义:</strong></li>
        <ul>
            {" ".join(f"<li>{item}</li>" for item in self.part)}
        </ul>
        <li><strong>形式:</strong></li>
        <ul>
            {" ".join(f"<li>{item}</li>" for item in self.form)}
        </ul>
        <li><strong>更多:</strong></li>
        <ul>
            {" ".join(f"<li>{item}</li>" for item in self.more)}
        </ul>
    </ul>"""

class TranslationResult(BaseModel):
    translation: str
    details: DetailedResult

    def __str__(self) -> str:
        return f"""
    <h3>结果</h3>
    <p>{self.translation}</p>
    <h3>细节</h3>
    {self.details}
    """


class YouDictTranslater:
    def __init__(self) -> None:
        self.headers: dict[str, str] = header
        self.url = url

    @property
    def data(self) -> dict[str, object]:
        mysticTime = str(int(time() * 1000))
        sign_raw = f"client=fanyideskweb&mysticTime={mysticTime}&product=webfanyi&key=fsdsogkndfokasodnaso"
        sign_hash = hashes.Hash(hashes.MD5())
        sign_hash.update(sign_raw.encode(encoding='utf-8'))
        sign = sign_hash.finalize().hex()
        data = data_template.copy()
        data["sign"] = sign
        data["mysticTime"] = mysticTime
        return data

    @staticmethod
    def __decrypt_data(t: str, o: str, n: str) -> str:
        o_hash = hashes.Hash(hashes.MD5())
        o_hash.update(o.encode('utf-8'))
        a = o_hash.finalize()

        n_hash = hashes.Hash(hashes.MD5())
        n_hash.update(n.encode('utf-8'))
        r = n_hash.finalize()

        cipher = Cipher(algorithms.AES128(a), modes.CBC(r))
        decryptor = cipher.decryptor()

        encrypted_data = urlsafe_b64decode(t.encode('utf-8'))
        decrypted_data = decryptor.update(
            encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES128.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode('utf-8')

    @staticmethod
    def __process_result(result: dict[str, Any]) -> TranslationResult:
        detailed_result = DetailedResult(part=[], form=[], more=[])

        if "dictResult" in result:
            if "ec" in result["dictResult"]:
                if "trs" in result["dictResult"]["ec"]["word"]:
                    for e in result["dictResult"]["ec"]["word"]["trs"]:
                        try:
                            detailed_result.part.append(
                                f"{e['pos']} {e['tran']}")
                        except KeyError:
                            detailed_result.part.append(
                                e.get(next(iter(e))))

                if "wfs" in result["dictResult"]["ec"]["word"]:
                    for e in result["dictResult"]["ec"]["word"]["wfs"]:
                        detailed_result.form.append(
                            f"{e['wf']['name']} {e['wf']['value']}")

            elif "ce" in result["dictResult"]:
                if "trs" in result["dictResult"]["ce"]["word"]:
                    for e in result["dictResult"]["ce"]["word"]["trs"]:
                        detailed_result.more.append(e["#text"])

        translation_result = TranslationResult(
            translation=result["translateResult"][0][0]["tgt"], details=detailed_result)

        return translation_result

    async def send_word(self, word: str) -> str:
        data = self.data.copy()
        data["i"] = word

        async with ClientSession() as session:
            async with session.post(url=self.url, headers=self.headers, data=data, cookies=cookies) as response:
                return await response.text()

    def decode_result(self, text: str) -> TranslationResult:
        result = self.__decrypt_data(text, O, N)
        return self.__process_result(json_loads(result))
