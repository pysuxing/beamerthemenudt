#! /usr/bin/python3

import re

class BeamerColor:
    def __init__(self, name, parent = None, use = None):
        self.name = name
        self.parent = parent
        self.use = use
        self.id = None
    def __str__(self):
        return '{{name={}, parent={}, use={}, id={}}}'.format(self.name, self.parent, self.use, self.id)

class Parser:
    #attribute_str = r'(?P<key>.+)=(?P<value>.+))'
    #apattern = re.compile(attribute_str)
    pattern_str = r'\\setbeamercolor\{(?P<name>.+)\}\{(?P<attributes>.*)\}'
    pattern = re.compile(pattern_str)
    def __init__(self):
        self.colors = dict()
    def parse(self, filename):
        current = 0
        with open(filename) as f:
            for line in f:
                match = self.pattern.match(line)
                if not match:
                    continue
                groupdict = match.groupdict()
                name = groupdict['name']
                attributes = groupdict['attributes']
                assert name not in self.colors
                self.colors[name] = BeamerColor(name)
                self.colors[name].id = current
                current += 1
                if not attributes:
                    continue
                for kv in attributes.split(','):
                    k, v = kv.strip().split('=')
                    k, v = k.strip(), v.strip(' {}')
                    if k == 'parent':
                        self.colors[name].parent = v
                    if k == 'use':
                        self.colors[name].use = v

def dot(filename, colors):
    with open(filename, 'w') as f:
        f.write('digraph G {\n')
        for color in colors.values():
            f.write('    {}[label="{}"];\n'.format(color.id, color.name))
            if color.parent:
                print(color)
                f.write('    {} -> {}[style=solid];\n'.format(color.id, colors[color.parent].id))
            if color.use:
                f.write('    {} -> {}[style=dashed];\n'.format(color.id, colors[color.use].id))
        f.write('}\n')

p = Parser()
p.parse('beamercolorthemedefault.sty')
dot('beamercolorthemedefault.dot', p.colors)
