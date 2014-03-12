"""LEXOR: LOG Writer Style

This style displays message nodes provided by other lexor parsing and
converting styles.

"""

from lexor import init
from lexor.core.writer import NodeWriter

INFO = init(
    version=(0, 0, 2, 'final', 1),
    lang='lexor',
    type='writer',
    description='Display messages from parsed/converted documents.',
    url='http://jmlopez-rod.github.io/lexor-lang/lexor-writer-log',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'explanation': 'off',
    'module': 'off',
    'nodeid': 'off',
}


class MsgNW(NodeWriter):
    """Display messages stored in the nodes. """

    def __init__(self, writer):
        NodeWriter.__init__(self, writer)
        self.log = writer.root

    def start(self, node):
        mod = self.log.modules[node['module']]
        exp = self.log.explanation[node['module']]
        mod_msg = mod.MSG[node['code']]
        code_index = exp.get(node['code'], None)
        pos = [0, 0]
        if 'position' in node:
            pos = node['position']
        name = ''
        if self.writer.defaults['module'] in ['true', 'on']:
            name = '[{name}]'
        location = '{line}:{column:2}:'
        if 'node_id' in node:
            if self.writer.defaults['nodeid'] in ['true', 'on']:
                location = '0x%x:' % node['node_id']
            else:
                location = ''
        msg = '{fname}:%s %s[{code}] {msg}\n' % (location, name)
        msg = msg.format(fname=node['uri'],
                         line=pos[0], column=pos[1],
                         name=node['module'],
                         code=node['code'],
                         msg=mod_msg.format(*node['arg']))
        self.write(msg)
        if self.writer.defaults['explanation'] in ['true', 'on']:
            if code_index is not None:
                self.write('%s\n' % mod.MSG_EXPLANATION[code_index])
            else:
                self.write('\n    No description found.\n\n')


MAPPING = {
    'msg': MsgNW,
}
