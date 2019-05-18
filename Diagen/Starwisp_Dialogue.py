from diagen import Label, Choice, Condition, Goto, End, Event, Reply, InlineEvent, EventDef, ChainEvent, SpawnNPC, AddShip, Ai, AddDebris
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
    Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SPAWNED", var_value=1),
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

Vatish_Description = [
    "[ACTION]Wearing a standard human civilian space suit the figure stands about 5 foot 2 inches.",
    "[ACTION]Only their face is exposed with the visor open.",
    "[ACTION]The person has an androgynous face, with a just as unclear body covered by their suit.",
    "[ACTION]Their face has missmatched eyes, one green and one blueish violet.",
    "[ACTION]They have a lively expression but unstable personality, yet seems quite friendly.",
]

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
            "[ACTION]Something feels a bit off about their appearance.",
            Label("1stDialogue"),
            Choice("[ACTION]The figure looks at you.", [
                [
                    Reply("Who are you?"),
                    Goto("Vatish_WhoAreYou"),
                ],
                [
                    Reply("You're that Starwisp I saw before I died. (Skip Dialogue)"),
                    "That's right, we agreed to assist you. I'll call our ship.",
                    "[ACTION]Vatish's form vanishes replaced by a green and purple orb of plasma.",
                    "[ACTION]The starwisp reaches out energy tendrils sending an energy pulse to the reactor.",                    
                    Goto("AuroraWarpsIn"),
                ],
                [
                    Reply("[SKIP](Examine)"),
                    *Vatish_Description,
                    Goto("1stDialogue"),
                ],
            ]),
            Label("Vatish_WhoAreYou"),
            "The name's [NPC_NAME]. Are you one of the crew?",
            Reply("Yes, I'm a guard, my name is [PLAYER_NAME]."),
            "I see! The clone replication system must have actually worked!",
            "It was pretty smashed up. But it's okay. I hotwired it back together!",
            Reply("Yes, except that I don't remember anything."),
            "There were some broken pieces left over... I did what I could.",
            "You look fine otherwise... I think.",
            Reply("You aren't part of the crew, are you?"),
            "No. I came on board as soon as the pirates left and did what I could.",
            Reply("Why were you out here in the first place?"),
            "I'm aware of your prototype ship, the DF.",
            "I was sent to investigate it, but the pirates got here first.",
            Reply("What do you know about it?"),
            "[ACTION]Vatish's expression becomes much more serious.",
            "There is powerful alien technology in your 'prototype' ship.",
            "In fact, it never belonged to the humans in the first place.",
            "But somehow, you got a hold of that technology. And what did you do?",
            "You reverse-engineered it into a super-weapon.",
            "It's a threat to every living being in the universe!",
            Reply("...And the pirates have it now too."),
            "Exactly. They need to be stopped, no matter what.",
            Reply("I'll stop them any way I can."),
            "If you promise us you will destroy it, the Collective will assist you.",
            "It's too dangerous to let it fall into pirate hands.",
            Reply("Collective? What are you talking about?"),
            "[ACTION]The human's form vanishes, revealing a glowing orb of plasma in its place.",
            Reply("What the hell are you?"),
            "We are Starwisps. No time to explain, you can ask on the trip if you must.",
            "[ACTION]The creature sends a pulse of energy into the reactor using thin tendrils of plasma.",
            "I called for our ship, they will assist you on your journey.",
            Reply("Why are you willing to help us?"),
            "If that prototype ship isn't destroyed, we may all perish.",
            Reply("Fair enough."),
            Label("AuroraWarpsIn"),
            "[ACTION]Outside of the station there's a bright flash, and a giant crystal ship jumps close.",
            Event("SPAWN_WispShip", "PLAYER"),
            Event("STARWISP_CAPTAIN_BABBLE_ON", "PLAYER"),
            Event("WISPSHIP_COMPLETE", "PLAYER"),
            "The S.S Aurora is waiting. Radio Solaria on the COMMS when you get to your ship.",
            "[ACTION]The starwisp creature reassumes the illusion of a human.",
            Choice("I'll stay behind and send any other surviving crew your way. Good luck.", [
                [Reply("Yes, sir! ...lady... thing."),],
                [Reply("Thanks!")],
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
            Reply("Hello? (Ask for a ship)"),
            "[ACTION]The androgynous-looking person turns to face you.",

            Choice("Oh! Another survivor! The clone replication system managed to recover you as well.", [
                [
                    Reply("I don't remember anything. What's going on?"),
                    "The cloning system was damaged, so you didn't recover all of your memories.",
                    "Long story short, pirates attacked this space station and stole a prototype ship.",
                    "Your mission is to hunt down the prototype ship D.F and destroy it.",
                    "The prototype has a super-weapon made using powerful reverse-engineered alien technology.",
                    "We, the Starwisp Collective, agreed to help you in your mission.",
                    "The D.F prototype is a threat to all life in the universe. It must be destroyed.",
                    "I'm sure your crew can catch you up to speed otherwise...",
                    Reply("Then I need to join the crew on our ship."),
                ],
                [
                    Reply("I need to join the crew on our ship. (Skip Recap)"),
                ],
                [
                    Reply("I'm in a hurry. I need to catch up with my ship. (Skip All Dialogue)"),
                    "Okay, I'll have a ship waiting for you outside. It's called the P.U.C.C.",
                    Goto("Skip_PUCC_Convo"),
                ]
            ]),

            "Right... about that. There's no more proper space ships in this sector you can use.",
            "Even if you got one, it could take forever to catch up with your ship.",
            "I did come up with something for you, however!",
            Reply("What was that?"),
            "[ACTION]Vatish gives a grin like a mad scientist.",
            "This space station has a shipyard that makes Prototype Unmanned Construction Crafts.",
            Choice("P.U.C.Cs for short. They weren't meant to be manned, but...", [
                [Reply("I don't like where this is going..."),],
                [Reply("Uhh...")],
            ]),
            "I modified the blueprints, removed some parts and crammed a life support unit inside.",
            "It's a tight fit, but it's spaceworthy and very fast, though it lacks a shield generator.",
            Reply("How would that possibly catch up with our ship?"),
            "Well... I've been tinkering, and modified a FTL engine to fit inside it.",
            "I took out all the... 'unnecessary' parts, but it's still quite weak on such a tiny ship.",
            "So I hooked it up to the station and super-charged it with the reactor!",
            Reply("That can't be safe..."),
            "Well... it only needs to work once.",
            "We attached a beacon to your ship so the Aurora can follow it.",
            "I'll program it into the FTL system and the autopilot will follow the ship automatically.",
            "The P.U.C.C is so small it can ride the FTL wake your ship makes when it jumps.",
            "It can also be handy in a dogfight. It's fast and can damage the hull or systems quickly.",
            "But it doesn't have any shields, so make sure to dodge frequently.",
            Reply("Okay. You really think this will work?"),
            "I'm... pretty sure it will work. The P.U.C.C is outside.",
            Label("Skip_PUCC_Convo"),
            "Contact me on the COMMS when you're ready and I'll install the FTL unit.",
            Event("SPAWN_PUCC", "PLAYER"),
            Reply("Will do."),
        ],

        # When radioed on comms
        [
            *pucc_ready,
            Reply("I'm ready. Send the P.U.C.C to the ship!"),
            Choice("Okay, make sure you're INSIDE the ship and have already claimed it.", [
                [
                    Reply("Wait! I'll get in the ship and claim it."),
                    End,
                ],
                [
                    *inside_pucc,
                    Reply("Wait, can I give my ship a name?"),
                    Choice("Sure, what do you want to name it?", [
                        [Reply("[INPUT]Let's call it...", regex="^[a-zA-Z0-9 -]+$"),],
                    ]),
                    "Okay I'll name it VAR(PUCC_New_Name).",
                    Event("SET_PUCC_New_Name", "PLAYER"),
                ],
                [
                    *inside_pucc,
                    Reply("Yes, ready to go!"),
                ],
                [
                    *inside_pucc,
                    Reply("Fire away! (Skip Dialogue)"),
                    Goto("Bon_Voyage"),
                ],
            ]),
            Event("DEFAULT_PUCC_New_Name", "PLAYER"),
            Label("WarpPuccConvo"),
            "The modified FTL engine is ready, and will engage the moment I install it.",
            "By the way... the ship has a built-in fire suppression and repair system.",
            Reply("Oh, nice!"),
            Choice("It'll come in handy if it bursts into flames from the FTL engine.", [
                [Reply("Wait, what?"),],
                [Reply("Oh, great...")],
            ]),
            Label("Bon_Voyage"),
            "Bon voyage!",
            Event("PUCC_Follow_Beacon", "PLAYER"),
            End,

        ],

        #If beacon is lost
        [
            Reply("[SKIP](Beacon Lost)"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SPAWNED", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="PUCC_BEACON_SECTOR_LOC", any_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="CAMPAIGN_SHIP_ID", any_value=1),
            "...Strange. I can't find any trace of the beacon we put on your ship.",
            "Without it, I don't know where to send you.",
            "I'm afraid I can't help you without a beacon to guide us.",
            "(If the campaign ship was destroyed, it's Game Over. Reset the server.)",
            End,
        ],
        [
        Reply("(Examine)"),
        Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SPAWNED", var_value=1),
        Condition("SERVER_VARIABLE_ABSENT", var_name="SOLARIA_CONVO_1", var_value=1),
        *Vatish_Description,
        ],
    ]),
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
            Reply("Hello?"),
            "[ACTION]The woman speaks formally but bluntly.",
            "Hello, this is Solaria, captain of the Aurora.",
            Choice("Are you the captain of that ship?", [
                [
                    Reply("Yes, the name is [PLAYER_NAME]."),
                    Condition("SECTOR_SHIPS_PRESENT", target_player=1, owner="[PLAYER_NAME]", qty=1),
                    Goto("FirstConvo"),
                ],
                [
                    Reply("No."),
                    Condition("SECTOR_SHIPS_ABSENT", target_player=1, owner="[PLAYER_NAME]", qty=1),
                    "I would like to speak with the captain first please.",
                    "I'll stand by for them to contact me on the COMMS.",
                    "[ACTION]The woman ends the transmission.",
                    End,
                ],
                [
                    Reply("...Yes."),
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
            Reply("I was told to contact you.")
        ],
        [
            Reply("I remember talking to starwisp Vatish before I died. (Skip Dialogue)"),
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
    Reply("Sounds useful."),
    "We can also mine for asteroids, pick up debris and so forth, just ask.",
    "I can also try to answer any questions you have along the way.",
    Reply("Are you a starwisp like Vatish?"),
    Choice("Well, yes. What did Vatish tell you about starwisps?", [
        [
            Reply("He... she... or they turned into a glowing ball of plasma."),
            "What!?... they revealed their true form just like that?!",
            "[ACTION]Solaria face-palms making a sigh and no longer speaks formally.",
            "I've got to teach them subtlety. But yes, we are plasma creatures called starwisps.",
            "Our whole ship is manned by starwisps. Our technology a mix of yours and our own.",
            #Continues to 'why look like humans'
        ],
        [
            Reply("Nothing much other than that you're the Starwisp Collective."),
            "I see. The Aurora is a small piece of the collective. Our species is called starwisps.",
            "We are a type of plasma creature. We just look like humans at the moment.",
            Reply("I know. I saw Vatish turn into a ball of plasma."),
            "... They already revealed their true form?",
            "[ACTION]Solaria rolls her eyes and no longer speaks formally.",
            "I really got to teach them subtlety.",
        ],
    ]),
    "In any case, we use holographic projections to appear like humans.",
    Reply("Why do you make yourselves look like humans?"),
    "Well... Part of it is to make a good first impression.",
    Choice("Another part is small stuff like you can read our expressions and we don't stand out.", [
        [
            Reply("Well, your ship looks rather alien as well."),
            "Ya got me there. Our technology is very different from yours.",
            "Though I must say it's still less shocking than balls of plasma approaching you.",
            Reply("I suppose."),
        ],
        [
            Reply("I can understand that."),
        ],
    ]),
    "Well there's no point keeping up my human guise at this point.",
    "[ACTION]The human figure vanishes revealing a white ball of plasma.",
    "At least I can relax now.",

    Label("EndFirstConvo"),
    Choice("Contact me on the comms if ya need anything or have any more questions.", [
        [
            Reply("Okay, thanks!"),
            End
        ],
        [
            Reply("Well... (Main Menu)"),
            Goto("Main")
        ],
    ]),
    Event("SOLARIA_CONVO_1", "PLAYER"),
    Event("CAMPAIGN_SHIP_ID", "PLAYER"),
    Event("WISPSHIP_GUARD_SHIP_ID", "PLAYER"),
    Event("Add_PUCC_Beacon_To_Ship", "PLAYER"),

    Label("Main"),
    Choice("What can I do for ya?", [
        [
            Reply("I need you to do something... (Commands)"),
            Goto("Requests"),
        ],
        [
            Reply("What do I need to know about your ship?"),
            "Well, there is the repair drones, the mining drones, and our weapons.",
            "Or about our research and development.",
            Label("About_Important"),
            Choice("What did you want to ask about?", [
                [
                    Reply("About your repair drones."),
                    "Unlike most ships, the Aurora has the ability to repair it's own hull.",
                    "As long as we aren't in a battle and we have enough scrap on board",
                    "we can deploy special drones that will patch up our hull without need of a repair depot.",
                    "We can't repair your hull though. It's too different from our crystal hull.",
                    "Please consider sharing a bit of scrap with us so we can keep our hull in top shape.",
                    #Insert about repair drones
                ],
                [
                    Reply("About your mining drones."),
                    "If you ask me to mine asteroids, I can deploy mining drones.",
                    "I'll only deploy them if there are asteroids nearby.",
                    "They're fragile, but cheap so I can deploy them even during a fight.",
                    "Although they are slower than just shooting asteroids, they yield more scrap.",
                    "We can only get the most scrap out of asteroids we mine without assistance.",
                    "They're useless against ships and only target asteroids.",
                    #Insert about mining drones
                ],
                [
                    Reply("About your weapons."),
                    "We will research weapons among other things as we travel.",
                    "However all of our weapons are plasma or ion based.",
                    "They are great at taking out ship systems.",
                    "...and the occasional personnel that get in the way.",
                    "However they do not damage ship hulls so we can't destroy a ship by ourselves.",
                    "Our targeting systems are fast as well, but highly inaccurate I must say.",
                    Reply("[SKIP]..."),
                    "If you need us to stop attacking ships, just tell us to stop guarding you.",
                    "Make sure to ask us to guard you again if you want us to follow you.",
                    #Insert about weapons
                ],
                [
                    Reply("About your research."),
                    "(Currently unfinished.)"
                    #Insert about research
                ],
                [
                    Reply("(Main Menu)"),
                    Goto("Main"),
                ],
            ]),
            Goto("About_Important"),
        ],
        [
            Reply("So... (Other questions)"),
            Label("About_OtherQuestions"),
            Choice("What did you want to know?", [
                [
                    Reply("About your crew..."),
                    Label("About_Crew"),
                    Choice("Who were you curious about?", [
                        [
                            Reply("You (Solaria)"),
                            "Oh me? As you know I'm the captian of this crew.",
                            "I'm here to try to set things straight if I can.",
                            "Gaia assigned us to the task of helping you since we're familiar with humaniod races.",
                            Reply("Who's Gaia?"),
                            "Oh, right. Gaia is the closest thing to a 'queen' of our kind.",
                            "The whole collective make decisions as a whole, but Gaia is responcible",
                            "for making sense of the needs and desires of the collective and take action upon them.",
                            "We think for ourselves both as individuals, and as a whole.",
                            Reply("What can you do for us?"),
                            "Well, you can ask questions like you are now. But as acting captian",
                            "you can contact me for major ship operations.",
                            "Let me know if we should follow and guard your ship, mine asteroids, exchange cargo",
                            "and so on. Just contact me on the COMMS when you need us.",
                            Reply("Understood. What about another crew member..."),
                        ],
                        [
                            Reply("Vatish"),
                            "Ah, yes Vatish... Long story that one.",
                            "They are an ambitious one, thinks very outside the box. Also our best engineer.",
                            "Don't worry though, Vatish wouldn't hurt you even with their crazy inventions.",
                            Reply("Is Vatish a he, she or...?"),
                            "[ACTION]Solaria makes a small laugh.",
                            "Well, yes, and no. Although Starwisps don't have simple male or female sexes,",
                            "meaning we can be any gender or no gender, Vatish is a plural 'they'..",
                            Reply("Huh?"),
                            "Vatish is two starwisps fused together. It's part of our reproductive cycle.",
                            "Two starwisps fuse, combine traits, then split off into 3 or more wisplings.",
                            "We become our own children, each with a piece of the parents, mind and body.",
                            "Vatish however is... 'unresolved'. The two halves haven't sorted themselves out.",
                            "Hence the split personality. They are half way between being two and one.",
                            Reply("That must be confusing."),
                            "Perhaps, but it's in our nature.",
                            Reply("What does Vatish do?"),
                            "Vatish is our lead engineer. They will do research from the station there.",
                            "They already turned the station's reactor and ship hanger into a lab.",
                            "We will share discovery data and Vatish will send us designs as we go.",
                            "beyond that, Vatish has modified small ships so if any other cloned people",
                            "wake up, they will send them our way to assist us.",
                            Reply("What about someone else?"),
                            Goto("About_Crew"),
                        ],
                        [
                            Reply("(Back to other questions)"),
                            Goto("About_OtherQuestions"),
                        ],
                        [
                            Reply("(Main Menu)"),
                            Goto("Main")
                        ],

                    ]),
                ],
            ]),
            "(Currently no other questions available)",
            Reply("(Main Menu)"),
            Goto("Main"),
        ],
    ]),


    Label("Requests"),
    Choice("What can I do for ya?", [
        [
            Reply("Please stop following or guarding the VAR(WISPSHIP_GUARD_ID) for now."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_GUARD_ID", any_value=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            
            "Acknowledged. We will wait here.",
            Event("WISPSHIP_STOP_GUARD", "PLAYER"),
        ],
        [
            Reply("Guard our ship please."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_GUARD_ID", any_value=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),

            "Acknowledged. We'll look out for you.",
            Event("WISPSHIP_GUARD_SHIP_ID", "PLAYER"),
        ],
        [
            Reply("About your cargo...", any_condition=1),
            *[check_cargo(t) for t in all_cargo_types],

            "We can jettison our cargo out the back of the ship.",
            Goto("cargo"),
        ],
        [
            Reply("Can you send us your scrap?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_SCRAP_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_scrap"),
        ],
        [
            Reply("Can you send us your missiles?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_MISSILES_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_missiles"),
        ],
        [
            Reply("Can you send us your drones?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SHIP_DRONES_PRESENT", target_player=0, all_mob_ships=0, qty=1),
            Condition("SECTOR_SHIPS_PRESENT", target_player=1, crew="[PLAYER_NAME]", qty=1),
            Goto("give_drones"),
        ],
        [
            Reply("Can you mine asteroids for us?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SHOOT_ASTEROID", var_value=1),

            "Sure! Any asteroids we see are toast.",
            Event("WISPSHIP_SHOOT_ASTEROID_ON", "PLAYER"),
        ],
        [
            Reply("Don't shoot asteroids any more please."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SHOOT_ASTEROID", var_value=1),

            "Understood.  We'll leave the asteroids alone.",
            Event("WISPSHIP_SHOOT_ASTEROID_OFF", "PLAYER"),
        ],
        [
            Reply("Pick up any scrap and cargo you find."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISPSHIP_SCAVENGE", var_value=1),

            "Sure, we'll collect any scrap or cargo we see.",
            Event("WISPSHIP_START_SCAVENGE", "NPC"),
        ],
        [
            Reply("Please stop picking up scrap or cargo."),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISPSHIP_SCAVENGE", var_value=1),

            "We'll leave the scrap and cargo for you to pick up.",
            Event("WISPSHIP_STOP_SCAVENGE", "NPC"),
        ],
        [
            Reply("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("Requests"),


    Label("cargo"),
    Choice("Would you like us jettison something?", [
        [
            Reply("Jettison EVERYTHING from your cargo.", any_condition=1),
            *[check_cargo(t) for t in all_cargo_types],

            "Okay, we've dumped everything from our cargo hold out the back.",
            Event("Aurora_Jet_ALL", "NPC"),
        ],
        [
            Reply("Jettison your WEAPONS in your cargo.", any_condition=1),

           *[check_cargo(t) for t in ["LASER_WEAPONS", "BEAM_WEAPONS", "MISSILE_WEAPONS"]],

            "The weapons have been jettisoned.",
            Event("Aurora_Jet_WEAPONS", "NPC"),
        ],

        *[[
            Reply(f"Jettison your {cargo_type} in your cargo."),
            check_cargo(cargo_type),

            "The requested cargo has been jettisoned.",
            Event(f"Aurora_Jet_{cargo_type}", "NPC"),
        ] for cargo_type in [
            "WEAPONS_CONTROL", "CLOAKING", "SHIELDS", "REACTOR", "OXYGEN", "PILOTING", "TELEPORT", "CAPACITOR",
            "DOOR_CONTROL", "ENGINES", "HYPERDRIVE", "MEDICAL", "SENSORS",
        ]],

        [
            Reply("Jettison your SHOPS in your cargo.", any_condition=1),
            *[check_cargo(t) for t in ["REPAIR", "SYSTEMS_SHOP", "SHIPS_SHOP", "CONSUMABLES_SHOP", "SHIPYARD"]],

            "The requested cargo has been jettisoned.",
            Event("Aurora_Jet_SHOPS", "NPC"),
        ],
        [
            Reply("That's it for cargo. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Reply("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("cargo"),


    Label("give_scrap"),
    Choice("How much scrap would you like?", [
        *[[
            Reply(f"{count} scrap please."),
            Condition("SHIP_SCRAP_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            "I've transferred the scrap to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_SCRAP", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_SCRAP", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Reply("That's it for scrap. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Reply("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("give_scrap"),


    Label("give_missiles"),
    Choice("How many missiles would you like?", [
        *[[
            Reply(f"{count} missile{'s' if count > 1 else ''} please."),
            Condition("SHIP_MISSILES_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            f"I've transferred the missile{'s' if count > 1 else ''} to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_MISSILES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_MISSILES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Reply("That's it for missiles. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Reply("(Main Menu)"),
            Goto("Main"),
        ]
    ]),
    Goto("give_missiles"),


    Label("give_drones"),
    Choice("How many drones would you like?", [
        *[[
            Reply(f"{count} drone{'s' if count > 1 else ''} please."),
            Condition("SHIP_DRONES_PRESENT", target_player=0, all_mob_ships=0, qty=f"{count}"),

            f"I've transferred the drone{'s' if count > 1 else ''} to your ship.",
            Event(f"WISPSHIP_TAKE_{count}_DRONES", "NPC"),
            Event(f"WISPSHIP_GIVE_{count}_DRONES", "PLAYER"),
        ] for count in [100, 50, 25, 15, 10, 5, 4, 3, 2, 1]],
        [
            Reply("That's it for drones. But can you... (Commands)"),
            Goto("Requests"),
        ],
        [
            Reply("(Main Menu)"),
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
            Reply("Hello?"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_ABSENT", var_name="WISP_DEBUG", var_value=1),
            "[ACTION]The starwisp doesn't seem to acknowledge you or even sense you?",
            End,
        ],
        [
            Reply("DEBUG MENU"),
            Condition("SERVER_VARIABLE_PRESENT", var_name="SOLARIA_CONVO_1", var_value=1),
            Condition("SERVER_VARIABLE_PRESENT", var_name="WISP_DEBUG", var_value=1),
            Goto("Wisp_Debug_Menu"),
        ],
    ]),

    Label("Wisp_Debug_Menu"),
    Choice("DEBUG MENU:", [
        [
            Reply("DEBUG: Special Gear"),

            "Adding special gear to your ship cargo.",
            Event("Debug_SpecialGear", "PLAYER"),
        ],
        [
            Reply("DEBUG: Deck the Halls"),

            "Power overwhelming...",
            Event("Debug_Decked_Out", "PLAYER"),
        ],
        [
            Reply("DEBUG: Spawn Asteroids"),

            "Asteroids!",
            Event("SPAWN_DEAD_SHIP_PART", "PLAYER"),
        ],
        [
            Reply("DEBUG: Spawn Lots of Ships"),

            "Spawning a ton of random ships.",
            Event("WISP_DEBUG_SPAWN_SHIPS", "PLAYER"),
        ],
        [
            Reply("DEBUG: Make me Aurora crew"),

            "You're now an honorary starwisp.",
            Event("Debug_Become_Crew", "PLAYER"),
        ],
        [
            Reply("DEBUG: Jet TEST"),

            "Testing Jettison.",
            Event("WISP_DEBUG_Jet_TEST", "NPC"),
        ],
        [
            Reply("DEBUG: Jettison your scrap."),

            "Jettisoning scrap...",
            Event("Aurora_Jet_Scrap", "NPC"),
        ],
        [
            Reply("DEBUG: Jettison your missiles."),

            "Jettisoning missiles...",
            Event("Aurora_Jet_Missiles", "NPC"),
        ],
        [
            Reply("DEBUG: Jettison your drones."),

            "Jettisoning drones...",
            Event("Aurora_Jet_Drones", "NPC"),
        ],
        [
            Reply("DEBUG: Damage your ship."),

            "Taking damage...",
            Event("Debug_Damage_Aurora", "NPC"),
        ],
        [
            Reply("DEBUG: Force Story Trigger"),

            Choice("Which Story Trigger?", [
                [
                    Reply("Story 1 - Tutorial"),
                    "Story 1 Triggered",
                    Event("WISP_STORY_TRIGGER_1", "NPC"),
                ],
                [
                    Reply("Story 2 - USC"),
                    "Story 2 Triggered",
                    Event("WISP_STORY_TRIGGER_2", "NPC"),
                ],
                [
                    Reply("Story 3 - KEK"),
                    "Story 3 Triggered",
                    Event("WISP_STORY_TRIGGER_3", "NPC"),
                ],
                [
                    Reply("Story 4 - Fought Bears"),
                    "Story 4 Triggered",
                    Event("WISP_STORY_TRIGGER_4", "NPC"),
                ],
                [
                    Reply("Story 5 - Return to Kek with crystal"),
                    "Story 5 Triggered",
                    Event("WISP_STORY_TRIGGER_5", "NPC"),
                ],
                [
                    Reply("Story 6 - EMP_Error Quest"),
                    "Story 6 Triggered",
                    Event("WISP_STORY_TRIGGER_6", "NPC"),
                ],
            ]),
        ],
    ]),
    Reply("Debug Menu"),
    Goto("Wisp_Debug_Menu"),


]


dialogues = {
    "Vatish": Vatish,
    "Solaria": Solaria,
    "Debug": Debug,
}
