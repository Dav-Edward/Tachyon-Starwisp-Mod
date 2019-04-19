from diagen import *
#remove above line before compile. This just stils python linter from freaking out

vatish = [
    Choice("[ACTION]You see a catch a human fiddling with the reactor", [
        [
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "WISPSHIP_SPAWNED", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "HJ_TUTORIAL_STARTED", "var_value": "1"}),

            "[ACTION]Noticing you the person quickly withdraws from the reactor.",
            Response("Hello?"),
            "Oh, uh hi, I'm [NPC_NAME], I'm aware of the theft that recently took place.",
            Response("Of the prototype ship?"),
            "The alien technology in your 'prototype' ship.",
            "That technology is dangerous and must be tracked down.",
            "It never belonged to humans in the first place...",
            "But then of course humans reverse-engineered it into a weapon.",
            "This is a threat to all life in all known space.",
            "As such, we, the collective, decided to assist you,",
            "but only to destroy it. It's too dangerous.",
            Response("Collective? what are you talking about?"),
            "[ACTION]The human briefly reveals the form of a glowing orb before changing back to human appearance.",
            "We are starwisps. No time. Ask Solaria on the trip if you must.",
            "Our ship will guard the Falcon. Now go before you lose the trail.",
            Response("What ship?"),
            "[ACTION]The creature sends pulses of a beam of light out the window.",
            "[ACTION]In a flash a giant crystal ship warps in.",
            Event("SPAWN_WispShip", target="PLAYER"),
            Event("STARSHIP_CAPTAIN_BABBLE_ON", target="PLAYER"),
            Event("WISPSHIP_COMPLETE", target="PLAYER"),
            Event("WISPSHIP_GUARD_SHIP", target="PLAYER"),
            "A starship of our own design. Take haste, and good luck.",
            Response("Yes sir!..lady..thing."),
        ],
        [
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "HJ_TUTORIAL_STARTED", "var_value": "1"}),

            "[ACTION]They seems busy working on the reactor. Perhaps you should talk to the captain first.)",
        ],
        [
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WARSHIP_SPAWNED", "var_value": "1"}),

            "Well..go on. Get to your ship and contact Solaria on the comm and get on your way.",
        ],
        [
            Response("The Falcon already left.."),
            Condition("SECTOR_SHIPS_ABSENT", {"ship_name": "Falcon", "qty": "1"}),
            Condition("SECTOR_SHIPS_ABSENT", {"ship_name": "P.U.C.C", "qty": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "PUCC_BEACON_SECTOR_LOC", "any_value": "1"}),

            "The Falcon already left?",
            "Well.. in that case you better you better catch up with them",
            "If the Falcon is destroyed it's all over. There's a P.U.C.C ship just outside the station",
            "Now go! It's right outside!",
            Response("I'm ony my way!"),
        ],
        [
            Response("Send the P.U.C.C to the Aurora!"),
            Condition("SECTOR_SHIPS_PRESENT", {"ship_name": "P.U.C.C", "qty": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "PUCC_BEACON_SECTOR_LOC", "any_value": "1"}),
            Condition("SHIP_SYSTEM_ABSENT", {
                "system_type": "ENGINES", "system_model": "PUCC_Engines", "target_player": "1",
                "all_mob_ships": "0", "active_systems": "0", "qty": "1",
            }),

            Choice("Make sure you are INSIDE the P.U.C.C. First. Are you ready?", [
                [
                    Response("Wait, no! I'll get in the ship and claim it."),
                    End,
                ],
                [
                    Response("Yes, ready to go!"),
                    Condition("SECTOR_SHIPS_PRESENT",
                        {"target_players": "1", "ship_name": "P.U.C.C", "crew": "[PLAYER NAME]", "qty": "1"}
                    ),
                    Condition("SHIP_SYSTEM_ABSENT", {
                        "system_type": "ENGINES", "system_model": "PUCC_Engines", "target_player": "1",
                        "all_mob_ships": "0", "active_systems": "0", "qty": "1",
                    }),
                ],
            ]),
            "Good luck, this might be a long ride!",
            Response("Okay!"),
            Event("PUCC_Follow_Beacon", "PLAYER"),
        ],
        [
            Response("[SKIP](Beacon Lost)"),
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "PUCC_BEACON_SECTOR_LOC", "any_value": "1"}),

            "...Strange. I can't find any trace of the beacon we put on your ship.",
            "Without it I don't know where to send you.",
            "I'm afraid I can't help you without a beacon to guide us.",
            "(If the campaign ship was destroyed. It might be game over and reset the server.)",
        ],
    ]),
]


def check_cargo(system_type):
    return Condition("SHIP_CARGO_PRESENT",
        {"cargo_type": "SHIP_SYSTEM", "system_type": system_type, "target_player": "0", "qty": "1"}
    )

all_cargo_types = [
    "LASER_WEAPONS", "BEAM_WEAPONS", "MISSILE_WEAPONS", "SHIELDS", "REACTOR", "OXYGEN", "PILOTING", "TEELEPORT",
    "CAPASITOR", "DOOR_CONTROL", "ENGINES", "HYPERDRIVE", "MEDICAL", "SENSORS", "REPAIR", "SYSTEMS_SHOP",
    "SHIP_SHOP", "CONSUMABLES_SHOP", "SHIPYARD"
]

solaria = [
    Label("start"),
    Choice("[ACTION]You see a white wispy creature surrounded by screens.", [
        [
            Response("...Hello?"),
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            Choice("[ACTION]The creature speaks in a surpringly human female voice", [
                [
                    Condition("SERVER_SECTOR_SHIPS_ABSENT", {"target_player": "1", "owner": "[PLAYER NAME]", "qty": "1"}),
                    "...I would like to speak to the captian. If you haven't claimed your ship, cliam it then contact me again.",
                    End
                ],
                [
                    Condition("SERVER_SECTOR_SHIPS_PRESENT", {"target_player": "1", "owner": "[PLAYER NAME]", "qty": "1"}),
                ]
            ]),
            "Hello [SHIP_NAME], I'm Solaria, captian of the starship Aurora...",
            "Our ship will follow and guard you as best we can...",
            "and our researcher Donis will develop technology on the way.",
            "Call me on the comms if you have any orders",
            Response("Understood. Thanks for the help."),
            Event("SOLARIA_CONVO_1", "PLAYER"),
            Event("Add_PUCC_Beacon_To_Ship", "PLAYER"),
            End
        ],
        [
            Response("Stop following us for now."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WISPSHIP_GUARD_FALCON", "var_value": "1"}),

            "Acknowledged. We will wait here.",
            Event("WISPSHIP_STOP_GUARD", "PLAYER"),
        ],
        [
            Response("Guard our ship please."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WISPSHIP_GUARD_FALCON", "var_value": "0"}),

            "Acknowledged. We'll guard your ship.",
            Event("WISPSHIP_STOP_GUARD", "PLAYER"),
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
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SHIP_CARGO_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": "1"}),
            Condition("SECTOR_SHIPS_PRESENT", {"ship_name": "Falcon", "qty": "1"}),
            Condition("SHIP_HULL_PRESENT", {"target_player": "1", "all_mob_ships": "0", "qty": "1"}),
            Goto("give_scrap"),
        ],
        [
            Response("Can you send us your missiles?"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SHIP_MISSILES_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": "1"}),
            Condition("SECTOR_SHIPS_PRESENT", {"ship_name": "Falcon", "qty": "1"}),
            Condition("SHIP_HULL_PRESENT", {"target_player": "1", "all_mob_ships": "0", "qty": "1"}),
            Goto("give_missiles"),
        ],
        [
            Response("Can you send us your drones?"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SHIP_DRONES_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": "1"}),
            Condition("SECTOR_SHIPS_PRESENT", {"ship_name": "Falcon", "qty": "1"}),
            Condition("SHIP_HULL_PRESENT", {"target_player": "1", "all_mob_ships": "0", "qty": "1"}),
            Goto("give_drones"),
        ],
        [
            Response("Shoot Asteroids for us please."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "WISPSHIP_SHOOT_ASTEROID", "var_value": "1"}),

            "Acknowledged. Any asteroids we see are toast.",
            Event("WISPSHIP_SHOOT_ASTEROID_ON", "PLAYER"),
        ],
        [
            Response("Don't shoot asteroids any more please."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WISPSHIP_SHOOT_ASTEROID", "var_value": "1"}),

            "Understood.  We'll leave the asteroids alone.",
            Event("WISPSHIP_SHOOT_ASTEROID_OFF", "PLAYER"),
        ],
        [
            Response("Pick up any scrap you find."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_ABSENT", {"var_name": "WISPSHIP_SCAVENGE", "var_value": "1"}),

            "Sure, we'll collect any scrap we see.",
            Event("WISPSHIP_START_SCAVENGE", "NPC"),
        ],
        [
            Response("Please stop picking up scrap."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WISPSHIP_SCAVENGE", "var_value": "1"}),

            "We'll leave the scrap for you then.",
            Event("WISPSHIP_STOP_SCAVENGE", "NPC"),
        ],
    ]),
    Event("STARWISP_CAPTAIN_BABBLE_OFF", "PLAYER"),
    Goto("start"),


    Label("cargo"),
    Choice("Would you like us jettison something?", [
        [
            Response("Jettison everything from your cargo,"),
            AnyCondition("1"),
            *[check_cargo(t) for t in all_cargo_types],

            "The requested cargo has been jettisoned.",
            Event("Aurora_Jet_ALL", "NPC"),
        ],
        [
            Response("Jettison your WEAPONS in your cargo."),
            AnyCondition("1"),

           *[check_cargo(t) for t in ["LASER_WEAPONS", "BEAM_WEAPONS", "MISSILE_WEAPONS"]],

            "The requested cargo has been jettisoned.",
            Event("Aurora_Jet_WEAPONS", "NPC"),
        ],

        *[[
            Response(f"Jettison your {cargo_type} in your cargo"),
            check_cargo(cargo_type),

            "The requested cargo has been jettisoned.",
            Event(f"Aurora_Jet_{cargo_type}", "NPC"),
        ] for cargo_type in [
            "SHIELDS", "REACTOR", "OXYGEN", "PILOTING", "TEELEPORT", "CAPASITOR",
            "DOOR_CONTROL", "ENGINES", "HYPERDRIVE", "MEDICAL", "SENSORS", "REPAIR",
        ]],

        [
            Response("Jettison your SHOPS in your cargo."),
            AnyCondition("1"),
            *[check_cargo(t) for t in ["SYSTEMS_SHOW", "SHIPS_SHOP", "CONSUMABLES_SHOP", "SHIPYARD"]],

            "The requested cargo has been jettisoned.",
            Event("Aurora_Jet_SHOPS", "NPC"),
        ],

        # No "I don't want to jettison" option?  Well I guess
        # you'll be jettisoning everything and then some...
    ]),
    Goto("cargo"),


    Label("give_scrap"),
    Choice("How much scrap would you like?", [
        *[[
            Response(f"{count} scrap please."),
            Condition("SHIP_SCRAP_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": f"{count}"}),

            "I've transferred the scrap to your ship",
            Event(f"WISPSHIP_TAKE_{count}_SCRAP", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_SCRAP", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 1]],

        [
            Response("(Main Menu)"),
            Goto("start"),
        ]
    ]),
    Goto("give_scrap"),


    Label("give_missiles"),
    Choice("How many missiles would you like?", [
        *[[
            Response(f"{count} missile{'s' if count > 1 else ''} please."),
            Condition("SHIP_MISSILES_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": f"{count}"}),

            f"I've transferred the missile{'s' if count > 1 else ''} to your ship",
            Event(f"WISPSHIP_TAKE_{count}_MISSILES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_MISSILES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 1]],

        [
            Response("(Main Menu)"),
            Goto("start"),
        ]
    ]),
    Goto("give_missiles"),


    Label("give_drones"),
    Choice("How many drones would you like?", [
        *[[
            Response(f"{count} drone{'s' if count > 1 else ''} please."),
            Condition("SHIP_DRONES_PRESENT", {"target_player": "0", "all_mob_ships": "0", "qty": f"{count}"}),

            f"I've transferred the drone{'s' if count > 1 else ''} to your ship",
            Event(f"WISPSHIP_TAKE_{count}_DRONES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_DRONES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 1]],

        [
            Response("(Main Menu)"),
            Goto("start"),
        ]
    ]),
    Goto("give_drones"),
]

research = [
    Choice("[ACTION]blah blah", [
        [
            Response("...okay"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "message id M1 is missing in the source",
        ],
        [
            Response("DEBUG MENU"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "WISP_DEBUG_LOCKOUT", "var_value": "1"}),
            Goto("wisp_debug_menu"),
        ],
    ]),
    Event("STARWISP_RESEARCH_BABBLE_OFF", "PLAYER"),
    End,

    # Why, when this menu cannot be entered without SOLARIA_CONVO_1, does every item in it check for it?
    Label("wisp_debug_menu"),
    Choice("DEBUG MENU:", [
        [
            Response("...okay"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "message id M1 is missing in the source",
        ],
        [
            Response("DEBUG: Spawn Asteroids"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Asteroids!",
            Event("SPAWN_DEAD_SHIP_PART", "PLAYER"),
        ],
        [
            Response("DEBUG: Spawn Lots of Ships"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Spawning a ton of random ships.",
            # Event("WISP_DEBUG_SPAWN_SHIPS"), # XXX Huh? No target?
        ],
        [
            Response("DEBUG: Jet TEST"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Testing Jettison.",
            # Event("WISP_DEBUG_Jet_TEST"), # XXX Huh? No target?
        ],
        [
            Response("DEBUG: Boarding Drone"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Adding Boarding Drones to your ship cargo.",
            Event("Debug_BoardingDrone", "PLAYER"),
        ],
        [
            Response("DEBUG: Jettison your scrap."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Jettisoning scrap...",
            Event("Aurora_Jet_Scrap", "NPC"),
        ],
        [
            Response("DEBUG: Jettison your missiles."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Jettisoning missiles...",
            Event("Aurora_Jet_Missiles", "NPC"),
        ],
        [
            Response("DEBUG: Jettison your drones."),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

            "Jettisoning drones...",
            Event("Aurora_Jet_Drones", "NPC"),
        ],
        [
            Response("DEBUG: Force Story Trigger"),
            Condition("SERVER_VARIABLE_PRESENT", {"var_name": "SOLARIA_CONVO_1", "var_value": "1"}),

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
                    Response("Story 4 - Faught Bears"),
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
]

dialogues = {
    "Vatish": vatish,
    "Solaria": solaria,
    "STARWISP_RESEARCH": research,
    "STARWISP_UPGRADES": [
        "[ACTION]blah blah",
        Response("...okay"),
        Event("STARWISP_UPGRADES_BABBLE_OFF", "PLAYER"),
        "message id M1 is missing in the source",
    ],
}
