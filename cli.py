import json
import argparse

from source.simulator import *


def encrypt_text(text, enigma):
    ans = []
    for c in text:
        ans.append(enigma.encrypt(c))
    return ''.join(ans)


def config(args):
    name = args.name
    assert name is not None

    rotors = [int(x) - 1 for x in args.rotors.split(',')]
    assert len(rotors) == 3

    rotor_init = [int(x) for x in args.rotor_init.split(',')]
    assert len(rotor_init) == 3

    rotor_setting = [int(x) for x in args.rotor_setting.split(',')]
    assert len(rotor_setting) == 3

    reflector_letter = args.reflector_letter
    assert len(reflector_letter) == 1

    plugboard_settings = [x for x in args.plugboard_pins.split(',')]
    plugboard_settings = { x[0]: x[1] for x in plugboard_settings }

    setting = {
        'rotors': rotors,
        'rotor_init': rotor_init,
        'rotor_setting': rotor_setting,
        'reflector_letter': reflector_letter,
        'plugboard_settings': plugboard_settings
    }

    with open(f'/tmp/enigma_{name}', 'w') as f:
        f.write(json.dumps(setting))


def run(args):
    name = args.name
    assert name is not None

    with open(f'/tmp/enigma_{name}', 'r') as f:
        val = json.loads(f.read())
        enigma = Enigma.new_enigma(val['rotors'],
                                   val['rotor_init'],
                                   val['rotor_setting'],
                                   val['plugboard_settings'],
                                   val['reflector_letter'])

    print (encrypt_text(args.text, enigma))


def cli():
    parser = argparse.ArgumentParser(prog="enigma")
    parser.add_argument('program', help='Program can either be config to build the machine config or run to run the machine')
    parser.add_argument('--name', help='Name of the machine. Used to store the config')

    # config options
    parser.add_argument('--rotors', help='Comma separated numbers for rotors like 1,2,3. 1 based.')
    parser.add_argument('--rotor_init', help='Comma separated numbers for rotor initial positions. 1 based.')
    parser.add_argument('--rotor_setting', help='Comma separated numbers for rotor ring settings. 1 based.')
    parser.add_argument('--reflector_letter', help='The letter indicating the reflector (B or C)')
    parser.add_argument('--plugboard_pins', help='Comma separated pairs of letters like AK, XP')

    # run options
    parser.add_argument('--text', help='Text to encrypt or decrypt')

    args = parser.parse_args()

    if args.program == 'config':
        config(args)
    else:
        run(args)


if __name__ == '__main__':
    cli()
