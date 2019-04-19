Tachyon Diagen
==============

A simple Python based generator script for the horrendus dialogue XML
format used by the FTL inspired Tachyon game.


Contents
--------

- [Contents](#contents)
- [Motivation](#motivation)
- [Installation](#installation)
- [Usage](#usage)
- [Script format](#script-format)
    * [Dialogues](#dialogues)
    * [Events](#events)
    * [Order of Directives](#order-of-directives)
    * [Auto Generated Ids](#auto-generated-ids)
- [Options Controlling Behaviour](#options-controlling-behaviour)
    - [default\_resopnse](#default_response)
    - [mangle\_any\_value](#mangle_any_value)
    - [mangle\_empty\_value](#mangle_empty_value)
- [Directives](#directives)
    * [Note about params](#note-about-params)
    * [Label(id)](#labelid)
    * [Reply(text=None, params)](#replytextnone-params)
    * [Goto(target)](#gototarget)
    * [End](#end)
    * [Event(id, target)](#eventid-target)
    * [Choice(text, choices)](#choicetext-choices)
    * [Condition(type, params)](#conditiontype-params)
    * [InlineEvent(type, target, name=None, params)][1]
    * [EventDef(type, name, params)](#eventdeftype-name-params)
    * [SpawnNPC(params)](#spawnnpcparams)
    * [AddShip(params)](#addshipparams)
    * [Ai(type, params)](#aitype-params)
    * [AddDebris(params)](#adddebrisparams)
    * [Item(params)](#itemparams)
- [Examples](#examples)

[1]: #inlineeventtype-target-namenone-params


Motivation
----------

The XML format used by Tachyon to author dialogues and events is very
tedious to work with.  Writing a message that follows up from another
message requires manually assigning message ids and referencing these in
reply blocks that have their own ids in addition.  There's no nested
definitons, causing large multiple choice dialogs to have the the
choices and the response texts spread far appart and events have to be
defined in a separate file despite many events being only referenced by
one dialogue message.

Worse still, because of the manual id assigment and referencing moving
arround and reorganizing text may in the worst case require renumbering
a bunch of messages, some that can be reference multiple spread out
places in a dialog.

Appart from solving these issues, a Python based generator also allows
for scripted generation of repeated structures.


Installation
------------

You can download the [diagen.py](diagen.py) file (right click and save
as on the raw button) and put it where you like.  The script is runned
from a command line.  On Linux you will need to do `chmod +x diagen.py`
in order to run it if obtained this way.

Perhaps the best way to integrate Diagen into the development flow is to
put it into the server folder and add it to the start of the
StartServerConsole startup script.  For example on Windows:

```cmd
DEL WorldGen\Dialogues\MyScript.xml
.\diagen.py WorldGen\Dialogues\MyScript.py

java -jar ...
```

Or on Linux

```sh
rm WorldGen/Dialogues/MyScript.xml
./diagen.py WorldGen/Dialogues/MyScript.py

java -jar ...
```

This ensures every time you start the server that you will have the up
to date dialogues.


Usage
-----

In a command line in the directory the script is installed to:

`.\diagen.py script.py [dialog file] [event file]` (Windows command and
powershell)  
`./diagen.py script.py [dialog file] [event file]` (Linux command line)

Generates a dialogue XML file based on a python script and writes it to
output.xml.  If not specified the dialog output file defaults to the
name of the input file with a .xml suffix, and the event file defaults
to the name of the input file pluss _event.xml.

Both the script and the output files may be denoted as `-` to indicate
they should be read from standard input or written to standard outupt
respectively.


Script format
-------------

A Diagen script is a Python script that sets a global variable named
`dialogues` to a dictionary of dialogue name to a dialogue section
definetion.  And optionally sets another global variable named `events`
with event definitions.  In other words, a typical script will have the
following form:

```py
dialogues = {
    "MY_DIALOGUE": [
        section content,
        ...
    ],
}

events = [
    EventDef("EVENT_TYPE", "MY_EVENT", ...),
]
```


### Dialogues

Dialogue sections are Python lists consisting of strings and
[Directives](#directives).  Strings correspond to the text content of
messages, and multiple consecutive messages will be linked together with
auto generated replies.  The text content of replies can be controlled
with the [Reply](#replytextnone-params) directive, though by default the
reply text is `[SKIP]...`.  Here's a complete Diagen script containing a
short exchange of words.

```py
dialogues = {
    "MY_DIALOGUE": [
        "Hi. Who are you?",
        Reply("[PLAYER_NAME]"),
        "Oh, Hi [PLAYER_NAME], I'm [NPC_NAME]",
        "I have an important mission for you.",
        "I need you to go to the other side of the space station.",
    ],
}
```

To represent dialogue trees with multiple paths diverging and converging
the [Choice](#choicetext-choices) directive is used.  For example,
here's a choice where the character asks about the favorite color with 3
different responses.

```py
Choice("What is your favorite color?", [
    [
        Reply("Red"),
        "Cool, that's my favorite too!",
    ],
    [
        Reply("Green"),
        "Green reminds me of the grass fields at home.",
    ],
    [
        # Without a response, the default ('[SKIP]...') is used
        "Silent protagonist, eh?",
        Choice("Would you like some tea perhaps?", [
            [
                Reply("Yes"),
                "I'll see what I can find",
                End,
            ],
            [Reply("No")],
            [], # Empty responses are also possible
        ]),
    ],
]),
"I guess it was nice talking to you",
```

Note: To reduce distracting clutter, only the section content is shown
here.

Using Reply at the beginning of a choice sub section sets the text of
the reply used.  Once the message flow reaches the end of a choice
subsection it contiues after the Choice directive it was defined in.
Here, after `Reply("No")` the flow exits the nested choice subsection
and continues out another choice subsection and into `"I guess it was
nice talking to you"`

Another flow control directive used here is [End](#end).  It means the
flow of messages in that given path ends there.

When processed through Diagen choice section produces the following XML:

```xml
<message id="M0" text="What is your favorite color?">
    <reply id="R1" next="M1" text="Red" />
    <reply id="R2" next="M2" text="Green" />
    <reply id="R3" next="M3" text="[SKIP]..." />
</message>
<message id="M1" text="Cool, that's my favorite too!">
    <reply id="R1" next="M6" text="[SKIP]..." />
</message>
<message id="M2" text="Green reminds me of the grass fields at home.">
    <reply id="R1" next="M6" text="[SKIP]..." />
</message>
<message id="M3" text="Silent protagonist, eh?">
    <reply id="R1" next="M4" text="[SKIP]..." />
</message>
<message id="M4" text="Would you like some tea instead?">
    <reply id="R1" next="M5" text="Yes" />
    <reply id="R2" next="M6" text="No" />
    <reply id="R3" next="M6" text="[SKIP]..." />
</message>
<message id="M5" text="I'll see what I can find" />
<message id="M6" text="I guess it was nice talking to you" />
```

This nested method of defining dialogue paths does not turn into the
unmanagable clutter that the flat message structure inevitably becomes,
and requries far less explicit jumps to accomplish the same things.

Despite this, jumps are still necessary for some things and to support
them Diagen provides two Directives: [Label](#labelid) and
[Goto](#gototarget).  Label specifies the id of the next message, and
Goto specifies that the flow of messages should continue at the given
message id.

The simplest and most straightforward use case for Label and Goto is
implementing a looping menu:

```py
Label("Menu"),
Choice("What can I do for you?", [
    [
        Reply("Tell me about the station"),
        "This station was ...",
        # ...
    ],
    [
        # More choices ...
    ],
    [
        Reply("That was all"),
        End,
    ],
]),
Goto("Menu"),
```

The last thing to mention is [Condition](#conditiontype-params) and
[Event](#eventid-target).  Contion may appear at the start of a choice
subsection and adds a `<condition>` element to the reply element leading
to that subsection, and Event attaches an `<event>` element to the
message preceeding it.

```py
Choice("Greetings", [
    [
        Reply("Give me a challange"),
        Condition("SECTOR_SHIPS_ABSENT", qty=1, owner="THE_BEARS"),
        "Here you go!",
        Event("SPAWN_CHALLANGE", "PLAYER"),
    ],
    [Reply("Bye!")],
]),
```

As an alternative to referencing an event definition with Event, the
event can be defined inside dialogue sections with the [InlineEvent][1]
directive.  InlineEvent takes as argument the event type, the target,
and optionally the name of the event, followed by the event parameters.
If not given the name of an inline event is automatically generated
based on the name of the dialogue.  See the next section for more
details on defining events.


### Events

Events are primarily defined with [EventDef](#eventdeftype-name-params)
inside the `events` global variable.  For example to create an event
named SET\_MY\_VAR which will set the server variable MY\_VAR to 1 when
invoked one can use the following:

```py
events = [
    EventDef("SERVER_VARIABLE", "SET_MY_VAR",
        var_name="MY_VAR", var_value="1"
    ),
]
```

Some events have aditional elementes in the XML specifying various extra
things associated with the event.  For SPAWN\_SHIP there's the
`<add_ship>` element specifying the ship.  In diagen this is specified
with the [AddShip](#addshipparams) directive after the event definition.
For example to spawn a particularly bad pirate ship, the following
diagen code can be used:

```py
EventDef("SPAWN_SHIP", "MY_PIRATE_SHIP_SPAWN"),
AddShip(
    gen_ship_model="MY_PIRATE_SHIP_MODEL", ship_qty=1, ship_name="Pirate",
    random_pos=1, min_healt=10, max_health=10
),
Ai("LIFE_SUPPORT"),
Ai("EVADER"),
Ai("SENTRY"),

SpawnNPC(
    qty=1, is_captain=1, random_name=1, race="HUMAN",
    home_system="PILOTING", spawn_at_home=1
),
Ai("NPC_TALKER", timer=30, mes="I will shot you to bits!"),
```

Note: To reduce distracting clutter, only the events content is shown
here.

This also shows how [Ai](#aitype-params) can be added to AddShip, as
well as [SpawnNPC](#spawnnpcparams), and generally ends up attached
whichever is the closest previous applicable directive.  There is also
[AddDebris](#adddebrisparams) and [Item](#itemparams) for placing items
into sectiors.


### Order of Directives

Directives apply for the most part to some previous directive or
message.  This means that unless care is taken to avoid mixing
directives altering flow of message with ones that apply to the message
itself the behaviour may be very confusing.  For example, in the
following section the Event, Reply and End all applies to the `"that was
all"` message.  This means that even though the event and response
appears after the End marker they are still triggered/shown.

```py
"that was all",
End
Event("EVENT", "PLAYER"),
Reply("Thank you"),
```

Future version may disallow this kind of order breakage.


### Auto Generated Ids

Ids generated are of the form `M{unique number}` for messages and
`R{number}` for replies.  The message id for a message can be overriden
with the Label directive

For inline events with auto generated names its of the form `{dialogue
name}_E{number}`

Since I'm not aware of any use for the reply id, there's no way to
influence the reply ids generated.


Options Controlling Behaviour
-----------------------------

To control the behaviour of Diagen you can set `diagen_options` to a
dictionary of option name to option value.  The available options are:


### default\_response

By default the reply text of a message is `[SKIP]...`, this can be
changed by setting `'default_response'`.  For example you can make the
character overly affirmative with:

```py
diagen_options = {
    'default_response': "[SKIP]Aye sir!",
}
```


### mangle\_any\_value

To work around a bug in a0.8.19 you can set `'mangle_any_value'` option
to `True`.  This will cause Diagen to add a `var_value="1"` to
conditions with the type `SERVER_VARIABLE_(ABSENT|PRESENT)` and
`any_value="1"` set.  Since this got fixed in a0.8.20 this option
defaults to `False`.


### mangle\_empty\_value

By default Diagen will swap the condition type of
`SERVER_VARIABLE_(ABSENT|PRESENT)` conditions to their logical opposite
if neither `any_value`, nor `var_value` is set.  This is due to the
highly unintuitive behavour of using these conditions, where they act in
the reverse of what the name logically implies.  I.e. the following

```xml
<condition type="SERVER_VARIABLE_PRESENT" var_name="MY_VAR" />
```

will match if `MY_VAR` _is not set_.  Diagen reverse this so that

```py
Condition("SERVER_VARIABLE_PRESENT", var_name="MY_VAR")
```

will produce the `_ABSENT` variant that matches if `MY_VAR` is set.  You
can disable this behaviour by setting the `'mangle_empty_value'` option
to `False`.


Directives
----------

Dialogue sections are lists consists of strings denoting message
contents and directives describing special elements or properties these
messages should have.  There's also subsections thare are made with the
[Choice](#choicetext-choices) directive.


### Note about params

Many directives have a `params` parameter.  These are name, value pairs
that have form `name="value", ...` and correspond to the `<node_param
name="value" \>` element in the XML, where `node` is the relevant tag,
i.e. `event` for an event node.  Values can also be integeres instead of
strings, in this case they will be converted to strings in the XML
output.

If a param value is a list, it'll output one `<node_param>` element for
each element in the list into the generated XML.  Otherwise the short
form of putting it as an attribute to the `<node>` element is used.

It's also possible to specify params as a python dictionary mapping name
to values.  This should be supplied either as the position argument
corresponding to params, or as a keyword argument named `params`.
If both params and keyword arguments are used, both will be included and
the latter with take precedence if keys are duplicated.


### Label(id)

Specifies that the next message should have the given id.  This directly
corresponds to the id attribute of the message element in the XML
output.

Attaches to the next message or the next choice.


### Reply(text=None, params)

Set the reply text of the previous message to the given text.  When used
at the start of a choice section it specifies the text of that choice,
as well as any extra attributes for the `<reply>` element.  When used
imminently after a Choice section it sets the default response
text for all choices in that choice section.

Note: params can only be set when this directive is used at the start of
a choice section.  It's also possible to leave out the text parameter
there to use the default.

Attaches to the previous message or the choice subsection.


### Goto(target)

Continue the message flow from another message.  Works by setting the
next attribute on the reply of the previous message to the given target.
Target should be a message id set by Label.

Attaches to the previous message or the choice subsection.


### End

Signify the end of the message stream.  Normally the next message is
automatically linked via the next attribute of the reply element, this
flag specifies that the previous message should not be linked, and thus
ends the dialogue there.

Attaches to the previous message or the choice subsection.


### Event(id, target)

Attach an event to the previous message.  This tacks an `<event>`
element to the previous message where id and target correspond to their
respective attributes in the XML.

Attaches to the previous message or the previous choice.


### Choice(text, choices)

Specifies a multiple choice message.  Each choice is of the form
[subsection content, ...] and emulates a reply element in the XML.  The
reply element can be modified with Reply, Condition, Goto and End added
to the start of the subsection


### Condition(type, params)

Specifies the condition of a reply, event, or AI.  Can only be used at
the start of a choice subsection, after an EventDef or InlineEvent
directive, or after an Ai directive.

The element created in the xml depens on what the condition is applied
to.  For replies in inside Choice subsections and events it creates a
`<condition>` element, for Ai's attached to SpawnNPC directives it
creates an `<npc_ai_condition>` element, and for Ai's attached to
AddShip directives it creates an `<ship_ai_condition>`.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the choice subsection, or the previous event or AI.


### InlineEvent(type, target, name=None, params)

Defines and attaches an event to the previous message.  Like Event, but
instead of referencing an event defined elsewhere the event is defined
inline with the dialogue.  The name of the event if not defined is
generated based on the dialoge name and takes the form
`{dialogue name}_E{number}`.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous message.


### EventDef(type, name, params)

Defines an event in the event list.  This corresponds to the `<event>`
element in an events XML file.

See [note about params](#note-about-params) for a description of the
`params` parameter.


### SpawnNPC(params)

Adds an NPC node to the previous event or ship.  When used after an
EventDef it creates a `<spawn_npc>` element in the event.  When used
after a AddShip it creates a `<spawn_npc_on_ship>` element in the ship.
Both of these support adding AIs with the Ai directive after this one.

As a convenience all parameter names passed to SpawnNPC is prefixed with
`npc_` in the generated XML.  This means that parameters such as
`npc_qty`, `npc_is_crew`, `npc_race` etc, should be written as `qty`,
`is_crew`, `race`, etc.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous EventDef, InlineEvent, or AddShip.


### AddShip(params)

Adds a `<add_ship>` node to the previous event.  NPCs can be spawned on
the ship by using the SpawnNPC directive after this one.  AIs to attach
to ship can also be added with the Ai directive, but note that this
would have to come before any SpawnNPC directives, otherwise the Ai
directive would apply to those instead.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous EventDef or InlineEvent.


### Ai(type, params)

Adds an AI element to an NPC or ship.  When put after an AddShip it
procudes a `<ship_ai>` element inside the ship element, and when put
after a SpawnNPC it produces an `<npc_ai>` element inside the spawn npc
element.  Both of these support adding conditions to the AI element by
using the Condition directive after this one.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous SpawnNPC or AddShip.


### AddDebris(params)

Used for the SPAWN\_DEBRIS event to add an `<add_debris>` nodes to it.
For example, a simple debris spawning event can be defined as.

```py
EventDef("SPAWN_DEBRIS", "MY_DEBRIS"),
AddDebris(owner="Lost ship", random_pos=1),
Item(item_type="SHIP_SYSTEM", system_model="SENSORS1"),
Item(item_type="SHIP_SYSTEM", system_model="SENSORS2"),
```

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous EventDef or InlineEvent.


### Item(params)

Item definition for AddDebris, corresponds to the `<debris_item>`
element.  Should have an `item_type` and a `system_model` parameter.

See [note about params](#note-about-params) for a description of the
`params` parameter.

Attaches to the previous AddDebris.


Examples
--------

A simple dialog with a captain character.

```py
dialogues = {
    "Captain": [
        "Hello [PLAYER_NAME], I'm the captain of this ship",
        Choice("Would you like some tea?", [
            [
                Reply("No thanks"),

                "Alright then, no tea for you",
                InlineEvent("SERVER_VARIABLE",
                    var_name="PLAYER_DECLINED_TEA", var_value=1
                ),
            ],
            [
                Reply("Yes please"),

                "Here you go. Now go out there and fight some foes!",
                Event("GIVE_TEA", "PLAYER"),
                Reply("Aye sir!"),
            ]
        ]),
    ],
}

events = [
    EventDef("MODIFY_SHIP", "GIVE_TEA",
        all_mob_ships=0, ignore_passenger_access=0,
        add_system_model_to_cargo="TeaBrewer"
    ),
]
```

When processed through Tachyon Diagen it produces the following XML for
the dialogues:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<dialogues>
    <!-- Generated by diagen.py -->
    <dialogue name="Captain">
        <start>M0</start>
        <message id="M0" text="Hello [PLAYER_NAME], I'm the captain of this ship">
            <reply id="R1" text="[SKIP]..." next="M1" />
        </message>
        <message id="M1" text="Would you like some tea?">
            <reply id="R1" text="No thanks" next="M2" />
            <reply id="R2" text="Yes please" next="M3" />
        </message>
        <message id="M2" text="Alright then, no tea for you">
            <event id="Captain_E0" target="PLAYER" />
        </message>
        <message id="M3" text="Here you go. Now go out there and fight some foes!">
            <event id="GIVE_TEA" target="PLAYER" />
            <reply id="R1" text="Aye sir!" />
        </message>
    </dialogue>
</dialogues>
```

And the following XML for the events:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<events>
    <!-- Generated by diagen.py -->
    <event type="MODIFY_SHIP" name="GIVE_TEA" all_mob_ships="0" ignore_passenger_access="0" add_system_model_to_cargo="TeaBrewer" />
    <event type="SERVER_VARIABLE" name="Captain_E0" var_name="PLAYER_DECLINED_TEA" var_value="1" />
</events>
```

For more complete examples see the the [examples directory](examples).
