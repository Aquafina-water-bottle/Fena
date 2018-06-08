from test_fena.test_common import test_selector

def test_selectors():
    test_selector("@p")
    test_selector("@a[]")
    test_selector("@e[type=armor_stand]", "@e[type=minecraft:armor_stand]")
    test_selector("@e[type=minecraft:armor_stand]")
    test_selector("@e[type=armor_stand,c=1]", "@e[type=minecraft:armor_stand,c=1]")
    test_selector("@e[type=armor_stand,dist=1..2]", "@e[type=minecraft:armor_stand,rm=1,r=2]")
    test_selector("@a[x]", "@a[tag=x]")

    test_selector("@a[RRpl=3..4]", "@a[score_RRpl_min=3,score_RRpl=4]")
    test_selector("@a[RRpl=3..]", "@a[score_RRpl_min=3]")
    test_selector("@a[RRpl=..3]", "@a[score_RRpl=3]")
    test_selector("@a[RRpl=3]", "@a[score_RRpl_min=3,score_RRpl=3]")
    test_selector("@a[RRpl=*]", "@a[score_RRpl_min=-2147483648]")
    test_selector("@a[RRpl=(3..4)]", "@a[score_RRpl_min=3,score_RRpl=4]")
    test_selector("@a[RRpl=(3..)]", "@a[score_RRpl_min=3]")
    test_selector("@a[RRpl=(..3)]", "@a[score_RRpl=3]")
    test_selector("@a[RRpl=(3)]", "@a[score_RRpl_min=3,score_RRpl=3]")
    test_selector("@a[RRpl=(*)]", "@a[score_RRpl_min=-2147483648]")
    test_selector("@a[RRpl=((((3..))))]", "@a[score_RRpl_min=3]")

    test_selector("@a[distance=2..5]", "@a[rm=2,r=5]")
    test_selector("@a[distance=5]", "@a[rm=5,r=5]")
    test_selector("@a[distance=2..]", "@a[rm=2]")
    test_selector("@a[distance=..5]", "@a[r=5]")
    test_selector("@a[dist=2..5]", "@a[rm=2,r=5]")
    test_selector("@a[dist=5]", "@a[rm=5,r=5]")
    test_selector("@a[dist=2..]", "@a[rm=2]")
    test_selector("@a[dist=..5]", "@a[r=5]")
    test_selector("@a[dist=(2..5)]", "@a[rm=2,r=5]")
    test_selector("@a[dist=(5)]", "@a[rm=5,r=5]")
    test_selector("@a[dist=(2..)]", "@a[rm=2]")
    test_selector("@a[dist=(..5)]", "@a[r=5]")

    test_selector("@a[level=2..5]", "@a[lm=2,l=5]")
    test_selector("@a[level=5]", "@a[lm=5,l=5]")
    test_selector("@a[level=2..]", "@a[lm=2]")
    test_selector("@a[level=..5]", "@a[l=5]")
    test_selector("@a[lvl=2..5]", "@a[lm=2,l=5]")
    test_selector("@a[lvl=5]", "@a[lm=5,l=5]")
    test_selector("@a[lvl=2..]", "@a[lm=2]")
    test_selector("@a[lvl=..5]", "@a[l=5]")
    test_selector("@a[lvl=(2..5)]", "@a[lm=2,l=5]")
    test_selector("@a[lvl=(5)]", "@a[lm=5,l=5]")
    test_selector("@a[lvl=(2..)]", "@a[lm=2]")
    test_selector("@a[lvl=(..5)]", "@a[l=5]")

    test_selector("@a[x_rotation=2..5]", "@a[rxm=2,rx=5]")
    test_selector("@a[x_rotation=5]", "@a[rxm=5,rx=5]")
    test_selector("@a[x_rotation=2..]", "@a[rxm=2]")
    test_selector("@a[x_rotation=..5]", "@a[rx=5]")
    test_selector("@a[xrot=2..5]", "@a[rxm=2,rx=5]")
    test_selector("@a[xrot=5]", "@a[rxm=5,rx=5]")
    test_selector("@a[xrot=2..]", "@a[rxm=2]")
    test_selector("@a[xrot=..5]", "@a[rx=5]")
    test_selector("@a[xrot=(2..5)]", "@a[rxm=2,rx=5]")
    test_selector("@a[xrot=(5)]", "@a[rxm=5,rx=5]")
    test_selector("@a[xrot=(2..)]", "@a[rxm=2]")
    test_selector("@a[xrot=(..5)]", "@a[rx=5]")

    test_selector("@a[y_rotation=2..5]", "@a[rym=2,ry=5]")
    test_selector("@a[y_rotation=5]", "@a[rym=5,ry=5]")
    test_selector("@a[y_rotation=2..]", "@a[rym=2]")
    test_selector("@a[y_rotation=..5]", "@a[ry=5]")
    test_selector("@a[yrot=2..5]", "@a[rym=2,ry=5]")
    test_selector("@a[yrot=5]", "@a[rym=5,ry=5]")
    test_selector("@a[yrot=2..]", "@a[rym=2]")
    test_selector("@a[yrot=..5]", "@a[ry=5]")
    test_selector("@a[yrot=(2..5)]", "@a[rym=2,ry=5]")
    test_selector("@a[yrot=(5)]", "@a[rym=5,ry=5]")
    test_selector("@a[yrot=(2..)]", "@a[rym=2]")
    test_selector("@a[yrot=(..5)]", "@a[ry=5]")

    test_selector("@a[limit=5,gamemode=creative]", "@a[c=5,m=1]")

    test_selector("@a[hello]", "@a[tag=hello]")

    # note that things will become rearranged in the following order:
    # defaults, scores, tags
    test_selector("@a[hello,objective=2..,x=5]", "@a[x=5,score_objective_min=2,tag=hello]")
    
    test_selector(
        "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,RRar=3..5]",
        "@a[x=-153,y=0,z=299,dx=158,dy=110,dz=168,m=2,score_RRar_min=3,score_RRar=5]")

    test_selector(
        "@a[g.hello=5,x=-153,y=0,z=299,RRar=3..5]",
        "@a[x=-153,y=0,z=299,score_g.hello_min=5,score_g.hello=5,score_RRar_min=3,score_RRar=5]")

    test_selector("@3", expect_error=True)
    test_selector("@a[a,b,c]", expect_error=True)
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
    test_selector("@a[obj=25=5]", expect_error=True)

    test_selector("@a[obj=25,obj=24]", expect_error=True)
    test_selector("@a[tag1,tag1]", expect_error=True)
    test_selector("@a[x=5,x=4]", expect_error=True)

