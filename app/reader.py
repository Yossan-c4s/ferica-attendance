import binascii
from smartcard.System import readers

class FelicaReader:
    def __init__(self):
        self.reader = readers()[0]

    def polling_card(self):
        try:
            connection = self.reader.createConnection()
            connection.connect()
            # カードID取得コマンド例（RC-S380/Felica Lite用）:
            # 実際はpyscardのコマンドを適宜調整
            idm = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])[0:8]
            card_id = binascii.hexlify(bytearray(idm)).decode().upper()
            return card_id
        except Exception:
            return None