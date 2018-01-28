execute @e[type=ArmorStand,tag=RRStand] ~ ~ ~ scoreboard players operation @e[c=1,r=1,type=ArmorStand,tag=RRStand] RRti = @e[c=1,r=1,type=ArmorStand,tag=RRStand] RRti2
execute @e[type=ArmorStand,tag=RRStand] ~ ~ ~ scoreboard players operation @e[c=1,r=1,type=ArmorStand,tag=RRStand] RRti = 3 Number
scoreboard players add @e[type=ArmorStand,tag=RRStand] RRti 1 {Tags:["RREntity","RRDisplay","RRAestheticsStand"],DisabledSlots:2096896,Marker:1,NoGravity:1,NoBasePlate:1,ShowArms:1,Small:1,Invulnerable:1,PersistenceRequired:1,Invisible:1,Rotation:[0f,0f],Pose:{Body:[0f,0f,0f],Head:[0f,0f,0f],LeftArm:[0f,0f,0f],RightArm:[0f,0f,0f],LeftLeg:[0f,0f,0f],RightLeg:[0f,0f,0f]},ArmorItems:[{},{},{},{id:quartz_stairs,Count:1}]}
scoreboard players remove @e[type=ArmorStand,tag=RRStand] RRti 1 {DisabledSlots:2096896}
scoreboard players set @e[type=ArmorStand,tag=RRStand] RRti 10 {DisabledSlots:2096896}
scoreboard players test @e[type=ArmorStand,tag=RRStand] RRti 5
scoreboard players test @e[type=ArmorStand,tag=RRStand] RRti 0 10
scoreboard players reset @e[type=ArmorStand,tag=RRStand] RRti
scoreboard players enable @e[type=ArmorStand,tag=RRStand] RRti
scoreboard players tag @e[type=ArmorStand,tag=RRStand] add RRTimer {Marker:1b}
scoreboard players tag @e[type=ArmorStand,tag=RRStand] remove RRTimer {Marker:1b}
scoreboard teams join RRd_y @e[type=ArmorStand,tag=RRStand]
scoreboard teams leave @e[type=ArmorStand,tag=RRStand]
scoreboard teams empty RRd_y
