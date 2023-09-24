from typing import Any, List

class LibObject:
    @staticmethod
    def get(array: List[Any], index: int, default_value: Any = None):
        return array[index] if len(array) > index else default_value

    @staticmethod
    def escape_str(data: str) -> str:
        """Escape special characters in a string."""
        return (
            data.replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace("\0", "\\0")
        )

    @staticmethod
    def set_escape(data):
        """Escape special characters in a string or dictionary."""
        if isinstance(data, str):
            return LibObject.escape_str(data)
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = LibObject.set_escape(v)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                data[i] = LibObject.set_escape(v)

        return data

    @staticmethod
    def cut_string_by_byte_utf16(input_text: str = "", cut_byte=0):
        """
        문자열의 UTF-16 표현식 바이트 수 계산
        (영문 1byte, 한글 2byte)
        (주문서 작성시 배송메시지 입력길이 제한하는 JS와 동일한 사양)
        :param input_text: 계산할 문자열
        :param cut_byte: 바이트 수
        :return:
        """
        total_bytes = 0
        max_index = len(input_text)
        converted_utf16_input = input_text.encode("utf-16")[2:]
        # 문자열 처리
        for i in range(0, len(converted_utf16_input), 2):
            value = converted_utf16_input[i : i + 2]
            value_decimal = int.from_bytes(value, byteorder="little")
            # UTF-16 기준 0x00 ~ 0xFF => 1byte, 0x0100 ~ 0xFFFF => 2byte
            if value_decimal < 256:
                total_bytes += 1
            else:
                total_bytes += 2
            # 요청한 절사 바이트 ($iCutByte) 보다 크면 마지막 문자 인덱스로 설정
            if total_bytes >= cut_byte:
                max_index = i // 2  # Because each character has 2 bytes
                break
        return input_text[:max_index]
