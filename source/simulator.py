from typing import NamedTuple, Tuple, Dict

CHARSET_SIZE = 26
ILLEGAL_LOCATION = 27


class RotorConfig(NamedTuple):
    encoding: str
    notches: Tuple[int, int]


# Known configurations for the real enigma rotors
ROTOR_CONFIGS = [
    # First five rotors have one one notch
    RotorConfig(encoding='EKMFLGDQVZNTOWYHXUSPAIBRCJ', notches=(ILLEGAL_LOCATION, 16)),
    RotorConfig(encoding='AJDKSIRUXBLHWTMCQGZNPYFVOE', notches=(ILLEGAL_LOCATION, 4)),
    RotorConfig(encoding='BDFHJLCPRTXVZNYEIWGAKMUSQO', notches=(ILLEGAL_LOCATION, 21)),
    RotorConfig(encoding='ESOVPZJAYQUIRHXLNFTGKDCMWB', notches=(ILLEGAL_LOCATION, 9)),
    RotorConfig(encoding='VZBRGITYUPSDNHLXAWMJQOFECK', notches=(ILLEGAL_LOCATION, 25)),

    # Last three have two notches that adds some more randomness
    RotorConfig(encoding='JPGVOUMFYQBENHZRDKASXLICTW', notches=(12, 25)),
    RotorConfig(encoding='NZJHGRCXMYSWBOUFAIVLPEKQDT', notches=(12, 25)),
    RotorConfig(encoding='FKQHTLXOCBJSPDZRAMEWNIUYGV', notches=(12, 25)),
]


class Rotor:
    def __init__(self,
                 notches: list[int],
                 position: int,
                 setting: int,
                 forward_mapping: list[int],
                 reverse_mapping: list[int]):
        self.notches = notches
        self.position = position
        self.setting = setting
        self.forward_mapping = forward_mapping
        self.reverse_mapping = reverse_mapping

    def at_notch(self) -> bool:
        return self.notches[0] == self.position or self.notches[1] == self.position

    def turnover(self):
        self.position = (self.position + 1) % CHARSET_SIZE

    def forward(self, num: int) -> int:
        shift_add = 26 + self.position - self.setting
        shift_sub = 26 - self.position + self.setting

        x = (num + shift_add) % 26
        return (self.forward_mapping[x] + shift_sub) % 26

    def backward(self, num: int) -> int:
        shift_add = 26 + self.position - self.setting
        shift_sub = 26 - self.position + self.setting

        x = (num + shift_add) % 26
        return (self.reverse_mapping[x] + shift_sub) % 26

    @classmethod
    def rotor_by_index(cls, idx: int, position: int, setting: int) -> "Rotor":
        rotor_config = ROTOR_CONFIGS[idx]
        enc_u8 = [ord(c) - 65 for c in rotor_config.encoding]
        
        rev_enc_u8 = [0 for i in range(26)]
        for i in range(26):
            rev_enc_u8[ord(rotor_config.encoding[i]) - 65] = i

        return cls(rotor_config.notches, position, setting, enc_u8, rev_enc_u8)


class Reflector:
    def __init__(self, reflector_mapping_arr: list[int]):
        self.reflector_mapping_arr = reflector_mapping_arr

    def forward(self, num: int) -> int:
        return self.reflector_mapping_arr[num]

    @classmethod
    def reflection_from_letterid(cls, letterid: str) -> "Reflector":
        if letterid == "B":
            return cls([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
        elif letterid == "C":
            return cls([5, 21, 15, 9, 8, 0, 14, 24, 4, 3, 17, 25, 23, 22, 7, 1, 18, 11, 13, 6, 12, 20, 10, 19, 16, 2])
        else:
            return cls(list(range(26)))


class Plugboard:
    def __init__(self, plugboard_mappings: list[int]):
        self.plugboard_mappings = plugboard_mappings

    def forward(self, num: int) -> int:
        return self.plugboard_mappings[num]

    @classmethod
    def new_plugboard(cls, letter_mapping: Dict[str, str]) -> "Plugboard":
        mappings = [i for i in range(26)]

        for key, value in letter_mapping.items():
            mappings[ord(key) - 65] = ord(value) - 65
            mappings[ord(value) - 65] = ord(key) - 65

        return cls(mappings)


class Enigma:
    def __init__(self,
                 plugboard: Plugboard,
                 left_rotor: Rotor,
                 middle_rotor: Rotor,
                 right_rotor: Rotor,
                 reflector: Reflector):
        self.plugboard = plugboard
        self.left_rotor = left_rotor
        self.middle_rotor = middle_rotor
        self.right_rotor = right_rotor
        self.reflector = reflector

    def rotate(self):
        if self.middle_rotor.at_notch():
            self.middle_rotor.turnover()
            self.left_rotor.turnover()

        if self.right_rotor.at_notch():
            self.middle_rotor.turnover()

        self.right_rotor.turnover()

    def encrypt(self, c: str) -> str:
        num = ord(c) - 65

        self.rotate()

        num = self.plugboard.forward(num)

        num = self.right_rotor.forward(num)
        num = self.middle_rotor.forward(num)
        num = self.left_rotor.forward(num)

        num = self.reflector.forward(num)

        num = self.left_rotor.backward(num)
        num = self.middle_rotor.backward(num)
        num = self.right_rotor.backward(num)

        num = self.plugboard.forward(num)

        return chr(num + 65)
    
    @classmethod
    def new_enigma(cls,
                   rotor_indexes: list[int],
                   rotor_positions: list[int],
                   rotor_settings: list[int],
                   plugboard_mappings: Dict[str, str],
                   reflector_letterid: str) -> "Enigma":
        return cls(Plugboard.new_plugboard(plugboard_mappings),
            Rotor.rotor_by_index(rotor_indexes[0], rotor_positions[0], rotor_settings[0]),
            Rotor.rotor_by_index(rotor_indexes[1], rotor_positions[1], rotor_settings[1]),
            Rotor.rotor_by_index(rotor_indexes[2], rotor_positions[2], rotor_settings[2]),
            Reflector.reflection_from_letterid(reflector_letterid))
