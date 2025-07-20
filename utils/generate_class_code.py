generate_class_code = lambda school_code, class_name, key="crax6ix" : f"{hex(int(school_code))[2:]}#{'-'.join(hex(ord(char) ^ ord(key[i % len(key)]))[2:] for i, char in enumerate(class_name))}"

reverse_class_code = lambda code, key="crax6ix": (str(int(code.split('#')[0], 16)), ''.join(chr(int(h, 16) ^ ord(key[i % len(key)])) for i, h in enumerate(code.split('#')[1].split('-'))))
