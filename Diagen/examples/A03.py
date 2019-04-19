# Recreation of the WorldGen/Dialogues/A03.xml file from release a0819
# as a Tachyon Diagen script

dialogues = {
    "A03": [
        Choice("[ACTION]You see a scientist in a lab coat.", [
            [
                Reply("Hello, I'm here to pick up the EMP Cannon."),
                Condition("SECTOR_SHIPS_PRESENT", qty=1, owner="THE_BEARS"),

                "Are you nuts? There are pirates here! Let's talk after we survive!",
            ],
            [
                Reply("Hello, I'm here to pick up the EMP Cannon."),
                Condition("SECTOR_SHIPS_ABSENT", qty=1, owner="THE_BEARS"),
                Condition("SERVER_VARIABLE_ABSENT", var_name="EMP_CANNON_COLLECTED", var_value=1),

                "Whew, that was close! I will order to transfer the EMP Cannon to you.",
                InlineEvent("MODIFY_SHIP", "PLAYER",
                    all_mob_ships=0, ignore_passenger_access=0, add_system_model_to_cargo="EMP_Cannon"
                ),
                InlineEvent("MODIFY_SHIP", "PLAYER",
                    for_ship_name="Science  station  D31", remove_system_model_from_cargo="EMP_Cannon", safe_zone=0
                ),
                Event("EMP_CANNON_COLLECTED", "PLAYER"),

                Reply("Thanks."),
            ],
            [
                "Don't forget to pick up the Super Sensors at USC. And good luck to you!",
                Reply("Thanks."),
            ],
        ]),
    ],
}

events = [
    EventDef("SPAWN_SHIP", "SPAWN_A03",
        nonstop=1, random_sector=1, area_start="34:1", area_end="47:13",
        chain_event=[
            "A03_SPAWNED_VAR", "A03_SECTOR_VAR", "A03_SECTOR_UPDATE",
            "ADD_EMP_CANNON_TO_A03", "A03_SPAWN_SPIKE", "SPAWN_RANDOM_B_FORCE",
        ]
    ),

    AddShip(
        gen_ship_model="SS_A03", free_doors=1, free_med=1, free_oxygen=1, safe_zone=1, free_sensors=1,
        ship_name="Science  Station  A03", ship_owner="THE_UNITY", random_pos=1, min_health=20, max_health=30,
        min_missile_ammo=10, max_missile_ammo=20, min_drone_ammo=0, max_drone_ammo=10, min_scrap=10,
        max_scrap=100,
    ),
    *[Ai(t) for t in ["LIFE_SUPPORT", "EVADER", "ENEMY_SHOOTER", "TRADER"]],

    SpawnNPC(
        qty=1, is_crew=1, random_name=1, race="HUMAN", home_system="PILOTING",
        spawn_at_home=1, dialogue="A03", remote_dialogue="A03",
    ),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER", systems=["PILOTING", "WEAPONS_CONTROL"], work_time=40),

    SpawnNPC(
        qty=1, is_crew=1, random_name=1, race="HUMAN", home_system="MEDICAL", spawn_at_home=1
    ),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER",
        systems=["MEDICAL", "SHIELDS", "OXYGEN", "SENSORS", "DOOR_CONTROL", "REACTOR", "CAPACITOR"], work_time=15
    ),

    SpawnNPC(
        qty=1, is_crew=1, random_name=1, race="HUMAN", home_system="MEDICAL", spawn_at_home=1
    ),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER",
        systems=["MEDICAL", "SHIELDS", "OXYGEN", "SENSORS", "DOOR_CONTROL", "REACTOR", "CAPACITOR"], work_time=27
    ),

    SpawnNPC(
        qty=1, is_crew=1, random_name=1, race="HUMAN", home_system="MEDICAL", spawn_at_home=1
    ),
    *[Ai(f"NPC_{t}") for t in ["LIFESUPPORT", "DEFENDER", "FIREMAN", "REPAIRMAN"]],
    Ai("NPC_WORKER",
        systems=["MEDICAL", "SHIELDS", "OXYGEN", "SENSORS", "DOOR_CONTROL", "REACTOR", "CAPACITOR"], work_time=20
    ),

    EventDef("THREAT_SPIKE", "A03_SPAWN_SPIKE",
        nonstop=1, min_event_qty=1, max_event_qty=1, radius_min=20, radius_max=20, threat_min=14, threat_max=14
    ),

    EventDef("SERVER_VARIABLE", "A03_SPAWNED_VAR", var_name="A03_SPAWNED", var_value=1),
    EventDef("SERVER_VARIABLE", "A03_SECTOR_VAR", var_name="A03_SECTOR", var_value="[SECTOR]"),
    EventDef("SERVER_VARIABLE", "EMP_CANNON_COLLECTED", var_name="EMP_CANNON_COLLECTED", var_value=1),
    EventDef("MODIFY_SECTOR", "A03_SECTOR_UPDATE", nonstop=1, sector_type=30, visible_to_all=1),

    EventDef("MODIFY_SHIP", "ADD_EMP_CANNON_TO_A03",
        for_ship_name="Science  Station  A03",
        add_system_model_to_cargo="EMP_Cannon",
    ),
]
