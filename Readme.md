## Enigma Simulator

### Setting up a machine

```
python3 cli.py config \
    --name my_machine \
    --rotors 8,6,4 \
    --rotor_init 18,10,12 \
    --rotor_setting 1,1,5 \
    --plugboard_pins BQ,CR,DI,EJ,KW,MT,OS,PX,UZ,GH \
    --reflector_letter B
```

### Running encryption/decryption with a machine

```
python3 cli.py run \
    --name my_machine \
    --text HELLO
```
