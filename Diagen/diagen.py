#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2018 Hornwitser
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from xml.etree.ElementTree import Comment, Element, ElementTree, SubElement
from collections import namedtuple
from itertools import count

__all__ = [
    'Label', 'Choice', 'Condition', 'Goto', 'End',
    'Event', 'Reply', 'InlineEvent', 'EventDef', 'ChainEvent', 'SpawnNPC',
    'AddShip', 'Ai', 'AddDebris', 'Item', 'xml_dialogues', 'xml_pretty',
]



## Message Dirictives

# Set the next message's id
Label = namedtuple('Label', 'id')

# Signal the end of the message stream.
class EndType:
    def __new__(cls):
        return End

    @staticmethod
    def __repr__():
        return 'End'

End = object.__new__(EndType)

# Continue with given id.
Goto = namedtuple('Goto', 'target')

# Attach an event to the previous message.
Event = namedtuple('Event', 'id target')

# Set the reply text of the previous message.
_BaseReply = namedtuple('Reply', 'text params')
class Reply(_BaseReply):
    def __new__(cls, text=None, params={}, **extra):
        return super().__new__(cls, text, {**params, **extra})

# Specifies a multiple choice message.  Choices is a list of subsections.  The
# reply element generated can be modified with Reply, Condition, Goto and End
# put at the start of a choice subsection
Choice = namedtuple('Choice', 'text choices')

# Attach an event defined inline to the previous message
_BaseInlineEvent = namedtuple('InlineEvent', 'type target name params')
class InlineEvent(_BaseInlineEvent):
    def __new__(cls, type, target, name=None, params={}, **extra):
        return super().__new__(cls, type, target, name, {**params, **extra})


## Event Directives

# Define an event
_BaseEventDef = namedtuple('EventDef', 'type name params')
class EventDef(_BaseEventDef):
    def __new__(cls, type, name, params={}, **extra):
        return super().__new__(cls, type, name, {**params, **extra})

# Define an event and attach it to the previous event
_BaseChainEvent = namedtuple('ChainEvent', 'type name params')
class ChainEvent(_BaseChainEvent):
    def __new__(cls, type, name=None, params={}, **extra):
        return super().__new__(cls, type, name, {**params, **extra})

# Defines an npc spawn for either an event or a ship
_BaseSpawnNPC = namedtuple('SpawnNPC', 'params')
class SpawnNPC(_BaseSpawnNPC):
    def __new__(cls, params={}, **extra):
        return super().__new__(cls, {**params, **extra})

# Defines a ship for an event
_BaseAddShip = namedtuple('AddShip', 'params')
class AddShip(_BaseAddShip):
    def __new__(cls, params={}, **extra):
        return super().__new__(cls, {**params, **extra})

# Defines an ai for either a ship or npc
_BaseAi = namedtuple('Ai', 'type params')
class Ai(_BaseAi):
    def __new__(cls, type, params={}, **extra):
        return super().__new__(cls, type, {**params, **extra})

# Defines a debris node for an event
_BaseAddDebris = namedtuple('AddDebris', 'params')
class AddDebris(_BaseAddDebris):
    def __new__(cls, params={}, **extra):
        return super().__new__(cls, {**params, **extra})

# Defines an item for a debris node
_BaseItem = namedtuple('Item', 'params')
class Item(_BaseItem):
    def __new__(cls, params={}, **extra):
        return super().__new__(cls, {**params, **extra})


## Shared Directives

# Specifies the condition of a choice, event or ai.  May only be used at the
# start of a choice subsection or after an event, ship or npc definition.
_BaseCondition = namedtuple('Condition', 'type params')
class Condition(_BaseCondition):
    def __new__(cls, type, params={}, **extra):
        return super().__new__(cls, type, {**params, **extra})


# Internal use types
class AutoType:
    def __new__(cls):
        return Auto

    @staticmethod
    def __repr__():
        return 'Auto'

Auto = object.__new__(AutoType)

class ParsedReply:
    def __init__(self, target, text, params):
        self.id = Auto
        self.target = target
        self.text = text
        self.params = params
        self.conditions = []

class ParsedMessage:
    def __init__(self, mid, text):
        self.id = mid
        self.text = text
        self.next = Auto
        self.response = Auto
        self.choices = []
        self.events = []

class ParsedEvent:
    def __init__(self, event_type, name, params):
        self.type = event_type
        self.name = name
        self.params = params
        self.target = None
        self.conditions = []
        self.npcs = []
        self.debris = []
        self.ships = []

class ParsedDebri:
    def __init__(self, params):
        self.params = params
        self.items = []

class ParsedAi:
    def __init__(self, ai_type, params):
        self.type = ai_type
        self.params = params
        self.conditions = []

class ParsedNPC:
    def __init__(self, params):
        self.params = params
        self.ais = []

class ParsedShip:
    def __init__(self, params):
        self.params = params
        self.ais = []
        self.npcs = []

class ParseError(Exception):
    """Raised if an error occurs during section parsing"""

    def __init__(self, msg, pos, section):
        self.msg = msg
        self.pos = pos
        self.section = section
        self.parents = []

FlatMessage = namedtuple('FlatMessage', 'id text replies events')
FlatReply = namedtuple('FlatReply', 'id target text conditions params')

def auto(value, auto_value):
    """Replace a value being Auto with auto_value"""
    return auto_value if value is Auto else value

def parse_reply(pos, section):
    """Parse reply modifiers from the start of a subsection"""
    reply = ParsedReply(Auto, Auto, {})
    while pos < len(section):
        mod = section[pos]

        if type(mod) is Reply:
            if mod.text is not None:
                if reply.text is not Auto:
                    raise ParseError("Reply cannot be chained", pos, section)
                reply.text = mod.text
            reply.params.update(mod.params)

        elif type(mod) is Condition:
            reply.conditions.append(mod)

        elif mod is End:
            reply.target = None

        elif type(mod) is Goto:
            reply.target = mod.target

        else:
            break
        pos += 1
    return pos, reply

def parse_debris(pos, section):
    """Parse derbis node with items"""
    if type(section[pos]) is not AddDebris:
        raise TypeError(f"parse_debris called on {section[pos]}")

    debris = ParsedDebri(section[pos].params)
    pos += 1

    while pos < len(section):
        item = section[pos]

        if type(item) is Item:
            debris.items.append(item)

        else:
            break
        pos += 1
    return pos, debris

def parse_ai(pos, section):
    """Parse AI node with conditions"""
    if type(section[pos]) is not Ai:
        raise TypeError(f"parse_ai called on {section[pos]}")

    ai = ParsedAi(section[pos].type, section[pos].params)
    pos += 1

    while pos < len(section):
        item = section[pos]

        if type(item) is Condition:
            ai.conditions.append(item)

        else:
            break
        pos += 1
    return pos, ai

def parse_npc(pos, section):
    """Parse NPC node with AIs"""
    if type(section[pos]) is not SpawnNPC:
        raise TypeError(f"parse_npc called on {section[pos]}")

    npc = ParsedNPC(section[pos].params)
    pos += 1

    while pos < len(section):
        item = section[pos]

        if type(item) is Ai:
            pos, ai = parse_ai(pos, section)
            npc.ais.append(ai)
            continue

        else:
            break
        pos += 1
    return pos, npc

def parse_ship(pos, section):
    """Parse ship with AIs and NPCs"""
    if type(section[pos]) is not AddShip:
        raise TypeError(f"parse_ship called on {section[pos]}")

    ship = ParsedShip(section[pos].params)
    pos += 1

    while pos < len(section):
        item = section[pos]

        if type(item) is Ai:
            pos, ai = parse_ai(pos, section)
            ship.ais.append(ai)
            continue

        elif type(item) is SpawnNPC:
            pos, npc = parse_npc(pos, section)
            ship.npcs.append(npc)
            continue

        else:
            break
        pos += 1
    return pos, ship

def parse_event(pos, section):
    """Parse event with conditions, npcs, ships and debris"""
    item = section[pos]
    if type(item) is InlineEvent:
        event = ParsedEvent(item.type, item.name, item.params)
        event.target = item.target
        if event.name is None:
            event.name = Auto
    elif type(item) is EventDef:
        event = ParsedEvent(item.type, item.name, item.params)
    else:
        raise TypeError(f"parse_event called on {item}")
    pos += 1

    while pos < len(section):
        item = section[pos]

        if type(item) is Condition:
            event.conditions.append(item)

        elif type(item) is SpawnNPC:
            pos, npc = parse_npc(pos, section)
            event.npcs.append(npc)
            continue

        elif type(item) is AddDebris:
            pos, debris = parse_debris(pos, section)
            event.debris.append(debris)
            continue

        elif type(item) is AddShip:
            pos, ship = parse_ship(pos, section)
            event.ships.append(ship)
            continue

        else:
            break
        pos += 1
    return pos, event

def parse_events(section):
    """Parse event objects and modifiers"""
    pos = 0
    events = []
    while pos < len(section):
        item = section[pos]

        if type(item) is EventDef:
            pos, event = parse_event(pos, section)
            events.append(event)

        else:
            msg = f"Unkown item type {item.__class__.__name__}"
            raise ParseError(msg, pos, section)

    return events

def parse_message(pos, section):
    """Parse message with associated modifiers"""
    mid = Auto

    if type(section[pos]) is Label:
        if pos == len(section):
            msg = "Label is not allowed at the end of a section"
            raise ParseError(msg, pos, section)

        mid = section[pos].id
        pos += 1

    if type(section[pos]) is str:
        message = ParsedMessage(mid, section[pos])
        pos += 1

    elif type(section[pos]) is Choice:
        choices = []
        for content in section[pos].choices:
            try:
                subpos, reply = parse_reply(0, content)
                _, subsection = parse_dialogue(subpos, content)

            except ParseError as err:
                err.parents.append((pos, section))
                raise err

            except Exception as exc:
                msg = (
                    f"Exception while parsing this section:"
                    f" {exc.__class__.__name__}: {exc}"
                )
                raise ParseError(msg, pos, section)

            else:
                choices.append((reply, subsection))

        message = ParsedMessage(mid, section[pos].text)
        message.choices.extend(choices)
        pos += 1

    elif mid is not Auto:
        msg = f"{section[pos].__class__.__name__} is not allowed after a Label"
        raise ParseError(msg, pos, section)

    else:
        raise TypeError(f"parse_message called on {section[pos]}")

    while pos < len(section):
        item = section[pos]

        if item is End:
            message.next = None

        elif type(item) is Goto:
            message.next = item.target

        elif type(item) is Event:
            message.events.append(item)

        elif type(item) is Reply:
            if item.params:
                msg = "Reply not part of choice can't have params"
                raise ParseError(msg, pos, section)
            if message.response is not Auto:
                raise ParseError("Reply cannot be chained", pos, section)
            message.response = item.text

        elif type(item) is InlineEvent:
            pos, event = parse_event(pos, section)
            message.events.append(event)
            continue

        else:
            break
        pos += 1
    return pos, message

def parse_dialogue(pos, section):
    """Parse message objects and modifiers"""
    if isinstance(section, tuple):
        msg = f"Expected section but got tuple, content: {section}"
        raise ParseError(msg, pos, None)

    dialogue = []
    while pos < len(section):
        item = section[pos]

        if type(item) in [Label, Choice, str]:
            pos, message = parse_message(pos, section)
            dialogue.append(message)
            continue

        elif type(item) in [Condition, EndType, Goto, Event, Reply]:
            msg = f"{item.__class__.__name__} is not allowed here"
            raise ParseError(msg, pos, section)

        else:
            msg = f"Unkown item type {item.__class__.__name__}"
            raise ParseError(msg, pos, section)

        pos += 1

    return pos, dialogue

def assign_ids(section, mid_gen, ename_gen):
    """Assign ids for messages, replies and events that has Auto as the id"""
    for item in section:
        if item.id is Auto:
            item.id = next(mid_gen)

        for event in item.events:
            if type(event) is ParsedEvent and event.name is Auto:
                event.name = next(ename_gen)

        # If there are more than 9 choices, R10 will sort before R2
        if len(item.choices) > 9:
            rid_gen = map("R{:02}".format, count(1))
        else:
            rid_gen = map("R{}".format, count(1))

        for reply, sub in item.choices:
            if reply.id is Auto:
                reply.id = next(rid_gen)

            assign_ids(sub, mid_gen, ename_gen)

def resolve(section, end=None):
    """Resolve next, target and reply text references that are set to Auto"""
    for i, item in enumerate(section):
        if item.next is Auto:
            item.next = section[i+1].id if i+1 < len(section) else end

        for reply, sub in item.choices:
            if reply.target is Auto:
                reply.target = sub[0].id if sub else item.next

            if reply.text is Auto:
                reply.text = item.response

            resolve(sub, end=item.next)

def separate_events(message):
    """Separate event calls from event definitions in a message"""
    calls = []
    defs = []
    for event in message.events:
        if type(event) is Event:
            calls.append(event)

        elif type(event) is ParsedEvent:
            calls.append(Event(event.name, event.target))
            defs.append(event)

        else:
            assert False, "Should not be possible"

    return calls, defs

def flatten(section):
    """Creates a flat representation of a processed section"""
    output = []
    events = []
    for item in section:
        assert type(item) is ParsedMessage, "Should not be possible"

        event_calls, event_defs = separate_events(item)
        events.extend(event_defs)

        replies = []
        sub_outputs = []
        if item.choices:
            for reply, sub in item.choices:
                replies.append(FlatReply(
                    reply.id, reply.target, reply.text,
                    reply.conditions, reply.params
                ))
                sub_output, sub_defs = flatten(sub)
                sub_outputs.extend(sub_output)
                events.extend(sub_defs)

        elif item.response is not Auto or item.next is not None:
            replies.append(FlatReply('R1', item.next, item.response, [], {}))

        output.append(FlatMessage(item.id, item.text, replies, event_calls))
        output.extend(sub_outputs)

    return output, events

SERVER_VAR_TYPES = [
    "SERVER_VARIABLE_PRESENT",
    "SERVER_VARIABLE_ABSENT",
]

def xml_params(node, param_node_name, params):
    """Add possibly duplicated params to node"""
    for key, value in params.items():
        if type(value) is list:
            for item in value:
                if type(item) is int:
                    item = str(item)
                SubElement(node, param_node_name, {key: item})
        else:
            if type(value) is int:
                value = str(value)
            node.set(key, value)

def xml_conditions(node, node_name, conditions, options):
    """Add xml condition and condition_param nodes from condition list"""
    for condition in conditions:
        if condition.type in SERVER_VAR_TYPES:
            if (
                options['mangle_any_value']
                and 'any_value' in condition.params
                and 'var_value' not in condition.params
            ):
                condition.params['var_value'] = '1'

            if (
                options['mangle_empty_value']
                and 'any_value' not in condition.params
                and 'var_value' not in condition.params
            ):
                index = 1 - SERVER_VAR_TYPES.index(condition.type)
                condition = condition._replace(type=SERVER_VAR_TYPES[index])

        condition_node = SubElement(node, node_name, type=condition.type)
        xml_params(condition_node, 'condition_param', condition.params)

def xml_messages(node, messages, options):
    """Add xml message nodes to dialog node from flat message list"""
    for msg in messages:
        msg_node = SubElement(node, 'message', id=msg.id, text=msg.text)

        for event in msg.events:
            SubElement(msg_node, 'event', id=event.id, target=event.target)

        for reply in msg.replies:
            text = auto(reply.text, options['default_response'])
            reply_node = SubElement(msg_node, 'reply', id=reply.id, text=text)

            if reply.target is not None:
                reply_node.set('next', reply.target)

            for key, value in reply.params.items():
                if type(value) is int:
                    value = str(value)
                reply_node.set(key, value)

            xml_conditions(reply_node, 'condition', reply.conditions, options)

def xml_dialogues(dialogues, options):
    """Create dialogues node from diagen dialogue mapping"""
    mid_gen = map("M{}".format, count())

    dialogues_node = Element('dialogues')
    extra_events = []
    for name, section in dialogues.items():
        ename_gen = map(f"{name}_E{{}}".format, count())

        try:
            _, section = parse_dialogue(0, section)

        except ParseError as err:
            err.parents.append((name, None))
            raise err

        assign_ids(section, mid_gen, ename_gen)
        resolve(section)
        messages, events = flatten(section)
        if not messages:
            raise ValueError(f"'{name}' has no messages")

        extra_events.extend(events)
        dialogue_node = SubElement(dialogues_node, 'dialogue', name=name)

        start_node = SubElement(dialogue_node, 'start')
        start_node.text = messages[0].id

        xml_messages(dialogue_node, messages, options)

    return dialogues_node, extra_events

def xml_ai(node, prefix, ais, options):
    """Create ai nodes with conditions from list of ais"""
    for ai in ais:
        ai_node = SubElement(node, f'{prefix}', type=ai.type)
        xml_params(ai_node, f'{prefix}_param', ai.params)
        xml_conditions(ai_node, f'{prefix}_conditions', ai.conditions, options)

def xml_npcs(node, node_name, npcs, options):
    """Create npc nodes with ais from list of npcs"""
    for npc in npcs:
        npc_node = SubElement(node, node_name)
        params = {f'npc_{k}': v for k, v in npc.params.items()}
        xml_params(npc_node, 'npc_param', params)
        xml_ai(npc_node, 'npc_ai', npc.ais, options)

def xml_events(events, options):
    """Create event nodes with ships, npcs and debris from list of npcs"""
    events_node = Element('events')
    for event in events:
        event_node = SubElement(
            events_node, 'event', type=event.type, name=event.name
        )
        xml_params(event_node, 'event_param', event.params)
        xml_conditions(event_node, 'condition', event.conditions, options)
        xml_npcs(event_node, 'spawn_npc', event.npcs, options)

        for ship in event.ships:
            ship_node = SubElement(event_node, 'add_ship')
            xml_params(ship_node, 'ship_param', ship.params)
            xml_ai(ship_node, 'ship_ai', ship.ais, options)
            xml_npcs(ship_node, 'spawn_npc_on_ship', ship.npcs, options)

        for debris in event.debris:
            debris_node = SubElement(event_node, 'add_debris')
            xml_params(debris_node, 'debris_param', debris.params)

            for item in debris.items:
                item_node = SubElement(debris_node, 'debris_item')
                xml_params(item_node, 'debris_item_param', item.params)

    return events_node

def debug_format(item, indent=0):
    """Format a pretty representation of a processed section"""
    if type(item) is ParsedMessage:
        return "\n".join([
            f"{' '*indent}<ParsedMessage id={item.id!r} text={item.text!r}"
            f" next={item.next!r} response={item.response!r}"
            f" events={item.events} choices=["
        ] + [debug_format(c, indent+4) + ',' for c in item.choices] + [
            f"{' '*indent}]>"
        ])

    if type(item) is ParsedReply:
        return (
            f"{' '*indent}<ParsedReply id={item.id!r} target={item.target!r}"
            f" text={item.text!r} conditions={item.conditions}"
            f" params={item.params}>"
        )

    if type(item) is list:
        return "\n".join([
            f"{' '*indent}[",
        ] + [debug_format(sub, indent+4) + ',' for sub in item] + [
            f"{' '*indent}]"
        ])

    if type(item) is tuple:
        return "\n".join([
            f"{' '*indent}(",
        ] + [debug_format(sub, indent+4) + ',' for sub in item] + [
            f"{' '*indent})"
        ])

    return ' ' * indent + repr(item)

def format_pos(pos, section):
    """Formats the last entries before pos with an arrow point at pos"""
    if section is None:
        return f">{pos:3}: Unkown"

    parts = []
    for i in range(max(pos - 2, 0), pos + 1):
        if type(section[i]) is Choice:
            content = f"Choice({section[i].text!r}, ...)"
        else:
            content = repr(section[i])

        parts.append(f"{'>' if i == pos else ' '}{i:3}: {content}")
    return "\n".join(parts)

def format_parse_error(err):
    """Formats a parse error into a traceback like message"""
    parts = []
    parts.append(format_pos(err.pos, err.section))
    for pos, section in err.parents:
        if type(pos) is int:
            parts.insert(0, "in subsection")
            parts.insert(0, format_pos(pos, section))
        else:
            parts.insert(0, f"in dialogue '{pos}'")

    parts.append(f"ParseError: {err.msg}")
    return "\n".join(parts)

def xml_pretty(node, indent=0):
    """Indents and spreads out compact nodes representaions over lines"""
    if len(node):
        text = node.text if node.text is not None else ""
        node.text = f"\n{'    ' * (indent + 1)}{text}"

    for i, sub in enumerate(node):
        tail = sub.tail if sub.tail is not None else ""
        sub.tail = f"\n{'    ' * (indent + (i < len(node)-1))}{tail}"

        xml_pretty(sub, indent+1)

def main():
    """Parse command line argements and do dialogue generation"""
    from argparse import ArgumentParser
    from pathlib import Path
    import sys

    def error(message, code=1):
        """Print message to stderr and exit with code"""
        print(message, file=sys.stderr)
        exit(code)

    def handle_open(path, out):
        """Opens path as output if out otherwise as input"""
        if path == "-":
            return sys.stdout if out else sys.stdin
        try:
            return open(path, 'x' if out else 'r')
        except OSError as err:
            error(f"Error opening {path}: {err}")

    options = {
        'default_response': "[SKIP]...",
        'mangle_any_value': False,
        'mangle_empty_value': True,
    }


    parser = ArgumentParser(description="Generate Tachyion dialogue XML")
    parser.add_argument(
        'script', help="Script file containing the dialogues definition"
    )
    parser.add_argument(
        'output', nargs='?', default=None,
        help="Output file, defaults to script name with an xml extension"
    )
    parser.add_argument(
        'events', nargs='?', default=None,
        help="Events file, defaults to script name + _events with an xml"
        " extension"
    )

    args = parser.parse_args()

    if args.output is None:
        args.output = Path(args.script).with_suffix('.xml')

    if args.events is None:
        args.events = Path(args.script)
        args.events = args.events.with_name(f'{args.events.stem}_events.xml')

    in_file = handle_open(args.script, False)
    out_file = handle_open(args.output, True)

    script_vars = {k: v for k, v in globals().items() if k in __all__}
    exec(in_file.read(), script_vars)

    if 'dialogues' not in script_vars:
        error(f"Script does not set the dialogues variable", 2)

    dialogues = script_vars['dialogues']
    events = script_vars.get('events', [])
    options.update(script_vars.get('diagen_options', {}))

    try:
        root, extra_events = xml_dialogues(dialogues, options)
    except ParseError as err:
        error(format_parse_error(err))

    root.insert(0, Comment(" Generated by diagen.py "))
    xml_pretty(root)
    root.tail = "\n"

    document = ElementTree(root)
    document.write(out_file, encoding="unicode", xml_declaration=True)

    if events or extra_events:
        try:
            events = parse_events(events)
        except ParseError as err:
            msg = format_parse_error(err)
            error("\n".join(["in events section", msg]))

        events.extend(extra_events)
        event_file = handle_open(args.events, True)
        event_root = xml_events(events, options)
        event_root.insert(0, Comment(" Generated by diagen.py "))
        xml_pretty(event_root)
        event_root.tail = "\n"
        event_document = ElementTree(event_root)
        event_document.write(
            event_file, encoding="unicode", xml_declaration=True
        )

if __name__ == '__main__':
    main()
