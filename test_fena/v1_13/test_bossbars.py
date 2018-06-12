from test_fena.test_common import test_cmd

def test_bossbars():
    test_cmd(r'bossbar add ayylmao {"text":"test"}', r'bossbar add minecraft:ayylmao {"text":"test"}')
    test_cmd(r'bossbar add ayylmao "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove ayylmao',              r'bossbar remove minecraft:ayylmao')

    test_cmd(r'bossbar ayylmao color = white',  r'bossbar set minecraft:ayylmao color white')
    test_cmd(r'bossbar ayylmao color = pink',   r'bossbar set minecraft:ayylmao color pink')
    test_cmd(r'bossbar ayylmao color = red',    r'bossbar set minecraft:ayylmao color red')
    test_cmd(r'bossbar ayylmao color = yellow', r'bossbar set minecraft:ayylmao color yellow')
    test_cmd(r'bossbar ayylmao color = green',  r'bossbar set minecraft:ayylmao color green')
    test_cmd(r'bossbar ayylmao color = blue',   r'bossbar set minecraft:ayylmao color blue')
    test_cmd(r'bossbar ayylmao color = purple', r'bossbar set minecraft:ayylmao color purple')
    test_cmd(r'bossbar ayylmao color = nou',    expect_error=True)

    test_cmd(r'bossbar ayylmao style = 0',  r'bossbar set minecraft:ayylmao style progress')
    test_cmd(r'bossbar ayylmao style = 5',  expect_error=True)
    test_cmd(r'bossbar ayylmao style = 6',  r'bossbar set minecraft:ayylmao style notched_6')
    test_cmd(r'bossbar ayylmao style = 10', r'bossbar set minecraft:ayylmao style notched_10')
    test_cmd(r'bossbar ayylmao style = 12', r'bossbar set minecraft:ayylmao style notched_12')
    test_cmd(r'bossbar ayylmao style = 20', r'bossbar set minecraft:ayylmao style notched_20')

    test_cmd(r'bossbar ayylmao max = -1', expect_error=True)
    test_cmd(r'bossbar ayylmao max = 0',  expect_error=True)
    test_cmd(r'bossbar ayylmao max = 1',  r'bossbar set minecraft:ayylmao max 1')

    test_cmd(r'bossbar ayylmao value = -1', expect_error=True)
    test_cmd(r'bossbar ayylmao value = 0',  r'bossbar set minecraft:ayylmao value 0')
    test_cmd(r'bossbar ayylmao value = 1',  r'bossbar set minecraft:ayylmao value 1')

    test_cmd(r'bossbar ayylmao name = 1',               expect_error=True)
    test_cmd(r'bossbar ayylmao name = {"text":"test"}', r'bossbar set minecraft:ayylmao name {"text":"test"}')

    test_cmd(r'bossbar ayylmao players = @a',    r'bossbar set minecraft:ayylmao players @a')
    test_cmd(r'bossbar ayylmao visible = true',  r'bossbar set minecraft:ayylmao visible true')
    test_cmd(r'bossbar ayylmao visible = false', r'bossbar set minecraft:ayylmao visible false')

    test_cmd(r'bossbar ayylmao <- max',     r'bossbar get minecraft:ayylmao max')
    test_cmd(r'bossbar ayylmao <- value',   r'bossbar get minecraft:ayylmao value')
    test_cmd(r'bossbar ayylmao <- players', r'bossbar get minecraft:ayylmao players')
    test_cmd(r'bossbar ayylmao <- visible', r'bossbar get minecraft:ayylmao visible')


    test_cmd(r'bossbar add minecraft:ayylmao {"text":"test"}', r'bossbar add minecraft:ayylmao {"text":"test"}')
    test_cmd(r'bossbar add minecraft:ayylmao "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove minecraft:ayylmao',              r'bossbar remove minecraft:ayylmao')

    test_cmd(r'bossbar minecraft:ayylmao color = white',  r'bossbar set minecraft:ayylmao color white')
    test_cmd(r'bossbar minecraft:ayylmao color = pink',   r'bossbar set minecraft:ayylmao color pink')
    test_cmd(r'bossbar minecraft:ayylmao color = red',    r'bossbar set minecraft:ayylmao color red')
    test_cmd(r'bossbar minecraft:ayylmao color = yellow', r'bossbar set minecraft:ayylmao color yellow')
    test_cmd(r'bossbar minecraft:ayylmao color = green',  r'bossbar set minecraft:ayylmao color green')
    test_cmd(r'bossbar minecraft:ayylmao color = blue',   r'bossbar set minecraft:ayylmao color blue')
    test_cmd(r'bossbar minecraft:ayylmao color = purple', r'bossbar set minecraft:ayylmao color purple')
    test_cmd(r'bossbar minecraft:ayylmao color = nou',    expect_error=True)

    test_cmd(r'bossbar minecraft:ayylmao style = 0',  r'bossbar set minecraft:ayylmao style progress')
    test_cmd(r'bossbar minecraft:ayylmao style = 5',  expect_error=True)
    test_cmd(r'bossbar minecraft:ayylmao style = 6',  r'bossbar set minecraft:ayylmao style notched_6')
    test_cmd(r'bossbar minecraft:ayylmao style = 10', r'bossbar set minecraft:ayylmao style notched_10')
    test_cmd(r'bossbar minecraft:ayylmao style = 12', r'bossbar set minecraft:ayylmao style notched_12')
    test_cmd(r'bossbar minecraft:ayylmao style = 20', r'bossbar set minecraft:ayylmao style notched_20')

    test_cmd(r'bossbar minecraft:ayylmao max = -1', expect_error=True)
    test_cmd(r'bossbar minecraft:ayylmao max = 0',  expect_error=True)
    test_cmd(r'bossbar minecraft:ayylmao max = 1',  r'bossbar set minecraft:ayylmao max 1')

    test_cmd(r'bossbar minecraft:ayylmao value = -1', expect_error=True)
    test_cmd(r'bossbar minecraft:ayylmao value = 0',  r'bossbar set minecraft:ayylmao value 0')
    test_cmd(r'bossbar minecraft:ayylmao value = 1',  r'bossbar set minecraft:ayylmao value 1')

    test_cmd(r'bossbar minecraft:ayylmao name = 1',               expect_error=True)
    test_cmd(r'bossbar minecraft:ayylmao name = {"text":"test"}', r'bossbar set minecraft:ayylmao name {"text":"test"}')

    test_cmd(r'bossbar minecraft:ayylmao players = @a',    r'bossbar set minecraft:ayylmao players @a')
    test_cmd(r'bossbar minecraft:ayylmao visible = true',  r'bossbar set minecraft:ayylmao visible true')
    test_cmd(r'bossbar minecraft:ayylmao visible = false', r'bossbar set minecraft:ayylmao visible false')

    test_cmd(r'bossbar minecraft:ayylmao <- max',     r'bossbar get minecraft:ayylmao max')
    test_cmd(r'bossbar minecraft:ayylmao <- value',   r'bossbar get minecraft:ayylmao value')
    test_cmd(r'bossbar minecraft:ayylmao <- players', r'bossbar get minecraft:ayylmao players')
    test_cmd(r'bossbar minecraft:ayylmao <- visible', r'bossbar get minecraft:ayylmao visible')


    test_cmd(r'bossbar add nou:ayylmao {"text":"test"}', r'bossbar add nou:ayylmao {"text":"test"}')
    test_cmd(r'bossbar add nou:ayylmao "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove nou:ayylmao',              r'bossbar remove nou:ayylmao')

    test_cmd(r'bossbar nou:ayylmao color = white',  r'bossbar set nou:ayylmao color white')
    test_cmd(r'bossbar nou:ayylmao color = pink',   r'bossbar set nou:ayylmao color pink')
    test_cmd(r'bossbar nou:ayylmao color = red',    r'bossbar set nou:ayylmao color red')
    test_cmd(r'bossbar nou:ayylmao color = yellow', r'bossbar set nou:ayylmao color yellow')
    test_cmd(r'bossbar nou:ayylmao color = green',  r'bossbar set nou:ayylmao color green')
    test_cmd(r'bossbar nou:ayylmao color = blue',   r'bossbar set nou:ayylmao color blue')
    test_cmd(r'bossbar nou:ayylmao color = purple', r'bossbar set nou:ayylmao color purple')
    test_cmd(r'bossbar nou:ayylmao color = nou',    expect_error=True)

    test_cmd(r'bossbar nou:ayylmao style = 0',  r'bossbar set nou:ayylmao style progress')
    test_cmd(r'bossbar nou:ayylmao style = 5',  expect_error=True)
    test_cmd(r'bossbar nou:ayylmao style = 6',  r'bossbar set nou:ayylmao style notched_6')
    test_cmd(r'bossbar nou:ayylmao style = 10', r'bossbar set nou:ayylmao style notched_10')
    test_cmd(r'bossbar nou:ayylmao style = 12', r'bossbar set nou:ayylmao style notched_12')
    test_cmd(r'bossbar nou:ayylmao style = 20', r'bossbar set nou:ayylmao style notched_20')

    test_cmd(r'bossbar nou:ayylmao max = -1', expect_error=True)
    test_cmd(r'bossbar nou:ayylmao max = 0',  expect_error=True)
    test_cmd(r'bossbar nou:ayylmao max = 1',  r'bossbar set nou:ayylmao max 1')

    test_cmd(r'bossbar nou:ayylmao value = -1', expect_error=True)
    test_cmd(r'bossbar nou:ayylmao value = 0',  r'bossbar set nou:ayylmao value 0')
    test_cmd(r'bossbar nou:ayylmao value = 1',  r'bossbar set nou:ayylmao value 1')

    test_cmd(r'bossbar nou:ayylmao name = 1',               expect_error=True)
    test_cmd(r'bossbar nou:ayylmao name = {"text":"test"}', r'bossbar set nou:ayylmao name {"text":"test"}')

    test_cmd(r'bossbar nou:ayylmao players = @a',    r'bossbar set nou:ayylmao players @a')
    test_cmd(r'bossbar nou:ayylmao visible = true',  r'bossbar set nou:ayylmao visible true')
    test_cmd(r'bossbar nou:ayylmao visible = false', r'bossbar set nou:ayylmao visible false')

    test_cmd(r'bossbar nou:ayylmao <- max',     r'bossbar get nou:ayylmao max')
    test_cmd(r'bossbar nou:ayylmao <- value',   r'bossbar get nou:ayylmao value')
    test_cmd(r'bossbar nou:ayylmao <- players', r'bossbar get nou:ayylmao players')
    test_cmd(r'bossbar nou:ayylmao <- visible', r'bossbar get nou:ayylmao visible')



    test_cmd(r'bossbar add _pl {"text":"test"}', r'bossbar add minecraft:fena.pl {"text":"test"}')
    test_cmd(r'bossbar add _pl "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove _pl',              r'bossbar remove minecraft:fena.pl')

    test_cmd(r'bossbar _pl color = white',  r'bossbar set minecraft:fena.pl color white')
    test_cmd(r'bossbar _pl color = pink',   r'bossbar set minecraft:fena.pl color pink')
    test_cmd(r'bossbar _pl color = red',    r'bossbar set minecraft:fena.pl color red')
    test_cmd(r'bossbar _pl color = yellow', r'bossbar set minecraft:fena.pl color yellow')
    test_cmd(r'bossbar _pl color = green',  r'bossbar set minecraft:fena.pl color green')
    test_cmd(r'bossbar _pl color = blue',   r'bossbar set minecraft:fena.pl color blue')
    test_cmd(r'bossbar _pl color = purple', r'bossbar set minecraft:fena.pl color purple')
    test_cmd(r'bossbar _pl color = nou',    expect_error=True)

    test_cmd(r'bossbar _pl style = 0',  r'bossbar set minecraft:fena.pl style progress')
    test_cmd(r'bossbar _pl style = 5',  expect_error=True)
    test_cmd(r'bossbar _pl style = 6',  r'bossbar set minecraft:fena.pl style notched_6')
    test_cmd(r'bossbar _pl style = 10', r'bossbar set minecraft:fena.pl style notched_10')
    test_cmd(r'bossbar _pl style = 12', r'bossbar set minecraft:fena.pl style notched_12')
    test_cmd(r'bossbar _pl style = 20', r'bossbar set minecraft:fena.pl style notched_20')

    test_cmd(r'bossbar _pl max = -1', expect_error=True)
    test_cmd(r'bossbar _pl max = 0',  expect_error=True)
    test_cmd(r'bossbar _pl max = 1',  r'bossbar set minecraft:fena.pl max 1')

    test_cmd(r'bossbar _pl value = -1', expect_error=True)
    test_cmd(r'bossbar _pl value = 0',  r'bossbar set minecraft:fena.pl value 0')
    test_cmd(r'bossbar _pl value = 1',  r'bossbar set minecraft:fena.pl value 1')

    test_cmd(r'bossbar _pl name = 1',               expect_error=True)
    test_cmd(r'bossbar _pl name = {"text":"test"}', r'bossbar set minecraft:fena.pl name {"text":"test"}')

    test_cmd(r'bossbar _pl players = @a',    r'bossbar set minecraft:fena.pl players @a')
    test_cmd(r'bossbar _pl visible = true',  r'bossbar set minecraft:fena.pl visible true')
    test_cmd(r'bossbar _pl visible = false', r'bossbar set minecraft:fena.pl visible false')

    test_cmd(r'bossbar _pl <- max',     r'bossbar get minecraft:fena.pl max')
    test_cmd(r'bossbar _pl <- value',   r'bossbar get minecraft:fena.pl value')
    test_cmd(r'bossbar _pl <- players', r'bossbar get minecraft:fena.pl players')
    test_cmd(r'bossbar _pl <- visible', r'bossbar get minecraft:fena.pl visible')


    test_cmd(r'bossbar add minecraft:_pl {"text":"test"}', r'bossbar add minecraft:fena.pl {"text":"test"}')
    test_cmd(r'bossbar add minecraft:_pl "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove minecraft:_pl',              r'bossbar remove minecraft:fena.pl')

    test_cmd(r'bossbar minecraft:_pl color = white',  r'bossbar set minecraft:fena.pl color white')
    test_cmd(r'bossbar minecraft:_pl color = pink',   r'bossbar set minecraft:fena.pl color pink')
    test_cmd(r'bossbar minecraft:_pl color = red',    r'bossbar set minecraft:fena.pl color red')
    test_cmd(r'bossbar minecraft:_pl color = yellow', r'bossbar set minecraft:fena.pl color yellow')
    test_cmd(r'bossbar minecraft:_pl color = green',  r'bossbar set minecraft:fena.pl color green')
    test_cmd(r'bossbar minecraft:_pl color = blue',   r'bossbar set minecraft:fena.pl color blue')
    test_cmd(r'bossbar minecraft:_pl color = purple', r'bossbar set minecraft:fena.pl color purple')
    test_cmd(r'bossbar minecraft:_pl color = nou',    expect_error=True)

    test_cmd(r'bossbar minecraft:_pl style = 0',  r'bossbar set minecraft:fena.pl style progress')
    test_cmd(r'bossbar minecraft:_pl style = 5',  expect_error=True)
    test_cmd(r'bossbar minecraft:_pl style = 6',  r'bossbar set minecraft:fena.pl style notched_6')
    test_cmd(r'bossbar minecraft:_pl style = 10', r'bossbar set minecraft:fena.pl style notched_10')
    test_cmd(r'bossbar minecraft:_pl style = 12', r'bossbar set minecraft:fena.pl style notched_12')
    test_cmd(r'bossbar minecraft:_pl style = 20', r'bossbar set minecraft:fena.pl style notched_20')

    test_cmd(r'bossbar minecraft:_pl max = -1', expect_error=True)
    test_cmd(r'bossbar minecraft:_pl max = 0',  expect_error=True)
    test_cmd(r'bossbar minecraft:_pl max = 1',  r'bossbar set minecraft:fena.pl max 1')

    test_cmd(r'bossbar minecraft:_pl value = -1', expect_error=True)
    test_cmd(r'bossbar minecraft:_pl value = 0',  r'bossbar set minecraft:fena.pl value 0')
    test_cmd(r'bossbar minecraft:_pl value = 1',  r'bossbar set minecraft:fena.pl value 1')

    test_cmd(r'bossbar minecraft:_pl name = 1',               expect_error=True)
    test_cmd(r'bossbar minecraft:_pl name = {"text":"test"}', r'bossbar set minecraft:fena.pl name {"text":"test"}')

    test_cmd(r'bossbar minecraft:_pl players = @a',    r'bossbar set minecraft:fena.pl players @a')
    test_cmd(r'bossbar minecraft:_pl visible = true',  r'bossbar set minecraft:fena.pl visible true')
    test_cmd(r'bossbar minecraft:_pl visible = false', r'bossbar set minecraft:fena.pl visible false')

    test_cmd(r'bossbar minecraft:_pl <- max',     r'bossbar get minecraft:fena.pl max')
    test_cmd(r'bossbar minecraft:_pl <- value',   r'bossbar get minecraft:fena.pl value')
    test_cmd(r'bossbar minecraft:_pl <- players', r'bossbar get minecraft:fena.pl players')
    test_cmd(r'bossbar minecraft:_pl <- visible', r'bossbar get minecraft:fena.pl visible')


    test_cmd(r'bossbar add nou:_pl {"text":"test"}', r'bossbar add nou:fena.pl {"text":"test"}')
    test_cmd(r'bossbar add nou:_pl "test"',          expect_error=True) # note that this is valid in minecraft
    test_cmd(r'bossbar remove nou:_pl',              r'bossbar remove nou:fena.pl')

    test_cmd(r'bossbar nou:_pl color = white',  r'bossbar set nou:fena.pl color white')
    test_cmd(r'bossbar nou:_pl color = pink',   r'bossbar set nou:fena.pl color pink')
    test_cmd(r'bossbar nou:_pl color = red',    r'bossbar set nou:fena.pl color red')
    test_cmd(r'bossbar nou:_pl color = yellow', r'bossbar set nou:fena.pl color yellow')
    test_cmd(r'bossbar nou:_pl color = green',  r'bossbar set nou:fena.pl color green')
    test_cmd(r'bossbar nou:_pl color = blue',   r'bossbar set nou:fena.pl color blue')
    test_cmd(r'bossbar nou:_pl color = purple', r'bossbar set nou:fena.pl color purple')
    test_cmd(r'bossbar nou:_pl color = nou',    expect_error=True)

    test_cmd(r'bossbar nou:_pl style = 0',  r'bossbar set nou:fena.pl style progress')
    test_cmd(r'bossbar nou:_pl style = 5',  expect_error=True)
    test_cmd(r'bossbar nou:_pl style = 6',  r'bossbar set nou:fena.pl style notched_6')
    test_cmd(r'bossbar nou:_pl style = 10', r'bossbar set nou:fena.pl style notched_10')
    test_cmd(r'bossbar nou:_pl style = 12', r'bossbar set nou:fena.pl style notched_12')
    test_cmd(r'bossbar nou:_pl style = 20', r'bossbar set nou:fena.pl style notched_20')

    test_cmd(r'bossbar nou:_pl max = -1', expect_error=True)
    test_cmd(r'bossbar nou:_pl max = 0',  expect_error=True)
    test_cmd(r'bossbar nou:_pl max = 1',  r'bossbar set nou:fena.pl max 1')

    test_cmd(r'bossbar nou:_pl value = -1', expect_error=True)
    test_cmd(r'bossbar nou:_pl value = 0',  r'bossbar set nou:fena.pl value 0')
    test_cmd(r'bossbar nou:_pl value = 1',  r'bossbar set nou:fena.pl value 1')

    test_cmd(r'bossbar nou:_pl name = 1',               expect_error=True)
    test_cmd(r'bossbar nou:_pl name = {"text":"test"}', r'bossbar set nou:fena.pl name {"text":"test"}')

    test_cmd(r'bossbar nou:_pl players = @a',    r'bossbar set nou:fena.pl players @a')
    test_cmd(r'bossbar nou:_pl visible = true',  r'bossbar set nou:fena.pl visible true')
    test_cmd(r'bossbar nou:_pl visible = false', r'bossbar set nou:fena.pl visible false')

    test_cmd(r'bossbar nou:_pl <- max',     r'bossbar get nou:fena.pl max')
    test_cmd(r'bossbar nou:_pl <- value',   r'bossbar get nou:fena.pl value')
    test_cmd(r'bossbar nou:_pl <- players', r'bossbar get nou:fena.pl players')
    test_cmd(r'bossbar nou:_pl <- visible', r'bossbar get nou:fena.pl visible')

