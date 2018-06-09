from test_fena.test_common import test_cmd

"""
    # @p ~2 ~1 ~-1 execute @a 3 5.2 -2 @s @r ifblock 2 ~-1 ~ stonebrick 0 @e ifblock stonebrick *: say @a
    @p ~2 ~1 ~-1 @a 3 5.2 -2 @s @r if(stonebrick[0] 2 ~-1 ~) @e if(stonebrick): say @a
    # execute @p ~ -4.2 3 execute @a ~ ~ ~ execute @s ~ ~ ~ execute @r ~ ~ ~ ifblock ~ ~-1 ~ minecraft:stonebrick 0 execute @e ~ ~ ~ detect ~ ~ ~ minecraft:stonebrick * say @a

    # execute @a ~ ~ ~: say test
    @a ~ ~ ~: say test
    @a: say test
    # @s @s @s: kill @a[_ti>=1,testTag,kek>=1<=3]
    @s @s @s: kill @a[_ti=(1..),testTag,kek=1..3]

    # execute @a ~ ~ ~ ifblock ~ ~ ~ stonebrick 0: say test
    # @a ~ ~ ~ ifblock ~ ~ ~ stonebrick 0: say test
    # @a ~ ~ ~ ifblock stonebrick 0: say test
    # @a ifblock ~ ~ ~ stonebrick 0: say test
    # @a ifblock stonebrick 0: say test
    @a if(stonebrick[0]): say test

    # execute @a ~ ~ ~ detect ~ ~ ~ stonebrick * execute @a ~ ~ ~ detect ~ ~ ~ stonebrick *: say test
    # @a ~ ~ ~ ifblock ~ ~ ~ stonebrick * @a ~ ~ ~ ifblock ~ ~ ~ stonebrick *: say test
    # @a ~ ~ ~ ifblock stonebrick * @a ~ ~ ~ ifblock stonebrick *: say test
    # @a ifblock ~ ~ ~ stonebrick * @a ifblock ~ ~ ~ stonebrick *: say test
    # @a ifblock stonebrick * @a ifblock stonebrick: say test
    # @a ifblock stonebrick @a ifblock stonebrick: clear
    @a if(stonebrick) @a if(stonebrick): clear

    # execute @a ifblock stonebrick 0: say test
    # execute @a: say test
    
    # execute @s ~ ~ ~ detect ~ ~-1 ~ stonebrick * execute @s ~ ~ ~ detect ~ ~ ~ stonebrick_stairs facing=west execute @s ~ ~ ~ detect ~ ~1 ~ stonebrick *: kill
    # @s ifblock ~ ~-1 ~ stonebrick * @s detect stonebrick_stairs facing=west @s ifblock ~ ~1 ~ stonebrick *: kill
    @s if(stonebrick ~ ~-1 ~) @s if(stonebrick_stairs[facing=west]) @s if(stonebrick ~ ~1 ~): kill
    @s if(stonebrick ~ ~-1 ~, stonebrick_stairs[facing=west], stonebrick ~ ~1 ~): kill

    # testing out chained commands: DISCONTINUED
    # @e[type=armor_stand,_ti=(0..20)]:
    #     say @s
    #     @r _ti + 1
    #     @a[_pl=1]:
    #         _pl = 0
    #         playsound:
    #             sound_1 voice @a
    #             sound_2 voice @a

    # @e[type=armor_stand,_ti=0]: effect @a[_pl=0]:
    #     effect_1 20 0 true
    #     effect_2 20 0 true
    
    @e[type=armor_stand,_ti=(0..20)]: say @s
    @e[type=armor_stand,_ti=(0..20)]: @r _ti += 1
    @e[type=armor_stand,_ti=(0..20)]: @a[_pl=1] _pl = 0
    @e[type=armor_stand,_ti=(0..20)] @a[_pl=1]: playsound sound_1 voice @a
    @e[type=armor_stand,_ti=(0..20)] @a[_pl=1]: playsound sound_2 voice @a
    @e[type=armor_stand,_ti=0]: effect @a[_pl=0] effect_1 20 0 true
    @e[type=armor_stand,_ti=0]: effect @a[_pl=0] effect_2 20 0 true
"""