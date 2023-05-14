import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

import unittest
from typing import List, Tuple, Dict
from simulator import Rotor, RotorConfig, Reflector, Plugboard, Enigma

CHARSET_SIZE = 26
ILLEGAL_LOCATION = 27

class TestRotor(unittest.TestCase):
    def test_at_notch(self):
        rotor = Rotor([ILLEGAL_LOCATION, 16], 0, 0, list(range(26)), list(range(26)))
        self.assertEqual(rotor.at_notch(), False)
        rotor.position = 16
        self.assertEqual(rotor.at_notch(), True)

    def test_turnover(self):
        rotor = Rotor([ILLEGAL_LOCATION, 16], 0, 0, list(range(26)), list(range(26)))
        rotor.turnover()
        self.assertEqual(rotor.position, 1)
        rotor.position = CHARSET_SIZE - 1
        rotor.turnover()
        self.assertEqual(rotor.position, 0)

    def test_forward(self):
        rotor = Rotor([ILLEGAL_LOCATION, 16], 0, 0, [4, 9, 3, 2, 13, 12, 11, 7, 0, 1, 5, 10, 17, 20, 19, 18, 25, 6, 24, 16, 14, 22, 23, 15, 8, 21], list(range(26)))
        self.assertEqual(rotor.forward(0), 4)
        self.assertEqual(rotor.forward(25), 21)

    def test_backward(self):
        rotor = Rotor([ILLEGAL_LOCATION, 16], 0, 0, list(range(26)), [4, 9, 3, 2, 13, 12, 11, 7, 0, 1, 5, 10, 17, 20, 19, 18, 25, 6, 24, 16, 14, 22, 23, 15, 8, 21])
        self.assertEqual(rotor.backward(4), 13)
        self.assertEqual(rotor.backward(21), 22)


class TestReflector(unittest.TestCase):
    def test_forward(self):
        reflector = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
        self.assertEqual(reflector.forward(0), 24)
        self.assertEqual(reflector.forward(25), 19)


class TestPlugboard(unittest.TestCase):
    def test_forward(self):
        plugboard = Plugboard.new_plugboard({'A': 'F', 'B': 'Q', 'C': 'Z'})
        self.assertEqual(plugboard.forward(0), 5)
        self.assertEqual(plugboard.forward(16), 1)


class TestEnigma(unittest.TestCase):
    def setUp(self):
        plugboard_settings = {
            'B': 'Q',
            'C': 'R',
            'D': 'I',
            'E': 'J',
            'K': 'W',
            'M': 'T',
            'O': 'S',
            'P': 'X',
            'U': 'Z',
            'G': 'H'
        }
        self.enigma = Enigma.new_enigma([7, 5, 3], [18, 10, 12], [1, 1, 5], plugboard_settings, 'B')

    def test_rotate(self):
        for i in range(5):
          self.enigma.rotate()
        self.assertEqual(self.enigma.left_rotor.position, 18)
        self.assertEqual(self.enigma.middle_rotor.position, 10)
        self.assertEqual(self.enigma.right_rotor.position, 17)

        for i in range(25):
          self.enigma.rotate()
        
        self.assertEqual(self.enigma.left_rotor.position, 18)
        self.assertEqual(self.enigma.middle_rotor.position, 11)
        self.assertEqual(self.enigma.right_rotor.position, 16)

    def test_encrypt(self):
        # Known good emulator output
        input = 'HELLOWORLDANDTHISISJUSTATESTHJDLSDHGUROSLJKSHDJKSBDJKBSJKDBSKJBFJKSBFJKSFGHJGHGJYKFYJFYKTFTFKYFTFIYU'
        expected = 'OJWAHLFOZNXGNBBWWJTSSWCSHSYLZMTENWAMIMUGRTFFJMYNTQCNSJAKTUYJRDSCCOHEXERXDIGVQWAPABBBNUQMDNFJXKKOXSQM'
        self.assertEqual(encrypt_text(input, self.enigma), expected)
    
    def test_decrypt(self):
        # Known good emulator output
        input = 'OJWAHLFOZNXGNBBWWJTSSWCSHSYLZMTENWAMIMUGRTFFJMYNTQCNSJAKTUYJRDSCCOHEXERXDIGVQWAPABBBNUQMDNFJXKKOXSQM'
        expected = 'HELLOWORLDANDTHISISJUSTATESTHJDLSDHGUROSLJKSHDJKSBDJKBSJKDBSKJBFJKSBFJKSFGHJGHGJYKFYJFYKTFTFKYFTFIYU'
        self.assertEqual(encrypt_text(input, self.enigma), expected)

def encrypt_text(text, enigma):
    ans = []
    for c in text:
        ans.append(enigma.encrypt(c))
    return ''.join(ans)
