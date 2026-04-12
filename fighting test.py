#Note: When playing this game, there is a chance that the first few rooms will all contain nothing. In this case, just keep moving.


from cave import Cave
from character import Character,Enemy,Friend
from item import Item, Card
#from cards import Card (removed code)
import random
import copy
dead=False
'''
cavern = Cave("Cavern")
cavern.set_description("A dank and dirty cave ")
dungeon = Cave("Dungeon")
dungeon.set_description("A large cave with a rack")
grotto = Cave("Grotto")
grotto.set_description("A small cave with ancient graffiti")

cavern.link_cave(dungeon, 'south')
grotto.link_cave(dungeon, 'east')
dungeon.link_cave(cavern, 'north')
dungeon.link_cave(grotto, 'west')

harry = Enemy("Harry", "A smelly Wumpus")
harry.set_conversation("Hangry…Hanggrry")
harry.set_weakness("vegemite")

dungeon.set_character(harry)

josephine = Friend("Josephine", "A friendly bat")
josephine.set_conversation("Gidday")
grotto.set_character(josephine)
vegemite = Item("vegemite")
vegemite.set_description("A Wumpuses worst nightmare")
grotto.set_item(vegemite)

torch = Item("torch")
torch.set_description("A light for the end of the tunnel")
dungeon.set_item(torch)


cavern.describe()


current_cave = cavern
'''

#Creating cards
draw_strike = Card('Draw Strike')
draw_strike.create([['Attack', 8],['Draw', 1]])
draw_strike.set_description('Deal 8 damage to an enemy and draw a card.')
draw_strike.set_cost(1)

quick_strike = Card('Quick Strike')
quick_strike.create([['Attack', 5]])
quick_strike.set_description('Deal 5 damage to an enemy. Costs no energy. Warning: Turn ends automatically at 0 energy, even if you have a free card!')
quick_strike.set_cost(0)

heavy_blade = Card('Heavy Blade')
heavy_blade.create([['Attack', 12]])
heavy_blade.set_description('Deal 12 damage to an enemy.')
heavy_blade.set_cost(1)

big_shield = Card('Big Shield')
big_shield.create([['Block', 12]])
big_shield.set_description('Gain 12 block.')
big_shield.set_cost(1)

energy = Card('Energy')
energy.create([])
energy.set_description('Gain 1 energy. Exhaust.')
energy.set_cost(-1)
energy.exhaust = True

blood_spike = Card('Blood Spike')
blood_spike.create([['Attack', 20]])
blood_spike.set_description('Deal 20 damage to an enemy. You lose 3 hp.')
blood_spike.set_cost(1)
blood_spike.set_hp_loss(3)

draw = Card('Draw')
draw.create([['Draw', 3]])
draw.set_description('Draw 3 cards.')
draw.set_cost(1)

inflame = Card('Inflame')
inflame.create([])
inflame.set_description('Gain 2 strength. Strength increases damage dealt.')
inflame.set_cost(1)

poison = Card('Poison')
poison.create([['Attack', 0]])
poison.set_description('Apply 5 poison to an enemy. Poison does damage at the end of your turn and decrements by 1.')
poison.set_cost(1)
poison.set_poison(5)

armour_up = Card('Armour Up')
armour_up.create([])
armour_up.set_description('Gain 4 block each turn. Exhaust.')
armour_up.set_cost(1)
armour_up.exhaust = True

twin_strike = Card('Twin Strike')
twin_strike.create([['Attack',5],['Attack',5]])
twin_strike.set_description('Deal 5 damage twice.')
twin_strike.set_cost(1)

heal = Card('Heal')
heal.create([])
heal.set_description('Heal for 5 hp. Exhaust.')
heal.set_hp_loss(-5)
heal.set_cost(1)
heal.exhaust = True



#rare
bludgeon = Card('Bludgeon')
bludgeon.create([['Attack', 40]])
bludgeon.set_description('Deal 40 damage to an enemy.')
bludgeon.set_cost(3)

immolate = Card('Immolate')
immolate.create([['Attack', 35]])
immolate.set_description('Deal 35 damage to an enemy. Shuffle 2 burns into your deck.')
immolate.set_cost(2)

ritual = Card('Ritual')
ritual.create([['Draw', 2]])
ritual.set_description('Draw 2 cards and gain 2 energy, but you lose 6 hp.')
ritual.set_cost(-2)
ritual.set_hp_loss(6)

impervious = Card('Impervious')
impervious.create([['Block', 30]])
impervious.set_description('Gain 30 block.')
impervious.set_cost(2)

mind_bloom = Card('Mind Bloom')
mind_bloom.create([['Draw', 30]])
mind_bloom.set_description('Draw 30 cards. Warning: Will only draw as many cards as you have!')
mind_bloom.set_cost(1)

deadly_poison = Card('Deadly Poison')
deadly_poison.create([['Attack', 0]])
deadly_poison.set_description('Apply 10 poison.')
deadly_poison.set_cost(1)
deadly_poison.set_poison(10)

demon_form = Card('Demon Form')
demon_form.create([])
demon_form.set_description('Gain 3 strength each turn. Exhaust.')
demon_form.set_cost(3)
demon_form.exhaust = True

arcane_mastery = Card('Arcane Mastery')
arcane_mastery.create([['Draw', 3], ['Attack', 3], ['Block', 3]])
arcane_mastery.set_description('Deal 3 damage, gain 3 block, and draw 3 cards. Exhaust.')
arcane_mastery.set_cost(0)
arcane_mastery.exhaust = True

judgement = Card('Judgement')
judgement.create([['Attack', 0]])
judgement.set_description('Kill an enemy if it has 30 hp or less.')
judgement.set_cost(1)

ragnarok = Card('Ragnarok')
ragnarok.create([['Attack', 5],['Attack', 5],['Attack', 5],['Attack', 5]])
ragnarok.set_description('Deal 5 damage 4 times.')
ragnarok.set_cost(1)

#status
burn = Card('Burn')
burn.create([])
burn.set_description('Take 2 damage if this card is in your hand at end of turn.')
burn.set_cost(2)

dazed = Card('Dazed')
dazed.create([])
dazed.set_description('Exhaust.')
dazed.set_cost(0)
dazed.exhaust = True

wound = Card('Wound')
wound.create([])
wound.set_description('Does nothing.')
wound.set_cost(0)

slimed = Card('Slimed')
slimed.create([])
slimed.set_description('Exhaust.')
slimed.set_cost(1)

dread = Card('Dread')
dread.create([])
dread.set_description('You feel a sense of Dread. If this is still in your hand at the end of your turn, the Maw gains 10 strength.')
dread.set_cost(999)

erased = Card('Erased')
erased.create([])
erased.set_description('You feel the erasure growing. If this is still in your hand at the end of your turn, copy this card.')
erased.set_cost(1)

glitched = Card('Glitched')
glitched.create([])
glitched.set_description('Gain 1 strength. Double your strength.')
glitched.set_cost(1)

voided = Card('Void')
voided.create([])
voided.set_description('If this card is in your hand at the end of your turn, lose one energy next turn.')
voided.set_cost(1)

darkness = Card('Doom')
darkness.create([])
darkness.set_description('If this card is in your hand at the end of your turn, lose 5 hp and gain 5 strength.')
darkness.set_cost(1)

statuses = [burn, dazed, wound, slimed, dread, erased, glitched, voided, darkness]

card_pool = [draw_strike, quick_strike, heavy_blade, big_shield, energy, blood_spike, poison, armour_up, twin_strike, heal]
rare_card_pool = [bludgeon, ritual, mind_bloom, deadly_poison, demon_form, impervious, arcane_mastery, judgement, ragnarok, immolate]
#Creating cards end

combat_manual = Item('Combat Manual')
combat_manual.set_description('Draw one more card each turn.')

small_heart = Item('Small Heart')
small_heart.set_description('Gain 20 hp.')

whetstone = Item('Whetstone')
whetstone.set_description('Gain 2 strength each battle.')

wet_stone = Item('Wet Stone')
wet_stone.set_description('Gain 2 dexterity each battle.')

power_ring = Item('Power Ring')
power_ring.set_description('At the start of your turn, deal 4 damage to the first enemy.')

anchor = Item('Anchor')
anchor.set_description('Gain 10 block on turn 1.')

piggy_bank = Item('Piggy Bank')
piggy_bank.set_description('Gain 10 extra gold each combat.')




relic_pool = [power_ring, small_heart, whetstone, wet_stone, combat_manual, anchor, piggy_bank]

big_heart = Item('Big Heart')
big_heart.set_description('Gain 40 hp.')

horn_cleat = Item('Horn Cleat')
horn_cleat.set_description('Gain 14 block on turn 2.')

captains_wheel = Item("Captain's Wheel")
captains_wheel.set_description('Gain 18 block on turn 3.')

shuriken = Item('Shuriken')
shuriken.set_description('Every 2 attacks you play, gain 1 strength.')
shuriken_count = False

kunai = Item('Kunai')
kunai.set_description('Every 2 non-attacks you play, gain 1 dexterity.')
kunai_count = False

black_blood = Item('Black Blood')
black_blood.set_description('Heal for 10 at the end of each elite.')

rare_relic_pool = [big_heart, horn_cleat, captains_wheel, shuriken, kunai, black_blood]

poisoned = Item('Poisoned')
poisoned.set_description('Start each combat poisoned for 3. WARNING: POISON ON YOU CARRIES OVER BETWEEN FIGHTS.')

burned = Item('Burned')
burned.set_description('Add 2 burns to your deck.')

wounded = Item('Wounded')
wounded.set_description('Lose 30 hp.')

doomed = Item('Doomed')
doomed.set_description('Teleport to the boss.')

scatterbrained = Item('Scatterbrained')
scatterbrained.set_description('Add 7 dazed to your deck.')

incapacitated = Item('Incapacitated')
incapacitated.set_description('Draw one less card each turn.')

blight_pool = [poisoned, burned, wounded, doomed, scatterbrained, incapacitated]

coffee = Item('Coffee')
coffee.set_description('Gain 1 energy each turn.')

arcane_manual = Item('Arcane Manual')
arcane_manual.set_description('Draw 5 additional cards each turn.')

snecko_eye = Item('Snecko Eye')
snecko_eye.set_description('Draw 2 additional cards each turn. Randomise all card costs between -1 and 2. Warning: cards will no longer give energy.')

ships_sail = Item("Ship's Sail")
ships_sail.set_description('Gain 22 block each turn after turn 4.')

abbis_eye = Item("Abbi's Eye")
abbis_eye.set_description('Start each comabt with 5 strength and dexterity.')

empty_cage = Item('Empty Cage')
empty_cage.set_description('Remove 3 cards from your deck.')

boss_relic_pool = [coffee, arcane_manual, snecko_eye, abbis_eye, ships_sail, empty_cage]

#VOID relics
transient_soul = Item('Transient Soul')
transient_soul.set_description('Whenever you deal damage, gain that much block.')

infinite_maw = Item('Infinite Maw')
infinite_maw.set_description('Status cards in your hand at the end of your turn give you 10 strength.')

shield_module = Item('Shield Module')
shield_module.set_description('When you are attacked, gain 12 block each turn this combat.')

hud_module = Item('HUD Module')
hud_module.set_description('Draw an extra 10 cards each turn, but you start each combat with 10 Dazed.')

laser_module = Item('Laser Module')
laser_module.set_description('Deal 50 damage to the first enemy each turn.')

bomb_module = Item('Bomb Module')
bomb_module.set_description('Whenever you end your turn yourself, gain 20 strength.')

relic_shapes = [shield_module, hud_module, laser_module, bomb_module]

cultists_amulet = Item('Cultist\'s Amulet')
cultists_amulet.set_description('Gain 1 energy, 10 strength, and 10 dexterity.')

blueprints = Item('Blueprints')
blueprints.set_description('At the start of every 3 turns: Gain 999 block.')
b_count = 0

error = Item('Error')
error.set_description('At the start of your turn: If you have less than 50 strength, double your strength.')

eternal_feather = Item('Eternal Feather')
eternal_feather.set_description('Lose 75% of your hp. At the start of each of your turns, gain 0 strength. Permanently increase the amount gained by 10.')
ef_str = 0

effigy = Item("Machine God's Effigy")
effigy.set_description('Deal no damage with cards. At the start of each turn, deal 1 damage to all enemies, then double this number.')
ef_dmg = 1

watch = Item('Doomsday Clock')
watch.set_description('Lose 1 strength and dexterity each turn. When you reach -13 strength or -13 dexterity in a combat, shuffle 5 amazing cards into your deck permanently.')
win = Card('Tick Tock')
win.create([['Attack', 1313], ['Block', 1313]])
win.set_description('Deal 1313 damage and gain 1313 block.')
win.set_cost(0)


ruins = Cave('The Ruins')
ruins.set_description("The ruins of an ancient city lie around you. All that remains are the crumbling houses. Monsters roam the landscape around you, making traversing the ruins difficult.")
ruins.link_cave(ruins, 'north')
ruins.link_cave(ruins, 'east')
ruins.link_cave(ruins, 'south')
ruins.link_cave(ruins, 'west')

#Cultist enemy
ruins_cultist = Cave('An Encounter')
ruins_cultist.set_description("The ruins of an ancient city lie around you. As you traverse the landscape, you notice a humanoid figure wearing blue robes watching you.")
ruins_cultist.link_cave(ruins, 'north')
ruins_cultist.link_cave(ruins, 'east')
ruins_cultist.link_cave(ruins, 'south')
ruins_cultist.link_cave(ruins, 'west')
cultist = Enemy("Cultist", "A cultist wearing feathered blue robes.")
cultist.set_conversation("You do not belong here!")
cultist.set_health(40)
cultist.set_action(5,5)
cultist1 = Enemy("Cultist", "A cultist wearing feathered blue robes.")
cultist1.set_conversation("You do not belong here!")
cultist1.set_health(40)
cultist1.set_action(5,5)

#Serpent enemy
ruins_serpent = Cave('An Encounter')
ruins_serpent.set_description("The ruins of an ancient city lie around you. As you traverse the landscape, you notice a large snake folowing you.")
ruins_serpent.link_cave(ruins, 'north')
ruins_serpent.link_cave(ruins, 'east')
ruins_serpent.link_cave(ruins, 'south')
ruins_serpent.link_cave(ruins, 'west')
serpent = Enemy("Serpent", "A giant snake approaches, looking for a meal.")
serpent.set_conversation("Ssssssssssssss...")
serpent.set_health(50)
serpent.set_action(9,0)

#Insects enemy
ruins_swarm = Cave('An Encounter')
ruins_swarm.set_description("The ruins of an ancient city lie around you. As you traverse the landscape, you notice a swarm of insects beginning to surround you.")
ruins_swarm.link_cave(ruins, 'north')
ruins_swarm.link_cave(ruins, 'east')
ruins_swarm.link_cave(ruins, 'south')
ruins_swarm.link_cave(ruins, 'west')

bug1 = Enemy("Bug", "A bug. One of many.")
bug1.set_conversation("Why are you trying to talk to a bug it can't talk (snakes can).")
bug1.set_health(7)
bug1.set_action(4,1)

bug2 = Enemy("Bug", "A bug. One of many.")
bug2.set_conversation("Why are you trying to talk to a bug it can't talk (snakes can).")
bug2.set_health(7)
bug2.set_action(4,1)

bug3 = Enemy("Bug", "A bug. One of many.")
bug3.set_conversation("Why are you trying to talk to a bug it can't talk (snakes can).")
bug3.set_health(7)
bug3.set_action(4,1)

#Golem elite
ruins_golem = Cave('An Elite')
ruins_golem.set_description("The ruins of an ancient city lie around you. As you inspect one of the piles of rubble, you notice that it has eyes... and is moving towards you.")
ruins_golem.link_cave(ruins, 'north')
ruins_golem.link_cave(ruins, 'east')
ruins_golem.link_cave(ruins, 'south')
ruins_golem.link_cave(ruins, 'west')

golem = Enemy("Golem", "A huge pile of rocks, arranged in a humanoid form.")
golem.set_conversation("Death... to... intruders")
golem.set_health(75)
golem.set_actions([2,20],[16,0])
ruins_golem.set_character(golem)

#High Priest elite
ruins_priest = Cave('An Elite')
ruins_priest.set_description("The ruins of an ancient city lie around you. You notice that a priest wearing blue robes with a cultist following closely behind.")
ruins_priest.link_cave(ruins, 'north')
ruins_priest.link_cave(ruins, 'east')
ruins_priest.link_cave(ruins, 'south')
ruins_priest.link_cave(ruins, 'west')

priest = Enemy("High Priest", "A cultist that has been promoted to a higher rank.")
priest.set_conversation("My power is unmatched!")
priest.set_health(50)
priest.set_action(8,8)
ruins_priest.set_character(cultist)
ruins_priest.set_character(priest)

#Acid Slime elite
ruins_slime = Cave('An Elite')
ruins_slime.set_description("The ruins of an ancient city lie around you. As you move across the terrain, you notice a pool of acid beginnig to pursue you.")
ruins_slime.link_cave(ruins, 'north')
ruins_slime.link_cave(ruins, 'east')
ruins_slime.link_cave(ruins, 'south')
ruins_slime.link_cave(ruins, 'west')

slime = Enemy("Slime", "An acidic slime, dissolving everything nearby.")
slime.set_conversation("*Slime noises*")
slime.set_health(100)
slime.set_action(0,0)
ruins_slime.set_character(slime)

#BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES BOSSES
ghost = Enemy("Phantom", "A large apparition blocks your way up. As its eyes begin to glow with a sickly radience, you feel yourself getting weaker.")
ghost.set_conversation('Fool...')
ghost.set_health(100)
ghost.set_actionss([0,0], [0,0], [18, 6], [24,0])


scavenger1 = Enemy("Scavenger", "An agent of the Vulture, lord of the ruins. Protects their leader.")
scavenger1.set_conversation('Hand over your loot!')
scavenger1.set_health(45)
scavenger1.set_action(7,0)

scavenger2 = Enemy("Scavenger", "An agent of the Vulture, lord of the ruins. Protects their leader.")
scavenger2.set_conversation('Hand over your loot!')
scavenger2.set_health(45)
scavenger2.set_action(7,0)

vulture = Enemy("Vulture", "The Vulture, the ruler of the ruins. Leads a group of scavengers, looking for any resources avaliable... including you. Steals 10 of your gold every attack.")
vulture.set_conversation('Die!')
vulture.set_health(70)
vulture.set_actionss([0,0], [13,0], [0,15], [6,6])





#Chest room
ruins_chest = Cave('A Reward')
ruins_chest.set_description("A chest lies in this area, seemingly abandoned. You should claim the treasure inside fast, as scavengers are prevelant in the ruins.")
ruins_chest.link_cave(ruins, 'north')
ruins_chest.link_cave(ruins, 'east')
ruins_chest.link_cave(ruins, 'south')
ruins_chest.link_cave(ruins, 'west')

blight_chest = Cave('An Offer')
blight_chest.set_description("A chest lies in this area. This chest appears to exude a dark aura. You sense that a great reward lies inside, in exchange for a blight.")
blight_chest.link_cave(ruins, 'north')
blight_chest.link_cave(ruins, 'south')
blight_chest.link_cave(ruins, 'east')
blight_chest.link_cave(ruins, 'west')

ruins_mimic = Cave('A Reward')
ruins_mimic.set_description('A chest lies in this area. AS you open it to claim its reward, you are instead greeted by rows of teeth.')
ruins_mimic.link_cave(ruins, 'north')
ruins_mimic.link_cave(ruins, 'east')
ruins_mimic.link_cave(ruins, 'south')
ruins_mimic.link_cave(ruins, 'west')
mimic = Enemy('Mimic', 'Not a chest.')
mimic.set_conversation('You found a [Draw Strike] - Deal 8 damage to an enemy and draw a card.')
mimic.set_health(80)
mimic.set_actions([24,0],[0,0])

ruins_healer = Cave('A Healer')
ruins_healer.set_description("A healer is travelling through this area. For some gold, they may be able to heal your injuries. Type 'heal' to heal.")
ruins_healer.link_cave(ruins, 'north')
ruins_healer.link_cave(ruins, 'south')
ruins_healer.link_cave(ruins, 'east')
ruins_healer.link_cave(ruins, 'west')
harmicist = Character("Healer", "A healer. Carries a gun (You should really do that as well).")
harmicist.set_conversation('I am a licenced medical professional.')
ruins_healer.set_character(harmicist)

ruins_shop = Cave('Capitalism')
ruins_shop.set_description('A merchant passes through this area, with a display of cards and relics. You might also be able to dump your trash on them.')
ruins_shop.link_cave(ruins, 'north')
ruins_shop.link_cave(ruins, 'south')
ruins_shop.link_cave(ruins, 'east')
ruins_shop.link_cave(ruins, 'west')
merchant = Character("Merchant", "A merchant. Has literally everything. Is god.")
ruins_shop.set_character(merchant)

city = Cave('The City')
city.set_description("The great city extends in every direction around you. You may have left the monsters behind, but the crime rings of this place still pose a great threat.")
city.link_cave(city, 'north')
city.link_cave(city, 'east')
city.link_cave(city, 'south')
city.link_cave(city, 'west')

city_chest = Cave('A Reward')
city_chest.set_description('A chest lies in this area. Nobody seems to be around except you, but criminals are hiding everywhere in the city.')
city_chest.link_cave(city, 'north')
city_chest.link_cave(city, 'south')
city_chest.link_cave(city, 'east')
city_chest.link_cave(city, 'west')

#Thief enemy
city_thieves = Cave('An Encounter')
city_thieves.set_description('You encounter a group of thieves. As you prepare for combat, you notice one of them preparing a smoke bomb.')
city_thieves.link_cave(city, 'north')
city_thieves.link_cave(city, 'south')
city_thieves.link_cave(city, 'east')
city_thieves.link_cave(city, 'west')
thief = Enemy('Thief', 'A thief. Common in the city.')
thief.set_conversation('Hand over your money!')
thief.set_health(40)
thief.set_action(6,0)
looter = Enemy('Looter', 'A thief. Will flee on turn 2, stealing some of your gold.')
looter.set_conversation("Where's my smoke bomb...")
looter.set_health(40)
looter.set_actions([6,0],[0,0])

#Sentry enemy
city_sentry = Cave('An Encounter')
city_sentry.set_description("You're stopped by a sentry, built to protect the city from unwanted personnel. For some reason, they aren't doing anything about the city's crime issue.")
city_sentry.link_cave(city, 'north')
city_sentry.link_cave(city, 'south')
city_sentry.link_cave(city, 'east')
city_sentry.link_cave(city, 'west')
sentry = Enemy('Sentry', 'A bronze sentry designed to protect the city.')
sentry.set_conversation('DESTROY DESTROY DESTROY')
sentry.set_health(45)
sentry.set_actions([10,10],[0,0])

#Guard/Mystic enemy
city_guard = Cave('An Encounter')
city_guard.set_description("You notice a group of people. One of them is a royal guard, and the other is their accompanying doctor.")
city_guard.link_cave(city, 'north')
city_guard.link_cave(city, 'south')
city_guard.link_cave(city, 'east')
city_guard.link_cave(city, 'west')
guard = Enemy('Guard', 'A royal guard, employed by the government of the city.')
guard.set_conversation('Stand down!')
guard.set_health(60)
guard.set_action(16,4)
mystic = Enemy('Mystic', 'A healer assigned to guards for their protection.')
mystic.set_health(40)
mystic.set_actions([0,0],[0,0])

#Orb Guardian elite
city_orb = Cave('An Elite')
city_orb.set_description("A large machine blocks your way forwards. As you approach it, a whirring sound feels the area, and the orb in the centre begins to glow.")
city_orb.link_cave(city, 'north')
city_orb.link_cave(city, 'south')
city_orb.link_cave(city, 'east')
city_orb.link_cave(city, 'west')
orb = Enemy('Orb', 'A more advanced sentry. Fires lasers at you. ')
orb.set_conversation('Bzzzzzt')
orb.set_health(280)
orb.set_actionss([0,0],[0,0],[0,0],[63,0])

#Taskmaster elite
city_task = Cave('An Elite')
city_task.set_description('You encounter one of the city\'s taskmasters leading a group of underlings.')
city_task.link_cave(city, 'north')
city_task.link_cave(city, 'south')
city_task.link_cave(city, 'east')
city_task.link_cave(city, 'west')
b_slaver = Enemy('Blue Slaver', 'A guy in a blue hood.')
b_slaver.set_health(50)
b_slaver.set_action(7,0)
taskmaster = Enemy('Taskmaster', 'The leader of the group. Wields a large whip.')
taskmaster.set_health(50)
taskmaster.set_actions([9,0],[7,0])
r_slaver = Enemy('Red Slaver', 'A guy in a red hood.')
r_slaver.set_health(50)
r_slaver.set_action(6,2)

#Procession elite
city_line = Cave('An Elite')
city_line.set_description('You encounter a cultist, a priest, and one of the chosen of the Crow God. This is getting out of hand.')
city_line.link_cave(city, 'north')
city_line.link_cave(city, 'south')
city_line.link_cave(city, 'east')
city_line.link_cave(city, 'west')
chosen = Enemy('Chosen', 'A human wearing blue feathered robes with wings, and a crow mask.')
chosen.set_conversation('Suffer...')
chosen.set_health(60)
chosen.set_action(11,11)

city_shop = Cave('Capitalism')
city_shop.set_description('A merchant passes through this area, with a display of cards and relics. You might also be able to dump your trash on them.')
city_shop.link_cave(city, 'north')
city_shop.link_cave(city, 'south')
city_shop.link_cave(city, 'east')
city_shop.link_cave(city, 'west')
city_shop.set_character(merchant)

check = False
bag = ['qwert']
strike = Card('Strike')
strike.set_description('Deal 6 damage to an enemy.')
strike.create([['Attack', 6]])
strike.set_cost(1)
defend = Card('Defend')
defend.set_description('Gain 6 block.')
defend.create([['Block', 6]])
defend.set_cost(1)

#test only
instawin = Card('Instawin')
instawin.set_description('')
instawin.create([['Attack', 99999]])
instawin.set_cost(0)

perma_deck = [strike, strike, strike, strike, defend, defend, defend, draw_strike]
deck = []
hand = []
discard = []
current_cave = ruins


ruins_staircase = Cave('The Ascent')
ruins_staircase.set_description("The singular staircase located in the ruins. You can ascend this to enter the Great City.")
ruins_staircase.link_cave(ruins, 'north')
ruins_staircase.link_cave(ruins, 'east')
ruins_staircase.link_cave(ruins, 'south')
ruins_staircase.link_cave(ruins, 'west')
ruins_staircase.link_cave(city, 'up')
ruins_staircase_generated = False

city_staircase = Cave('The Descent')
city_staircase.set_description("The manhole containing the staircase back down to the ruins.")
city_staircase.link_cave(city, 'north')
city_staircase.link_cave(city, 'east')
city_staircase.link_cave(city, 'south')
city_staircase.link_cave(city, 'west')
city_staircase.link_cave(ruins_staircase, 'down')
city.link_cave(city_staircase, 'back')

city_dealer = Cave('An Offer')
city_dealer.set_description("A shady looking person walks up to you, with an offer.")
city_dealer.link_cave(city, 'north')
city_dealer.link_cave(city, 'south')
city_dealer.link_cave(city, 'east')
city_dealer.link_cave(city, 'west')
dealer = Character("Shady Guy", "Looks shady. Wants your rare cards.")
dealer.set_conversation('You got any rare cards to trade? I\'ll pay you 40 gold.')
city_dealer.set_character(dealer)

elevator = Cave('The Elevator')
elevator.set_description("The great elevator leads to the Void - a place so distant that the laws of the world no longer apply.")
elevator.link_cave(city, 'north')
elevator.link_cave(city, 'south')
elevator.link_cave(city, 'east')
elevator.link_cave(city, 'west')
elevator_generated = False

#BOSSES AGAIN
crime_boss = Enemy('Crime Boss', 'The true ruler of this city. Leads criminals with his vast money and power.')
crime_boss.set_conversation("You're in the wrong city.")
crime_boss.set_health(300)
crime_boss.set_actionss([35,35],[17,12],[49,0],[0,0])

automaton = Enemy('Automaton', 'A giant bronze machine. Surrounded by both offensive and defensive sentries.')
automaton.set_conversation("DESTROY DESTROY DESTROY")
automaton.set_health(150)
automaton.set_actionss([0,0],[16,0],[0,0],[99,0])
auto_check = True
a_sentry = Enemy('Attack Sentry', 'A sentry. Orbits the Automaton')
a_sentry.set_conversation("DESTROY DESTROY DESTROY")
a_sentry.set_health(50)
a_sentry.set_action(13,0)
b_sentry = Enemy('Defence Sentry', 'A sentry. Orbits the Automaton')
b_sentry.set_conversation("DESTROY DESTROY DESTROY")
b_sentry.set_health(50)
b_sentry.set_action(0,0)
a_sentry1 = Enemy('Attack Sentry', 'A sentry. Orbits the Automaton')
a_sentry1.set_conversation("DESTROY DESTROY DESTROY")
a_sentry1.set_health(50)
a_sentry1.set_action(13,0)
b_sentry1 = Enemy('Defence Sentry', 'A sentry. Orbits the Automaton')
b_sentry1.set_conversation("DESTROY DESTROY DESTROY")
b_sentry1.set_health(50)
b_sentry1.set_action(0,0)


void = Cave('The Void')
void.set_description("The beings which were too powerful to exist in the city were banished here. You should watch your step. It is recommended that you go back down.")
void.link_cave(void, 'north')
void.link_cave(void, 'south')
void.link_cave(void, 'east')
void.link_cave(void, 'west')


void_elevator = Cave('The Elevator')
void_elevator.set_description('It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down. It is recommended that you go back down.')
void_elevator.link_cave(void, 'north')
void_elevator.link_cave(void, 'south')
void_elevator.link_cave(void, 'east')
void_elevator.link_cave(void, 'west')
void.link_cave(void_elevator, 'back')

#Transient enemy
void_transient = Cave('The Transient')
void_transient.set_description('The Transient resides in the Void. Your attacks will instead grant you block.')
void_transient.link_cave(void, 'north')
void_transient.link_cave(void, 'south')
void_transient.link_cave(void, 'east')
void_transient.link_cave(void, 'west')
transient = Enemy('Transient', 'VEhFIFRSQU5TSUVOVA==')
transient.set_conversation("Hi! I'm the Transient. I'm from hit game Slay the Spire!")
transient.set_health(1)
transient.set_actionss([700,0],[800,0],[900,0],[1000,0])
void_transient.set_character(transient)
transient_beaten = False

#Maw enemy
void_maw = Cave('The Maw')
void_maw.set_description('The Maw resides in the Void. Being in its presence, you feel a sense of Dread.')
void_maw.link_cave(void, 'north')
void_maw.link_cave(void, 'south')
void_maw.link_cave(void, 'east')
void_maw.link_cave(void, 'west')
maw = Enemy('Maw', 'Comprised entirely of a giant mouth. It seems to stretch out infinitely.')
maw.set_conversation('RROOARRRGH')
maw.set_health(400)
maw.set_actions([0,0],[30,15])
void_maw.set_character(maw)
maw_beaten = False

#Shapes enemy
void_shapes = Cave('The Shapes')
void_shapes.set_description('The Shapes reside in the Void. A group of robots, led by Donu and Deca. Make sure to destroy the Exploder first.')
void_shapes.link_cave(void, 'north')
void_shapes.link_cave(void, 'south')
void_shapes.link_cave(void, 'east')
void_shapes.link_cave(void, 'west')
bulwark = Enemy('Bulwark', 'The Bulwark. Protects the rest of the group.')
bulwark.set_conversation('YORTSED YORTSED YORTSED')
bulwark.set_health(200)
bulwark.set_action(0,0)
repulse = Enemy('Repulsor', 'The Repulsor. Inhibits your abilities.')
repulse.set_conversation('YORTSED YORTSED YORTSED')
repulse.set_health(150)
repulse.set_action(0,0)
laserbot = Enemy('Laser', 'The Laser. Inhibits your ability to stay alive.')
laserbot.set_conversation('YORTSED YORTSED YORTSED')
laserbot.set_health(100)
laserbot.set_action(50,0)
exploder = Enemy('Exploder', 'The Exploder. The only reason why this battle is difficult. Kill it first.')
exploder.set_conversation('I explode in 2 turns, dealing massive damage!')
exploder.set_health(100)
exploder.set_actions([0,0], [300,0])
void_shapes.set_character(repulse)
void_shapes.set_character(laserbot)
void_shapes.set_character(exploder)
void_shapes.set_character(bulwark)
shapes_beaten = False

#Procession elite
void_line = Cave('The Procession')
void_line.set_description('A line of cultists. They seem to be lost.')
void_line.link_cave(void, 'north')
void_line.link_cave(void, 'south')
void_line.link_cave(void, 'east')
void_line.link_cave(void, 'west')
archbishop = Enemy('Archbishop', 'A trusted leader of the cult.')
archbishop.set_conversation('CAW CAW!!!')
archbishop.set_health(200)
archbishop.set_action(14,14)
crow = Enemy('Crow', 'A regular crow. Warped by the presence of the Crow God.')
crow.set_conversation('CAW!!!!!! CAW!!!!!! CAW!!!!!! CAW!!!!!!')
crow.set_health(275)
crow.set_action(17,17)
for cult in [cultist, priest, chosen, archbishop, crow]:
    void_line.set_character(cult)
procession_beaten = False

#Concept elite
void_concept = Cave('The Concept')
void_concept.set_description('The work of a higher being, as proof that the machine gods could exist.')
void_concept.link_cave(void, 'north')
void_concept.link_cave(void, 'south')
void_concept.link_cave(void, 'east')
void_concept.link_cave(void, 'west')
concept = Enemy('Concept', 'The prototype of the machine gods, built to prove that multiple complex beings could exist in one place.')
concept.set_conversation('HelpDESTROYHelp')
concept.set_health(400)
concept.set_action(0,0)
void_concept.set_character(orb)
void_concept.set_character(concept)
concept_beaten = False

#Glitch Elite
void_glitch = Cave('The 011001110110110001101001011101000110001101101000')
void_glitch.set_description('Something in the')
void_glitch.link_cave(void, 'north')
void_glitch.link_cave(void, 'south')
void_glitch.link_cave(void, 'east')
void_glitch.link_cave(void, 'west')
glitch = Enemy('Glitch', "Don't worry, you don't actually have to type in all that binary.")
glitch.set_conversation('glitch.set_conversation(glitch.set_conversation(glitch.set_conversation(glitch.set_conversation(glitch.set_conversation(...)))))')
glitch.set_health(404)
glitch.set_actionss([0,666],[0,666],[0,666],[0,666])
bug_temp = Enemy('Bug', "A computer bug.")
bug_temp.set_conversation('You cannot talk to this bug. How are you doing this?')
bug_temp.set_health(66)
bug_temp.set_action(0,0)
void_glitch.set_character(glitch)
glitch_beaten = False

#Awakened One
void_one = Cave('The Awakened One')
void_one.set_description('The Crow God, worshipped by all those guys you probably killed.')
void_one.link_cave(void, 'north')
void_one.link_cave(void, 'south')
void_one.link_cave(void, 'east')
void_one.link_cave(void, 'west')
one = Enemy('Awakened One', 'The Crow God')
one.set_conversation('Insert a bunch of CAWs here.')
one.set_health(900)
one.set_actionss([30,30],[55,55],[90,0],[0,0])
void_one.set_character(one)

#Donu and Deca
void_dd = Cave('The Machine Gods')
void_dd.set_description('The machine gods, once built to protect the city. As their power grew, they had to be exiled to the Void. Each attacks on alternating turns.')
void_dd.link_cave(void, 'north')
void_dd.link_cave(void, 'south')
void_dd.link_cave(void, 'east')
void_dd.link_cave(void, 'west')
deca = Enemy('Deca', 'A machine god.')
deca.set_conversation('PROTECT PROTECT PROTECT')
deca.set_health(500)
deca.set_action(0,0)
donu = Enemy('Donu', 'A machine god.')
donu.set_conversation('DESTROY DESTROY DESTROY')
donu.set_health(500)
donu.set_action(0,0)
void_dd.set_character(donu)
void_dd.set_character(deca)

#Doomsday Clock
void_clock = Cave('The Doomsday Clock')
void_clock.set_description('The Doomsday Clock, signalling the end of the world. While confined to the void, it does not tick.')
void_clock.link_cave(void, 'north')
void_clock.link_cave(void, 'south')
void_clock.link_cave(void, 'east')
void_clock.link_cave(void, 'west')
clock = Enemy('Doomsday Clock', 'Your life begins to falter.')
clock.set_conversation('Bro it\'s literally a clock, what did you want to hear? Tick Tock?')
clock.set_health(3000)
clock.set_actions([0,0],[0,0])
void_clock.set_character(clock)

void_boss_beaten = False




pit = Cave('The Pit')
pit.set_description('The Pit. Your final challenge lies ahead.')


pit_shop = Cave('Capitalism - The Final')
pit_shop.set_description('The Merchant.')
pit_shop.set_character(merchant)
pit.link_cave(pit_shop, 'forward')

pit_elite = Cave('An Elite')
pit_elite.set_description('Some of the most powerful beings in this game.')
pit_shop.link_cave(pit_elite, 'forward')



match random.randint(1,2):
    case 1:
        ruins_staircase.set_character(ghost)
    case 2:
        ruins_staircase.set_character(vulture)
        ruins_staircase.set_character(scavenger1)
        ruins_staircase.set_character(scavenger2)
        
match random.randint(1,2):
    case 1:
        elevator.set_character(crime_boss)
    case 2:
        elevator.set_character(a_sentry)
        elevator.set_character(a_sentry1)
        elevator.set_character(automaton)
        elevator.set_character(b_sentry)
        elevator.set_character(b_sentry1)
        

moves_ruins_staircase = {
    'north':0,
    'east':0
}

moves_elevator = {
    'north' : 0,
    'east' : 0
}

moves_since_pit = {
    'north':0,
    'south':0,
    'east':0,
    'west':0
}

draw_count = 5
energy_count = 3
energy = 0
hp = 80
block = 0
strength = 0
perma_str = 0
dexterity = 0
perma_dex = 0
poison = 0
powers = []
gold = 70

chest_limit_ruins = 5
enemy_limit_ruins = 10
heal_limit = 3
heal_check = True
ruins_hard = 0
ruins_hard_check = False

chest_limit_city = 5
enemy_limit_city = 10
city_hard = 0
city_hard_check = False





while dead==False:		
    print("\n")
    
    ruins.link_cave(ruins, 'north') #reset ruins
    ruins.link_cave(ruins, 'east')
    ruins.link_cave(ruins, 'south')
    ruins.link_cave(ruins, 'west')

    cultist.set_health(40)
    cultist1.set_health(40)
    serpent.set_health(50)
    bug1.set_health(7)
    bug2.set_health(7)
    bug3.set_health(7)
    golem.set_health(65)
    priest.set_health(50)
    slime.set_health(100)
    mimic.set_health(80)

    if ruins_hard > 4:
        golem.set_actions([7,40], [23,0])

    city.link_cave(city, 'north')#reset city
    city.link_cave(city, 'east')
    city.link_cave(city, 'south')
    city.link_cave(city, 'west')
    
    thief.set_health(40)
    looter.set_health(40)
    sentry.set_health(45)
    guard.set_health(60)
    mystic.set_health(40)
    orb.set_health(280)
    b_slaver.set_health(50)
    taskmaster.set_health(50)
    r_slaver.set_health(50)
    chosen.set_health(60)

    void.link_cave(void, 'north')
    void.link_cave(void, 'south')
    void.link_cave(void, 'east')
    void.link_cave(void, 'west')

    if void_boss_beaten == True:
        ruins.link_cave(pit, 'down')

    
    if current_cave == ruins:
        match random.randint(1,11): #determine event
            case 1 | 2 | 3: #encounter
                if enemy_limit_ruins>0:
                    enemy_limit_ruins -= 1
                    if enemy_limit_ruins == 0:
                        print('You have built a name for yourself in these ruins. None but the strongest will challenge you.')
                    match random.randint(1,4):
                        case 1 | 2: #cultist encounter
                            if ruins_cultist.get_character('f') == []:
                                ruins_cultist.set_character(cultist)
                                #cultist.health(15)
                            match random.randint(1,4):
                                
                                case 1:
                                    ruins.link_cave(ruins_cultist, 'north')
                                case 2:
                                    ruins.link_cave(ruins_cultist, 'south')
                                case 3:
                                    ruins.link_cave(ruins_cultist, 'east')
                                case 4:
                                    ruins.link_cave(ruins_cultist, 'west')
                            
                        case 3: #serpent
                            if ruins_serpent.get_character('f') == []:
                                ruins_serpent.set_character(serpent)
                                #serpent.health(20)
                            match random.randint(1,4):
                                
                                case 1:
                                    ruins.link_cave(ruins_serpent, 'north')
                                case 2:
                                    ruins.link_cave(ruins_serpent, 'south')
                                case 3:
                                    ruins.link_cave(ruins_serpent, 'east')
                                case 4:
                                    ruins.link_cave(ruins_serpent, 'west')
                        case 4: #swarm
                            if ruins_swarm.get_character('f') == []:
                                ruins_swarm.set_character(bug1)
                                ruins_swarm.set_character(bug2)
                                ruins_swarm.set_character(bug3)
                                #bug1.health(6)
                                #bug2.health(6)
                                #bug3.health(6)
                            match random.randint(1,4):
                                
                                case 1:
                                    ruins.link_cave(ruins_swarm, 'north')
                                case 2:
                                    ruins.link_cave(ruins_swarm, 'south')
                                case 3:
                                    ruins.link_cave(ruins_swarm, 'east')
                                case 4:
                                    ruins.link_cave(ruins_swarm, 'west')
                else:
                    ruins_hard += 1
                    if ruins_hard == 5 and ruins_hard_check == False:
                        ruins_hard_check == True
                        print('\nThe ruins shift. You sense that elites have become stronger.\n')
                    match random.randint(1,3):
                        case 1:
                            if ruins_golem.get_character('f') == []:
                                ruins_golem.set_character(golem)
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_golem, 'north')
                                case 2:
                                    ruins.link_cave(ruins_golem, 'south')
                                case 3:
                                    ruins.link_cave(ruins_golem, 'east')
                                case 4:
                                    ruins.link_cave(ruins_golem, 'west')
                        case 2:
                            if ruins_priest.get_character('f') == []:
                                ruins_priest.set_character(cultist)
                                ruins_priest.set_character(priest)
                                if ruins_hard > 4:
                                    ruins_priest.set_character(cultist1)
                                    print('hi')
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_priest, 'north')
                                case 2:
                                    ruins.link_cave(ruins_priest, 'south')
                                case 3:
                                    ruins.link_cave(ruins_priest, 'east')
                                case 4:
                                    ruins.link_cave(ruins_priest, 'west')
                        case 3:
                            if ruins_slime.get_character('f') == []:
                                ruins_slime.set_character(slime)
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_slime, 'north')
                                case 2:
                                    ruins.link_cave(ruins_slime, 'south')
                                case 3:
                                    ruins.link_cave(ruins_slime, 'east')
                                case 4:
                                    ruins.link_cave(ruins_slime, 'west')
            case 4:
                match random.randint(1,6):
                    case 1|2:
                        if chest_limit_ruins>0:
                            ruins_chest.set_item(random.choice(card_pool))
                            chest_limit_ruins -= 1
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_chest, 'north')
                                case 2:
                                    ruins.link_cave(ruins_chest, 'south')
                                case 3:
                                    ruins.link_cave(ruins_chest, 'east')
                                case 4:
                                    ruins.link_cave(ruins_chest, 'west')
                    case 3:
                        if chest_limit_ruins>0:
                            chest_limit_ruins -= 1
                            ruins_chest.set_item(random.choice(rare_card_pool))
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_chest, 'north')
                                case 2:
                                    ruins.link_cave(ruins_chest, 'south')
                                case 3:
                                    ruins.link_cave(ruins_chest, 'east')
                                case 4:
                                    ruins.link_cave(ruins_chest, 'west')
                    case 4:
                        if chest_limit_ruins>0:
                            chest_limit_ruins -= 1
                            ruins_chest.set_item(random.choice(relic_pool))
                            match random.randint(1,4):
                                case 1:
                                    ruins.link_cave(ruins_chest, 'north')
                                case 2:
                                    ruins.link_cave(ruins_chest, 'south')
                                case 3:
                                    ruins.link_cave(ruins_chest, 'east')
                                case 4:
                                    ruins.link_cave(ruins_chest, 'west')
                    case 5|6:
                        if ruins_mimic.get_character('a') == []:
                            ruins_mimic.set_character(mimic)
                        match random.randint(1,4):
                            case 1:
                                ruins.link_cave(ruins_mimic, 'north')
                            case 2:
                                ruins.link_cave(ruins_mimic, 'south')
                            case 3:
                                ruins.link_cave(ruins_mimic, 'east')
                            case 4:
                                ruins.link_cave(ruins_mimic, 'west')

            case 5:
                if ruins_staircase_generated == False and current_cave == ruins:
                    ruins.link_cave(ruins_staircase, 'forward')
                    match random.randint(1,4):
                        case 1:
                            ruins.link_cave(ruins_staircase, 'north')
                            moves_ruins_staircase['north'] -= 1
                            ruins_staircase_generated = True
                        case 2:
                            ruins.link_cave(ruins_staircase, 'south')
                            moves_ruins_staircase['north'] += 1
                            ruins_staircase_generated = True
                        case 3:
                            ruins.link_cave(ruins_staircase, 'east')
                            moves_ruins_staircase['east'] -= 1
                            ruins_staircase_generated = True
                        case 4:
                            ruins.link_cave(ruins_staircase, 'west')
                            moves_ruins_staircase['east'] += 1
                            ruins_staircase_generated = True
            case 6:
                ruins_hard += 1
                if ruins_hard == 5 and ruins_hard_check == False:
                    ruins_hard_check == True
                    print('\nThe ruins shift. You sense that elites have become stronger.\n')
                match random.randint(1,3):
                    case 1:
                        if ruins_golem.get_character('f') == []:
                            ruins_golem.set_character(golem)
                        match random.randint(1,4):
                            case 1:
                                ruins.link_cave(ruins_golem, 'north')
                            case 2:
                                ruins.link_cave(ruins_golem, 'south')
                            case 3:
                                ruins.link_cave(ruins_golem, 'east')
                            case 4:
                                ruins.link_cave(ruins_golem, 'west')
                    case 2:
                        if ruins_priest.get_character('f') == []:
                            ruins_priest.set_character(cultist)
                            ruins_priest.set_character(priest)
                        if ruins_hard > 4:
                            ruins_priest.set_character(cultist1)
                        match random.randint(1,4):
                            case 1:
                                ruins.link_cave(ruins_priest, 'north')
                            case 2:
                                ruins.link_cave(ruins_priest, 'south')
                            case 3:
                                ruins.link_cave(ruins_priest, 'east')
                            case 4:
                                ruins.link_cave(ruins_priest, 'west')
                    case 3:
                        if ruins_slime.get_character('f') == []:
                            ruins_slime.set_character(slime)
                        match random.randint(1,4):
                            case 1:
                                ruins.link_cave(ruins_slime, 'north')
                            case 2:
                                ruins.link_cave(ruins_slime, 'south')
                            case 3:
                                ruins.link_cave(ruins_slime, 'east')
                            case 4:
                                ruins.link_cave(ruins_slime, 'west')
                                
            case 7:
                blight_chest.set_item(random.choice(blight_pool))
                match random.randint(1,4):
                    case 1:
                        ruins.link_cave(blight_chest, 'north')
                    case 2:
                        ruins.link_cave(blight_chest, 'south')
                    case 3:
                        ruins.link_cave(blight_chest, 'east')
                    case 4:
                        ruins.link_cave(blight_chest, 'west')
            case 8:
                if heal_limit>0:
                    heal_check = True
                    match random.randint(1,4):
                        case 1:
                            ruins.link_cave(ruins_healer, 'north')
                        case 2:
                            ruins.link_cave(ruins_healer, 'south')
                        case 3:
                            ruins.link_cave(ruins_healer, 'east')
                        case 4:
                            ruins.link_cave(ruins_healer, 'west')
            case 9:
                match random.randint(1,4):
                    case 1:
                        ruins.link_cave(ruins_shop, 'north')
                    case 2:
                        ruins.link_cave(ruins_shop, 'south')
                    case 3:
                        ruins.link_cave(ruins_shop, 'east')
                    case 4:
                        ruins.link_cave(ruins_shop, 'west')
    elif current_cave == city:
        match random.randint(1,12):
            case 1|2|3|4:
                if enemy_limit_city>0:
                    enemy_limit_city -= 1
                    match random.randint(1,3):
                        case 1:
                            if city_thieves.get_character('a') == []:
                                city_thieves.set_character(thief)
                                city_thieves.set_character(looter)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_thieves, 'north')
                                case 2:
                                    city.link_cave(city_thieves, 'south')
                                case 3:
                                    city.link_cave(city_thieves, 'east')
                                case 4:
                                    city.link_cave(city_thieves, 'west')
                        case 2:
                            if city_sentry.get_character('a') == []:
                                city_sentry.set_character(sentry)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_sentry, 'north')
                                case 2:
                                    city.link_cave(city_sentry, 'south')
                                case 3:
                                    city.link_cave(city_sentry, 'east')
                                case 4:
                                    city.link_cave(city_sentry, 'west')
                        case 3:
                            if city_guard.get_character('a') == []:
                                city_guard.set_character(guard)
                                city_guard.set_character(mystic)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_guard, 'north')
                                case 2:
                                    city.link_cave(city_guard, 'south')
                                case 3:
                                    city.link_cave(city_guard, 'east')
                                case 4:
                                    city.link_cave(city_guard, 'west')
                else:
                    city_hard += 1
                    if city_hard == 5 and city_hard_check == False:
                        city_hard_check == True
                        print('\nThe city shifts. You sense that elites have become stronger.\n')
                    match random.randint(1,3):
                        case 1:
                            if city_orb.get_character('a') == []:
                                city_orb.set_character(orb)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_orb, 'north')
                                case 2:
                                    city.link_cave(city_orb, 'south')
                                case 3:
                                    city.link_cave(city_orb, 'east')
                                case 4:
                                    city.link_cave(city_orb, 'west')
                        case 2:
                            if city_task.get_character('a') == []:
                                city_task.set_character(b_slaver)
                                city_task.set_character(taskmaster)
                                city_task.set_character(r_slaver)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_task, 'north')
                                case 2:
                                    city.link_cave(city_task, 'south')
                                case 3:
                                    city.link_cave(city_task, 'east')
                                case 4:
                                    city.link_cave(city_task, 'west')
                        case 3:
                            if city_task.get_character('a') == []:
                                city_line.set_character(cultist)
                                city_line.set_character(priest)
                                city_line.set_character(chosen)
                            if city_hard > 4:
                                city_line.set_character(cultist1)
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_task, 'north')
                                case 2:
                                    city.link_cave(city_task, 'south')
                                case 3:
                                    city.link_cave(city_task, 'east')
                                case 4:
                                    city.link_cave(city_task, 'west')
            case 4:
                if chest_limit_city>0:
                    match random.randint(1,6):
                        case 1|2|5:
                            city_chest.set_item(random.choice(card_pool))
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_chest, 'north')
                                case 2:
                                    city.link_cave(city_chest, 'south')
                                case 3:
                                    city.link_cave(city_chest, 'east')
                                case 4:
                                    city.link_cave(city_chest, 'west')
                        case 3|6:
                            city_chest.set_item(random.choice(rare_card_pool))
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_chest, 'north')
                                case 2:
                                    city.link_cave(city_chest, 'south')
                                case 3:
                                    city.link_cave(city_chest, 'east')
                                case 4:
                                    city.link_cave(city_chest, 'west')
                        case 4:
                            city_chest.set_item(random.choice(relic_pool))
                            match random.randint(1,4):
                                case 1:
                                    city.link_cave(city_chest, 'north')
                                case 2:
                                    city.link_cave(city_chest, 'south')
                                case 3:
                                    city.link_cave(city_chest, 'east')
                                case 4:
                                    city.link_cave(city_chest, 'west')
            case 5:
                city_hard += 1
                if city_hard == 5 and city_hard_check == False:
                        city_hard_check == True
                        print('\nThe city shifts. You sense that elites have become stronger.\n')
                match random.randint(1,3):
                    case 1:
                        if city_orb.get_character('a') == []:
                            city_orb.set_character(orb)
                        match random.randint(1,4):
                            case 1:
                                city.link_cave(city_orb, 'north')
                            case 2:
                                city.link_cave(city_orb, 'south')
                            case 3:
                                city.link_cave(city_orb, 'east')
                            case 4:
                                city.link_cave(city_orb, 'west')
                    case 2:
                        if city_task.get_character('a') == []:
                            city_task.set_character(b_slaver)
                            city_task.set_character(taskmaster)
                            city_task.set_character(r_slaver)
                        match random.randint(1,4):
                            case 1:
                                city.link_cave(city_task, 'north')
                            case 2:
                                city.link_cave(city_task, 'south')
                            case 3:
                                city.link_cave(city_task, 'east')
                            case 4:
                                city.link_cave(city_task, 'west')
                    case 3:
                        if city_task.get_character('a') == []:
                            city_line.set_character(cultist)
                            city_line.set_character(priest)
                            city_line.set_character(chosen)
                        if city_hard > 4:
                            city_line.set_character(cultist1)
                        match random.randint(1,4):
                            case 1:
                                city.link_cave(city_task, 'north')
                            case 2:
                                city.link_cave(city_task, 'south')
                            case 3:
                                city.link_cave(city_task, 'east')
                            case 4:
                                city.link_cave(city_task, 'west')
            case 6:
                if elevator_generated == False and current_cave == city:
                    city.link_cave(elevator, 'forward')
                    match random.randint(1,4):
                        case 1:
                            city.link_cave(elevator, 'north')
                            moves_elevator['north'] -= 1
                            elevator_generated = True
                        case 2:
                            city.link_cave(elevator, 'south')
                            moves_elevator['north'] += 1
                            elevator_generated = True
                        case 3:
                            city.link_cave(elevator, 'east')
                            moves_elevator['east'] -= 1
                            elevator_generated = True
                        case 4:
                            city.link_cave(elevator, 'west')
                            moves_elevator['east'] += 1
                            elevator_generated = True
            case 7:
                match random.randint(1,4):
                    case 1:
                        city.link_cave(city_dealer, 'north')
                    case 2:
                        city.link_cave(city_dealer, 'south')
                    case 3:
                        city.link_cave(city_dealer, 'east')
                    case 4:
                        city.link_cave(city_dealer, 'west')
    elif current_cave == void:
        match random.randint(1,3):
            case 1:
                match random.randint(1,3):
                    case 1:
                        if transient_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_transient, 'north')
                                case 2:
                                    void.link_cave(void_transient, 'south')
                                case 3:
                                    void.link_cave(void_transient, 'east')
                                case 4:
                                    void.link_cave(void_transient, 'west')
                    case 2:
                        if maw_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_maw, 'north')
                                case 2:
                                    void.link_cave(void_maw, 'south')
                                case 3:
                                    void.link_cave(void_maw, 'east')
                                case 4:
                                    void.link_cave(void_maw, 'west')
                    case 3:
                        if shapes_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_shapes, 'north')
                                case 2:
                                    void.link_cave(void_shapes, 'south')
                                case 3:
                                    void.link_cave(void_shapes, 'east')
                                case 4:
                                    void.link_cave(void_shapes, 'west')
            case 2:
                match random.randint(1,3):
                    case 1:
                        if procession_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_line, 'north')
                                case 2:
                                    void.link_cave(void_line, 'south')
                                case 3:
                                    void.link_cave(void_line, 'east')
                                case 4:
                                    void.link_cave(void_line, 'west')
                    case 2:
                        if concept_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_concept, 'north')
                                case 2:
                                    void.link_cave(void_concept, 'south')
                                case 3:
                                    void.link_cave(void_concept, 'east')
                                case 4:
                                    void.link_cave(void_concept, 'west')
                    case 3:
                        if glitch_beaten == False:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_glitch, 'north')
                                case 2:
                                    void.link_cave(void_glitch, 'south')
                                case 3:
                                    void.link_cave(void_glitch, 'east')
                                case 4:
                                    void.link_cave(void_glitch, 'west')
            case 3:
                if void_boss_beaten == False:
                    match random.randint(1,3):
                        case 1:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_line, 'north')
                                case 2:
                                    void.link_cave(void_line, 'south')
                                case 3:
                                    void.link_cave(void_line, 'east')
                                case 4:
                                    void.link_cave(void_line, 'west')
                        case 2:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_concept, 'north')
                                case 2:
                                    void.link_cave(void_concept, 'south')
                                case 3:
                                    void.link_cave(void_concept, 'east')
                                case 4:
                                    void.link_cave(void_concept, 'west')
                        case 3:
                            match random.randint(1,4):
                                case 1:
                                    void.link_cave(void_glitch, 'north')
                                case 2:
                                    void.link_cave(void_glitch, 'south')
                                case 3:
                                    void.link_cave(void_glitch, 'east')
                                case 4:
                                    void.link_cave(void_glitch, 'west')   

    if current_cave == ruins:
        if moves_ruins_staircase['north'] == 0 and moves_ruins_staircase['east'] == 1:
            ruins.link_cave(ruins_staircase, 'west')
        elif moves_ruins_staircase['north'] == 0 and moves_ruins_staircase['east'] == -1:
            ruins.link_cave(ruins_staircase, 'east')
        elif moves_ruins_staircase['north'] == 1 and moves_ruins_staircase['east'] == 0:
            ruins.link_cave(ruins_staircase, 'south')
        elif moves_ruins_staircase['north'] == -1 and moves_ruins_staircase['east'] == 0:
            ruins.link_cave(ruins_staircase, 'north')
    elif current_cave == city:
        if moves_ruins_staircase['north'] == 0 and moves_ruins_staircase['east'] == 1:
            city.link_cave(city_staircase, 'west')
        elif moves_ruins_staircase['north'] == 0 and moves_ruins_staircase['east'] == -1:
            city.link_cave(city_staircase, 'east')
        elif moves_ruins_staircase['north'] == 1 and moves_ruins_staircase['east'] == 0:
            city.link_cave(city_staircase, 'south')
        elif moves_ruins_staircase['north'] == -1 and moves_ruins_staircase['east'] == 0:
            city.link_cave(city_staircase, 'north')
            
        if moves_elevator['north'] == 0 and moves_elevator['east'] == 1:
            city.link_cave(elevator, 'west')
        elif moves_elevator['north'] == 0 and moves_elevator['east'] == -1:
            city.link_cave(elevator, 'east')
        elif moves_elevator['north'] == 1 and moves_elevator['east'] == 0:
            city.link_cave(elevator, 'south')
        elif moves_elevator['north'] == -1 and moves_elevator['east'] == 0:
            city.link_cave(elevator, 'north')
    elif current_cave == void:
        if moves_elevator['north'] == 0 and moves_elevator['east'] == 1:
            void.link_cave(void_elevator, 'west')
        elif moves_elevator['north'] == 0 and moves_elevator['east'] == -1:
            void.link_cave(void_elevator, 'east')
        elif moves_elevator['north'] == 1 and moves_elevator['east'] == 0:
            void.link_cave(void_elevator, 'south')
        elif moves_elevator['north'] == -1 and moves_elevator['east'] == 0:
            void.link_cave(void_elevator, 'north')


    current_cave.get_details()
    inhabitant = current_cave.get_character('notanerror') #will trigger the 'except' clause
    names = []
    for i in inhabitant:
        names.append(i.name.lower())
    for i in inhabitant:
        i.describe()
    item = current_cave.get_item()
    if item is not None:
        item.describe()
    command = input("> ")    
    if command in ["north", "south", "east", "west", "up", "down", "forward", "back"]:
        check = False
        for i in inhabitant:
            if isinstance(i, Enemy):
                check = True
        if check == False:
            current_cave = current_cave.move(command)
            if current_cave == ruins_staircase:
                moves_ruins_staircase = {
                    'north':0,
                    'east':0
                }
            if current_cave == ruins:
                if ruins_staircase_generated == True:
                    if command == 'north':
                        moves_ruins_staircase['north'] += 1
                    elif command == 'south':
                        moves_ruins_staircase['north'] -= 1
                    elif command == 'east':
                        moves_ruins_staircase['east'] += 1
                    elif command == 'west':
                        moves_ruins_staircase['east'] -= 1
                        
            if current_cave == city:
                if ruins_staircase_generated == True:
                    if command == 'north':
                        moves_ruins_staircase['north'] += 1
                    elif command == 'south':
                        moves_ruins_staircase['north'] -= 1
                    elif command == 'east':
                        moves_ruins_staircase['east'] += 1
                    elif command == 'west':
                        moves_ruins_staircase['east'] -= 1
                        
                if elevator_generated == True:
                    if command == 'north':
                        moves_elevator['north'] += 1
                    elif command == 'south':
                        moves_elevator['north'] -= 1
                    elif command == 'east':
                        moves_elevator['east'] += 1
                    elif command == 'west':
                        moves_elevator['east'] -= 1
                        
            if current_cave in [ruins_shop, city_shop, pit_shop]:
                purchase = 'placeholder'
                print('You arrived at a shop.')
                print(f'You have {gold} gold')
                wares = random.sample(card_pool, 2)
                waress = random.choice(rare_card_pool)
                waresss = random.sample(relic_pool, 2)
                waressss = []
                for i in wares:
                    i.money = 10
                    waressss.append(i)
                    i.describe()
                waress.money = 40
                waressss.append(waress)
                waress.describe()
                for i in waresss:
                    i.money = 70
                    waressss.append(i)
                    i.describe()
                waressss.append('Remove')
                while purchase.lower() != 'exit':
                    count = 0
                    for i in waressss:
                        if i != 'Remove':
                            print(f"[{count}] {i.name} - {i.money} gold")
                        else:
                            print(f"[{count}] Remove a card - 40 gold")
                        count += 1
                    purchase = input("Enter number of item, or 'exit' ")
                    if purchase.lower() != 'exit':
                        try:
                            p = int(purchase)
                        except:
                            print('Enter a number, or exit')
                        try:
                            if waressss[p].money<=gold:
                                if isinstance(waressss[p], Card):
                                    perma_deck.append(waressss[p])
                                    print("You put the " + waressss[p].get_name() + " in your deck")
                                elif isinstance(waressss[p], Item):
                                    bag.append(waressss[p])
                                    if item == combat_manual:
                                        draw_count += 1
                                    elif item == small_heart:
                                        hp += 20
                                    elif item == whetstone:
                                        perma_str += 2
                                    elif item == wet_stone:
                                        perma_dex += 2
                                gold -= waressss[p].money
                                    
                                waressss.pop(p)
                                print(f'You have {gold} gold\n')
                            else:
                                print("You don't have enough gold")
                                print(f'You have {gold} gold\n')
                        except:
                            if waressss[p] == 'Remove': #Card remove code
                                if gold>=40:
                                    count = 0
                                    for i in perma_deck:
                                        print(f"[{count}] - {i.name}")
                                        count += 1
                                    rere = False
                                    re = input('Which card do you want to remove?')
                                    while rere == False:
                                        try:
                                            print(f'You removed the {perma_deck[int(re)].name} from your deck')
                                            perma_deck.pop(int(re))
                                            rere = True
                                            waressss.pop(p)
                                            gold-=40
                                            print(f'You have {gold} gold')
                                        except:
                                            print('Enter a valid number.')
                                            rere = True
                                else:
                                    print("You don't have enough gold.")
                            else:
                                print('Enter a valid number, or exit')
            elif current_cave in [city_dealer]:
                current_cave.get_details()
                print('Trade a rare card for 40 gold?')
                choice = input('Y/N ')
                rares = []
                while choice == 'Y':
                    count = 0
                    for rare in perma_deck:
                        if rare in rare_card_pool:
                            print(f'[{count}] - {rare.name}')
                            rares.append(rare)
                            count += 1
                    if count == 0:
                        print('You have no rare cards.')
                        break
                    else:
                        choice = input('Which card do you want to trade? ')
                        try:
                            perma_deck.remove(rares[int(choice)])
                            gold += 40
                            print(f'You removed the {rares[int(choice)].name} and have {gold} gold')
                        except:
                            print('Input a valid number.')
                    choice = input('Trade another? (Y/N) ')
        else:
            print("There is an enemy here! You can't run from it (Your friends would make fun of you).")
    elif command == "talk":
        # Talk to the inhabitant - check whether there is one!
        talkto = input('Talk to who? ').lower()
        if inhabitant != []:
            check = False
            for i in inhabitant:
                if i.name.lower() == talkto:
                    i.talk()
                    check = True
            if check == False:
                print(f'{talkto.capitalize()} is not in this area.')
        else:
            print('There is nobody here.')

#FIGHTING CODE STARTS HERE
    elif command == "fight":
        win_s = False
        void_count = 0
        enemies = []
        turn = 0
        for i in bag:
            if i == poisoned:
                poison += 3
        for i in inhabitant:
            if isinstance(i, Enemy):
                enemies.append(i)
        for i in enemies:
            i.poison = 0
        strength = 0
        strength += perma_str
        if eternal_feather in bag:
            strength += ef_str
            ef_str += 10
        dexterity = 0
        dexterity += perma_dex
        powers = []
        check = False
        action_to_do = 0
        if inhabitant != []:
            # Fight with the inhabitant, if there is one
            for i in inhabitant:
                if isinstance(i, Enemy):
                    check = True

            deck = []
            for i in perma_deck:
                deck.append(i)
            hand = []
            discard = []
            
            while check == True:
                turn += 1
                if effigy in bag:
                    for en in enemies:
                        if en != transient:
                            try:
                                en.take_damage(ef_dmg)
                                if en == glitch:
                                    inhabitant.append(copy.copy(bug_temp))
                                    enemies.append(copy.copy(bug_temp))
                                    names.append('bug')
                                    print('A bug!')
                                if en.health <= 0:
                                    inhabitant.remove(enemies[0])
                                    names.remove(enemies[0].name.lower())
                                    enemies.remove(enemies[0])
                            except:
                                pass
                    ef_dmg = ef_dmg*2
                if watch in bag:
                    strength -= 1
                    dexterity -= 1
                    if strength <= -13 or dexterity <= -13:
                        if win_s == False:
                            win_s == True
                            print('The Clock strikes.')
                            for wi in range(5):
                                perma_deck.append(win)
                if strength < 50 and error in bag:
                    strength = strength*2
                for i in bag:
                    if i == power_ring:
                        if enemies[0] != transient:
                            try:
                                enemies[0].take_damage(4)
                                if enemies[0] == glitch:
                                    inhabitant.append(copy.copy(bug_temp))
                                    enemies.append(copy.copy(bug_temp))
                                    names.append('bug')
                                    print('A bug!')
                                if enemies[0].health <= 0:
                                    inhabitant.remove(enemies[0])
                                    names.remove(enemies[0].name.lower())
                                    enemies.remove(enemies[0])
                            except:
                                pass
                    elif i == laser_module:
                        if enemies[0] != transient:
                            try:
                                enemies[0].take_damage(50)
                                if enemies[0] == glitch:
                                    inhabitant.append(copy.copy(bug_temp))
                                    enemies.append(copy.copy(bug_temp))
                                    names.append('bug')
                                    print('A bug!')
                                if enemies[0].health <= 0:
                                    inhabitant.remove(enemies[0])
                                    names.remove(enemies[0].name.lower())
                                    enemies.remove(enemies[0])
                            except:
                                pass
                            
                
                if enemies == []:
                    break
                energy = energy_count
                energy -= void_count
                void_count = 0
                print(f'\nYou have {energy} energy')
                for i in powers:
                    if i == demon_form:
                        strength += 3
                        print('Demon Form grant you 3 strength')
                if strength:
                    print(f'You have {strength} strength')
                if dexterity:
                    print(f'You have {dexterity} dexterity')
                if poison:
                    print(f'You have {poison} poison')
                print('Your block resets')
                for j in inhabitant:
                    print(f'{j.name} is at {j.health} hp and {j.block} block')
                    if j.poison:
                        print(f'{j.name} has {j.poison} poison')
                    if j.str:
                        print(f'{j.name} has {j.str} strength')
                block = 0
                #power code
                for i in bag:
                    if i == anchor:
                        if turn == 1:
                            print('Anchor gives you 10 block')
                            block += 10
                    elif i == horn_cleat:
                        if turn == 2:
                            print('Horn Cleat gives you 14 block')
                            block += 14
                    elif i == captains_wheel:
                        if turn == 3:
                            print("Captain's Wheel gives you 18 block")
                            block += 18
                    elif i == ships_sail:
                        if turn > 3:
                            print("Ship's Sail gives you 22 block")
                            block += 22
                    elif i == blueprints:
                        if b_count != 2:
                            b_count += 1
                        else:
                            block += 999
                            b_count = 0
                    
                for card in perma_deck:
                        if snecko_eye in bag:
                            card.set_cost(random.randint(-1,2))


                for i in powers:
                    if i == armour_up:
                        block += 4
                        print('Armour Up gives you 4 block')
                if block:
                    print(f'You have {block} block')
                if energy>0:
                    try:
                        discard += hand
                        hand = random.sample(deck, draw_count)
                    except:
                        deck += discard
                        discard = hand
                        try:
                            hand = random.sample(deck, draw_count)
                        except:
                            hand = random.sample(deck, len(deck))
                        
                    for card in hand:
                        deck.remove(card)
                else:
                    discard += hand
                    hand = []
                    
                print()
                for i in inhabitant: #display enemy intent
                    if i not in [donu,deca]:
                        if i.complex == False:
                            if i.action['Attack'] == 0 and i.action['Block'] == 0:
                                print(f'{i.name} will do something...')
                            else:
                                print(f"{i.name} will do {i.action['Attack'] + i.str} damage to you and gain {i.action['Block']} block after your turn.")
                        else:
                            if i.actions[action_to_do]['Attack'] == 0 and i.actions[action_to_do]['Block'] == 0:
                                print(f'{i.name} will do something...')
                            else:
                                print(f"{i.name} will do {i.actions[action_to_do]['Attack'] + i.str} damage to you and gain {i.actions[action_to_do]['Block']} block after your turn.")
                    else:
                        if turn%2 == 0 and i == donu:
                            print(f'Donu will do {44 + donu.str} damage to you twice.')
                        elif turn%2 == 1 and i == deca:
                            print(f'Deca will do {60 + deca.str} damage to you.')
                while energy>0 and len(hand)>0:
                    count=0
                    for card in hand:
                        print(f'[{count}] {card.name} ({card.cost}) - {card.description}')
                        count+=1
                    pc = input("\nWhich card do you want to play? (Enter number of card without square brackets, or 'end turn')")
                    if pc.lower() == 'end turn':
                        if bomb_module in bag:
                            strength += 20
                        break
                    try:
                        playedcard=int(pc)
                    except:
                        playedcard=99999999999999999999999999999999999999999
                    finally:
                        if playedcard == 123456789:
                            print(a)
                        while playedcard > len(hand)-1:
                            print("You don't have that many cards")
                            pc = input("\nWhich card do you want to play? (Enter number of card without square brackets, or 'end turn')")
                            if pc.lower() == 'end turn':
                                if bomb_module in bag:
                                    strength += 20
                                break
                            try:
                                playedcard=int(pc)
                            except:
                                playedcard=99999999999999999999999999999999999999999
                    if hand[playedcard].cost<=energy:
                        if hand[playedcard].action['damage'] != []:
                            if len(enemies)>1:
                                opponent=input('Who do you want to fight? ').lower()
                            else:
                                try:
                                    opponent = names[0]
                                except:
                                    pass
                            print()
                            if opponent in names:
                                if shuriken_count == True:
                                    for i in bag:
                                        if i == shuriken:
                                            strength += 1
                                            print('Skuriken gives 1 strength')
                                    print(f'You have {strength} strength')
                                shuriken_count = not shuriken_count
                                
                                for i in inhabitant:
                                        if i.name.lower() == opponent:
                                            if hand[playedcard] == judgement:
                                                if i.health <= 30:
                                                    i.set_health(0)
                                            if hand[playedcard] == immolate:
                                                for j in range(2):
                                                    deck.append(burn)
                                                random.shuffle(deck)
                                            if i == glitch:
                                                for thing in hand[playedcard].action['damage']:
                                                    b = copy.copy(bug_temp)
                                                    inhabitant.append(b)
                                                    enemies.append(b)
                                                    names.append('bug')
                                                    print('A bug!')
                                            if i != transient:
                                                if effigy not in bag:
                                                    i.fight(hand[playedcard].action, strength) #damage
                                                i.poison += hand[playedcard].poison
                                            else:
                                                for thing in hand[playedcard].action['damage']:
                                                    block += thing
                                                    block += strength
                                            if transient_soul in bag:
                                                for thing in hand[playedcard].action['damage']:
                                                    block += thing
                                                    block += strength
                                                    print(f'You have {block} block')
                                            if i.health <= 0:
                                                inhabitant.remove(i)
                                                enemies.remove(i)
                                                names.remove(i.name.lower())
                                            for j in inhabitant:
                                                print(f'{j.name} is at {j.health} hp and {j.block} block')
                                                if j.poison != 0:
                                                    print(f'{j.name} has {j.poison} poison')
                                            for i in hand[playedcard].action['draw']:
                                                for j in range(i):
                                                    try:
                                                        hand.append(deck.pop(0))
                                                    except:
                                                        deck = discard
                                                        discard = []
                                            for i in hand[playedcard].action['block']:
                                                if i+dexterity>0:
                                                    block += i
                                                    block += dexterity
                                            energy -= hand[playedcard].cost
                                            hp -= hand[playedcard].loss
                                            if hand[playedcard].exhaust == False:
                                                discard.append(hand.pop(playedcard))
                                            else:
                                                hand.pop(playedcard)
                                            check = False
                                            for i in inhabitant:
                                                if isinstance(i, Enemy):
                                                    check = True
                                            if check == False:
                                                energy = 0

                                            
                                            break
                            else:
                                print('There is no ' + opponent + ' here')
                        else:
                            if kunai_count == True:
                                for i in bag:
                                    if i == kunai:
                                        dexterity += 1
                                        print('Kunai gives 1 dexterity')
                                print(f'You have {dexterity} dexterity')
                            kunai_count = not kunai_count
                                
                            for i in hand[playedcard].action['draw']:
                                if deck == []:
                                    for f in discard:
                                        deck.append(f)
                                    discard = []
                                for j in range(i):
                                    try:
                                        hand.append(deck.pop(0))
                                    except:
                                        deck = discard.copy()
                                        discard = []
                                
    

                            for i in hand[playedcard].action['block']:
                                if i+dexterity>0:
                                    block += i
                                    block += dexterity

                            energy -= hand[playedcard].cost
                            hp -= hand[playedcard].loss
                            #random cases begin
                            if hand[playedcard] == inflame:
                                strength += 2
                            elif hand[playedcard] == glitched:
                                strength += 1
                                strength = strength*2

                            
                            #random cases end

                            #power handling code
                            if hand[playedcard] == armour_up:
                                powers.append(armour_up)
                            elif hand[playedcard] == demon_form:
                                powers.append(demon_form)
                            #power handling code end
                            if hand[playedcard].exhaust == False:
                                discard.append(hand.pop(playedcard))
                            else:
                                hand.pop(playedcard)
                            
                            
                        print(f'\nYou have {energy} energy remaining')
                        print(f'You have {hp} hp and {block} block')
                        
                    else:
                        print("You don't have enough energy for that card")

                for i in hand:
                    if i == burn:
                        block -= 2
                        print('Burn does 2 damage to you')
                        if block<0:
                                hp += block
                                block = 0
                        print(f'You have {hp} hp and {block} block')
                    elif i == dread:
                        maw.str += 10
                        print('\nThe Maw \npreys on you\n')
                    elif i == erased:
                        deck.append(erased)
                        print('Your mind blanks')
                        random.shuffle(deck)

                    elif i == voided:
                        void_count += 1
                        print('The Void consumes you')
                    elif i == darkness:
                        hp -= 5
                        strength += 5
                        print('Time moves forwards')
                    if i in statuses:
                        print(f'You have {strength} strength')
                        strength += 10
                
                if poison:
                    print(f'You take {poison} damage from poison')
                    block -= poison
                    if poison>0:
                        poison -= 1
                        
                    if block<0:
                            hp += block
                            block = 0
                    print(f'You have {hp} hp and {block} block')
                
                for i in inhabitant:
                    if isinstance(i, Enemy):
                        #attack
                        i.take_damage(i.poison)
                        if i.poison>0:
                            i.poison -= 1
                        if i.health <= 0:
                            inhabitant.remove(i)
                            names.remove(i.name.lower())
                            enemies.remove(i)
                            continue
                        if i not in [donu,deca]:
                            if i.complex == False:
                                print(f"{i.name} does {i.action['Attack'] + i.str} damage to you")
                            else:
                                print(f"{i.name} does {i.actions[action_to_do]['Attack'] + i.str} damage to you")
                        if i.complex == False:
                            if i not in [donu,deca]:
                                block -= i.action['Attack']
                                block -= i.str
                                if shield_module in bag and i.actions[action_to_do]['Attack'] + i.str != 0:
                                    powers.append(armour_up)
                                    powers.append(armour_up)
                                    powers.append(armour_up)
                            i.reset_block()
                            i.set_block(i.action['Block'])
                            if i in [slime]:
                                if ruins_hard<=4:
                                    print('You gain 3 poison')
                                    poison += 3
                                else:
                                    print('You got 5 poison and 2 slimed')
                                    poison += 5
                                    for i in range(2):
                                        deck.append(slimed)
                                    random.shuffle(deck)
                            if i in [scavenger1, scavenger2]:
                                if vulture in inhabitant:
                                    vulture.set_block(6)
                                    print('Scavenger gives the vulture 6 block')
                                else:
                                    print('Scavenger also blocks for 6')
                                    i.set_block(6)
                            if i in [b_slaver]:
                                print('Slaver weakens you')
                                if city_hard <= 4:
                                    strength -= 1
                                else:
                                    strength -= 3
                            if i in [r_slaver]:
                                print('Slaver vulnerates you')
                                if city_hard <= 4:
                                    dexterity -= 1
                                else:
                                    dexterity -= 3
                            if i in [b_sentry, b_sentry1]:
                                print('Defence Sentry protects everyone')
                                for i in enemies:
                                    i.set_block(13)
                            if i in [bulwark]:
                                for i in enemies:
                                    i.set_block(20)
                            if i in [repulse]:
                                for i in range(7):
                                    deck.append(dazed)
                                random.shuffle(deck)
                            if i in [laserbot]:
                                for i in range(2):
                                    deck.append(burn)
                            if i in [concept]:
                                city_hard = 5
                                if turn%2 == 0:
                                    print('Concept protects the Orb')
                                    orb.set_block(999)
                                else:
                                    if orb not in enemies:
                                        print('Concept summons the Orb')
                                        orb.set_health(280)
                                        inhabitant.append(orb)
                                        enemies.append(orb)
                                        names.append('orb')
                                        inhabitant.reverse()
                                        enemies.reverse()
                                        names.reverse()
                                    else:
                                        print('Concept erases the enemy\'s mind')
                                        for rangee in range(10):
                                            deck.append(erased)
                                        random.shuffle(deck)
                            if i in [deca]:
                                if turn%2 == 0:
                                    for i in enemies:
                                        i.block += 150
                                else:
                                    print(f"Deca does {44 + deca.str} damage to you. You are dazed.")
                                    for ronge in range(4):
                                        discard.append(dazed)
                                    block -= 44
                                    block -= deca.str
                                    if block<0:
                                        hp += block
                                        block = 0
                            if i in [donu]:
                                if turn%2 == 0:
                                    for ronge in range(2):
                                        print(f'Donu does {44 + donu.str} damage to you')
                                        block -= 44
                                        block -= donu.str
                                        if block<0:
                                            hp += block
                                            block = 0
                                else:
                                    for i in enemies:
                                        i.str += 40
                                    
                        else:
                            block -= i.actions[action_to_do]['Attack']
                            block -= i.str
                            i.reset_block()
                            i.set_block(i.actions[action_to_do]['Block'])
                            if shield_module in bag and i.actions[action_to_do]['Attack'] + i.str != 0:
                                powers.append(armour_up)
                                powers.append(armour_up)
                                powers.append(armour_up)
                            if i in [golem, mimic, looter, exploder]:
                                if action_to_do == 0:
                                    action_to_do = 1
                                else:
                                    action_to_do = 0
                                    if i in [looter]:
                                        print('Looter steals 40 gold and leaves')
                                        inhabitant.remove(looter)
                                        enemies.remove(looter)
                                        names.remove('looter')
                                        gold -= 40
                                        if gold<0:
                                            gold = 0
                                        print(f'You have {gold} gold')
                                    if i in [exploder]:
                                        print('Exploder explodes')
                                        inhabitant.remove(exploder)
                                        enemies.remove(exploder)
                                        names.remove('exploder')
                            elif i in [taskmaster]:
                                if action_to_do == 0:
                                    action_to_do = 1
                                    print('Taskmaster wounds you')
                                    deck.append(wound)
                                else:
                                    action_to_do = 0
                                    print('Taskmaster wounds you')
                                    deck.append(wound)
                                    if city_hard > 4:
                                        print('Taskmaster rallys its allies!')
                                        for i in enemies:
                                            i.str += 3
                            elif i in [sentry]:
                                if action_to_do == 0:
                                    action_to_do = 1
                                else:
                                    print('Sentry dazes you')
                                    for i in range(5):
                                        deck.append(dazed)
                                    random.shuffle(deck)
                                    action_to_do = 0
                            elif i in [ghost]:
                                if action_to_do == 0:
                                    print('You lose 3 strength.')
                                    strength -= 3
                                    action_to_do = 1
                                elif action_to_do == 1:
                                    print('You gain 6 poison and 3 burn')
                                    poison += 6
                                    for i in range(3):
                                        deck.append(burn)
                                    random.shuffle(deck)
                                    action_to_do = 2
                                elif action_to_do == 2:
                                    print('You gain 2 poison')
                                    poison += 2
                                    action_to_do = 3
                                elif action_to_do == 3:
                                    print('You gain 1 burn')
                                    deck.append(burn)
                                    random.shuffle(deck)
                                    action_to_do = 2
                            elif i in [vulture]:
                                if action_to_do == 0:
                                    for i in deck:
                                        if i in rare_card_pool:
                                            print(f'Vulture steals your {i.name}')
                                            deck.remove(i)
                                            break
                                    action_to_do = 1
                                elif action_to_do == 1:
                                    print('Vulture steals 10 gold')
                                    gold -= 10
                                    action_to_do = 2
                                elif action_to_do == 2:
                                    action_to_do = 3
                                elif action_to_do == 3:
                                    print('Vulture steals 10 gold')
                                    gold -= 10
                                    action_to_do = 1
                            elif i in [mystic]:
                                if action_to_do == 0:
                                    try:
                                        print('Mystic heals the guard')
                                        guard.health += 20
                                    except:
                                        print('Mystic does nothing')
                                    action_to_to = 1
                                else:
                                    print('Mystic burns you')
                                    deck.append(burn)
                                    random.shuffle(deck)
                                    action_to_do = 0
                            elif i in [orb]:
                                if city_hard <= 4:
                                    if action_to_do in [0,1,2]:
                                        print('Orb charges up')
                                        action_to_do += 1
                                else:
                                    if action_to_do == 0:
                                        print('Orb charges up')
                                        action_to_do = 1
                                    elif action_to_do == 1:
                                        print('Orb charges up')
                                        action_to_do = 3
                            elif i in [crime_boss]:
                                if action_to_do == 0:
                                    action_to_do = 1
                                elif action_to_do == 1:
                                    print('Crime Boss calls in a Thief')
                                    b = copy.copy(thief)
                                    inhabitant.append(b)
                                    enemies.append(b)
                                    names.append('thief')
                                    action_to_do = 2
                                elif action_to_do == 2:
                                    print('Crime Boss is hurt by recoil')
                                    crime_boss.take_damage(30)
                                    if crime_boss.health <= 0:
                                        inhabitant.remove(i)
                                        enemies.remove(i)
                                        names.remove(i.name.lower())
                                    print(f'Crime Boss is at {crime_boss.health} hp')
                                    if crime_boss.health>150:
                                        action_to_do = 1
                                    else:
                                        action_to_do = 3
                                elif action_to_do == 3:
                                    print('Crime boss incapacitates you')
                                    for i in range(5):
                                        deck.append(dazed)
                                        deck.append(wound)
                                    random.shuffle(deck)
                                    action_to_do = 0
                            elif i in [automaton]:
                                if action_to_do == 0:
                                    print('The Automaton sears you')
                                    for i in range(3):
                                        deck.append(burn)
                                    random.shuffle(deck)
                                    if auto_check == True:
                                        action_to_do = 1
                                elif action_to_do == 1:
                                    print('The Automaton sunders your defences')
                                    dexterity -= 3
                                    action_to_do = 2
                                elif action_to_do == 2:
                                    print('The Automation prepares to use HYPERBEAM...')
                                    action_to_do = 3
                                elif action_to_do == 3:
                                    action_to_do = 0
                                    auto_check = False
                            elif i in [transient]:
                                if action_to_do != 3:
                                    action_to_do += 1
                                else:
                                    inhabitant.remove(transient)
                                    enemies.remove(transient)
                                    names.remove('transient')
                            elif i in [maw]:
                                if action_to_do == 0:
                                    print('You feel Dread')
                                    for i in range(10):
                                        deck.append(dread)
                                    random.shuffle(deck)
                                    action_to_do = 1
                                elif action_to_do == 1:
                                    for i in range(10):
                                        print('yO U fE EL UnEA S Y')
                                    for i in deck:
                                        if i == dread:
                                            hp -= 2
                                            print('yO U lO SE 2 H P')
                            elif i in [glitch]:
                                action_to_do = random.randint(0,3)
                                deck.append(glitched)
                                random.shuffle(deck)
                                for ye in enemies:
                                    if ye.name == 'Bug':
                                        ye.str += 20
                                        print(f"{ye} can't be replicated!")
                                if action_to_do == 0:
                                    print('Power Ring!')
                                    for yoy in enemies:
                                        if yoy.name == 'Bug':
                                            yoy.str += 5
                                elif action_to_do == 1:
                                    print('Your deck is decimated.')
                                    count = 0
                                    for cerd in deck:
                                        if count%4 == 0:
                                            deck.remove(cerd)
                                            print(f'Your {cerd.name} ceases to exist.')
                                elif action_to_do == 2:
                                    print('Mind Bloom!')
                                    defk = deck.copy()
                                    for derk in defk:
                                        deck.append(derk)
                                        deck.append(derk)
                                        print('Cards arent removed from your deck properly!')
                                elif action_to_do == 3:
                                    print('Hello World.')
                                    glitch.set_health(909)
                            elif i in [clock]:
                                if action_to_do == 0:
                                    for doom in range(turn):
                                        deck.append(darkness)
                                    random.shuffle(deck)
                                    if 13-turn != 1:
                                        print(f'{13-turn} turns left')
                                    else:
                                        print('1 turn left')
                                    if turn>=13:
                                        action_to_do = 1
                                elif action_to_do == 1:
                                    for tu in range(13):
                                        print('Doom')
                                        hp = int(hp/2)
                                        print(hp)
                            elif i in [one]:
                                if action_to_do == 0:
                                    for culte in [cultist, cultist1]:
                                        if culte not in inhabitant:
                                            inhabitant.append(culte)
                                            enemies.append(culte)
                                            names.append('cultist')
                                    action_to_do = 1
                                elif action_to_do == 1:
                                    for r in enemies:
                                        r.str += 20
                                        print(f'{r.name} gains 20 strength!')
                                    action_to_do = 2
                                elif action_to_do == 2:
                                    action_to_do = 3
                                elif action_to_do == 3:
                                    print('Awakened One sends you to the Void.')
                                    for i in range(5):
                                        deck.append(voided)
                                    random.shuffle(deck)
                                    action_to_do = 0

                            
                        if block<0:
                            hp += block
                            block = 0
                        if hp<=0:
                            dead = True
                            print('You are dead!')
                            exit()
                        else:
                            print(f'You are at {hp} hp and {block} block')
            


                check = False
                for i in inhabitant:
                    if isinstance(i, Enemy):
                        check = True
            #ending fight
            if current_cave in [ruins_cultist, ruins_serpent, ruins_swarm]:
                gold += 10
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank')
                print('You got 10 gold')
                print(f'You have {gold} gold')
                current_cave = ruins_chest
                match random.randint(1,5):
                    case 1|2|3|4:
                        ruins_chest.set_item(random.choice(card_pool))
                    case 5:
                        ruins_chest.set_item(random.choice(rare_card_pool))
                        
            elif current_cave in [city_thieves, city_sentry, city_guard]:
                gold += 15
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank')
                print('You got 15 gold')
                print(f'You have {gold} gold')
                current_cave = city_chest
                match random.randint(1,5):
                    case 1|2|3|4:
                        city_chest.set_item(random.choice(card_pool))
                    case 5:
                        city_chest.set_item(random.choice(rare_card_pool))
            elif current_cave in [ruins_golem, ruins_priest, ruins_slime, ruins_mimic]:
                gold += 25
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank')
                print('You got 25 gold')
                print(f'You have {gold} gold')
                current_cave = ruins_chest
                ruins_chest.set_item(random.choice(relic_pool))
                for i in bag:
                    if i == black_blood:
                        hp += 10
                print(f'You have {hp} hp')
            elif current_cave in [city_orb, city_task, city_line]:
                gold += 30
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank')
                print('You got 30 gold')
                print(f'You have {gold} gold')
                current_cave = city_chest
                match random.randint(1,5):
                    case 1|2|3|4:
                        city_chest.set_item(random.choice(relic_pool))
                    case 5:
                        city_chest.set_item(random.choice(rare_relic_pool))
            elif current_cave in [ruins_staircase, elevator]:
                hp += 20
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank')
                gold += 100
                print('You got 100 gold')
                print(f'You have {gold} gold')
                choices = random.sample(boss_relic_pool, 3)
                count = 0
                for choice in choices:
                    print(f'[{count}] {choices[count].name} - {choices[count].description}')
                    count += 1
                
                check = False
                while check == False:
                    try:
                        choice = input('Choose a boss relic ')
                        current_cave.set_item(choices[int(choice)])
                        check = True
                    except:
                        print('Input a valid number\n')
            elif current_cave == void_transient:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('You got the Transient Soul. From now on, your attacks will grant you protection.')
                bag.append(transient_soul)
                transient_soul.describe()
            elif current_cave == void_maw:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('You got the Infinite Maw. Your status cards will grant you power.')
                bag.append(infinite_maw)
                infinite_maw.describe()
            elif current_cave == void_shapes:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('''
[0] - Shield Module: You become more powerful the more you are attacked. The Machine Gods will conteract this.
[1] - HUD Module: You draw 10 more cards each turn, but you are dazed.
[2] - Laser Module: Deal 50 damage to the first enemy on each of your turns.
[3] - Bomb Module: Whenever you choose to end your turn, gain 20 strength.
''')
                while not isinstance(choice, int):
                    try:
                        choice = int(input('Choose a reward: '))
                        bad.append(relic_shapes[choice])
                        relic_shapes[choice].describe()
                        if relic_shapes[choice] == hud_module:
                            draw_count += 10
                            for d in range(10):
                                perma_deck.append(dazed)
                    except:
                        print('Enter a valid number')
                        choice = ''
            elif current_cave == void_line:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('You got the Cultist\'s Amulet. The Amulet empowers you with the strength of the Crow God.')
                cultists_amulet.describe()
                bag.append(cultists_amulet)
                perma_str += 10
                perma_dex += 10
                energy_count += 1
            elif current_cave == void_concept:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('You got some Blueprints. They show a detailed description of the Concept. With this, you can learn its protective properties.')
                blueprints.describe()
                bag.append(blueprints)
            elif current_cave == void_glitch:
                gold += 200
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 200 gold.')
                print(f'You have {gold} gold')
                print('You got an Error. Your strength grows massively, as long as you are weak.')
                error.describe()
                bag.append(error)
            elif current_cave == void_one:
                gold += 500
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 500 gold.')
                print(f'You have {gold} gold')
                bag.append(eternal_feather)
                print('The Eternal Feather grants you power.')
                print('\n\n\n\n YOU NEED TO PICK THIS ONE UP TO OBTAIN IT \n\n\n\n')
                current_cave.set_item(eternal_feather)
                void_boss_beaten = True
            elif current_cave == void_dd:
                gold += 500
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 500 gold.')
                print(f'You have {gold} gold')
                bag.append(effigy)
                print('The Machine God\'s Effigy grants you power.')
                print('\n\n\n\n YOU NEED TO PICK THIS ONE UP TO OBTAIN IT \n\n\n\n')
                current_cave.set_item(effigy)
                void_boss_beaten = True
            elif current_cave == void_clock:
                gold += 500
                for i in bag:
                    if i == piggy_bank:
                        gold += 10
                        print('You find 10 gold in your piggy bank. The only solice you will find in these parts.')
                print('You got 500 gold.')
                print(f'You have {gold} gold')
                bag.append(watch)
                print('The Doomsday Clock grants you power.')
                print('\n\n\n\n YOU NEED TO PICK THIS ONE UP TO OBTAIN IT \n\n\n\n')
                current_cave.set_item(watch)
                void_boss_beaten = True

        else:
            print("There is no one here to fight with")
#FIGHTING CODE ENDS HERE

    elif command == "pat": #Probably not in final game
        if inhabitant is not None:
            if isinstance(inhabitant, Enemy): #fix
                print("I wouldn't do that if I were you…")
            else:
                inhabitant.pat() #fix
        else:
            print("There is no one here to pat :(")
    elif command == "take":
        if item is not None:
            if isinstance(item, Card):
                print("You put the " + item.get_name() + " in your deck")
                perma_deck.append(item)
            else:
                bag.append(item)
                if item == combat_manual:
                    draw_count += 1
                elif item == small_heart:
                    hp += 20
                elif item == whetstone:
                    perma_str += 2
                elif item == wet_stone:
                    perma_dex += 2
                elif item == abbis_eye:
                    perma_str += 5
                    perma_dex += 5
                elif item == coffee:
                    energy_count += 1
                elif item == arcane_manual:
                    draw_count += 5
                elif item == snecko_eye:
                    draw_count += 2
                elif item == eternal_feather:
                    hp = hp*3
                    hp = int(hp/4)
                elif item == empty_cage:
                    for i in range(3):
                        count = 0
                        for i in perma_deck:
                            print(f"[{count}] - {i.name}")
                            count += 1
                        rere = False
                        re = input('Which card do you want to remove?')
                        while rere == False:
                            try:
                                print(f'You removed the {perma_deck[int(re)].name} from your deck')
                                perma_deck.pop(int(re))
                                rere = True
                            except:
                                print('Enter a valid number.')
                elif item in blight_pool:
                    if item == burned:
                        for i in range(2):
                            perma_deck.append(burn)
                    elif item == scatterbrained:
                        for i in range(7):
                            perma_deck.append(dazed)
                    elif item == wounded:
                        hp -= 30
                    elif item == doomed:
                        if current_cave in [ruins, blight_chest]:
                            ruins_staircase_generated = True
                            current_cave = ruins_staircase
                    elif item == incapacitated:
                        draw_count -= 1
                    x = random.choice(rare_relic_pool)
                    bag.append(x)
                    x.describe()
                    if x == big_heart:
                        hp += 40
            current_cave.set_item(None)
            if current_cave in [ruins_chest, blight_chest]:
                current_cave = ruins
            elif current_cave in [city_chest]:
                current_cave = city

    elif command == "test":
        print(a)
    elif command == "heal":
        if current_cave in [ruins_healer]:
            amount = input(f'Enter the amount you want to heal. Each hp healed costs 1 gold. You have {gold} gold.')
            try:
                confirm = int(amount)
                if confirm >= 0:
                    if confirm <= gold:
                        if heal_check == True:
                            heal_limit -= 1
                        heal_check = False
                        print(f'You gained {confirm} hp')
                        print(f'You payed {confirm} gold')
                        gold -= confirm
                        hp += confirm
                    else:
                        print("You don't have enough gold")
                else:
                    print(f'You can\'t heal a negative amount.')
                    
                print(f'You have {hp} hp and {gold} gold.')
            except:
                print('No. Try again.')
        else:
            print('There is no healer here.')
                
    if hp<=0:
        dead = True
        print('YOU DIED')
exit()


