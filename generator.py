import re
import sys
import time

from random import choice, randint

import colorama
colorama.initialise.init(autoreset=True)

# minecraft format (§)
colors = {
    "§0": "\x1b[30m",
    "§1": "\x1b[34m",
    "§2": "\x1b[32m",
    "§3": "\x1b[36m",
    "§4": "\x1b[31m",
    "§5": "\x1b[35m",
    "§6": "\x1b[33m",
    "§7": "\x1b[37m",
    "§8": "\x1b[90m",
    "§9": "\x1b[94m",
    "§a": "\x1b[92m",
    "§b": "\x1b[96m",
    "§c": "\x1b[91m",
    "§d": "\x1b[95m",
    "§e": "\x1b[93m",
    "§f": "\x1b[97m",
    "§r": "\x1b[0m",
}

rep = dict((re.escape(k), v) for k, v in colors.items())
pattern = re.compile("|".join(rep.keys()))

themes = {
    "candy": "fe6cd",
    "smootherRainbow": "c6ea395",
    "brightRainbow": "c6ea9b5",
    "chrome": "f787",
    "tropical": "c6b3b6c",
    "patroitic": "cf9fc",
    "random": "".join([choice(list(colors.keys())) for _ in range(randint(1, 16))]).replace("§", ""),
}

THEME = "smootherRainbow"

class Generator:
    def __init__(self, text: str = "", shifting: int = 0):
        self.color_format = themes.get(THEME)
        assert self.color_format, "Invalid color format"
        
        self.text = text
        self.shifting = shifting
        
        self.index = 0 + (self.shifting % len(self.color_format))
        self.text_size = len(self.text)
        
        self._color = self.color_format[self.index % len(self.color_format)]
    
    def write_info(self):
        print(f"""
Generator
---------
text: {self.text}
color_format: {self.color_format} :: ({len(self.color_format)})
shifting: {self.shifting}
---------""")
    
    @property
    def color(self):
        c = self._color
        
        if self.index + 1 < self.text_size:
            self.index += 1
            self._color = self.color_format[self.index % len(self.color_format)]
        else:
            self.index = 0
            self._color = self.color_format[self.index % len(self.color_format)]
            
        return c
    
    def _generate_text(self):
        text = ""
        for i in self.text:
            text += f"§{self.color}{i}"
        
        return text
    
    def generate(self):
        return self._generate_text()
    

class AnimatedGenerator(Generator):
    def __init__(self, text: str = "", shifting: int = 0):
        super().__init__(text, shifting)
    
    def generate(self):
        texts = []
        for _ in range(self.text_size):
            texts.append(self._generate_text())
            self.shifting += 1
            self.index = 0 + (self.shifting % len(self.color_format))
        
        return texts

class ViewOnTerminal(AnimatedGenerator):
    def __init__(self, text: str = "", shifting: int = 0):
        super().__init__(text, shifting)
    
    def view(self):
        try:
            for i in self.generate():
                t = pattern.sub(lambda m: rep[re.escape(m.group(0))], i)
                print(t, end="\r")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    text = input("Enter TEXT: ")
    
    for theme in themes.keys():
        print(f"{theme} :: {themes[theme]}")
        
    THEME = input("Enter THEME (default: smootherRainbow 'leave blank'): ") or "smootherRainbow"
    if THEME not in themes.keys():
        THEME = "smootherRainbow"
    
    generator = ViewOnTerminal(text, 2)
    generator.write_info()
    
    generator.view()
