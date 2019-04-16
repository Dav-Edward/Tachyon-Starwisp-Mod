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
    * [Order of Directives](#order-of-directives)
    * [Auto Generated Ids](#auto-generated-ids)
- [Options Controlling Behaviour](#options-controlling-behaviour)
    - [default\_resopnse](#default_response)
    - [mangle\_any\_value](#mangle_any_value)
    - [mangle\_empty\_value](#mangle_empty_value)
- [Directives](#directives)
    * [Label(id)](#labelid)
    * [Response(text)](#responsetext)
    * [Goto(target)](#gototarget)
    * [End](#end)
    * [Event(id, target)](#eventid-target)
    * [Choice(text, choices)](#choicetext-choices)
    * [Condition(type, params)](#conditiontype-params)
    * [AnyCondition(value)](#anyconditionvalue)
- [Examples](#examples)


Motivation
----------

The XML format used by Tachyon to author dialogues is very tedious to
work with.  Writing a message that follows up from another message
requires manually assigning message ids and referencing these in reply
blocks that have their own ids in addition.  There's no nested
definitons, causing large multiple choice dialogs to have the the
choices and the response texts spread far appart.

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

`.\diagen.py script.py [output file]` (Windows command and powershell)  
`./diagen.py script.py [output file]` (Linux command line)

Generates a dialogue XML file based on a python script and writes it to
output.xml.  If not specified the output file defaults to the name of
the input file with a .xml suffix.

Both the script and the output file may be denoted as `-` to indicate
they should be read from standard input or written to standard outupt
respectively.


Script format
-------------

A Diagen script is a Python script that sets a global variable named
`dialogues` to a dictionary of dialogue name to a dialogue section
definetion.  In other words, a typical script will have the following
form:

```py
dialogues = {
    "MY_DIALOGUE": [
        section content,
        ...
    ],
}
```

Dialogue sections are Python lists consisting of strings and
[Directives](#directives).  Strings correspond to the text content of
messages, and multiple consecutive messages will be linked together with
auto generated replies.  The text content of replies can be controlled
with the [Response](#responsetext) directive, though by default the
reply text is `[SKIP]...`.  Here's a complete Diagen script containing a
short exchange of words.

```py
dialogues = {
    "MY_DIALOGUE": [
        "Hi. Who are you?",
        Response("[PLAYER_NAME]"),
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
        Response("Red"),
        "Cool, that's my favorite too!",
    ],
    [
        Response("Green"),
        "Green reminds me of the grass fields at home.",
    ],
    [
        # Without a response, the default ('[SKIP]...') is used
        "Silent protagonist, eh?",
        Choice("Would you like some tea perhaps?", [
            [
                Response("Yes"),
                "I'll see what I can find",
                End,
            ],
            [Response("No")],
            [], # Empty responses are also possible
        ]),
    ],
]),
"I guess it was nice talking to you",
```

Note: To reduce distracting clutter, only the section content is shown
here.

Using Response at the beginning of a choice sub section sets the text
of the reply used.  Once the message flow reaches the end of a choice
subsection it contiues after the Choice directive it was defined in.
Here, after `Response("No")` the flow exits the nested choice subsection
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
        Response("Tell me about the station"),
        "This station was ...",
        # ...
    ],
    [
        # More choices ...
    ],
    [
        Response("That was all"),
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
        Response("Give me a challange"),
        Condition("SECTOR_SHIPS_ABSENT", qty=1, owner="THE_BEARS"),
        "Here you go!",
        Event("SPAWN_CHALLANGE", "PLAYER"),
    ],
    [Response("Bye!")],
]),
```

### Order of Directives

Directives apply for the most part _to messages_.  This means that
unless care is taken to avoid mixing directives applying to the previous
message with ones that apply to the next message the behaviour may be
very confusing.  For example, in the following section the Event,
Response and End applies to the `"that was all"` message, while the
Label is only for the `"A new day"` message, meaning a Goto to Confusion
will not trigger the event.

```py
"that was all",
Label("Confusion"),
End

Event("EVENT", "PLAYER"),
Response("Thank you"),
"A new day",
```

Future version may disallow this kind of order breakage.


### Auto Generated Ids

Ids generated are of the form `M{unique number}`for messages and
`R{number}` for replies.  The message id for a message can be overriden
with the Label directive

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

By default Diagen will add a `var_value="1"` to conditions with the
type `SERVER_VARIABLE_(ABSENT|PRESENT)` and `any_value="1"` set.  This
is due to a bug in a0.8.19 where `any_value="1"` doesn't work unless
`var_value` has been set.  You can disable this behavior by setting
the `'mangle_any_value'` option to `False`.


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


### Label(id)

Specifies that the next message should have the given id.  This directly
corresponds to the id attribute of the message element in the XML
output.

Note: this may not be placed at the end of a section or sub section.


### Response(text)

Set the reply text of the previous message to the given text.  When used
at the start of a choice section it specifies the text of that choice.
When used imminently after a Choice section it sets the default response
text for all choices in that choice section.


### Goto(target)

Continue the message flow from another message.  Works by setting the
next attribute on the reply of the previous message to the given target.
Target should be a message id set by Label.


### End

Signify the end of the message stream.  Normally the next message is
automatically linked via the next attribute of the reply element, this
flag specifies that the previous message should not be linked, and thus
ends the dialogue there.


### Event(id, target)

Attach an event to the previous message.  This tacks an `<event>`
element to the previous message where id and target correspond to their
respective attributes in the XML.


### Choice(text, choices)

Specifies a multiple choice message.  Each choice is of the form
[subsection content, ...] and emulates a reply element in the XML.  The
reply element can be modified with Response, Condition, AnyCondition,
Goto and End added to the start of the subsection


### Condition(type, params)

Specifies the condition of a reply.  Can only be used at the start of a
subsection inside a Choice.  The params is of the form `name="value",
...` and correspond to the `<condition_param name="value" \>` element in
the XML.  Values can also be integeres instead of strings, in this case
they will be converted to strings in the XML output.

It's also possible to specify params as a python dictionary mapping name
to values.  This should be supplied either as a position argument after
type, or keyword argument named `params`.  If both params and keyword
arguments are used, both will be included and the latter with take
precedence if keys are duplicated.

If a param value is a list, it'll output one `<conditior_param>` element
for each element in the list into the generated XML.  Otherwise the
short form of putting it as an attribute to the `<condition>` element is
used instead.


### AnyCondition(value)

Specifies the `any_condition` attribute of a reply.  Only usable at the
start of a subsection inside a Choice.


Examples
--------

A simple dialog with a captain character.

```py
dialogues = {
    "Captain": [
        "Hello [PLAYER_NAME], I'm the captain of this ship",
        Choice("Would you like some tea?", [
            [
                Response("No thanks"),

                "Alright then, no tea for you",
            ],
            [
                Response("Yes please"),

                "Here you go. Now go out there and fight some foes!",
                Event("GIVE_TEA", "PLAYER"),
                Response("Aye sir!"),
            ]
        ]),
    ],
}
```

When processed through Tachyon Diagen it produces the following XML.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<dialogues>
    <dialogue name="Captain">
        <start>M0</start>
        <message id="M0" text="Hello [PLAYER_NAME], I'm the captain of this ship">
            <reply id="R2" target="M1" text="[SKIP]..." />
        </message>
        <message id="M1" text="Would you like some tea?">
            <reply id="R0" target="M2" text="No thanks" />
            <reply id="R1" target="M3" text="Yes please" />
        </message>
        <message id="M2" text="Alright then, no tea for you" />
        <message id="M3" text="Here you go. Now go out there and fight some foes!">
            <event id="GIVE_TEA" target="PLAYER" />
            <reply id="R3" text="Aye sir!" />
        </message>
    </dialogue>
</dialogues>
```

For more complete examples see the the [examples directory](examples).
