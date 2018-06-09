from test_fena.test_common import test_nbt

def test_nbts():
    test_nbt(r'''{HurtByTimestamp: 0,
        Attributes: [
            {Base: 1.0E7d, Name: "generic.maxHealth"},
            {Base: 0.0d, Name: "generic.knockbackResistance"},
            {Base: 0.25d, Name: "generic.movementSpeed"},
            {Base: 0.0d, Name: "generic.armor"},
            {Base: 0.0d, Name: "generic.armorToughness"},
            {Base: 16.0d, Modifiers: [
                {UUIDMost: 5954586636154850795L, UUIDLeast: -5021346310275855673L, 
                Amount: -0.012159221696308982d, Operation: 1, Name: "Random spawn bonus"}],
                Name: "generic.followRange"}
            ],
        Invulnerable: 0b,
        FallFlying: 0b,
        ForcedAge: 0,
        PortalCooldown: 0,
        AbsorptionAmount: 0.0f,
        Saddle: 0b,
        FallDistance: 0.0f,
        InLove: 0,
        DeathTime: 0s,
        HandDropChances: [0.085f, 0.085f],
        PersistenceRequired: 0b,
        Age: 0,
        Motion: [0.0d, -0.0784000015258789d, 0.0d],
        Leashed: 0b,
        UUIDLeast: -8543204344868739349L,
        Health: 79.2f,
        LeftHanded: 0b,
        Air: 300s,
        OnGround: 1b,
        Dimension: 0,
        Rotation: [214.95569f, 0.0f],
        HandItems: [{}, {}],
        ArmorDropChances: [0.085f, 0.085f, 0.085f, 0.085f],
        UUIDMost: 900863262324051519L,
        Pos: [724.3034218419358d, 4.0d, 280.78117600802693d],
        Fire: -1s,
        ArmorItems: [{}, {}, {}, {}],
        CanPickUpLoot: 0b, 
        HurtTime: 0s}''',
    r'{HurtByTimestamp:0,Attributes:[{Base:1.0E7d,Name:"generic.maxHealth"},{Base:0.0d,Name:"generic.knockbackResistance"},{Base:0.25d,Name:"generic.movementSpeed"},{Base:0.0d,Name:"generic.armor"},{Base:0.0d,Name:"generic.armorToughness"},{Base:16.0d,Modifiers:[{UUIDMost:5954586636154850795L,UUIDLeast:-5021346310275855673L,Amount:-0.012159221696308982d,Operation:1,Name:"Random spawn bonus"}],Name:"generic.followRange"}],Invulnerable:0b,FallFlying:0b,ForcedAge:0,PortalCooldown:0,AbsorptionAmount:0.0f,Saddle:0b,FallDistance:0.0f,InLove:0,DeathTime:0s,HandDropChances:[0.085f,0.085f],PersistenceRequired:0b,Age:0,Motion:[0.0d,-0.0784000015258789d,0.0d],Leashed:0b,UUIDLeast:-8543204344868739349L,Health:79.2f,LeftHanded:0b,Air:300s,OnGround:1b,Dimension:0,Rotation:[214.95569f,0.0f],HandItems:[{},{}],ArmorDropChances:[0.085f,0.085f,0.085f,0.085f],UUIDMost:900863262324051519L,Pos:[724.3034218419358d,4.0d,280.78117600802693d],Fire:-1s,ArmorItems:[{},{},{},{}],CanPickUpLoot:0b,HurtTime:0s}'
    )

    test_nbt(
        r'''{
            LifeTime:20,
            FireworksItem:{
                id:"minecraft:fireworks",
                Count:1b,
                tag:{
                    Fireworks:{
                        Explosions:[
                            {
                                Type:0,
                                Trail:0,
                                Colors:[I;41728,65280],
                                Flicker:1,
                                FadeColors:[I;2883328]
                            }
                        ]
                    }
                },
                Damage:0s
            }
        }''',
        r'{LifeTime:20,FireworksItem:{id:"minecraft:fireworks",Count:1b,tag:{Fireworks:{Explosions:[{Type:0,Trail:0,Colors:[I;41728,65280],Flicker:1,FadeColors:[I;2883328]}]}},Damage:0s}}')

    # using byte and long int arrays
    test_nbt(r'{Bytes:[B;1b,3b,5b],Longs:[L;1L,3L,5L]}')

    test_nbt(r'{}')

    test_nbt(r'{', expect_error=True)
    test_nbt(r'}', expect_error=True)
    test_nbt(r'{"test":1}', expect_error=True)
    test_nbt(r'{test:1,}', expect_error=True)
    test_nbt(r'{,test:2}', expect_error=True)
    test_nbt(r'{test:1, test:2, test:3}', expect_error=True)
    test_nbt(r'{test:1, test2:2, test3:3, }', expect_error=True)
    test_nbt(r'{test:1, test2:2, test3:3{', expect_error=True)
    test_nbt(r'{test:1 test2:2}', expect_error=True)
    test_nbt(r'{test:}', expect_error=True)
    test_nbt(r'{test:somestring}', expect_error=True)
    test_nbt(r'{test:some string}', expect_error=True)
    test_nbt(r'nou', expect_error=True)
    test_nbt(r'{nou}', expect_error=True)
    test_nbt(r'{nou:1, nou}', expect_error=True)
    test_nbt(r'{nou:1, []}', expect_error=True)
    test_nbt(r'{nou:[1, 2,]}', expect_error=True)