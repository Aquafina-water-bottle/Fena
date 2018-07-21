from test_fena.test_common import test_json

def test_jsons():
    test_json(
        r'''{
            "text": "",
            "extra": [
                {
                    "text": "[",
                    "color": "gray"
                },
                {
                    "text": "MM",
                    "color": "gold",
                    "bold": "true",
                    "hoverEvent": {
                        "action": "show_text",
                        "value": {
                            "text": "Mastermind",
                            "color": "gold"
                        }
                    },
                    "clickEvent": {
                        "action": "run_command",
                        "value": "/scoreboard players set @p FLtp 1217546713"
                    }
                },
                {
                    "text": "]",
                    "color": "gray"
                },
                {
                    "text": ": "
                },
                {
                    "text": "The correct combo is ",
                    "color": "green"
                },
                {
                    "selector": "@e[type=armor_stand,MMrn=12,MMCorrect1]"
                },
                {
                    "text": ", ",
                    "color": "green"
                },
                {
                    "selector": "@e[type=armor_stand,MMrn=12,MMCorrect2]"
                },
                {
                    "text": ", ",
                    "color": "green"
                },
                {
                    "selector": "@e[type=armor_stand,MMrn=12,MMCorrect3]"
                },
                {
                    "text": " and ",
                    "color": "green"
                },
                {
                    "selector": "@e[type=armor_stand,MMrn=12,MMCorrect4]"
                },
                {
                    "text": "!",
                    "color": "green"
                }
            ]
        }''',
        r'{"text":"","extra":[{"text":"[","color":"gray"},{"text":"MM","color":"gold","bold":"true","hoverEvent":{"action":"show_text","value":{"text":"Mastermind","color":"gold"}},"clickEvent":{"action":"run_command","value":"/scoreboard players set @p FLtp 1217546713"}},{"text":"]","color":"gray"},{"text":": "},{"text":"The correct combo is ","color":"green"},{"selector":"@e[type=minecraft:armor_stand,score_MMrn_min=12,score_MMrn=12,tag=MMCorrect1]"},{"text":", ","color":"green"},{"selector":"@e[type=minecraft:armor_stand,score_MMrn_min=12,score_MMrn=12,tag=MMCorrect2]"},{"text":", ","color":"green"},{"selector":"@e[type=minecraft:armor_stand,score_MMrn_min=12,score_MMrn=12,tag=MMCorrect3]"},{"text":" and ","color":"green"},{"selector":"@e[type=minecraft:armor_stand,score_MMrn_min=12,score_MMrn=12,tag=MMCorrect4]"},{"text":"!","color":"green"}]}')

    test_json(r'{"asdf":1, "asdf2":2, "asdf3":3}', r'{"asdf":1,"asdf2":2,"asdf3":3}')
    test_json(r'{"asdf":1, "asdf2":2}', r'{"asdf":1,"asdf2":2}')
    test_json(r'{"asdf":1}')
    test_json(
        r'{"asdf": [{"arg": "value"}, 1, 1.2, 1e1, 1.2e1, 1.2e+1, [1, 2, 3], "hello", true, false, null]}',
        r'{"asdf":[{"arg":"value"},1,1.2,1e1,1.2e1,1.2e+1,[1,2,3],"hello",true,false,null]}')
    test_json(r'{}')

    # selectors
    test_json(r'{"selector":"@a[_pl=1..]"}', r'{"selector":"@a[score_fena.pl_min=1]"}')
    test_json(r'{"score":{"objective":"_pl","name":"@a[_pl=1..]"}}', r'{"score":{"objective":"fena.pl","name":"@a[score_fena.pl_min=1]"}}')
    test_json(r'{"score":{"objective":"_pl","name":"french_man"}}', r'{"score":{"objective":"fena.pl","name":"french_man"}}')

    test_json(r'{', expect_error=True)
    test_json(r'}', expect_error=True)
    test_json(r'{"test":1,}', expect_error=True)
    test_json(r'{,"test":2}', expect_error=True)
    test_json(r'{"test":1, "test":2, "test":3}', expect_error=True)
    test_json(r'{"test":1, "test2":2, "test3":3, }', expect_error=True)
    test_json(r'{"test":1, "test2":2, "test3":3{', expect_error=True)
    test_json(r'{"test":1 "test2":2}', expect_error=True)
    test_json(r'{test:1}', expect_error=True)
    test_json(r'{"test":not_null}', expect_error=True)
    test_json(r'nou', expect_error=True)
    test_json(r'{nou}', expect_error=True)
    test_json(r'{"nou":1, nou}', expect_error=True)
    test_json(r'{"nou:1}', expect_error=True)
    test_json(r'{"nou":1, []}', expect_error=True)
    test_json(r'{"nou":[1, 2,]}', expect_error=True)