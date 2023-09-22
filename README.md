![Logo](Nice.png)

# NiceFlor Encoder
A Python code that once provided with the right information, generates a Hexadecimal String that allows you to retransmit via a Transceiver.


## Installation

Install by cloning project or downloading source code

```bash
  git clone https://github.com/Jev1337/NiceFlor-Encoder.git
```


    
## Usage/Examples

Modify the following lines and make sure you change them with the desired codes (In Hexadecimal):

```python
send(0x00000000, 1, 1)
```

To generate new codes, you increase the code count, for example:

```python
send(0x00000000, 1, 2)
                    ^
```
To use another button, you increase the button count, for example:
```python
send(0x00000000, 2, 1)
                 ^
```
Output Example:
```
> send(0x00E48DCA, 1, 3)
encbuff:  0x1 , 0xf7 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe088e22acc582
encbuff:  0x1 , 0xc7 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe388e22acc582
encbuff:  0x1 , 0xd7 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe288e22acc582
encbuff:  0x1 , 0xa7 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe588e22acc582
encbuff:  0x1 , 0xb7 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe488e22acc582
encbuff:  0x1 , 0x87 , 0x71 , 0xdd , 0x53 , 0x3a , 0x7d
TX Code:  0xe788e22acc582
```

## FAQ

#### What does this do and why?

This allows you to clone your remote using cheap RF433 modules with an Arduino or Raspberry Pi. This allows you to make home automations for example.

#### Is this illegal?

Cloning a remote is illegal in some countries, as capturing signals itself is illegal. So use at your own risk, this is only for educational purposes.


## Optimizations

There are no optimizations that I see that should be done, there are functions that could be deleted as they are there to let you know how things work.


## Used By

This is tested on:
- Nice FLO2 R-S (Also known as: Nice FLOR-S, Nice FLOR-S2)

## Credits

[Kaiju](https://rolling.pandwarf.com/): This helped me with confirming that the code works perfectly.

[rtl_433](https://github.com/merbanan/rtl_433/): This helped me with the python code, as it was not originaly mine. I modified it in a way it displays the encbuff which we use to transmit using RF433_Send library on Arduino

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

