#from diagen import Choice, Condition, Label, Event, End, Response, Goto, AnyCondition
#remove above line before compile. This just stops python linter from freaking out
# Starwisp Dialogue Rewirte

diagen_options = {
    'default_response': "[SKIP][AUTO]",
}

#----------------------------------------------
#General Definitions

# The tutorial has not be completed
tutorial_wait = [
    Condition("SERVER_VARIABLE_ABSENT", var_name="HJ_TUTORIAL_STARTED", var_value=1),
]


#----------------------------------------------
#Vatish Definitions

#Check if the PUCC is spawned and waiting outside
pucc_ready = [
    Condition("SECTOR_SHIPS_PRESENT", ship_name="P.U.C.C", qty=1),
    Condition("SECTOR_SHIPS_ABSENT", ship_name="VAR(CAMPAIGN_SHIP_ID)", qty=1),
    Condition("SERVER_VARIABLE_PRESENT", var_name="PUCC_BEACON_SECTOR_LOC", any_value=1),
    Condition("SHIP_SYSTEM_ABSENT",
        system_type="HYPERDRIVE", system_model="PUCC_HyperDrive", target_player=1, all_mob_ships=0, active_system=0, qty=1,
    ),
]

#Check if the player owns a PUCC that hasn't been warped yet
inside_pucc = [
    Condition("SECTOR_SHIPS_PRESENT", target_player=1, ship_name="P.U.C.C", crew="[PLAYER_NAME]", qty=1),
    Condition("SHIP_SYSTEM_ABSENT",
        system_type="HYPERDRIVE", system_model="PUCC_HyperDrive", target_player=1, all_mob_ships=0, active_system=0, qty=1,
    ),
    Condition("SERVER_VARIABLE_PRESENT", var_name="PUCC_BEACON_SECTOR_LOC", any_value=1),
]

# See Tachyon Diagen's README.md for explanation of the script format
Vatish = [
    Label("Start"),
    Choice("[ACTION]You see a human figure working on the reactor.", [

        # If you haven’t finished the tutorial yet
        [
            *tutorial_wait,
            "[ACTION]They seem to be busy digging around inside. Perhaps you should talk to the captain first.",
        ],

        # After tutorial, first conversation
        [
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SPAWNED", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="HJ_TUTORIAL_STARTED", var_value=1),
            Label("1stConvo"),
            "[ACTION]On closer observation, the reactor has been repaired with odd-looking crystals.",
            "[ACTION]Noticing you, the figure quickly withdraws from the reactor.",
            "[ACTION]The figure looks androgynous, short, and rather slim.",
            Choice("[ACTION]Something feels a bit off about their appearance.", [
                [
                    Response("Who are you?"),
                    Goto("Vatish_WhoAreYou"),
                ],
                [
                    Response("You're that Starwisp I saw before I died. (Skip Dialogue)"),
                    "That's right, we agreed to assist you. I'll call our ship.",
                    "[ACTION]Vatish's form vanishes replaced by a green and purple orb of plasma.",
                    "[ACTION]The starwisp reaches out energy tendrils sending an energy pulse to the reactor.",                    
                    Goto("AuroraWarpsIn"),
                ],
            ]),
            Label("Vatish_WhoAreYou"),
            "The name's [NPC_NAME]. Are you one of the crew?",
            Response("Yes, I'm a guard, my name is [PLAYER_NAME]."),
            "I see! The clone replication system must have actually worked!",
            "It was pretty smashed up. But it's okay. I hotwired it back together!",
            Response("Yes, except that I don't remember anything."),
            "There were some broken pieces left over... I did what I could.",
            "You look fine otherwise... I think.",
            Response("You aren't part of the crew, are you?"),
            "No. I came on board as soon as the pirates left and did what I could.",
            Response("Why were you out here in the first place?"),
            "I'm aware of your prototype ship, the DF.",
            "I was sent to investigate it, but the pirates got here first.",
            Response("What do you know about it?"),
            "[ACTION]Vatish's expression becomes much more serious.",
            "There is powerful alien technology in your 'prototype' ship.",
            "In fact, it never belonged to the humans in the first place.",
            "But somehow, you got a hold of that technology. And what did you do?",
            "You reverse-engineered it into a super-weapon.",
            "It's a threat to every living being in the universe!",
            Response("...And the pirates have it now too."),
            "Exactly. They need to be stopped, no matter what.",
            Response("I'll stop them any way I can."),
            "If you promise us you will destroy it, the Collective will assist you.",
            "It's too dangerous to let it fall into pirate hands.",
            Response("Collective? What are you talking about?"),
            "[ACTION]The human's form vanishes, revealing a glowing orb of plasma in its place.",
            Response("What the hell are you?"),
            "We are Starwisps. No time to explain, you can ask on the trip if you must.",
            "[ACTION]The creature sends a pulse of energy into the reactor using thin tendrils of plasma.",
            "I called for our ship, they will assist you on your journey.",
            Response("Why are you willing to help us?"),
            "If that prototype ship isn't destroyed, we may all perish.",
            Response("Fair enough."),
            Label("AuroraWarpsIn"),
            "[ACTION]Outside of the station there's a bright flash, and a giant crystal ship jumps close.",
            Event("SPAWN_WispShip", "PLAYER"),
            Event("STARWISP_CAPTAIN_BABBLE_ON", "PLAYER"),
            Event("WISPSHIP_COMPLETE", "PLAYER"),
            "The S.S Aurora is waiting. Radio Solaria on the COMMS when you get to your ship.",
            "[ACTION]The starwisp creature reassumes the illusion of a human.",
            Choice("I'll stay behind and send any other surviving crew your way. Good luck.", [
                [Response("Yes, sir! ...lady... thing."),],
                [Response("Thanks!")],
            ]),
            End,
        ],

        #Finished the first converstation. Go talk to Solaria
        [
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SPAWNED", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="SOLARIA_CONVO_1", var_value=1),
            "Well, go on. Get to your ship, contact Solaria and get on your way.",
            End,
        ],

        #After first conversation and spoke to Solaria. Campaign ship hasn't left. Nothing left to do with Vatish
        [
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SPAWNED", var_value=1),
            Condition("SECTOR_SHIPS_PRESENT", ship_name="VAR(CAMPAIGN_SHIP_ID)", qty=1),
            "[ACTION]It doesn't seem like Vatish has anything to say to you right now.",
            End,
        ],

        # Later players joining game aka PUCC
        [
            Condition("SECTOR_SHIPS_ABSENT", ship_name="VAR(CAMPAIGN_SHIP_ID)", qty=1),
            Condition("SECTOR_SHIPS_ABSENT", ship_name="P.U.C.C", qty=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="PUCC_BEACON_SECTOR_LOC", any_value=1),
            Response("Hello? (Ask for a ship)"),
            "[ACTION]The androgynous-looking person turns to face you.",

            Choice("Oh! Another survivor! The clone replication system managed to recover you as well.", [
                [
                    Response("I don't remember anything. What's going on?"),
                    "The cloning system was damaged, so you didn't recover all of your memories.",
                    "Long story short, pirates attacked this space station and stole a prototype ship.",
                    "Your mission is to hunt down the prototype ship D.F and destroy it.",
                    "The prototype has a super-weapon made using powerful reverse-engineered alien technology.",
                    "We, the Starwisp Collective, agreed to help you in your mission.",
                    "The D.F prototype is a threat to all life in the universe. It must be destroyed.",
                    "I'm sure your crew can catch you up to speed otherwise...",
                    Response("Then I need to join the crew on our ship."),
                ],
                [
                    Response("I need to join the crew on our ship. (Skip Recap)"),
                ],
                [
                    Response("I'm in a hurry. I need to catch up with my ship. (Skip All Dialogue)"),
                    "Okay, I'll have a ship waiting for you outside. It's called the P.U.C.C.",
                    Goto("Skip_PUCC_Convo"),
                ]
            ]),

            "Right... about that. There's no more proper space ships in this sector you can use.",
            "Even if you got one, it could take forever to catch up with your ship.",
            "I did come up with something for you, however!",
            Response("What was that?"),
            "[ACTION]Vatish gives a grin like a mad scientist.",
            "This space station has a shipyard that makes Prototype Unmanned Construction Crafts.",
            Choice("P.U.C.Cs for short. They weren't meant to be manned, but...", [
                [Response("I don't like where this is going..."),],
                [Response("Uhh...")],
            ]),
            "I modified the blueprints, removed some parts and crammed a life support unit inside.",
            "It's a tight fit, but it's spaceworthy and very fast, though it lacks a shield generator.",
            Response("How would that possibly catch up with our ship?"),
            "Well... I've been tinkering, and modified a FTL engine to fit inside it.",
            "I took out all the... 'unnecessary' parts, but it's still quite weak on such a tiny ship.",
            "So I hooked it up to the station and super-charged it with the reactor!",
            Response("That can't be safe..."),
            "Well... it only needs to work once.",
            "We attached a beacon to your ship so the Aurora can follow it.",
            "I'll program it into the FTL system and the autopilot will follow the ship automatically.",
            "The P.U.C.C is so small it can ride the FTL wake your ship makes when it jumps.",
            "It can also be handy in a dogfight. It's fast and can damage the hull or systems quickly.",
            "But it doesn't have any shields, so make sure to dodge frequently.",
            Response("Okay. You really think this will work?"),
            "I'm... pretty sure it will work. The P.U.C.C is outside.",
            Label("Skip_PUCC_Convo"),
            "Contact me on the COMMS when you're ready and I'll install the FTL unit.",
            Event("SPAWN_PUCC", "PLAYER"),
            Response("Will do."),
        ],

        # When radioed on comms
        [
            *pucc_ready,
            Response("I'm ready. Send the P.U.C.C to the ship!"),
            Choice("Okay, make sure you're INSIDE the ship and have already claimed it.", [
                [
                    Response("Wait! I'll get in the ship and claim it."),
                    End,
                ],
                [
                    *inside_pucc,
                    Response("Wait, can I give my ship a name?"),
                    "Sure, what do you want to name it?",
                    Response("[INPUT]Let's call it..."),
                    "Okay I'll name it VAR(PUCC_New_Name).",
                    Event("SET_PUCC_New_Name", "PLAYER"),
                ],
                [
                    *inside_pucc,
                    Response("Yes, ready to go!"),
                ],
                [
                    *inside_pucc,
                    Response("Fire away! (Skip Dialogue)"),
                    Goto("Bon_Voyage"),
                ],
            ]),
            Event("DEFAULT_PUCC_New_Name", "PLAYER"),
            Label("WarpPuccConvo"),
            "The modified FTL engine is ready, and will engage the moment I install it.",
            "By the way... the ship has a built-in fire suppression and repair system.",
            Response("Oh, nice!"),
            Choice("It'll come in handy if it bursts into flames from the FTL engine.", [
                [Response("Wait, what?"),],
                [Response("Oh, great...")],
            ]),
            Label("Bon_Voyage"),
            "Bon voyage!",
            Event("PUCC_Follow_Beacon", "PLAYER"),
            End,

        ],

        #If beacon is lost
        [
            Response("[SKIP](Beacon Lost)"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SPAWNED", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="PUCC_BEACON_SECTOR_LOC", any_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="CAMPAIGN_SHIP_ID", any_value=1),
            "...Strange. I can't find any trace of the beacon we put on your ship.",
            "Without it, I don't know where to send you.",
            "I'm afraid I can't help you without a beacon to guide us.",
            "(If the campaign ship was destroyed, it's Game Over. Reset the server.)",
            End,
        ]
    ])
]
#End Vatish Dialogue

#----------------------------------------------
#Solaria definitions

def check_cargo(system_type):
    return Condition("SHIP_CARGO_PRESENT",
        cargo_type="SHIP_SYSTEM", system_type=system_type, target_player=0, qty=1
    )

all_cargo_types = [
    "WEAPONS_CONTROL", "CLOAKING", "LASER_WEAPONS", "BEAM_WEAPONS", "MISSILE_WEAPONS", "SHIELDS", "REACTOR", "OXYGEN", "PILOTING", "TELEPORT",
    "CAPACITOR", "DOOR_CONTROL", "ENGINES", "HYPERDRIVE", "MEDICAL", "SENSORS", "REPAIR", "SYSTEMS_SHOP",
    "SHIPS_SHOP", "CONSUMABLES_SHOP", "SHIPYARD"
]

Solaria = [
    Label("Start"),
    Choice("[ACTION]Connecting to Aurora...", [
        [
            #First conversation
            Condition("SERVER_VARIABLE_ABSENT", var_name="SOLARIA_CONVO_1", var_value=1),
            "[ACTION]A female human figure appears surrounded by screens.",
            Response("Hello?"),
            "[ACTION]The woman speaks formally but bluntly.",
            "Hello, this is Solaria, captain of the Aurora.",
            Choice("Are you the captain of that ship?", [
                [
                    Response("Yes, the name is [PLAYER_NAME]."),
                    Condition("SECTOR_SHIPS_PRESENT", target_player=1, owner="[PLAYER_NAME]", qty=1),
                    Goto("FirstConvo"),
                ],
                [
                    Response("No."),
                    Condition("SECTOR_SHIPS_ABSENT", target_player=1, owner="[PLAYER_NAME]", qty=1),
                    "I would like to speak with the captain first please.",
                    "I'll stand by for them to contact me on the COMMS.",
                    "[ACTION]The woman ends the transmission.",
                    End,
                ],
                [
                    Response("...Yes."),
                    Condition("SECTOR_SHIPS_ABSENT", target_player=1, owner="[PLAYER_NAME]", qty=1),
                    "[ACTION]The woman casually glances at her Identification, Friend or Foe (IFF) display.",
                    "[ACTION]She raises an eyebrow with a disgruntled expression.",
                    "...Huh, well your IFF registration looks rather... IFFy to me.",
                    "[ACTION]The woman cracks a grin at her pun.",
                    "But really, you're clearly not the captain of that ship.",
                    "If you haven't claimed your ship yet, claim it then contact me back.",
                    "Otherwise go get your captain and have them contact me on the COMMS.",
                    "[ACTION]The woman ends the transmission.",
                    End,
                ],
            ]),
        ],
        [
            #After first conversation
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            "[ACTION]You see a white wispy creature surrounded by screens.",
            Goto("Main"),
        ],
    ]),

    Label("FirstConvo"),
    Choice("Pleasure to meet you.", [
        [
            Response("I was told to contact you.")
        ],
        [
            Response("I remember talking to starwisp Vatish before I died. (Skip Dialogue)"),
            "You do? That'll save time then. No point having my human guise then.",
            "[ACTION]The human figure vanishes replaced by a white glowing orb of plasma.",
            Goto("EndFirstConvo"),
        ],
    ]),
    Event("STARWISP_CAPTAIN_BABBLE_OFF", "PLAYER"),
    "Yes, Vatish debriefed us on the situation. We will join you and provide support.",
    "We have good anti-ship system weapons on board and will defend you in battle.",
    "We also have a unique fabrication system of our own design.",
    "With it, we will research and build new systems and upgrades along the way.",
    Response("Sounds useful. But... I thought Vatish said you were all starwisps."),
    "[ACTION]The figure rolls her eyes and drops all formality in her speech.",
    "They revealed their true form just like that? So much for first impressions.",
    Response("Well, your ship looks rather alien as well."),
    "Ya got me there. Oh well, no point with my human guise then.",
    "[ACTION]The human figure vanishes revealing a white ball of plasma.",
    Response("Why appear human in the first place?"),
    "We make illusions to better communicate with other races.",
    "Otherwise we tend to get poor reactions or folk think we aren't intelligent.",
    Response("I see."),
    "Well, at least I can relax now.",

    Label("EndFirstConvo"),
    Choice("Contact me on the comms if ya need anything.", [
        [
            Response("Okay, thanks!"),
            End
        ],
        [
            Response("Well... (Main Menu)"),
            Goto("Main")
        ],
    ]),
    Event("SOLARIA_CONVO_1", "PLAYER"),
    Event("CAMPAIGN_SHIP_ID", "PLAYER"),
    Event("WISPSHIP_GUARD_SHIP_ID", "PLAYER"),
    Event("Add_PUCC_Beacon_To_Ship", "PLAYER"),

    Label("Main"),
    Choice("Hia, what can I do for ya?", [
        [
            Response("I need you to do something... (Commands)"),
            Goto("Requests"),
        ],
        [
            Response("(More dialogue options coming soon!)"),
            End,
        ],
    ]),


    Label("Requests"),
    Choice("What can I do for ya?", [
        [
            Response("Please stop following or guarding the VAR(WISPSHIP_GUARD_ID) for now."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_GUARD_ID", any_value=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            
            "Acknowledged. We will wait here.",
            Event("WISPSHIP_STOP_GUARD", "PLAYER"),
        ],
        [
            Response("Guard our ship please."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_GUARD_ID", any_value=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),

            "Acknowledged. We'll look out for you.",
            Event("WISPSHIP_GUARD_SHIP_ID", "PLAYER"),
        ],
        [
            Response("About your cargo..."),
            AnyCondition("1"),
            *[check_cargo(t) for t in all_cargo_types],

            "We can jettison our cargo out the back of the ship.",
            Goto("cargo"),
        ],
        [
            Response("Can you send us your scrap?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_SCRAP_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_scrap"),
        ],
        [
            Response("Can you send us your missiles?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_MISSILES_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_missiles"),
        ],
        [
            Response("Can you send us your drones?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_DRONES_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_drones"),
        ],
        [
            Response("Can you mine asteroids for us?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SHOOT_ASTEROID", var_value=1),

            "Sure! Any asteroids we see are toast.",
            Event("WISPSHIP_SHOOT_ASTEROID_ON", "PLAYER"),
        ],
        [
            Response("Don't shoot asteroids any more please."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SHOOT_ASTEROID", var_value=1),

            "Understood.  We'll leave the asteroids alone.",
            Event("WISPSHIP_SHOOT_ASTEROID_OFF", "PLAYER"),
        ],
        [
            Response("Pick up any scrap and cargo you find."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SCAVENGE", var_value=1),

            "Sure, we'll collect any scrap or cargo we see.",
            Event("WISPSHIP_START_SCAVENGE", "NPC"),
        ],
        [
            Response("Please stop picking up scrap or cargo."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SCAVENGE", var_value=1),

            "We'll leave the scrap and cargo for you to pick up.",
            Event("WISPSHIP_STOP_SCAVENGE", "NPC"),
        ],
        [
            Response("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("Requests"),


    Label("cargo"),
    Choice("Would you like us jettison something?", [
        [
            Response("Jettison EVERYTHING from your cargo."),
            AnyCondition("1"),
            *[check_cargo(t) for t in all_cargo_types],

            "Okay, we've dumped everything from our cargo hold out the back.",
            Event("Aurora_Jet_ALL", "NPC"),
        ],
        [
            Response("Jettison your WEAPONS in your cargo."),
            AnyCondition("1"),

           *[check_cargo(t) for t in ["LASER_WEAPONS", "BEAM_WEAPONS", "MISSILE_WEAPONS"]],

            "The weapons have been jettisoned.",
            Event("Aurora_Jet_WEAPONS", "NPC"),
        ],

        *[[
            Response(f"Jettison your {cargo_type} in your cargo."),
            check_cargo(cargo_type),

            "The requested cargo has been jettisoned.",
            Event(f"Aurora_Jet_{cargo_type}", "NPC"),
        ] for cargo_type in [
            "WEAPONS_CONTROL", "CLOAKING", "SHIELDS", "REACTOR", "OXYGEN", "PILOTING", "TELEPORT", "CAPACITOR",
            "DOOR_CONTROL", "ENGINES", "HYPERDRIVE", "MEDICAL", "SENSORS",
        ]],

        [
            Response("Jettison your SHOPS in your cargo."),
            AnyCondition("1"),
            *[check_cargo(t) for t in ["REPAIR", "SYSTEMS_SHOP", "SHIPS_SHOP", "CONSUMABLES_SHOP", "SHIPYARD"]],

            "The requested cargo has been jettisoned.",
            Event("Aurora_Jet_SHOPS", "NPC"),
        ],
        [
            Response("That's it for cargo. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Response("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("cargo"),


    Label("give_scrap"),
    Choice("How much scrap would you like?", [
        *[[
            Response(f"{count} scrap please."),
            Condition("SHIP_SCRAP_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            "I've transferred the scrap to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_SCRAP", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_SCRAP", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Response("That's it for scrap. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Response("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("give_scrap"),


    Label("give_missiles"),
    Choice("How many missiles would you like?", [
        *[[
            Response(f"{count} missile{'s' if count > 1 else ''} please."),
            Condition("SHIP_MISSILES_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            f"I've transferred the missile{'s' if count > 1 else ''} to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_MISSILES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_MISSILES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Response("That's it for missiles. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Response("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("give_missiles"),


    Label("give_drones"),
    Choice("How many drones would you like?", [
        *[[
            Response(f"{count} drone{'s' if count > 1 else ''} please."),
            Condition("SHIP_DRONES_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            f"I've transferred the drone{'s' if count > 1 else ''} to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_DRONES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_DRONES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Response("That's it for drones. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Response("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("give_drones"),

]
#End Solaria Dialogue

#----------------------------------------------
#Left over dialogues
#Research: Event("STARWISP_RESEARCH_BABBLE_OFF", "PLAYER"),
#Upgrades: Event("STARWISP_UPGRADES_BABBLE_OFF", "PLAYER"),

#----------------------------------------------
#Debug Menu Definitions

Debug = [
    Choice("[ACTION]This starwisp seems to be working on a terminal.", [
        [
            Response("Hello?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISP_DEBUG", var_value=1),
            "[ACTION]The starwisp doesn't seem to acknowledge you or even sense you?",
            End,
        ],
        [
            Response("DEBUG MENU"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISP_DEBUG", var_value=1),
            Goto("Wisp_Debug_Menu"),
        ],
    ]),

    Label("Wisp_Debug_Menu"),
    Choice("DEBUG MENU:", [
        [
            Response("DEBUG: Special Gear"),

            "Adding special gear to your ship cargo.",
            Event("Debug_SpecialGear", "PLAYER"),
        ],
        [
            Response("DEBUG: Deck the Halls"),

            "Power overwhelming...",
            Event("Debug_Decked_Out", "PLAYER"),
        ],
        [
            Response("DEBUG: Spawn Asteroids"),

            "Asteroids!",
            Event("SPAWN_DEAD_SHIP_PART", "PLAYER"),
        ],
        [
            Response("DEBUG: Spawn Lots of Ships"),

            "Spawning a ton of random ships.",
            Event("WISP_DEBUG_SPAWN_SHIPS", "PLAYER"),
        ],
        [
            Response("DEBUG: Make me Aurora crew"),

            "You're now an honorary starwisp.",
            Event("Debug_Become_Crew", "PLAYER"),
        ],
        [
            Response("DEBUG: Jet TEST"),

            "Testing Jettison.",
            Event("WISP_DEBUG_Jet_TEST", "NPC"),
        ],
        [
            Response("DEBUG: Jettison your scrap."),

            "Jettisoning scrap...",
            Event("Aurora_Jet_Scrap", "NPC"),
        ],
        [
            Response("DEBUG: Jettison your missiles."),

            "Jettisoning missiles...",
            Event("Aurora_Jet_Missiles", "NPC"),
        ],
        [
            Response("DEBUG: Jettison your drones."),

            "Jettisoning drones...",
            Event("Aurora_Jet_Drones", "NPC"),
        ],
        [
            Response("DEBUG: Force Story Trigger"),

            Choice("Which Story Trigger?", [
                [
                    Response("Story 1 - Tutorial"),
                    "Story 1 Triggered",
                    Event("WISP_STORY_TRIGGER_1", "NPC"),
                ],
                [
                    Response("Story 2 - USC"),
                    "Story 2 Triggered",
                    Event("WISP_STORY_TRIGGER_2", "NPC"),
                ],
                [
                    Response("Story 3 - KEK"),
                    "Story 3 Triggered",
                    Event("WISP_STORY_TRIGGER_3", "NPC"),
                ],
                [
                    Response("Story 4 - Fought Bears"),
                    "Story 4 Triggered",
                    Event("WISP_STORY_TRIGGER_4", "NPC"),
                ],
                [
                    Response("Story 5 - Return to Kek with crystal"),
                    "Story 5 Triggered",
                    Event("WISP_STORY_TRIGGER_5", "NPC"),
                ],
                [
                    Response("Story 6 - EMP_Error Quest"),
                    "Story 6 Triggered",
                    Event("WISP_STORY_TRIGGER_6", "NPC"),
                ],
            ]),
        ],
    ]),
    Response("Debug Menu"),
    Goto("Wisp_Debug_Menu"),


]


dialogues = {
    "Vatish": Vatish,
    "Solaria": Solaria,
    "Debug": Debug,
}
