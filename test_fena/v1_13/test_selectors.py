from test_fena.test_common import test_selector

def test_selectors():
    test_selector("@p")
    test_selector("@a[]")
    test_selector("@e[type=armor_stand]", "@e[type=minecraft:armor_stand]")
    test_selector("@e[type=minecraft:armor_stand]")
    test_selector("@e[type=armor_stand,c=1]", "@e[type=minecraft:armor_stand,limit=1]")
    test_selector("@e[type=armor_stand,dist=1..2]", "@e[type=minecraft:armor_stand,distance=1..2]")
    test_selector("@a[x]", "@a[tag=x]")

    test_selector("@a[RRpl=3..4]", "@a[scores={RRpl=3..4}]")
    test_selector("@a[RRpl=3..]", "@a[scores={RRpl=3..}]")
    test_selector("@a[RRpl=..3]", "@a[scores={RRpl=..3}]")
    test_selector("@a[RRpl=3]", "@a[scores={RRpl=3}]")
    test_selector("@a[RRpl=*]", "@a[scores={RRpl=-2147483648..}]")
    test_selector("@a[RRpl=(3..4)]", "@a[scores={RRpl=3..4}]")
    test_selector("@a[RRpl=(3..)]", "@a[scores={RRpl=3..}]")
    test_selector("@a[RRpl=(..3)]", "@a[scores={RRpl=..3}]")
    test_selector("@a[RRpl=(3)]", "@a[scores={RRpl=3}]")
    test_selector("@a[RRpl=(*)]", "@a[scores={RRpl=-2147483648..}]")
    test_selector("@a[RRpl=((((*)))]", "@a[scores={RRpl=-2147483648..}]")

    test_selector("@a[distance=2..5]")
    test_selector("@a[distance=5]")
    test_selector("@a[distance=2..]")
    test_selector("@a[distance=..5]")
    test_selector("@a[dist=2..5]", "@a[distance=2..5]")
    test_selector("@a[dist=5]", "@a[distance=5]")
    test_selector("@a[dist=2..]", "@a[distance=2..]")
    test_selector("@a[dist=..5]", "@a[distance=..5]")
    test_selector("@a[dist=(2..5)]", "@a[distance=2..5]")
    test_selector("@a[dist=(5)]", "@a[distance=5]")
    test_selector("@a[dist=(2..)]", "@a[distance=2..]")
    test_selector("@a[dist=(..5)]", "@a[distance=..5]")
    test_selector("@a[distance=2.1..5.1]")
    test_selector("@a[distance=5.1]")
    test_selector("@a[distance=2.1..]")
    test_selector("@a[distance=..5.1]")
    test_selector("@a[dist=2.1..5.1]", "@a[distance=2.1..5.1]")
    test_selector("@a[dist=5.1]", "@a[distance=5.1]")
    test_selector("@a[dist=2.1..]", "@a[distance=2.1..]")
    test_selector("@a[dist=..5.1]", "@a[distance=..5.1]")
    test_selector("@a[dist=(2.1..5.1)]", "@a[distance=2.1..5.1]")
    test_selector("@a[dist=(5.1)]", "@a[distance=5.1]")
    test_selector("@a[dist=(2.1..)]", "@a[distance=2.1..]")
    test_selector("@a[dist=(..5.1)]", "@a[distance=..5.1]")

    test_selector("@a[level=2..5]")
    test_selector("@a[level=5]")
    test_selector("@a[level=2..]")
    test_selector("@a[level=..5]")
    test_selector("@a[lvl=2..5]", "@a[level=2..5]")
    test_selector("@a[lvl=5]", "@a[level=5]")
    test_selector("@a[lvl=2..]", "@a[level=2..]")
    test_selector("@a[lvl=..5]", "@a[level=..5]")
    test_selector("@a[lvl=(2..5)]", "@a[level=2..5]")
    test_selector("@a[lvl=(5)]", "@a[level=5]")
    test_selector("@a[lvl=(2..)]", "@a[level=2..]")
    test_selector("@a[lvl=(..5)]", "@a[level=..5]")
    test_selector("@a[level=2.1..5.1]")
    test_selector("@a[level=5.1]")
    test_selector("@a[level=2.1..]")
    test_selector("@a[level=..5.1]")
    test_selector("@a[lvl=2.1..5.1]", "@a[level=2.1..5.1]")
    test_selector("@a[lvl=5.1]", "@a[level=5.1]")
    test_selector("@a[lvl=2.1..]", "@a[level=2.1..]")
    test_selector("@a[lvl=..5.1]", "@a[level=..5.1]")
    test_selector("@a[lvl=(2.1..5.1)]", "@a[level=2.1..5.1]")
    test_selector("@a[lvl=(5.1)]", "@a[level=5.1]")
    test_selector("@a[lvl=(2.1..)]", "@a[level=2.1..]")
    test_selector("@a[lvl=(..5.1)]", "@a[level=..5.1]")

    test_selector("@a[x_rotation=2..5]")
    test_selector("@a[x_rotation=5]")
    test_selector("@a[x_rotation=2..]")
    test_selector("@a[x_rotation=..5]")
    test_selector("@a[xrot=2..5]", "@a[x_rotation=2..5]")
    test_selector("@a[xrot=5]", "@a[x_rotation=5]")
    test_selector("@a[xrot=2..]", "@a[x_rotation=2..]")
    test_selector("@a[xrot=..5]", "@a[x_rotation=..5]")
    test_selector("@a[xrot=(2..5)]", "@a[x_rotation=2..5]")
    test_selector("@a[xrot=(5)]", "@a[x_rotation=5]")
    test_selector("@a[xrot=(2..)]", "@a[x_rotation=2..]")
    test_selector("@a[xrot=(..5)]", "@a[x_rotation=..5]")
    test_selector("@a[x_rotation=2.1..5.1]")
    test_selector("@a[x_rotation=5.1]")
    test_selector("@a[x_rotation=2.1..]")
    test_selector("@a[x_rotation=..5.1]")
    test_selector("@a[xrot=2.1..5.1]", "@a[x_rotation=2.1..5.1]")
    test_selector("@a[xrot=5.1]", "@a[x_rotation=5.1]")
    test_selector("@a[xrot=2.1..]", "@a[x_rotation=2.1..]")
    test_selector("@a[xrot=..5.1]", "@a[x_rotation=..5.1]")
    test_selector("@a[xrot=(2.1..5.1)]", "@a[x_rotation=2.1..5.1]")
    test_selector("@a[xrot=(5.1)]", "@a[x_rotation=5.1]")
    test_selector("@a[xrot=(2.1..)]", "@a[x_rotation=2.1..]")
    test_selector("@a[xrot=(..5.1)]", "@a[x_rotation=..5.1]")

    test_selector("@a[y_rotation=2..5]")
    test_selector("@a[y_rotation=5]")
    test_selector("@a[y_rotation=2..]")
    test_selector("@a[y_rotation=..5]")
    test_selector("@a[yrot=2..5]", "@a[y_rotation=2..5]")
    test_selector("@a[yrot=5]", "@a[y_rotation=5]")
    test_selector("@a[yrot=2..]", "@a[y_rotation=2..]")
    test_selector("@a[yrot=..5]", "@a[y_rotation=..5]")
    test_selector("@a[yrot=(2..5)]", "@a[y_rotation=2..5]")
    test_selector("@a[yrot=(5)]", "@a[y_rotation=5]")
    test_selector("@a[yrot=(2..)]", "@a[y_rotation=2..]")
    test_selector("@a[yrot=(..5)]", "@a[y_rotation=..5]")
    test_selector("@a[y_rotation=2.1..5.1]")
    test_selector("@a[y_rotation=5.1]")
    test_selector("@a[y_rotation=2.1..]")
    test_selector("@a[y_rotation=..5.1]")
    test_selector("@a[yrot=2.1..5.1]", "@a[y_rotation=2.1..5.1]")
    test_selector("@a[yrot=5.1]", "@a[y_rotation=5.1]")
    test_selector("@a[yrot=2.1..]", "@a[y_rotation=2.1..]")
    test_selector("@a[yrot=..5.1]", "@a[y_rotation=..5.1]")
    test_selector("@a[yrot=(2.1..5.1)]", "@a[y_rotation=2.1..5.1]")
    test_selector("@a[yrot=(5.1)]", "@a[y_rotation=5.1]")
    test_selector("@a[yrot=(2.1..)]", "@a[y_rotation=2.1..]")
    test_selector("@a[yrot=(..5.1)]", "@a[y_rotation=..5.1]")

    test_selector("@a[limit=5,gamemode=creative]")

    test_selector("@a[hello]", "@a[tag=hello]")
    test_selector("@a[hello,objective=2..,x=5]", "@a[x=5,scores={objective=2..},tag=hello]")
    
    test_selector(
        "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,RRar=3..5]",
        "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,scores={RRar=3..5}]")

    test_selector(
        "@a[g.hello=5,x=-153,y=0,z=299,RRar=3..5]",
        "@a[x=-153,y=0,z=299,scores={g.hello=5,RRar=3..5}]")

    # multiple tags are fine
    test_selector("@a[a,b,c]", "@a[tag=a,tag=b,tag=c]")
    test_selector("@a[!a,!b,!c]", "@a[tag=!a,tag=!b,tag=!c]")
    test_selector("@a[!a,b,!c]", "@a[tag=!a,tag=b,tag=!c]")

    # testing grouping of type, team, name and gamemode
    test_selector("@a[m=!(1, 2)]", "@a[gamemode=!creative,gamemode=!adventure]")
    test_selector("@a[type=!(armor_stand, player)]", "@a[type=!armor_stand,type=!player]")
    test_selector("@a[team=!(rr.g, rr.b)]", "@a[team=!rr.g,team=!rr.b]")

    # note that names can be both strings and literal strings
    test_selector('@a[name=!(aquafina, daa)]", "@a[name=!aquafina,name=!daa]')
    test_selector('@a[name=!(ENFORCER_GAMING, "is a scrub")]", "@a[name=!ENFORCER_GAMING,name=!"is a scrub"]')
    test_selector('@a[name=!("broke it", "daddy daa")]", "@a[name=!"broke it",name=!"daddy daa"]')
    
    # literally no grouping can be a non-negation grouping
    test_selector("@a[m=(1, 2)]", expect_error=True)
    test_selector("@a[type=(armor_stand, player)]", expect_error=True)
    test_selector("@a[team=(rr.g, rr.b)]", expect_error=True)
    test_selector("@a[name=(aquafina, daa)]", expect_error=True)

    test_selector("@3", expect_error=True)
    test_selector("@a[a,]", expect_error=True)
    test_selector("@a[a,", expect_error=True)
    test_selector("@a[a", expect_error=True)
    test_selector("@a[obj=25,]", expect_error=True)
    test_selector("@a[obj=25,", expect_error=True)
    test_selector("@a[obj=25", expect_error=True)
    test_selector("@a[tag=hello]", expect_error=True)
    test_selector("@a[rm=5,rm=7]", expect_error=True)
    test_selector("@[]", expect_error=True)
    test_selector("nahfam", expect_error=True)
    test_selector("@a[obj=number]", expect_error=True)

    test_selector("@a[obj=25,obj=24]", expect_error=True)
    test_selector("@a[tag1,tag1]", expect_error=True)
    test_selector("@a[x=5,x=4]", expect_error=True)