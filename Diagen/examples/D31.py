# Recreation of the WorldGen/Dialogues/D31.xml file from release a0819
# as a Tachyon Diagen script

from itertools import chain


# Shorthand for adding tutorial skip
def skippable(message):
    return Choice(message, [
        [],
        [Reply("I would like to skip the tutorial."), Goto("Skip")],
    ])

# Shorthand for hyperdrive test
def hyperdrive_condition(state, model, player):
    return Condition(
        f"SHIP_CARGO_{state}", cargo_type="SHIP_SYSTEM", system_model=model, target_player=player, qty=1
    )

dialogues = {
    "TUTORIAL": [
        Choice("[ACTION]You see a Human in a torn and burned space suit, with some blood stains...", [
            #[
            #    Reply("Run test event with player as target"),
            #
            #    "Executing test event, targeted at player!",
            #    Event("RUN_TEST", "PLAYER"),
            #    Reply("Thanks"),
            #],
            #[
            #    Reply("Run test event with npc as target"),
            #
            #    "Executing test event, targeted at npc!",
            #    Event("RUN_TEST", "NPC"),
            #    Reply("Thanks"),
            #],
            [
                Condition("SERVER_VARIABLE_ABSENT", var_name="TUTORIALS_STARTED", var_value=1),

                *[
                    skippable(item) if type(item) is str else item
                    for item in [
                        "Thank God! I thought I was the only survivor!",
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_STOP_CALLING_HELP", var_value=1),
                        Reply("Who are you?"),
                        "I'm [NPC_NAME], the captain of this station...  Well what's left of it...",
                        Reply("What happened here?"),
                        "You're [PLAYER_NAME] right? Don't you remember anything?",
                        Reply("No. I don't!"),
                        "Damn. The clone replication system must have been damaged.",
                        "This is the D31 Science station. You are posted here as one of the guards.",
                        "We were attacked by pirates, and they have stolen one of our prototype ships!",
                        "We need to report this to the Unity Science Centre. ASAP!",
                        "Problem is that the pirates have taken out our communications system.",
                        "We need to think of a way to get the message to the USC.",
                        Reply("How can I help?"),
                    ]
                ],

                Choice("Please repair all systems you can.", [
                    [
                        Reply("How do I repair stuff, or put out fires?"),
                        "Just walk into the room with a damaged system and it will auto repair.",
                        "Same thing with the hull breach, just stand on top of it, and it will auto repair.",
                        "To put out fire just stand on top of it and it will auto extinguish.",
                    ],
                    [Reply("I'm on it")],
                ]),
                "Thanks. Speak to me when you're done.",
                InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="TUTORIALS_STARTED", var_value=1),
                InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="REPAIR_TUTORIAL_STARTED", var_value=1),
                End,

                Label("Skip"),
                Choice("Are you sure?", [
                    [Reply("I changed my mind.  Teach me oh great master!"), Goto("M0")],
                    [
                        Reply("Yes.  let's go!"),

                        "Ok. Don't forget to power up the systems!",
                        InlineEvent("MODIFY_SHIP", "PLAYER",
                            for_ship_name="VAR(PLAYER_SHIP_NAME)", add_crew="[PLAYER_NAME]", set_owner="[PLAYER_NAME]",
                        ),
                        Event("SPAWN_USC", "PLAYER"),
                        Event("MAKE_USC_SECTOR_EXPLORED", "PLAYER"),
                        InlineEvent("MODIFY_SHIP", "NPC", put_out_fires=1),
                        Event("SKIP_TUTORIAL", "PLAYER"),
                        InlineEvent("MODIFY_SHIP", "NPC",
                            repair_breaches=1, repair_system_model="REPAIR1",
                            repair_system_type=["OXYGEN", "SHEILDS", "CAPASITOR", "LASER_WEAPONS"],
                            remove_system_type="LASER_WEAPONS"
                        ),
                        Goto("HJ"),
                    ],
                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="REPAIR_TUTORIAL_STARTED", var_value=1),

                Choice("Oh it's you [PLAYER_NAME].  Have you already finished all the repairs?", [
                    [
                        Reply("I've fixed all the systems and breaches I could reach."),
                        *[
                            Condition("SHIP_SYSTEM_PRESENT", system_type=system, active_system=1, qty=qty)
                            for system, qty in [
                                ("OXYGEN", 2), ("CAPACITOR", 4), ("REPAIR", 1), ("LASER_WEAPONS", 1), ("SHIELDS", 1),
                            ]
                        ],

                        "Excellent! And I have a plan how we can get that message to USC!",
                        Reply("How?"),
                        "Our second prototype ship, it's badly damaged but still operational.",
                        "I want you to go and repair it. And I suggest you start with the REACTOR.",
                        "Also keep an eye on your oxygen level. Because that ship probably has no O2.",
                        "After you have repaired it, I want you to take control of it and talk to me again.",
                        "You can use the Comms on the ship if you want.",
                        Choice("Meanwhile I want to check something in the Sensors room.", [
                            [Reply("OK.")],
                            [Reply("How do I claim a ship for my self?"), Goto("CL_HOWTO")],
                        ]),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="REPAIR_TUTORIAL_STARTED", var_value=1),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="CLAIM_TUTORIAL_STARTED", var_value=1),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_GO_TO_SENSORS", var_value=1),
                    ],
                    [
                        Reply("No, not yet.", any_condition=1),
                        *[
                            Condition("SHIP_SYSTEM_ABSENT", system_type=system, active_system=1, qty=qty)
                            for system, qty in [
                                ("OXYGEN", 2), ("CAPACITOR", 2), ("REPAIR", 1), ("LASER_WEAPONS", 1),
                            ]
                        ],

                        "Please speak to me again when you're done fixing.",
                        Reply("Ok."),
                    ],
                    [
                        Reply("Can you please remind me how to do repairs?"),

                        "Just walk into the room with a damaged system.",
                        "To put out fire just stand on top of it",
                        Reply("Thanks!"),
                    ],
                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="CLAIM_TUTORIAL_STARTED", var_value=1),

                Choice("Hello [PLAYER_NAME].  Are you now a captain or crew on a ship?", [
                    [
                        Reply("Yes, I am now port of a ship crew."),
                        Condition("SHIP_SYSTEM_PRESENT", target_player=1, system_type="PILOTING", qty=1),

                        "Good.  Let's see now... ",
                        "The Second prototype ship is near death. You'll never be able to reach USC like this.",
                        "Not to mention that the Hyper drive is missing completely!",
                        Reply("What do we do then?"),
                        "Well at least the engine is intact. ",
                        "Let me run a sector scan with the Sensors.",
                        "Maybe there's an HD in one of the debris fields.",
                        "Hmm... No luck.  But I see there are several broken ones.",
                        "Perhaps we can assemble a working one from all the broken pieces.",
                        "I see there's a Tachyon Stabilizer, Accelerator and Chamber floating in space.",
                        "I want you to pilot the second prototype ship and recover these parts for me.",
                        "With them I think I will be able to assemble a new Hyper drive for you.",

                        Choice("Look for me in the LASER WEAPON room when you are done.", [
                            [Reply("Great. I'll get right on it.")],
                            [Reply("Can you remind me how to pilot a ship within the sector?"), Goto("LJ_HOWTO")],
                            [Reply("How do I pick up debris and cargo in space?"), Goto("PICK_HOWTO")],
                            [Reply("How do I find items in space?"), Goto("FIND_HOWTO")],
                        ]),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="CLAIM_TUTORIAL_STARTED", var_value=0),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="LJ_TUTORIAL_STARTED", var_value=1),

                        InlineEvent("SPAWN_DEBRIS", "PLAYER"),
                        *chain(*[
                            [
                                AddDebris(qty=1, owner="Science  station  D31", random_pos=1),
                                Item(item_type="SHIP_SYSTEM", system_model=part),
                            ]
                            for part in ["TACSTAB", "TACCHAMB", "TACACC"]
                        ]),

                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_GO_TO_SENSORS", var_value=0),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_GO_TO_LASERS", var_value=1),
                    ],
                    [
                        Reply("No, not yet"),
                        Condition("SHIP_SYSTEM_ABSENT", target_player=1, system_type="PILOTING", qty=1),

                        "Well, what are you waiting for?  Go do it!",
                        Reply("OK. I'm on it"),
                    ],
                    [
                        Reply("Please remind me how to claim a ship or add crew."),

                        Label("CL_HOWTO"),
                        "You need to go to the PILOTING room, and open the system interface.",
                        "To open the system interface press SPACE.  There open the CREW page.",
                        "If a ship has no owner/captain, then there will be a CLAIM button.",
                        "When you are the captain of the ship you can add more crew to it.",
                        "To do that - press the ADD CREW button and input the name.",
                        "When the crew member is not present in the sector it shows - NO DATA",
                        "That's pretty much it.",
                        Reply("Thanks!"),
                    ],
                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="LJ_TUTORIAL_STARTED", var_value=1),

                Choice("Hi [PLAYER_NAME].  Did you recover the Hyper Drive parts?", [
                    [
                        Reply("Yes. All Hyper Drive parts are transferred to the station."),
                        hyperdrive_condition("PRESENT", "TACSTAB", 0),
                        hyperdrive_condition("PRESENT", "TACCHAMB", 0),
                        hyperdrive_condition("PRESENT", "TACACC", 0),

                        "Great work [PLAYER_NAME]!  I will start assembling the new HD right away.",
                        "Meanwhile you can do some hull repairs for the second prototype ship.",
                        "On this station there's a repair system.",
                        "But you will need some scrap metal to use it.",
                        Reply("Where can I get scrap?"),
                        "When a ship or an asteroid is blown up, there will be some scrap left.",
                        "I will uninstall the station's laser and send it to your ship, so you can use it.",
                        Choice("Install the laser, blow up asteroids and repair the ship.", [
                            [Reply("Will do.")],
                            [Reply("Wait, how do I install or uninstall systems on the ship?"), Goto("INST_HOWTO")],
                            [Reply("Wait, I don't know how to use weapons!"), Goto("SHOOT_HOWTO")],
                        ]),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="LJ_TUTORIAL_STARTED", var_value=0),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="INST_TUTORIAL_STARTED", var_value=0),

                        InlineEvent("SPAWN_SHIP", "PLAYER", random_ship=1, min_event_qty=3, max_event_qty=3),
                        AddShip(
                            gen_ship_model=[f"ASTEROID{i}" for i in range(1, 20)],
                            ship_name="Asteroid", random_pos=1, min_health=2,
                            max_health=3, min_scrap=120, max_scrap=120
                        ),

                        InlineEvent("MODIFY_SHIP", "NPC",
                            for_ship_name="Science  station  D31", remove_system_type="LASER_WEAPONS"
                        ),
                        InlineEvent("MODIFY_SHIP", "PLAYER",
                            for_ship_name="VAR(PLAYER_SHIP_NAME)", add_system_model_to_cargo="Triple_laser1"
                        ),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_GO_TO_SENSORS", var_value=1),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="SS31_GO_TO_LASERS", var_value=0),
                    ],
                    [
                        Reply("Yes, I have the Tachyon Stabilizer on my ship."),
                        hyperdrive_condition("PRESENT", "TACSTAB", 1),

                        Label("DROP_HD"),
                        Choice("Excellent! Please drop it off into the station.", [
                            [Reply("OK."), End],
                            [Reply("How do I do that?")],
                        ]),

                        "Open the PILOTING system interface and go to the CARGO page.",
                        "There you will see all your ship's cargo.  Click the one you want to jettison,",
                        "then select a direction in which you want to jettison the cargo box.",
                        "To do that you need to click the button that looks like a direction arrow.",
                        "It is located near the JET. CARGO button.  When you click it, it will change the direction.",
                        "So if the station is below your ship, then select direction DOWN.",
                        "Then press the JET. CARGO button to throw the cargo box out and it will fly in that direction.",
                        Reply("OK. Thanks!"),
                    ],
                    [
                        Reply("Yes, I have the Tachyon Chamber on my ship."),
                        hyperdrive_condition("PRESENT", "TACCHAMB", 1),
                        Goto("DROP_HD"),
                    ],
                    [
                        Reply("Yes, I have the Tachyon Accelerator on my ship."),
                        hyperdrive_condition("PRESENT", "TACACC", 1),
                        Goto("DROP_HD"),
                    ],
                    [
                        Reply("No, not yet."),
                        hyperdrive_condition("ABSENT", "TACSTAB", 1),
                        hyperdrive_condition("ABSENT", "TACCHAMB", 1),
                        hyperdrive_condition("ABSENT", "TACACC", 1),

                        "Please don't waste any time. It is of the essence.",
                    ],
                    [
                        Reply("Can you remind me how to pilot a ship within the sector?"),

                        Label("LJ_HOWTO"),
                        "Open the PILOTING system interface and go to SECTOR MAP page.",
                        "Or go to the ENGINES room and open the ENGINES system interface.",
                        "On the bottom you will see the Engines energy meter and power bars.",
                        "Left click on the power bars to divert some power to the engines.",
                        "Right click to de-power. Once the energy meter is full - you can jump.",
                        "Left click somewhere on the radar map where you want to move your ship.",
                        "Then press the JUMP button.  And away you go!",
                        "Don't forget to upgrade your engines to be able to charge them faster.",
                        Reply("Thanks!"),
                    ],
                    [
                        Reply("How do I pick up debris and cargo in space?"),

                        Label("PICK_HOWTO"),
                        "You can jump on top of them with your ship.",
                        "Or you can fly out in space through an airlock, approach the debris, ",
                        "and then press the debris button (SPACE) to grab it. Then haul it back to the ship.",
                        "Also most debris will be attracted to the ship if they are close enough.",
                        Reply("Thanks."),
                    ],
                    [
                        Reply("How do I find items in space?"),

                        Label("FIND_HOWTO"),
                        "On the sector map debris and cargo boxes are shown as orange dots.",
                        "And on the target map the cargo box looks like a box rather some scrap metal.",
                        Reply("Thanks."),
                    ],

                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="INST_TUTORIAL_STARTED", var_value=1),
                Choice("[PLAYER_NAME], Have you repaired the ship's hull?", [
                    [
                        Reply("No, not yet."),
                        Condition("SHIP_HULL_ABSENT", target_player=1, qty=50),

                        "Please hurry up and repair the ship.",
                        Reply("I'm on it."),
                    ],
                    [
                        Reply("Yes, the ship is fully repaired."),
                        Condition("SHIP_HULL_PRESENT", target_player=1, qty=50),

                        "Perfect timing [PLAYER_NAME]!",
                        "Sensors have detected an incomming ship signature.",
                        "It must be the pirates' salvage team, comming to finish us up!",
                        "Use the laser I gave you, and blow them to space dust!",
                        "Speak to me again when the pirates are dealt with.",
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="LJ_TUTORIAL_STARTED", var_value=0),
                        InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="FIGHT_TUTORIAL_STARTED", var_value=1),
                        Event("SPAWN_TUT_PIRATE", "PLAYER"),
                        Reply("I'm on it!"),
                    ],
                    [
                        Reply("Please remind me how to install and uninstall systems"),

                        Label("INST_HOWTO"),
                        "To uninstall a system - Open the PILOTING interface and go to the SYSTEMS page",
                        "There you will see the layout of the ship.  Click on a system you want to unsinstall,",
                        "then click the UNINSTALL button on the bottom left.  And it will be moved to your cargo hold.",
                        "If your cargo hold is full though, the system will be jettisoned into outer space.",
                        "Be careful, when you uninstall a system, it looses any upgrades it had.",
                        "And some systems can't be uninstalled without breaking and loosing them.",
                        Reply("OK. Got it."),

                        "To install a system - Open the PILOTING interface and go to the CARGO page",
                        "There you will see all the cargo that you have.  Click on the system that you want to install,",
                        "Then click on the INSTALL button on the bottom left.",
                        "A window will appear, where you can select the place to install the system.",
                        "Click the top left corner of any room to install a system in it.",
                        "On the bottom of the ship layout window there's a button that rotates the system.",
                        Reply("OK. Thanks."),
                    ],
                    [
                        Reply("Can you tell me how to shoot weapons?"),
                        Goto("SHOOT_HOWTO"),
                    ],
                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="FIGHT_TUTORIAL_STARTED", var_value=1),
                Condition("SECTOR_SHIPS_PRESENT", qty=3),

                Choice("What are you still doing here?!  Go blow up that pirate!", [
                    [Reply("I'm working on it.")],
                    [
                        Reply("I forgot how to shoot!"),

                        Label("SHOOT_HOWTO"),
                        "There are two ways to shoot your weapons,",
                        "First way is to man the weapon itself:",
                        "To do that you need to go into the room where the weapon is installed,",
                        "and open the system interface.",
                        "There you will see 2 screens: Radar screen and Target screen.",
                        "On the Radar screen you can see all the ships and space ojects in the sector.",
                        "On the target screen you see the ships in detail, with their systems and stats.",
                        "To shoot, you need to power the weapon, let it charge to full,",
                        "Then click a spot on the target map, and a croshair will appear there.",
                        "Then you just press the FIRE button and it's done.",
                        "You can see the projectiles traveling on the Radar map.",
                        Reply("And the second way?"),
                        "Second way is to man the WEAPONS CONTROL system.",
                        "Go to the WEAPONS CONTROL room and open the system interface.",
                        "It is almost the same as the WEAPON system interface,",
                        "but from here you can shoot any weapon on the ship.",
                        "Under the Radar map screen you will see a bar with all available weapons.",
                        "To shoot you first need to select which weapon you want to aim.",
                        "Click on the icon of the weapon you need and then select the target.",
                        "To fire each weapon individually you can press their own small FIRE button.",
                        "To fire all ready weapons at the same time, press the FRIE ALL button.",
                        Reply("Thanks."),
                    ],
                ]),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="FIGHT_TUTORIAL_STARTED", var_value=1),
                Condition("SECTOR_SHIPS_ABSENT", qty=3),

                "Great work destroying those pirates [PLAYER_NAME]!",
                Reply("Yeah, that wasn't so hard."),

                Choice("I've finished assembling the new HYPER DRIVE for you.", [
                    [
                        Reply(any_condition=1),
                        Condition("SERVER_VARIABLE_PRESENT", var_name="PLAYER_CREW_SPAWNED", var_value=1),
                        Condition("SECTOR_PLAYERS_PRESENT", qty=3),
                    ],
                    [
                        Condition("SERVER_VARIABLE_ABSENT", var_name="PLAYER_CREW_SPAWNED", var_value=1),
                        Condition("SECTOR_PLAYERS_ABSENT", qty=3),
                        Condition("SECTOR_PLAYERS_PRESENT", qty=2),

                        "I've also managed to assemble some repair droids for you.",
                        Event("SPAWN_NPC_CREW_2", "PLAYER"),
                        Reply("That's even better!"),
                    ],
                    [
                        Condition("SERVER_VARIABLE_ABSENT", var_name="PLAYER_CREW_SPAWNED", var_value=1),
                        Condition("SECTOR_PLAYERS_ABSENT", qty=2),

                        "I've also managed to assemble some repair droids for you.",
                        Event("SPAWN_NPC_CREW_3", "PLAYER"),
                        Reply("That's even better!"),
                    ],
                ]),
                Reply("That's great news!"),
                Choice("I will send the new Hyperdrive to the your ship's cargo hold.", [
                    [
                        Condition("SERVER_VARIABLE_ABSENT", var_name="USC_SPAWNED", var_value=1),

                        "Install the Hyper Drive and travel to the USC station in sector [SECTOR].",
                        Event("SPAWN_USC", "PLAYER"),
                        Event("MAKE_USC_SECTOR_EXPLORED", "PLAYER"),
                    ],
                    [
                        Condition("SERVER_VARIABLE_PRESENT", var_name="USC_SPAWNED", var_value=1),

                        "Install the Hyper Drive and travel to the USC station in sector VAR(USC_SECTOR).",
                    ],
                ]),
                Reply("Thanks"),
                Choice("There you will need to find Dr. Darius Graydon, and tell him what happened here.", [
                    [Reply("I will get right on it.")],
                    [Reply("Can you tell me how to do Hyper jumps?"), Goto("HJ_HOWTO")],
                ]),
                InlineEvent("MODIFY_SHIP", "PLAYER",
                    for_ship_name="VAR(PLAYER_SHIP_NAME)", add_system_model_to_cargo="FALCON_HD"
                ),
                InlineEvent("MODIFY_SHIP", "NPC",
                    for_ship_name="Science  station  D31", remove_system_type_from_cargo=["LASER_WEAPONS", "CAPACITOR"],
                    add_system_model_to_cargo="FIRE_BEAM5", safe_zone=0,
                ),
                InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="FIGHT_TUTORIAL_STARTED", var_value=0),
                InlineEvent("SERVER_VARIABLE", "PLAYER", var_name="HJ_TUTORIAL_STARTED", var_value=1),
            ],
            [
                Condition("SERVER_VARIABLE_PRESENT", var_name="HJ_TUTORIAL_STARTED", var_value=1),

                Label("HJ"),
                Choice("Please find Dr. Darius Graydon, at USC in sector VAR(USC_SECTOR)", [
                    [Reply("I'm on my way.")],
                    [
                        Reply("Please remind me ho to do Hyper jumps."),

                        Label("HJ_HOWTO"),
                        "To do a hyper jump, open the PILOTING interface and go to the STAR MAP page.",
                        "There you can see all the stars and empy space sectors.",
                        "The ship icon will indicate in which sector you are located right now.",
                        "You can see the glowing circles indicating what sectors you can reach.",
                        "The range depends on your Hyper Drive power and level and the class of your ship.",
                        "On the bottom of the screen you can see the Hyper Drive power bars and energy level.",
                        "Add some power to the Hyper Drive and see the energy bar filling up.",
                        "As the Hyper drive charges more energy, you will see glowing circles getting blue color.",
                        "Blue circles indicate the sectors that you can jump to with current stored energy.",
                        "Select a destination sector from one of the blue circles, then click the SET TARGET button.",
                        "Then press the HYPER JUMP button, and away you go, into the hyper space.",
                        Reply("Thanks!"),
                    ],
                ]),
            ],
        ]),
    ],
}


events = [
    EventDef("SPAWN_SHIP", "SPAWN_D31",
        sector="VAR(STARTING_SECTOR)",
        chain_event=[
            "SPAWN_PLAYER_SHIP", "MAIN_SPIKE",
            # "SPAWN_CUSTOM_PLAYER_SHIP",
        ],
    ),

    AddShip(
        gen_ship_model="SS_D31", free_doors=1, free_med=1, free_oxygen=1, safe_zone=1, free_sensors=1,
        ship_name="Science  station  D31", pos="6000:6000", min_health=10, max_health=20
    ),
    *[Ai(t) for t in ["LIFE_SUPPORT", "EVADER", "ENEMY_SHOOTER", "TRADER"]],

    SpawnNPC(
        qty=1, is_captain=1, random_name=1, race="HUMAN", home_system="DOOR_CONTROL",
        spawn_at_home=1, dialogue="TUTORIAL", remote_dialogue="TUTORIAL"
    ),
    Ai("NPC_TALKER",
        timer=15, ship=1, rand=1, mes=[
            "Hello? Can anyone hear me?",
            "If anyone can hear me, please come to the Door control room!",
            "Somebody please help!",
            "Press F1 if you don't know how to move.",
            "Oh, I hope that beam in the cargo hold didn't burn up...",
            "What a mess...",
            "How did I get into this mess...",
        ]
    ),
    Condition("SERVER_VARIABLE_ABSENT", var_name="SS31_STOP_CALLING_HELP", var_value=1),

    Ai("NPC_LIFESUPPORT"),

    Ai("NPC_DEFENDER"),
    Condition("SERVER_VARIABLE_PRESENT", var_name="HJ_TUTORIAL_STARTED", var_value=1),

    Ai("NPC_WORKER", systems="SENSORS", work_time=30, any_condition=0),
    Condition("SERVER_VARIABLE_PRESENT", var_name="SS31_GO_TO_SENSORS", var_value=1),

    Ai("NPC_WORKER", systems="LASER_WEAPONS", work_time=30, any_condition=0),
    Condition("SERVER_VARIABLE_PRESENT", var_name="SS31_GO_TO_LASER", var_value=1),


    EventDef("SPAWN_SHIP", "SPAWN_PLAYER_SHIP", chain_events_to_created=1, chain_event="PREPARE_PLAYER_SHIP"),
    AddShip(gen_ship_model="FALCON", ship_name="VAR(PLAYER_SHIP_NAME)", pos="6000:6900", min_health=50, max_health=50),

    EventDef("SPAWN_SHIP", "SPAWN_CUSTOM_PLAYER_SHIP",
        chain_events_to_created=1, chain_event=["PREPARE_CUSTOM_PLAYER_SHIP", "PREPARE_PLAYER_SHIP"]
    ),
    AddShip(gen_ship_model="FALCON", ship_name="VAR(PLAYER_SHIP_NAME)", pos="6000:6900", min_health=50, max_health=50),

    EventDef("MODIFY_SHIP", "PREPARE_CUSTOM_PLAYER_SHIP",
        install_system_model=[
            "PILOTING1", "FALCON_SHIELDS", "FALCON_REACTOR", "FALCON_ENGINES", "WEAPONS_CONTROL1",
            "FALCON_SENSORS", "CAPACITOR1", "MEDICAL1", "FALCON_O2", "FALCON_DC",
        ]
    ),

    EventDef("MODIFY_SHIP", "PREPARE_PLAYER_SHIP",
        safe_zone=0, take_hull=45,
        break_system_type=[
            "PILOTING", "SHIELDS", "REACTOR", "ENGINES", "WEAPONS_CONTROL",
            "SENSORS", "CAPACITOR", "MISSILE_WEAPONS", "MEDICAL",
        ],
        add_system_model_to_cargo="Basic_ML1"

        # add_system_model_to_cargo="SHIPYARD", give_scrap=1000, give_drones=100,
        # add_system_model_to_cargo="CLOAK1", add_system_model_to_cargo="TELEPORT2",
    ),

    EventDef("SPAWN_NPC", "SPAWN_NPC_CREW_2",
        nonstop=1, min_event_qty=1, max_event_qty=1, chain_event="PLAYER_CREW_SPAWNED",
        for_ship_name="VAR(PLAYER_SHIP_NAME)", random_npc=0,
    ),
    Condition("SERVER_VARIABLE_ABSENT", var_name="PLAYER_CREW_SPAWNED", var_value=1),
    Condition("SECTOR_PLAYERS_ABSENT", qty=3),
    Condition("SECTOR_PLAYERS_PRESENT", qty=2),
    SpawnNPC(qty=1, is_crew=1, random_name=1, race="CYBORG", home_system="MEDICAL", spawn_at_home=1),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="ENGINES:SHIELDS:REACTOR:HYPERDRIVE:MISSILE_WEAPONS:LASER_WEAPONS:", work_type=30),

    EventDef("SPAWN_NPC", "SPAWN_NPC_CREW_3",
        nonstop=1, min_event_qty=1, max_event_qty=1, chain_event="PLAYER_CREW_SPAWNED",
        for_ship_name="VAR(PLAYER_SHIP_NAME)", random_npc=0,
    ),
    Condition("SERVER_VARIABLE_ABSENT", var_name="PLAYER_CREW_SPAWNED", var_value=1),
    Condition("SECTOR_PLAYERS_ABSENT", qty=2),
    SpawnNPC(qty=1, is_crew=1, random_name=1, race="CYBORG", home_system="MEDICAL", spawn_at_home=1),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="ENGINES:SHIELDS:REACTOR:HYPERDRIVE:MISSILE_WEAPONS:LASER_WEAPONS:", work_type=30),

    EventDef("SERVER_VARIABLE", "PLAYER_CREW_SPAWNED", var_name="PLAYER_CREW_SPAWNED", var_value=1),
    EventDef("SERVER_VARIABLE", "SS31_STOP_CALLING_HELP", var_name="SS31_STOP_CALLING_HELP", var_value=1),
    EventDef("SERVER_VARIABLE", "STOP_HJ_TUTORIAL", var_name="HJ_TUTORIAL_STARTED", var_value=0),

    EventDef("MODIFY_SHIP", "ADD_CRYSTAL",
        all_mob_ships=0, ignore_passenger_access=0,
        add_system_model_to_cargo="CRYSTAL", chain_event="INC_CRYSTALS_COLLECTED",
    ),

    EventDef("SERVER_VARIABLE", "INC_CRYSTALS_COLLECTED", var_name="CRYSTALS_COLLECTED", var_value="++"),
    EventDef("SERVER_VARIABLE", "DROP_CRYSTALS_COLLECTED", var_name="CRYSTALS_COLLECTED", var_value=0),

    EventDef("THREAT_SPIKE", "MAIN_SPIKE",
        nonstop=1, min_event_qty=1, max_event_qty=1, sector="VAR(STARTING_SECTOR)",
        random_sector=0, radius_min=20, radius_max=20, threat_min=0, threat_max=0
    ),

    EventDef("MODIFY_SHIP", "SKIP_TUTORIAL",
        for_ship_name="VAR(PLAYER_SHIP_NAME)", add_system_model_to_cargo=["FALCON_HD", "Triple_laser1"],
        give_scrap=45, give_hull=45, give_missiles=4, repair_breaches=1, put_out_fires=1,
        repair_system_type=[
            "PILOTING", "ENGINES", "CAPACITOR", "REACTOR", "SHIELDS", "WEAPONS_CONTROL", "SENSORS", "MEDICAL",
        ],
        chain_event=[
            "START_TUTORIALS",
            "SS31_STOP_CALLING_HELP",
            "SS31_GO_TO_SENSORS",
            "START_HJ_TUTORIAL",
            "SKIP_TUTORIAL2",
            "SPAWN_NPC_CREW_3",
            "SPAWN_NPC_CREW_2",
        ]
    ),

    EventDef("SPAWN_SHIP", "SPAWN_TUT_PIRATE"),
    AddShip(random_pos=1, min_health=5, max_health=7),
    AddShip(
        gen_ship_model="TUT_PIRATE", ship_qty=1, ship_name="Pirate scavenger", random_pos=1,
        min_missile_ammo=20, max_missile_ammo=20, min_health=6, max_health=6,
    ),
    *[Ai(t) for t in ["LIFE_SUPPORT", "EVADER", "SENTRY"]],

    SpawnNPC(qty=1, is_captain=1, random_name=1, name="Pirate ", race="HUMAN", home_system="PILOTING", spawn_at_home=1),
    Ai("NPC_TALKER",
        timer=30, rand=1, mes=[
            "I'm gona destroy you!",
            "I'm gona blow you to small pieces!",
            "Your ship will make good scrap!",
            "I'm going to salvage what's left of your ship!",
            "I'm going to use the scrap from your ship to upgrade my Poop deck!",
        ]
    ),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="SHEILDS:PILOTING", work_time=10),

    SpawnNPC(qty=1, is_crew=1, random_name=1, name="Pirate ", race="HUMAN", home_system="OXYGEN", spawn_at_home=1),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="DOOR_CONTROL:OXYGEN", work_time=20),

    SpawnNPC(qty=1, is_crew=1, random_name=1, name="Pirate ", race="HUMAN", home_system="SHIELDS", spawn_at_home=1),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="SHIELDS:LASER_WEAPONS", work_time=20),

    SpawnNPC(qty=1, is_crew=1, random_name=1, name="Pirate ", race="HUMAN", home_system="ENGINES", spawn_at_home=1),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems="ENGINES:HYPERDRIVE", work_time=20),
]
