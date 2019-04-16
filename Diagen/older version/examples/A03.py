# Recreation of the WorldGen/Dialogues/A03.xml file from release a0819
# as a Tachyon Diagen script

dialogues = {
    "A03": [
        Choice("[ACTION]You see a scientist in a lab coat.", [
            [
                Response("Hello, I'm here to pick up the EMP Cannon."),
                Condition("SECTOR_SHIPS_PRESENT", qty=1, owner="THE_BEARS"),

                "Are you nuts? There are pirates here! Let's talk after we survive!",
            ],
            [
                Response("Hello, I'm here to pick up the EMP Cannon."),
                Condition("SECTOR_SHIPS_ABSENT", qty=1, owner="THE_BEARS"),
                Condition("SERVER_VARIABLE_ABSENT", var_name="EMP_CANNON_COLLECTED", var_value=1),

                "Whew, that was close! I will order to transfer the EMP Cannon to you.",
                Event("ADD_EMP_CANNON_TO_PLAYER", "PLAYER"),
                Event("REMOVE_EMP_CANNON_FROM_A03", "PLAYER"),
                Event("EMP_CANNON_COLLECTED", "PLAYER"),
                Response("Thanks."),
            ],
            [
                "Don't forget to pick up the Super Sensors at USC. And good luck to you!",
                Response("Thanks."),
            ]
        ]),
    ],
}
