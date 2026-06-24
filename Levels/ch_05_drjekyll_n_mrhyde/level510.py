import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, JumpPad, Ladder, PressTrap, Ice, Icicle, DynamicSpikePlatform, DynamicSpike, Lava, Water, Checkpoint, FragileGround, Fan,  GravityJumpPad, Bridge, StartPortal, EndPortal, TipCloud, Spike, Void
from physics import apply_gravity, apply_agt, move_and_collide, agt_move_and_collide, climb_ladder, jump_from_the_top_of_ladder, buoyant_force, crouching_adjustment, squash_adjustment
from dynamic_spike import dynamic_spike_movement_based_on_timer
from fragile_ground import trigger_fragile_ground, fragile_ground_check, respawn_fragile_ground
from fans import apply_fan_effect
from press_trap import apply_press_trap_effect, update_press_trap
from checkpoint import checkpoint_activation
from portals import link_portals, teleport_player, cooldown_timer, set_portal_exit_side
from maincamera import follow_player

class Level510:
       def __init__(self):
            self.WORLD_LEFT = -125
            self.WORLD_WIDTH = 5000
            self.WORLD_HEIGHT=8000
            self.all_sprites = pygame.sprite.LayeredUpdates()

            self.player = Player(-60, 900, 50, 50)
            self.ice_floor = Ice(-125, 950, 260, 500)
            self.ice_floor6 = Ice(325, 1000, 560, 500)
            self.small_wall = Bridge(135, 925, 25, 575)
            self.spike_down = Spike(135, 900, 25, 25, 0)
            self.ice_floor2 = Ice(160, 925, 165, 500)
            self.floating_platform = DynamicSpikePlatform(250, 800, 50, 50)
            self.dsu2 = DynamicSpike(250, 835, 25, 25, 180)
            self.dsu3 = DynamicSpike(275, 835, 25, 25, 180)
            self.icicle_down = Icicle(325, 965, 25,35, 0)
            self.icicle_down2 = Icicle(350, 965, 25,35, 0)
            self.icicle_down3 = Icicle(375, 965, 25,35, 0)
            self.icicle_down4 = Icicle(400, 965, 25,35, 0)
            self.icicle_down5 = Icicle(425, 965, 25,35, 0)
            self.wall = Bridge(450, 900, 50, 300)
            self.fg1 = FragileGround(575, 840, 50, 50)
            self.lava1 = Lava(500, 910, 200, 155)
            self.wall2 = Bridge(700, 900, 50, 300)
            self.floor = Ground(750, 950, 85, 200)
            self.fan_up = Fan(755, 900, 75, 50, (0, -1), 7000, 205)
            self.ice_wall = Ice(835, 650, 50, 300)

            # Second floor

            self.ice_ceiling = Ice(675, 425, 165, 50)
            self.ice_ceiling2 = Ice(745, 475, 90, 25)
            self.icicle_up = Icicle(675, 475, 25, 35, 180)
            self.icicle_up2 = Icicle(700, 475, 25, 35, 180)
            self.small_wall2 = DynamicSpikePlatform(675, 350, 50, 125)
            self.ice_ceiling3 = Ice(405, 425, 280, 25)
            self.block = DynamicSpikePlatform(475, 450, 50, 50)
            self.spike_right = Spike(525, 450, 50, 35, -90)
            self.blocks = DynamicSpikePlatform(475, 585, 50, 100)
            self.lava2 = Lava(325, 400, 80, 50)
            self.ice_ceiling4 = Ice(100, 425, 230, 50)
            self.checkpoint = Checkpoint(245, 475, 50, 50)
            self.agt_jump_pad2 = GravityJumpPad(155, 465, 35, 25, 3500)

            self.ice_floor3 = Ice(560, 620, 140, 25)
            self.agt_jump_pad = GravityJumpPad(585, 595, 50, 25, -1500)

            # Water Section

            self.wall3 = Bridge(75, 350, 25, 360)
            self.ice_wall2 = Ice(-125, 0, 50, 950)
            self.ice_ceiling5 = Ice(-125, 0, 725, 125)
            self.giant_icicle_up = Icicle(-75, 125, 65, 120, 180)
            self.giant_icicle_up2 = Icicle(-10, 125, 50, 65, 180)
            self.ice_floor4 = Ice(-125, 780, 375, 35)
            self.ice_wall3 = Ice(250, 580, 35, 235)
            self.water = Water(-75, 350, 175,430)
            self.water2 = Water(100, 675, 150, 130)
            self.icicle_left = Icicle(225, 675, 35, 25, 90)
            self.icicle_down6 = Icicle(210, 745, 25, 35, 0)
            self.icicle_up3 = Icicle(100, 660, 25, 35, -90)
            self.fan_up2 = Fan(-25, 775, 55, 50, (0, -1), 5000, 700)
            self.icicle_right = Icicle(-75, 615, 35, 25, -90)
            self.icicle_left2 = Icicle(50, 615, 30, 25, 90)
            self.icicle_right2 = Icicle(-75, 410, 35, 25, -90)
            self.icicle_left3 = Icicle(50, 450, 30, 25, 90)

            #Third floor
            self.ice_floor5 = Ice(100, 350, 300, 75)
            self.icicle_down7 = Icicle(240, 315, 25, 35, 0)
            self.ground = Ground(350, 325, 100, 100)
            self.dsp = DynamicSpikePlatform(375, 325, 50, 35)
            self.dsd = DynamicSpike(375, 320, 25, 25, 0)
            self.dsd2 = DynamicSpike(400, 320, 25, 25, 0)

            self.lava4 = Lava(450, 350, 225, 75)

            self.wall4 = Ice(575, 245, 35, 125 )
            self.icicle_left4 = Icicle(540, 245, 25, 35, 90)
            self.icicle_right3 = Icicle(610, 245, 25, 35, -90)
            self.wall5 = Ice(575, 40, 35, 125)
            self.icicle_left5 = Icicle(540, 140, 25, 35, 90)
            self.icicle_right4 = Icicle(610, 140, 25, 35, -90)

            self.platform = Ground(730, 380, 65, 25)
            self.ladder = Ladder(815, 345, 25, 85)
            self.water3 = Water(720, 350, 115, 70)

            self.ice_wall4 = Ice(835, 0, 50, 1150)
            self.platform2 = Bridge(775, 280, 60, 25)
            self.agt_jump_pad3 = GravityJumpPad(785, 255, 50, 25, -2000)
            self.ice_platform = Ice(720, 25, 115, 25)
            self.agt_jump_pad4 = GravityJumpPad(720, 50, 50, 25, 2000)
            self.ice_platform2 = Ice(625, 165, 85, 25)
            self.blue_portal = StartPortal(625, 90, 50, 75)

            #Void Rooms

            self.void = Void(-125, 1560, 5125, 5000)

            #Room 1
            self.room_wall = DynamicSpikePlatform(150, 1900, 25, 150)
            self.room_floor = DynamicSpikePlatform(150, 2050, 275, 25)
            self.room_ceiling = DynamicSpikePlatform(150, 1900, 250, 25)
            self.room_wall2 = DynamicSpikePlatform(400, 1900, 25, 150)
            self.orange_portal= EndPortal(175, 1950, 50, 100)
            self.blue_portal2 = StartPortal(350, 1950, 50, 100)

            #Room2
            self.room2_wall = DynamicSpikePlatform(2500, 2050, 25, 275)
            self.room2_floor = DynamicSpikePlatform(2500, 2325, 425, 25)
            self.room2_ceiling = DynamicSpikePlatform(2500, 2050, 400, 25)
            self.room2_wall2 = DynamicSpikePlatform(2900, 2050, 25, 275)
            self.orange_portal2 = EndPortal(2825, 2075, 75, 25)
            set_portal_exit_side(self.orange_portal2, "bottom")
            self.stairs1 = TipCloud(2875, 2230, 25, 95, "")
            self.stairs2 = TipCloud(2850, 2245, 25, 80, "")
            self.stairs3 = TipCloud(2825, 2260, 25, 65, "")
            self.stairs4 = TipCloud(2800, 2275, 25, 50, "")
            self.white_block = TipCloud(2600, 2075, 25, 125, "")
            self.spike_up = Spike(2600, 2200, 25, 25, 180)
            self.blue_portal3 = StartPortal(2525, 2250, 25, 75)

            #Room 3
            self.room3_wall = DynamicSpikePlatform(700, 3800, 25, 300)
            self.room3_floor = DynamicSpikePlatform(700, 4100, 325, 25)
            self.room3_ceiling = DynamicSpikePlatform(700, 3800, 300, 25)
            self.room3_wall2 = DynamicSpikePlatform(1000, 3800, 25, 300)
            self.orange_portal3 = EndPortal(725, 3955, 25, 75)
            self.floor2 = TipCloud(725, 4030, 75, 15, "")
            self.column = TipCloud(760, 4045, 15, 55, "")
            self.dsp2 = DynamicSpikePlatform(825, 3825, 50, 25)
            self.dsu4 = DynamicSpike(825, 3845, 25, 25, 180)
            self.dsu5 = DynamicSpike(850, 3845, 25, 25, 180)
            self.lava5 = Lava(760, 4085, 150, 15)
            self.floor3 = TipCloud(910, 4030, 75, 15, "")
            self.column2 = TipCloud(910, 4045, 15, 55, "")
            self.blue_portal4 = StartPortal(950, 3955, 50, 75)


            #Room 4
            self.room4_wall = DynamicSpikePlatform(1700, 2300, 25, 300)
            self.room4_floor = DynamicSpikePlatform(1700, 2600, 425, 25)
            self.room4_ceiling = DynamicSpikePlatform(1700, 2300, 400, 25)
            self.room4_wall2 = DynamicSpikePlatform(2100, 2300, 25, 300)
            self.orange_portal4 = EndPortal(1725, 2525, 50, 75)
            self.floor4= TipCloud(1700, 2450, 250, 15, "")
            self.jumpPad2 = JumpPad(2050, 2575, 50, 25, -950)
            self.spike_up2 = Spike(2050, 2325, 25, 25, 180)
            self.spike_up3 = Spike(2075, 2325, 25, 25, 180)
            self.blue_portal5 = StartPortal(1700, 2375, 50, 75)

            #Final Room 

            self.final_room_wall = DynamicSpikePlatform(100, 4800, 25, 200)
            self.final_room_floor = DynamicSpikePlatform(100, 5000, 925, 25)
            self.final_room_ceiling = DynamicSpikePlatform(100, 4800, 900, 25)
            self.final_room_wall2 = DynamicSpikePlatform(1000, 4800, 25, 200)
            self.orange_portal5 = EndPortal(100, 4850, 50, 100)
            self.blue_portal6 = StartPortal(950, 4850, 50, 100)
            self.press_trap2 = PressTrap(195, 4800, 70, 70, 180)
            self.small_floor = TipCloud(380, 4975, 50, 25, "")
            self.agt_jump_pad5 = GravityJumpPad(380, 4940, 35, 25, -700)
            self.spike_down2 = Spike(505, 4975, 25,25, 0)
            self.spike_down3 = Spike(530, 4975, 25,25, 0)
            self.spike_down4 = Spike(555, 4975, 25,25, 0)
            self.spike_up4 = Spike(550, 4825, 25, 25, 180)
            self.agt_jump_pad6 = GravityJumpPad(605, 4825, 35, 25, 700)
            self.spike_up5 = Spike(670, 4825, 25, 25, 180)
            self.wall6 =TipCloud(735, 4800, 100, 165, "")
            self.stairs5 = TipCloud(935, 4975, 65, 25, "")
            self.stairs6 = TipCloud(975, 4950, 25, 25, "")


            #Final Section: 


            self.orange_portal6 = EndPortal(885, 100, 200, 50)
            self.ice_wall5 = Ice(1035, 0, 50, 1150)
            self.void2 = Void(885, 650, 150, 2000)
            self.finish_level_trigger = FinishLevelTrigger(885, 1125, 150, 200)

            self.colliders = pygame.sprite.Group()
            self.colliders.add(self.ice_ceiling4, self.ice_floor6, self.ice_floor, self.small_wall,self.ice_floor2, self.ice_floor3,  self.agt_jump_pad, self.floating_platform, self.wall2, self.wall, self.fg1,  self.floor, self.fan_up, self.ice_wall, self.ice_wall5,  self.ice_ceiling, self.ice_ceiling2, self.small_wall2, self.ice_ceiling3, self.block, self.blocks,  self.agt_jump_pad2,  self.wall3, self.ice_wall2, self.ice_ceiling5, self.ice_floor4, self.ice_wall3, self.fan_up2, self.ice_floor5,self.ground,self.dsp,self.wall4,self.wall5,self.platform,self.ice_wall4,self.platform2,self.agt_jump_pad3,self.ice_platform,self.agt_jump_pad4,self.ice_platform2,self.room_wall,self.room_floor,self.room_ceiling,self.room_wall2,self.room2_wall,self.room2_floor,self.room2_ceiling,self.room2_wall2,self.stairs1,self.stairs2,self.stairs3,self.stairs4,self.white_block,self.room3_wall,self.room3_floor,self.room3_ceiling,self.room3_wall2,self.floor2,self.column,self.dsp2,self.floor3,self.column2,self.room4_wall,self.room4_floor,self.room4_ceiling,self.room4_wall2,self.floor4,self.jumpPad2,self.final_room_wall,self.final_room_floor,self.final_room_ceiling,self.final_room_wall2,self.small_floor,self.agt_jump_pad5,self.wall6, self.stairs5, self.stairs6, self.agt_jump_pad6, self.ice_wall5)
            self.triggers = pygame.sprite.Group()
            self.triggers.add(self.spike_down, self.fg1, self.spike_up5, self.icicle_left4, self.icicle_right3, self.icicle_left5, self.icicle_right4, self.spike_up4, self.press_trap2,  self.dsu2, self.dsu3, self.icicle_down, self.icicle_down2, self.icicle_down3, self.icicle_down4, self.icicle_down5, self.icicle_up, self.icicle_up2, self.spike_right,self.icicle_left,self.icicle_down6,self.icicle_up3,self.fan_up2,self.icicle_right,self.icicle_left2,self.icicle_right2,self.icicle_left3,self.icicle_down7,self.dsd,self.dsd2,self.spike_up2,self.spike_up3,self.agt_jump_pad,self.agt_jump_pad2,self.agt_jump_pad3,self.agt_jump_pad4,self.agt_jump_pad5,self.agt_jump_pad6, self.blue_portal,self.orange_portal,self.blue_portal2,self.orange_portal2,self.blue_portal3,self.orange_portal3,self.blue_portal4,self.orange_portal4,self.blue_portal5,self.orange_portal5,self.blue_portal6,self.orange_portal6, self.finish_level_trigger, self.checkpoint, self.water, self.water2, self.water3, self.lava1, self.lava2, self.lava4, self.lava5)
            

            self.all_sprites.add(self.player, layer = 2)
            self.all_sprites.add(self.spike_down, layer = 3)
            self.all_sprites.add(self.ice_floor, layer = 1)
            self.all_sprites.add(self.ice_floor6, layer = 2)
            self.all_sprites.add(self.small_wall, layer = 1)
            self.all_sprites.add(self.ice_floor2, layer = 1)
            self.all_sprites.add(self.floating_platform, layer = 2)
            self.all_sprites.add(self.dsu2, layer = 1)
            self.all_sprites.add(self.dsu3, layer = 1)
            self.all_sprites.add(self.icicle_down, layer = 3)
            self.all_sprites.add(self.icicle_down2, layer = 3)
            self.all_sprites.add(self.icicle_down3, layer = 3)
            self.all_sprites.add(self.icicle_down4, layer = 3)
            self.all_sprites.add(self.icicle_down5, layer = 3)
            self.all_sprites.add(self.wall, layer = 1)
            self.all_sprites.add(self.fg1, layer = 1)
            self.all_sprites.add(self.lava1, layer = 1)
            self.all_sprites.add(self.wall2, layer = 1)
            self.all_sprites.add(self.floor, layer = 1)
            self.all_sprites.add(self.fan_up, layer = 1)
            self.all_sprites.add(self.ice_wall, layer = 1)
            self.all_sprites.add(self.ice_ceiling, layer = 1)
            self.all_sprites.add(self.ice_ceiling2, layer = 1)
            self.all_sprites.add(self.icicle_up, layer = 2)
            self.all_sprites.add(self.icicle_up2, layer = 2)
            self.all_sprites.add(self.small_wall2, layer = 3)
            self.all_sprites.add(self.ice_ceiling3, layer = 1)
            self.all_sprites.add(self.block, layer = 1)
            self.all_sprites.add(self.spike_right, layer = 3)
            self.all_sprites.add(self.blocks, layer = 1)
            self.all_sprites.add(self.lava2, layer = 1)
            self.all_sprites.add(self.agt_jump_pad2, layer = 2)
            self.all_sprites.add(self.wall3, layer = 1)
            self.all_sprites.add(self.ice_wall2, layer = 1)
            self.all_sprites.add(self.ice_ceiling5, layer = 1)
            self.all_sprites.add(self.giant_icicle_up, layer = 3)
            self.all_sprites.add(self.giant_icicle_up2, layer = 3)
            self.all_sprites.add(self.ice_floor4, layer = 1)
            self.all_sprites.add(self.ice_wall3, layer = 1)
            self.all_sprites.add(self.water, layer = 0)
            self.all_sprites.add(self.water2, layer = 0)
            self.all_sprites.add(self.fan_up2, layer = 1)
            self.all_sprites.add(self.ice_floor5, layer = 1)
            self.all_sprites.add(self.icicle_left, layer = 3)
            self.all_sprites.add(self.icicle_down6, layer = 3)
            self.all_sprites.add(self.icicle_up3, layer = 3)
            self.all_sprites.add(self.icicle_right, layer = 3)
            self.all_sprites.add(self.icicle_left2, layer = 3)
            self.all_sprites.add(self.icicle_right2, layer = 3)
            self.all_sprites.add(self.icicle_left3, layer = 3)
            self.all_sprites.add(self.icicle_down7, layer = 3)
            self.all_sprites.add(self.icicle_down7, layer = 3)
            self.all_sprites.add(self.ground, layer = 1)
            self.all_sprites.add(self.dsp, layer = 2)
            self.all_sprites.add(self.dsd, layer = 1)
            self.all_sprites.add(self.dsd2, layer = 1)
            self.all_sprites.add(self.lava4, layer = 1)
            self.all_sprites.add(self.wall4, layer = 1)
            self.all_sprites.add(self.wall5, layer = 1)
            self.all_sprites.add(self.platform, layer = 1)
            self.all_sprites.add(self.ladder, layer = 1)
            self.all_sprites.add(self.water3, layer = 0)
            self.all_sprites.add(self.ice_wall4, layer = 1)
            self.all_sprites.add(self.platform2, layer = 1)
            self.all_sprites.add(self.agt_jump_pad3, layer = 1)
            self.all_sprites.add(self.ice_platform, layer = 1)
            self.all_sprites.add(self.agt_jump_pad4, layer = 1)
            self.all_sprites.add(self.ice_platform2, layer = 1)
            self.all_sprites.add(self.blue_portal, layer = 1)
            self.all_sprites.add(self.room_wall, layer = 1)
            self.all_sprites.add(self.room_floor, layer = 1)
            self.all_sprites.add(self.room_ceiling, layer = 1)
            self.all_sprites.add(self.room_wall2, layer = 1)
            self.all_sprites.add(self.orange_portal, layer = 1)
            self.all_sprites.add(self.blue_portal2, layer = 1)
            self.all_sprites.add(self.room2_wall, layer = 1)
            self.all_sprites.add(self.room2_floor, layer = 1)
            self.all_sprites.add(self.room2_ceiling, layer = 1)
            self.all_sprites.add(self.room2_wall2, layer = 1)
            self.all_sprites.add(self.orange_portal2, layer = 1)
            self.all_sprites.add(self.stairs1, layer = 1)
            self.all_sprites.add(self.stairs2, layer = 1)
            self.all_sprites.add(self.stairs3, layer = 1)
            self.all_sprites.add(self.stairs4, layer = 1)
            self.all_sprites.add(self.white_block, layer = 1)
            self.all_sprites.add(self.spike_up, layer = 3)
            self.all_sprites.add(self.blue_portal3, layer = 1)
            self.all_sprites.add(self.room3_wall, layer = 1)
            self.all_sprites.add(self.room3_floor, layer = 1)
            self.all_sprites.add(self.room3_ceiling, layer = 1)
            self.all_sprites.add(self.room3_wall2, layer = 1)
            self.all_sprites.add(self.orange_portal3, layer = 1)
            self.all_sprites.add(self.floor2, layer = 1)
            self.all_sprites.add(self.column, layer = 1)
            self.all_sprites.add(self.dsp2, layer = 1)
            self.all_sprites.add(self.dsu4, layer = 1)
            self.all_sprites.add(self.dsu5, layer = 1)
            self.all_sprites.add(self.lava5, layer = 1)
            self.all_sprites.add(self.floor3, layer = 1)
            self.all_sprites.add(self.column2, layer = 1)
            self.all_sprites.add(self.blue_portal4, layer = 1)
            self.all_sprites.add(self.room4_wall, layer = 1)
            self.all_sprites.add(self.room4_floor, layer = 1)
            self.all_sprites.add(self.room4_ceiling, layer = 1)
            self.all_sprites.add(self.room4_wall2, layer = 1)
            self.all_sprites.add(self.orange_portal4, layer = 1)
            self.all_sprites.add(self.blue_portal5, layer = 1)
            self.all_sprites.add(self.floor4, layer = 1)
            self.all_sprites.add(self.jumpPad2, layer = 3)
            self.all_sprites.add(self.spike_up2, layer = 3)
            self.all_sprites.add(self.spike_up3, layer = 3)
            self.all_sprites.add(self.final_room_wall, layer = 1)
            self.all_sprites.add(self.final_room_floor, layer = 1)
            self.all_sprites.add(self.final_room_ceiling, layer = 1)
            self.all_sprites.add(self.final_room_wall2, layer = 1)
            self.all_sprites.add(self.orange_portal5, layer = 1)
            self.all_sprites.add(self.blue_portal6, layer = 1)
            self.all_sprites.add(self.press_trap2, layer = 3)
            self.all_sprites.add(self.small_floor, layer = 1)
            self.all_sprites.add(self.agt_jump_pad5, layer = 1)
            self.all_sprites.add(self.spike_down2, layer = 3)
            self.all_sprites.add(self.spike_down3, layer = 3)
            self.all_sprites.add(self.spike_down4, layer = 3)
            self.all_sprites.add(self.spike_up4, layer = 3)
            self.all_sprites.add(self.agt_jump_pad6, layer = 1)
            self.all_sprites.add(self.spike_up5, layer = 3)
            self.all_sprites.add(self.wall6, layer = 1)
            self.all_sprites.add(self.stairs5, layer = 1)
            self.all_sprites.add(self.stairs6, layer = 1)
            self.all_sprites.add(self.orange_portal6, layer = 1)
            self.all_sprites.add(self.ice_wall5, layer = 1)
            self.all_sprites.add(self.void, layer = 0)
            self.all_sprites.add(self.void2, layer = 3)
            self.all_sprites.add(self.finish_level_trigger, layer = 1)
            self.all_sprites.add(self.ice_floor3, layer = 1)
            self.all_sprites.add(self.agt_jump_pad, layer = 3)
            self.all_sprites.add(self.checkpoint, layer = 2)
            self.all_sprites.add(self.ice_ceiling4, layer = 1)
            self.all_sprites.add(self.icicle_left4, layer = 3)
            self.all_sprites.add(self.icicle_right3, layer = 3)
            self.all_sprites.add(self.icicle_left5, layer = 3)
            self.all_sprites.add(self.icicle_right4, layer = 3)


       def update(self, dt):
            self.player.handle_input(dt)
            for ds in [self.dsu2, self.dsu3, self.dsd, self.dsd2, self.dsu4, self.dsu5]:
                   dynamic_spike_movement_based_on_timer(ds, dt)
              
            if self.player.gravity_direction == "up":
                    apply_agt(self.player, dt)
                    agt_move_and_collide(self.player, self.colliders, dt, self.triggers)
            else:
                    apply_gravity(self.player, dt)
                    move_and_collide(self.player, self.colliders, dt, self.triggers)
            apply_fan_effect(self.player, self.fan_up,  dt, water_multiplier=0.5)
            apply_fan_effect(self.player, self.fan_up2,  dt, water_multiplier=2)           
            trigger_fragile_ground(self.player, self.block, [self.fg1])
            fragile_ground_check(self.player, self.block, [self.fg1], self.colliders, dt)
            respawn_fragile_ground(self.colliders, self.all_sprites, [self.fg1], dt)
            checkpoint_activation(self.player, [self.checkpoint])
    
            apply_press_trap_effect(self.player, self.press_trap2, dt)
   
            update_press_trap(self.press_trap2, dt)
            link_portals(self.blue_portal, self.orange_portal)
            link_portals(self.blue_portal2, self.orange_portal2)
            link_portals(self.blue_portal3, self.orange_portal3)
            link_portals(self.blue_portal4, self.orange_portal4)
            link_portals(self.blue_portal5, self.orange_portal5)
            link_portals(self.blue_portal6, self.orange_portal6)
            for portal in [self.blue_portal, self.orange_portal, self.blue_portal2, self.orange_portal2, self.blue_portal3, self.orange_portal3, self.blue_portal4, self.orange_portal4, self.blue_portal5, self.orange_portal5, self.blue_portal6, self.orange_portal6]:
                    teleport_player(self.player, portal)
                    cooldown_timer(portal, dt)

            crouching_adjustment(self.player, self.colliders)
            squash_adjustment(self.player, self.colliders)
            buoyant_force(self.player, [self.water, self.water2, self.water3])
            climb_ladder(self.player, [self.ladder])
            jump_from_the_top_of_ladder(self.player, [self.ladder])


       def draw(self, screen):
                
                offset_x, offset_y = follow_player(
                    self.player,
                    screen.get_width(),
                    self.WORLD_WIDTH,
                    screen.get_height(),
                    self.WORLD_HEIGHT,
                    world_left=self.WORLD_LEFT,
                )
                screen.fill((163, 182, 196))
                for sprite in self.all_sprites:
                    screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

       def is_finished(self):
                return self.player.rect.colliderect(self.finish_level_trigger.rect)
