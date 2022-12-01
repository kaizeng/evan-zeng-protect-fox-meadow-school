@namespace
class SpriteKind:
    Thing = SpriteKind.create()
    Villager = SpriteKind.create()
    Title = SpriteKind.create()
    Darkness = SpriteKind.create()
def house_walls_around(column: number, row: number):
    tiles.set_wall_at(tiles.get_tile_location(column - 1, row - 1), True)
    tiles.set_wall_at(tiles.get_tile_location(column, row - 1), True)
    tiles.set_wall_at(tiles.get_tile_location(column + 1, row - 1), True)
    tiles.set_wall_at(tiles.get_tile_location(column - 1, row), True)
    tiles.set_wall_at(tiles.get_tile_location(column, row), True)
    tiles.set_wall_at(tiles.get_tile_location(column + 1, row), True)
    tiles.set_wall_at(tiles.get_tile_location(column - 1, row + 1), True)
    tiles.set_wall_at(tiles.get_tile_location(column + 1, row + 1), True)
def part_1_1():
    global can_skip_dialog, sprite_overlapping, sprite_leader, path
    for index in range(20):
        make_villager(randint(0, 2), True)
    
    def on_background():
        while current_part == "1.1":
            for sprite_villager in sprites.all_of_kind(SpriteKind.Villager):
                if sprites.read_data_string(sprite_villager, "state") == "panicking":
                    continue
                if sprites.read_data_string(sprite_villager, "state") == "idle":
                    if Math.percent_chance(50) and sprites.read_data_boolean(sprite_villager, "do_wandering"):
                        sprites.set_data_string(sprite_villager, "state", "walking")
                        scene.follow_path(sprite_villager,
                            scene.a_star(tiles.location_of_sprite(sprite_villager),
                                tiles.get_tiles_by_type(random_path_tile())._pick_random()),
                            50)
                else:
                    if not (character.matches_rule(sprite_villager, character.rule(Predicate.MOVING))):
                        sprites.set_data_string(sprite_villager, "state", "idle")
                pause(20)
            pause(500)
    timer.background(on_background)
    
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(17, 18))
    sprite_player.x += tiles.tile_width() / 2
    sprite_player.y += tiles.tile_width() / 2
    fade_out(False)
    color.pause_until_fade_done()
    can_skip_dialog = True
    story.print_character_text("What a nice day.", name3)
    story.print_character_text("Arden told me to meet Headmaster in a blue house",
        name3)
    enable_movement(True)
    while True:
        sprite_overlapping = overlapping_sprite_kind(sprite_player, SpriteKind.Thing)
        if sprite_overlapping and abs(sprite_overlapping.bottom - sprite_player.y) < 4:
            if sprites.read_data_boolean(sprite_overlapping, "is_house"):
                enable_movement(False)
                story.print_character_text("*knock knock knock*", name3)
                
                def on_background2():
                    story.sprite_move_to_location(sprite_player,
                        sprite_player.x,
                        sprite_player.y + tiles.tile_width(),
                        80)
                    character.set_character_state(sprite_player,
                        character.rule(Predicate.FACING_UP, Predicate.NOT_MOVING))
                timer.background(on_background2)
                
                if sprites.read_data_boolean(sprite_overlapping, "has_leader"):
                    break
                else:
                    story.print_character_text("No one is home!", "*Muffled voice*")
                enable_movement(True)
                character.clear_character_state(sprite_player)
        pause(100)
    sprite_leader = make_villager(3, False)
    tiles.place_on_tile(sprite_leader,
        tiles.location_in_direction(tiles.location_of_sprite(sprite_player),
            CollisionDirection.TOP))
    story.sprite_move_to_location(sprite_leader,
        sprite_leader.x,
        sprite_leader.y + tiles.tile_width(),
        50)
    character.set_character_state(sprite_leader, character.rule(Predicate.FACING_DOWN))
    pause(1000)
    story.print_character_text("Ah, hello there " + name3 + ". Today's the day. Come on, we have much to discuss. Follow me.",
        "Headmaster")
    path = scene.a_star(tiles.location_of_sprite(sprite_leader),
        tiles.get_tile_location(13, 12))
    pause(500)
    scene.camera_follow_sprite(None)
    character.clear_character_state(sprite_leader)
    scene.follow_path(sprite_leader, path, 50)
    pause(500)
    character.clear_character_state(sprite_player)
    scene.follow_path(sprite_player, path, 50)
    fade_in(True)
    sprite_leader.destroy()
    scene.camera_follow_sprite(sprite_player)
def place_thing(image2: Image, column2: number, row2: number):
    place_floor_thing(image2, column2, row2)
    tiles.set_wall_at(tiles.get_tile_location(column2, row2), True)
def get_relative_ground_tile(column3: number, row3: number):
    for direction in [CollisionDirection.TOP,
        CollisionDirection.RIGHT,
        CollisionDirection.BOTTOM,
        CollisionDirection.LEFT]:
        if tiles.tile_is(tiles.location_in_direction(tiles.get_tile_location(column3, row3), direction),
            assets.tile("""
                grass
            """)):
            return assets.tile("""
                grass
            """)
        elif tiles.tile_is(tiles.location_in_direction(tiles.get_tile_location(column3, row3), direction),
            assets.tile("""
                dark_grass
            """)):
            return assets.tile("""
                dark_grass
            """)
    return assets.tile("""
        grass
    """)

def on_b_pressed():
    global slowing_time
    if can_slow_time:
        if slowing_time:
            slowing_time = False
        elif energy_level > 0:
            slowing_time = True
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def make_serpent(column4: number, row4: number, health: number, size: number):
    global sprite_serpent9, temp_animation, sprite_id, status_bar
    sprite_serpent9 = sprites.create(assets.animation("""
            serpent_slither_right
        """)[0],
        SpriteKind.enemy)
    temp_animation = assets.animation("""
        serpent_slither_left
    """)
    character.loop_frames(sprite_serpent9,
        scale_animation_by(size),
        100,
        character.rule(Predicate.MOVING_LEFT))
    temp_animation = assets.animation("""
        serpent_slither_right
    """)
    character.loop_frames(sprite_serpent9,
        scale_animation_by(size),
        100,
        character.rule(Predicate.MOVING_RIGHT))
    temp_animation = [assets.animation("""
        serpent_slither_left
    """)[0]]
    character.run_frames(sprite_serpent9,
        scale_animation_by(size),
        100,
        character.rule(Predicate.FACING_LEFT))
    temp_animation = [assets.animation("""
        serpent_slither_right
    """)[0]]
    character.run_frames(sprite_serpent9,
        scale_animation_by(size),
        100,
        character.rule(Predicate.FACING_RIGHT))
    tiles.place_on_tile(sprite_serpent9, tiles.get_tile_location(column4, row4))
    sprites.set_data_sprite(sprite_serpent9, "target", sprite_player)
    sprites.set_data_number(sprite_serpent9, "id", sprite_id)
    sprite_id += 1
    sprites.set_data_boolean(sprite_serpent9, "slowed_down", False)
    multilights.add_light_source(sprite_serpent9, 5 * size)
    status_bar = statusbars.create(16 * size, 2 * size, StatusBarKind.enemy_health)
    status_bar.set_color(2, 0, 3)
    status_bar.set_status_bar_flag(StatusBarFlag.SMOOTH_TRANSITION, True)
    status_bar.attach_to_sprite(sprite_serpent9)
    status_bar.value = health
    status_bar.max = health
    status_bar.set_offset_padding(0, 1 * size)
    status_bar.position_direction(CollisionDirection.TOP)
    status_bar.set_flag(SpriteFlag.GHOST, True)
    return sprite_serpent9
def overlapping_sprite_kind(overlap_sprite: Sprite, kind: number):
    for sprite in sprites.all_of_kind(kind):
        if overlap_sprite.overlaps_with(sprite):
            return sprite
    return [][0]

def on_a_pressed():
    if sprite_player and can_fight:
        use_sword()
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def update_and_wait_till_x_serpents_left(left: number):
    while len(sprites.all_of_kind(SpriteKind.enemy)) > left:
        for sprite_serpent in sprites.all_of_kind(SpriteKind.enemy):
            update_serpent(sprite_serpent)
        pause(500)

def on_on_overlap(sprite2, otherSprite):
    sprite2.destroy()
    if not (sprites.read_data_boolean(otherSprite, "attacking")):
        scene.camera_shake(4, 500)
        info.change_life_by(-2)
sprites.on_overlap(SpriteKind.projectile, SpriteKind.player, on_on_overlap)

def on_combos_attach_combo():
    global dark_mode
    color.pause_until_fade_done()
    dark_mode = not (dark_mode)
    save_bool("dark_mode", dark_mode)
    multilights.toggle_lighting(dark_mode)
controller.combos.attach_combo("urdlurdlurdlurdl", on_combos_attach_combo)

def part_1():
    if current_part == "1.1":
        make_part_1_tilemap()
        part_1_1()
        clear_tilemap()
        save_part("1.2")
        pause(1000)
    if current_part == "1.2":
        make_part_1_tilemap()
        part_1_2()
        clear_tilemap()
        save_part("1.3")
        pause(1000)
    if current_part == "1.3":
        make_part_1_tilemap()
        part_1_3()
        clear_tilemap()
        save_part("2.1")
        pause(1000)
# def part_2():
#     if current_part == "2.1":
#         make_part_2_tilemap()
#         part_2_1()
#         clear_tilemap()
#         save_part("2.2")
#         pause(1000)
#     if current_part == "2.2":
#         make_part_2_tilemap()
#         part_2_2()
#         clear_tilemap()
#         save_part("2.3")
#         pause(1000)
#     if current_part == "2.3":
#         make_part_2_tilemap()
#         part_2_3()
#         clear_tilemap()
#         save_part("2.4")
#         pause(1000)
#     if current_part == "2.4":
#         part_2_4()
def make_part_1_tilemap():
    scene.set_background_color(7)
    tiles.set_tilemap(tilemap("""
        level_1
    """))
    for location in tiles.get_tiles_by_type(sprites.castle.rock0):
        tiles.set_wall_at(location, True)
    for location2 in tiles.get_tiles_by_type(sprites.castle.rock1):
        tiles.set_wall_at(location2, True)
    for location3 in tiles.get_tiles_by_type(assets.tile("""
        water
    """)):
        tiles.set_wall_at(location3, True)
    for location4 in tiles.get_tiles_by_type(assets.tile("""
        tree_1
    """)):
        place_thing(assets.image("""
                tree_1
            """),
            tiles.location_xy(location4, tiles.XY.COLUMN),
            tiles.location_xy(location4, tiles.XY.ROW))
        sprite_thing.y += -8
    for location5 in tiles.get_tiles_by_type(assets.tile("""
        tree_2
    """)):
        place_thing(assets.image("""
                tree_2
            """),
            tiles.location_xy(location5, tiles.XY.COLUMN),
            tiles.location_xy(location5, tiles.XY.ROW))
        sprite_thing.y += -8
    for location6 in tiles.get_tiles_by_type(assets.tile("""
        tree_3
    """)):
        place_thing(assets.image("""
                tree_3
            """),
            tiles.location_xy(location6, tiles.XY.COLUMN),
            tiles.location_xy(location6, tiles.XY.ROW))
        sprite_thing.y += -8
    for location7 in tiles.get_tiles_by_type(assets.tile("""
        tree_4
    """)):
        place_thing(assets.image("""
                tree_4
            """),
            tiles.location_xy(location7, tiles.XY.COLUMN),
            tiles.location_xy(location7, tiles.XY.ROW))
        sprite_thing.y += -4
    for location8 in tiles.get_tiles_by_type(assets.tile("""
        tree_4
    """)):
        place_thing(assets.image("""
                tree_4
            """),
            tiles.location_xy(location8, tiles.XY.COLUMN),
            tiles.location_xy(location8, tiles.XY.ROW))
        sprite_thing.y += -4
    for location9 in tiles.get_tiles_by_type(assets.tile("""
        flower_1
    """)):
        place_floor_thing(assets.image("""
                flower_1
            """),
            tiles.location_xy(location9, tiles.XY.COLUMN),
            tiles.location_xy(location9, tiles.XY.ROW))
    for location10 in tiles.get_tiles_by_type(assets.tile("""
        flower_2
    """)):
        place_floor_thing(assets.image("""
                flower_2
            """),
            tiles.location_xy(location10, tiles.XY.COLUMN),
            tiles.location_xy(location10, tiles.XY.ROW))
    for location11 in tiles.get_tiles_by_type(assets.tile("""
        mushroom_1
    """)):
        place_floor_thing(assets.image("""
                mushroom_1
            """),
            tiles.location_xy(location11, tiles.XY.COLUMN),
            tiles.location_xy(location11, tiles.XY.ROW))
    for location12 in tiles.get_tiles_by_type(assets.tile("""
        stump_1
    """)):
        place_thing(assets.image("""
                stump_1
            """),
            tiles.location_xy(location12, tiles.XY.COLUMN),
            tiles.location_xy(location12, tiles.XY.ROW))
    for location13 in tiles.get_tiles_by_type(assets.tile("""
        house_1
    """)):
        place_thing(assets.image("""
                house_1
            """),
            tiles.location_xy(location13, tiles.XY.COLUMN),
            tiles.location_xy(location13, tiles.XY.ROW))
        house_walls_around(tiles.location_xy(location13, tiles.XY.COLUMN),
            tiles.location_xy(location13, tiles.XY.ROW))
        multilights.add_light_source(sprite_thing, 15)
        sprites.set_data_boolean(sprite_thing, "is_house", True)
        sprite_thing.set_flag(SpriteFlag.GHOST_THROUGH_SPRITES, False)
    for location14 in tiles.get_tiles_by_type(assets.tile("""
        house_2
    """)):
        place_thing(assets.image("""
                house_2
            """),
            tiles.location_xy(location14, tiles.XY.COLUMN),
            tiles.location_xy(location14, tiles.XY.ROW))
        house_walls_around(tiles.location_xy(location14, tiles.XY.COLUMN),
            tiles.location_xy(location14, tiles.XY.ROW))
        multilights.add_light_source(sprite_thing, 15)
        sprites.set_data_boolean(sprite_thing, "is_house", True)
        sprite_thing.set_flag(SpriteFlag.GHOST_THROUGH_SPRITES, False)
    sprites.set_data_boolean(sprite_thing, "has_leader", True)

def on_overlap_tile(sprite3, location15):
    tiles.set_tile_at(location15, assets.tile("""
        darkness
    """))
    
    def on_after():
        tiles.set_tile_at(location15, sprites.dungeon.floor_light1)
    timer.after(2000, on_after)
    
scene.on_overlap_tile(SpriteKind.Darkness,
    sprites.dungeon.floor_light1,
    on_overlap_tile)

def fade_out(block: bool):
    color.start_fade(color.black, color.original_palette, 2000)
    if block:
        color.pause_until_fade_done()
def read_bool(name: str):
    return blockSettings.read_number(name) == 1
def update_serpents_for_x_ms(ms: number):
    global start_time
    start_time = game.runtime()
    while game.runtime() - start_time < ms:
        for sprite_serpent2 in sprites.all_of_kind(SpriteKind.enemy):
            update_serpent(sprite_serpent2)
        pause(500)
def fade_in(block2: bool):
    color.start_fade(color.original_palette, color.black, 2000)
    if block2:
        color.pause_until_fade_done()
def place_floor_thing(image22: Image, column5: number, row5: number):
    global sprite_thing
    sprite_thing = sprites.create(image22, SpriteKind.Thing)
    sprite_thing.set_flag(SpriteFlag.GHOST, True)
    tiles.place_on_tile(sprite_thing, tiles.get_tile_location(column5, row5))
    tiles.set_tile_at(tiles.get_tile_location(column5, row5),
        get_relative_ground_tile(column5, row5))
    sprites.set_data_boolean(sprite_thing, "is_house", False)
    sprites.set_data_boolean(sprite_thing, "has_leader", False)
def make_villager(picture_index: number, do_wandering: bool):
    global villager_down_animations, villager_up_animations, villager_right_animations, villager_left_animations, sprite_villager2
    villager_down_animations = [assets.animation("""
            villager_1_walk_down
        """),
        assets.animation("""
            villager_2_walk_down
        """),
        assets.animation("""
            villager_3_walk_down
        """),
        assets.animation("""
            village_leader_walk_down
        """)]
    villager_up_animations = [assets.animation("""
            villager_1_walk_up
        """),
        assets.animation("""
            villager_2_walk_up
        """),
        assets.animation("""
            villager_3_walk_up
        """),
        assets.animation("""
            villager_leader_walk_up
        """)]
    villager_right_animations = [assets.animation("""
            villager_1_walk_right
        """),
        assets.animation("""
            villager_2_walk_right
        """),
        assets.animation("""
            villager_3_walk_right
        """),
        assets.animation("""
            villager_leader_walk_right
        """)]
    villager_left_animations = [assets.animation("""
            villager_1_walk_left
        """),
        assets.animation("""
            villager_2_walk_left
        """),
        assets.animation("""
            villager_3_walk_left
        """),
        assets.animation("""
            village_leader_walk_left
        """)]
    sprite_villager2 = sprites.create(villager_down_animations[picture_index][0],
        SpriteKind.Villager)
    character.loop_frames(sprite_villager2,
        villager_up_animations[picture_index],
        100,
        character.rule(Predicate.MOVING_UP))
    character.loop_frames(sprite_villager2,
        villager_right_animations[picture_index],
        100,
        character.rule(Predicate.MOVING_RIGHT))
    character.loop_frames(sprite_villager2,
        villager_down_animations[picture_index],
        100,
        character.rule(Predicate.MOVING_DOWN))
    character.loop_frames(sprite_villager2,
        villager_left_animations[picture_index],
        100,
        character.rule(Predicate.MOVING_LEFT))
    character.run_frames(sprite_villager2,
        [villager_up_animations[picture_index][0]],
        100,
        character.rule(Predicate.FACING_UP))
    character.run_frames(sprite_villager2,
        [villager_right_animations[picture_index][0]],
        100,
        character.rule(Predicate.FACING_RIGHT))
    character.run_frames(sprite_villager2,
        [villager_down_animations[picture_index][0]],
        100,
        character.rule(Predicate.FACING_DOWN))
    character.run_frames(sprite_villager2,
        [villager_left_animations[picture_index][0]],
        100,
        character.rule(Predicate.FACING_LEFT))
    character.set_character_animations_enabled(sprite_villager2, True)
    sprites.set_data_string(sprite_villager2, "state", "idle")
    sprites.set_data_boolean(sprite_villager2, "do_wandering", do_wandering)
    sprites.set_data_boolean(sprite_villager2, "slowed_down", False)
    tiles.place_on_random_tile(sprite_villager2, random_path_tile())
    multilights.add_light_source(sprite_villager2, 5)
    return sprite_villager2
def part_2_1():
    global can_fight, can_slow_time, energy_level
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(79, 14))
    sprite_player.set_velocity(0, 0)
    scene.follow_path(sprite_player,
        scene.a_star(tiles.get_tile_location(0, 0), tiles.get_tile_location(0, 0)),
        0)
    sprite_player.set_flag(SpriteFlag.GHOST, False)
    scene.camera_follow_sprite(sprite_player)
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    fade_out(True)
    story.print_character_text("Oh no where did they go?", name3)
    story.print_character_text("Ah ha I see you over there!", name3)
    enable_movement(True)
    character.clear_character_state(sprite_player)
    can_fight = True
    can_slow_time = True
    energy_level = 100
    make_serpent(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) - (scene.screen_width() / tiles.tile_width() + 2),
        tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW),
        4,
        1)
    update_and_wait_till_x_serpents_left(0)
    pause(1000)
    make_serpent(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) - (scene.screen_width() / tiles.tile_width() + 2),
        Math.constrain(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW) - 1,
            0,
            tiles.tilemap_rows() - 1),
        4,
        1)
    make_serpent(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) - (scene.screen_width() / tiles.tile_width() + 2),
        Math.constrain(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW) + 1,
            0,
            tiles.tilemap_rows() - 1),
        4,
        1)
    update_and_wait_till_x_serpents_left(0)
    while tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) > 50:
        make_serpent(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) - (scene.screen_width() / tiles.tile_width() + 2),
            Math.constrain(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW) - 1,
                0,
                tiles.tilemap_rows() - 1),
            4,
            1)
        make_serpent(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN) - (scene.screen_width() / tiles.tile_width() + 2),
            Math.constrain(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW) + 1,
                0,
                tiles.tilemap_rows() - 1),
            4,
            1)
        update_and_wait_till_x_serpents_left(0)
    enable_movement(False)
    can_fight = False
    can_slow_time = False
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    story.print_character_text("Wow, this place is HUGE!", name3)
    character.clear_character_state(sprite_player)
    scene.follow_path(sprite_player,
        scene.a_star(tiles.location_of_sprite(sprite_player),
            tiles.get_tile_location(17, 14)),
        50)
    fade_in(True)
def update_serpent(serpent: Sprite):
    global path
    if not (spriteutils.is_destroyed(sprites.read_data_sprite(serpent, "target"))):
        if spriteutils.distance_between(serpent, sprites.read_data_sprite(serpent, "target")) > 8 * tiles.tile_width():
            return
        path = scene.a_star(tiles.location_of_sprite(serpent),
            tiles.location_of_sprite(sprites.read_data_sprite(serpent, "target")))
        if path:
            if slowing_time:
                scene.follow_path(serpent, path, 10)
            else:
                scene.follow_path(serpent, path, 50)
        else:
            serpent.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
            while tiles.tile_is_wall(tiles.location_of_sprite(serpent)):
                if slowing_time:
                    spriteutils.set_velocity_at_angle(serpent,
                        spriteutils.angle_from(serpent, sprites.read_data_sprite(serpent, "target")),
                        10)
                else:
                    spriteutils.set_velocity_at_angle(serpent,
                        spriteutils.angle_from(serpent, sprites.read_data_sprite(serpent, "target")),
                        50)
                pause(100)
            serpent.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, False)
        if spriteutils.distance_between(serpent, sprites.read_data_sprite(serpent, "target")) < 48:
            if character.matches_rule(serpent, character.rule(Predicate.FACING_LEFT)):
                character.set_character_animations_enabled(serpent, False)
                animation.run_image_animation(serpent,
                    assets.animation("""
                        serpent_attack_left
                    """),
                    100,
                    False)
            else:
                character.set_character_animations_enabled(serpent, False)
                animation.run_image_animation(serpent,
                    assets.animation("""
                        serpent_attack_right
                    """),
                    100,
                    False)
            shoot_fireball(serpent, sprites.read_data_sprite(serpent, "target"))
            
            def on_after2():
                character.set_character_animations_enabled(serpent, True)
            timer.after(300, on_after2)
            
def part_1_2():
    global sprite_leader, can_skip_dialog
    sprite_leader = make_villager(3, False)
    tiles.place_on_tile(sprite_leader, tiles.get_tile_location(13, 12))
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(14, 12))
    scene.follow_path(sprite_leader,
        scene.a_star(tiles.get_tile_location(0, 0), tiles.get_tile_location(0, 0)),
        0)
    scene.follow_path(sprite_player,
        scene.a_star(tiles.get_tile_location(0, 0), tiles.get_tile_location(0, 0)),
        0)
    character.set_character_state(sprite_leader, character.rule(Predicate.FACING_RIGHT))
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    fade_out(False)
    color.pause_until_fade_done()
    can_skip_dialog = True
    story.print_character_text("" + name3 + ", I've been wanting to tell you this for a long time, but I didn't feel like you were ready for it until now.",
        "Headmaster")
    story.print_character_text("You have the ability to control time.", "Headmaster")
    story.print_character_text("Wait, WHAT? Is this some sort of sick joke you are playing on me???",
        name3)
    story.print_character_text("No. I am serious. You can control time.", "Headmaster")
    story.print_character_text("Alright not really control as you (and I) can only slow it down. But it sounds cooler that way.",
        "Headmaster")
    story.print_character_text("Wait, you have that power too???", name3)
    story.print_character_text("Yes.", "Headmaster")
    story.print_character_text("Wouldn't other people have noticed?", name3)
    story.print_character_text("No, because everything, and I mean EVERYTHING slows down. Even a person's mind would slow down with everything else as well.",
        "Headmaster")
    story.print_character_text("But people who can slow down time, like you - they notice it as well.",
        "Headmaster")
    story.print_character_text("Believe it or not, I was actually young one time. Before I could slow down time and only require a 3 hour nap after. But now, I'm too old to do this stuff.",
        "Headmaster")
    story.print_character_text("If I was to do it, I would pass out for a whole week.",
        "Headmaster")
    story.print_character_text("Then how do I do it? Why did you tell me this?", name3)
    story.print_character_text("I told you this because the Serpents on the other side of the river-",
        "Headmaster")
    story.print_character_text("The SERPENTS?!?!?", name3)
    story.print_character_text("Yes, those snakes. Their leader wants to conquer everything, and this village is no exception. ",
        "Headmaster")
    story.print_character_text("I wanted to warn you before they att-", "Headmaster")
    
    def on_background3():
        Notification.wait_for_notification_finish()
        Notification.notify("Drums play in the distance",
            1,
            assets.image("""
                closed_captioning_icon
            """))
    timer.background(on_background3)
    
    music.set_volume(50)
    for index2 in range(24):
        music.thump.play_until_done()
        music.rest(music.beat(BeatFraction.HALF))
    music.set_volume(20)
    story.print_character_text("Oh no today is the day. They are attacking. Go fend them off. I assume you know how to use a sword? ",
        "Headmaster")
    story.print_character_text("No not reall-", name3)
    story.print_character_text("Then I will see you later. Good luck and hold them off until I get everyone to safety.",
        "Headmaster")
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_RIGHT, Predicate.NOT_MOVING))
    character.clear_character_state(sprite_leader)
    scene.follow_path(sprite_leader,
        scene.a_star(tiles.location_of_sprite(sprite_leader),
            tiles.get_tile_location(28, 26)),
        60)
    
    def on_background4():
        story.print_character_text("Wait no come back!!!", name3)
    timer.background(on_background4)
    
    fade_in(True)
    sprite_leader.destroy()
    character.clear_character_state(sprite_player)
def part_2_2():
    global can_fight, can_slow_time, energy_level
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(37, 14))
    sprite_player.y += tiles.tile_width() / 2
    sprite_player.set_velocity(0, 0)
    scene.follow_path(sprite_player,
        scene.a_star(tiles.get_tile_location(0, 0), tiles.get_tile_location(0, 0)),
        0)
    sprite_player.set_flag(SpriteFlag.GHOST, False)
    scene.camera_follow_sprite(sprite_player)
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    for location16 in [tiles.get_tile_location(36, 10),
        tiles.get_tile_location(36, 19),
        tiles.get_tile_location(2, 2),
        tiles.get_tile_location(2, 27),
        tiles.get_tile_location(10, 10),
        tiles.get_tile_location(10, 19)]:
        make_serpent(tiles.location_xy(location16, tiles.XY.COLUMN),
            tiles.location_xy(location16, tiles.XY.ROW),
            6,
            1)
    enable_movement(True)
    character.clear_character_state(sprite_player)
    fade_out(True)
    can_fight = True
    can_slow_time = True
    energy_level = 100
    update_and_wait_till_x_serpents_left(0)
    while not (within(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.COLUMN),
        18,
        30,
        True) and within(tiles.location_xy(tiles.location_of_sprite(sprite_player), tiles.XY.ROW),
        5,
        24,
        True)):
        pause(100)
    enable_movement(False)
    can_fight = False
    can_slow_time = False
    fade_in(True)

def on_overlap_tile2(sprite4, location17):
    
    def on_throttle():
        scene.camera_shake(4, 250)
        info.change_life_by(-1)
    timer.throttle("damage_from_darkness", 250, on_throttle)
    
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        darkness
    """),
    on_overlap_tile2)

def enable_movement(en: bool):
    if en:
        controller.move_sprite(sprite_player, 80, 80)
    else:
        controller.move_sprite(sprite_player, 0, 0)
def make_character():
    global sprite_player, status_bar
    sprite_player = sprites.create(assets.image("""
        character_front
    """), SpriteKind.player)
    animate_character()
    sprites.set_data_boolean(sprite_player, "attacking", False)
    status_bar = statusbars.create(16, 2, StatusBarKind.energy)
    status_bar.value = energy_level
    status_bar.max = 100
    status_bar.set_color(3, 10, 13)
    status_bar.set_status_bar_flag(StatusBarFlag.SMOOTH_TRANSITION, True)
    status_bar.attach_to_sprite(sprite_player)
    multilights.add_light_source(sprite_player, 10)
    scene.camera_follow_sprite(sprite_player)

def on_overlap_tile3(sprite5, location18):
    tiles.set_tile_at(location18, assets.tile("""
        darkness
    """))
    
    def on_after3():
        tiles.set_tile_at(location18, sprites.dungeon.floor_light0)
    timer.after(2000, on_after3)
    
scene.on_overlap_tile(SpriteKind.Darkness,
    sprites.dungeon.floor_light0,
    on_overlap_tile3)

def on_overlap_tile4(sprite6, location19):
    tiles.set_tile_at(location19, assets.tile("""
        darkness
    """))
    
    def on_after4():
        tiles.set_tile_at(location19, sprites.dungeon.floor_light_moss)
    timer.after(2000, on_after4)
    
scene.on_overlap_tile(SpriteKind.Darkness,
    sprites.dungeon.floor_light_moss,
    on_overlap_tile4)

def use_sword():
    
    def on_throttle2():
        sprites.set_data_boolean(sprite_player, "attacking", True)
        character.set_character_animations_enabled(sprite_player, False)
        if character.matches_rule(sprite_player, character.rule(Predicate.FACING_UP)):
            animation.run_image_animation(sprite_player,
                assets.animation("""
                    character_fight_up
                """),
                100,
                False)
        elif character.matches_rule(sprite_player, character.rule(Predicate.FACING_DOWN)):
            animation.run_image_animation(sprite_player,
                assets.animation("""
                    character_fight_down
                """),
                100,
                False)
        elif character.matches_rule(sprite_player, character.rule(Predicate.FACING_LEFT)):
            sprite_player.x += -4
            animation.run_image_animation(sprite_player,
                assets.animation("""
                    character_fight_left
                """),
                100,
                False)
        elif character.matches_rule(sprite_player, character.rule(Predicate.FACING_RIGHT)):
            animation.run_image_animation(sprite_player,
                assets.animation("""
                    character_fight_right
                """),
                100,
                False)
        else:
            sprites.set_data_boolean(sprite_player, "attacking", False)
            character.set_character_animations_enabled(sprite_player, True)
        
        def on_after5():
            sprites.set_data_boolean(sprite_player, "attacking", False)
            character.set_character_animations_enabled(sprite_player, True)
        timer.after(400, on_after5)
        
    timer.throttle("attack", 400, on_throttle2)
    
def shoot_fireball(_from: Sprite, to: Sprite):
    global sprite_fireball
    sprite_fireball = sprites.create(assets.image("""
        fireball
    """), SpriteKind.projectile)
    sprite_fireball.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
    sprites.set_data_boolean(sprite_fireball, "slowed_down", False)
    sprite_fireball.set_position(_from.x, _from.y)
    spriteutils.set_velocity_at_angle(sprite_fireball, spriteutils.angle_from(_from, to), 100)
    multilights.add_light_source(sprite_fireball, 2)

def on_overlap_tile5(sprite7, location20):
    tiles.set_tile_at(location20, assets.tile("""
        darkness
    """))
    
    def on_after6():
        tiles.set_tile_at(location20, sprites.dungeon.floor_light4)
    timer.after(2000, on_after6)
    
scene.on_overlap_tile(SpriteKind.Darkness,
    sprites.dungeon.floor_light4,
    on_overlap_tile5)

def on_menu_pressed():
    if can_skip_dialog:
        story.clear_all_text()
controller.menu.on_event(ControllerButtonEvent.PRESSED, on_menu_pressed)

def within(x: number, minimum: number, maximum: number, inclusive: bool):
    if inclusive:
        return x <= maximum and x >= minimum
    else:
        return x < maximum and x > minimum

def on_life_zero():
    
    def on_throttle3():
        
        def on_background5():
            sprite_player.destroy(effects.disintegrate, 100)
            fade_in(True)
            game.reset()
        timer.background(on_background5)
        
    timer.throttle("die", 3000, on_throttle3)
    
info.on_life_zero(on_life_zero)

def clear_tilemap():
    for kind2 in [SpriteKind.projectile,
        SpriteKind.food,
        SpriteKind.enemy,
        SpriteKind.Thing,
        SpriteKind.Villager]:
        for sprite8 in sprites.all_of_kind(kind2):
            sprite8.destroy()
def camera_glide_to(_from2: Sprite, to2: Sprite, speed: number):
    global sprite_camera
    if not (sprite_camera):
        sprite_camera = sprites.create(img("""
                . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . . 
                            . . . . . . . . . . . . . . . .
            """),
            SpriteKind.player)
    sprite_camera.set_position(_from2.x, _from2.y)
    sprite_camera.set_flag(SpriteFlag.GHOST, True)
    scene.camera_follow_sprite(sprite_camera)
    story.sprite_move_to_location(sprite_camera, to2.x, to2.y, speed)
    if sprite_camera:
        sprite_camera.destroy()
def save_part(part: str):
    global current_part
    current_part = part
    blockSettings.write_string("part", current_part)
    
    def on_after7():
        
        def on_background6():
            Notification.wait_for_notification_finish()
            Notification.notify("Your progress has been saved!",
                1,
                assets.image("""
                    floppy_disc
                """))
        timer.background(on_background6)
        
    timer.after(4000, on_after7)
    
def save_bool(name2: str, value: bool):
    if value:
        blockSettings.write_number(name2, 1)
    else:
        blockSettings.write_number(name2, 0)
# def part_2_4():
#     global can_fight, can_slow_time, sprite_end_screen
#     enable_movement(False)
#     can_fight = False
#     can_slow_time = False
#     sprite_end_screen = sprites.create(assets.image("""
#         part_2_end_1
#     """), SpriteKind.Title)
#     sprite_end_screen.top = 0
#     sprite_end_screen.left = 0
#     sprite_end_screen.z = 100
#     sprite_end_screen.set_flag(SpriteFlag.RELATIVE_TO_CAMERA, True)
#     sprite_end_screen.set_flag(SpriteFlag.GHOST, True)
#     fade_out(True)
#     while True:
#         for image23 in [assets.image("""
#                 part_2_end_2
#             """),
#             assets.image("""
#                 part_2_end_3
#             """),
#             assets.image("""
#                 part_2_end_1
#             """)]:
#             pause(5000)
#             if Math.percent_chance(3):
#                 imagemorph.morph(sprite_end_screen,
#                     assets.image("""
#                         part_2_end_easter_egg
#                     """))
#                 pause(5000)
#             imagemorph.morph(sprite_end_screen, image23)
def scale_animation_by(size2: number):
    global temp_array
    temp_array = []
    for frame in temp_animation:
        if size2 == 0.5:
            temp_array.append(scaling.scale_half_x(frame))
        elif size2 == 2:
            temp_array.append(scaling.scale2x(frame))
        elif size2 == 3:
            temp_array.append(scaling.scale3x(frame))
        else:
            temp_array.append(frame.clone())
    return temp_array

def on_overlap_tile6(sprite9, location21):
    tiles.set_tile_at(location21, assets.tile("""
        darkness
    """))
    
    def on_after8():
        tiles.set_tile_at(location21, sprites.dungeon.floor_light_moss)
    timer.after(2000, on_after8)
    
scene.on_overlap_tile(SpriteKind.Darkness,
    sprites.dungeon.floor_light3,
    on_overlap_tile6)

def animate_character():
    character.loop_frames(sprite_player,
        assets.animation("""
            character_walk_up
        """),
        100,
        character.rule(Predicate.MOVING_UP))
    character.loop_frames(sprite_player,
        assets.animation("""
            character_walk_right
        """),
        100,
        character.rule(Predicate.MOVING_RIGHT))
    character.loop_frames(sprite_player,
        assets.animation("""
            character_walk_down
        """),
        100,
        character.rule(Predicate.MOVING_DOWN))
    character.loop_frames(sprite_player,
        assets.animation("""
            character_walk_left
        """),
        100,
        character.rule(Predicate.MOVING_LEFT))
    character.run_frames(sprite_player,
        assets.animation("""
            character_up
        """),
        100,
        character.rule(Predicate.NOT_MOVING, Predicate.FACING_UP))
    character.run_frames(sprite_player,
        assets.animation("""
            character_right
        """),
        100,
        character.rule(Predicate.NOT_MOVING, Predicate.FACING_RIGHT))
    character.run_frames(sprite_player,
        assets.animation("""
            character_down
        """),
        100,
        character.rule(Predicate.NOT_MOVING, Predicate.FACING_DOWN))
    character.run_frames(sprite_player,
        assets.animation("""
            character_left
        """),
        100,
        character.rule(Predicate.NOT_MOVING, Predicate.FACING_LEFT))
def part_2_3():
    global sprite_boss, slowing_time, can_fight, can_slow_time, energy_level
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(19, 14))
    sprite_player.y += tiles.tile_width() / 2
    sprite_player.set_velocity(0, 0)
    scene.follow_path(sprite_player,
        scene.a_star(tiles.get_tile_location(0, 0), tiles.get_tile_location(0, 0)),
        0)
    sprite_player.set_flag(SpriteFlag.GHOST, False)
    scene.camera_follow_sprite(sprite_player)
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_RIGHT, Predicate.NOT_MOVING))
    character.clear_character_state(sprite_player)
    sprite_boss = make_serpent(28, 14, 50, 3)
    sprite_boss.y += tiles.tile_width() / 2
    fade_out(True)
    pause(1000)
    for index3 in range(6):
        tiles.set_tile_at(tiles.get_tile_location(17, 12 + index3),
            sprites.dungeon.green_outer_west0)
        tiles.set_wall_at(tiles.get_tile_location(17, 12 + index3), True)
        pause(500)
    pause(1000)
    story.sprite_move_to_location(sprite_boss,
        sprite_player.x + 3 * tiles.tile_width(),
        sprite_player.y,
        50)
    pause(1000)
    story.print_character_text("Hello there " + name3 + ", I've been waiting for you...",
        "The Snake Emperor")
    story.print_character_text("What do you want?", name3)
    story.print_character_text("I just need you, uh what do they say instead of killing? I just need you severely incapacitated so you don't get in the way of my world domination plans.",
        "The Snake Emperor")
    story.print_character_text("I've gotten maybe at least 90% of the world. What are the exact numbers again?",
        "The Snake Emperor")
    story.print_character_text("97.89%!", "*Voice in the distance*")
    story.print_character_text("Yea, whatever he said. I think you are the last village, but since I've conquered so many at this point I don't remember. ",
        "The Snake Emperor")
    story.print_character_text("Anyways, I just need you out of the way.",
        "The Snake Emperor")
    story.print_character_text("But what if I kill you right here?", name3)
    story.print_character_text("...", "The Snake Emperor")
    story.print_character_text("HAHA you are funny hero. Not like you could. I'm 3x bigger than you!",
        "The Snake Emperor")
    story.print_character_text("But if I'm dead then well, this whole empire collapses and all my hard work gets unwound. ",
        "The Snake Emperor")
    story.print_character_text("All the villages would be freed and there wouldn't be any unity amongst everyone!",
        "The Snake Emperor")
    story.print_character_text("And then it would be a pain in the butt to resurrect myself because it would take a couple years before I can come back.",
        "The Snake Emperor")
    story.print_character_text("Anyways let me just quickly throw some fireballs - you are in my way and I have a meeting with my advisors-",
        "The Snake Emperor")
    story.print_character_text("They are all dead!", "*Voice in the distance*")
    story.print_character_text("Dang, you are a pesky little hero. Stand still!",
        "The Snake Emperor")
    story.sprite_move_to_location(sprite_boss,
        sprite_player.x + 6 * tiles.tile_width(),
        sprite_player.y,
        50)
    story.sprite_move_to_location(sprite_boss,
        sprite_player.x + 5 * tiles.tile_width(),
        sprite_player.y,
        50)
    character.set_character_state(sprite_boss,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    for index4 in range(3):
        shoot_fireball(sprite_boss, sprite_player)
        pause(100)
        slowing_time = True
    story.sprite_move_to_location(sprite_player,
        sprite_player.x,
        sprite_player.y + 2 * tiles.tile_width(),
        50)
    slowing_time = False
    pause(1000)
    story.print_character_text("Oh, so you are gonna play that game huh?",
        "The Snake Emperor")
    story.print_character_text("ALRIGHT THEN FIGHT ME! DON'T BE A COWARD!", name3)
    story.print_character_text("ALRIGHT NOW I'M AAANNNGGGRRRYYY!!!", "The Snake Emperor")
    character.clear_character_state(sprite_boss)
    story.sprite_move_to_location(sprite_boss,
        sprite_boss.x + 5 * tiles.tile_width(),
        sprite_boss.y,
        50)
    story.sprite_move_to_location(sprite_boss,
        sprite_boss.x + -1 * tiles.tile_width(),
        sprite_boss.y,
        50)
    story.print_character_text("Also by the way, I'm not affected by your stupid \"time control.\"",
        "The Snake Emperor")
    story.print_character_text("Sadly my stupid fireballs are. I would have them be excluded from the time control but it's too much paperwork.",
        "The Snake Emperor")
    enable_movement(True)
    can_fight = True
    can_slow_time = True
    energy_level = 100
    character.set_character_state(sprite_boss,
        character.rule(Predicate.FACING_LEFT, Predicate.NOT_MOVING))
    story.sprite_move_to_location(sprite_boss,
        sprite_boss.x,
        sprite_boss.y + -5 * tiles.tile_width(),
        50)
    
    def on_background7():
        global sprite_darkness
        while not (spriteutils.is_destroyed(sprite_boss)):
            for index5 in range(3):
                shoot_fireball(sprite_boss, sprite_player)
                pause(100)
            if Math.percent_chance(20):
                sprite_darkness = sprites.create(assets.image("""
                        darkness_image
                    """),
                    SpriteKind.Darkness)
                sprite_darkness.set_position(sprite_boss.x, sprite_boss.y)
                sprite_darkness.set_flag(SpriteFlag.DESTROY_ON_WALL, True)
                sprite_darkness.set_flag(SpriteFlag.INVISIBLE, True)
                sprite_darkness.lifespan = 3000
                spriteutils.set_velocity_at_angle(sprite_darkness,
                    spriteutils.angle_from(sprite_darkness, sprite_player),
                    40)
            pause(2000)
    timer.background(on_background7)
    
    while not (spriteutils.is_destroyed(sprite_boss)):
        for diff in [5, 5, -5, -5]:
            pause(1000)
            if spriteutils.is_destroyed(sprite_boss):
                break
            else:
                story.sprite_move_to_location(sprite_boss,
                    sprite_boss.x,
                    sprite_boss.y + diff * tiles.tile_width(),
                    50)
    enable_movement(False)
    can_fight = False
    can_slow_time = False
    
    def on_background8():
        story.print_character_text("NOOOOOOOOOOOO I WAS SO CLOSE!", "The Snake Emperor")
    timer.background(on_background8)
    
    fade_in(True)
    story.clear_all_text()
def make_part_2_tilemap():
    scene.set_background_color(6)
    tiles.set_tilemap(tilemap("""
        level_2
    """))
    for location22 in tiles.get_tiles_by_type(sprites.castle.rock0):
        tiles.set_wall_at(location22, True)
    for location23 in tiles.get_tiles_by_type(sprites.castle.rock1):
        tiles.set_wall_at(location23, True)
    for location24 in tiles.get_tiles_by_type(sprites.dungeon.hazard_lava0):
        tiles.set_wall_at(location24, True)
    for location25 in tiles.get_tiles_by_type(sprites.dungeon.hazard_lava1):
        tiles.set_wall_at(location25, True)
    for location26 in tiles.get_tiles_by_type(assets.tile("""
        tree_1
    """)):
        place_thing(assets.image("""
                tree_1
            """),
            tiles.location_xy(location26, tiles.XY.COLUMN),
            tiles.location_xy(location26, tiles.XY.ROW))
        sprite_thing.y += -8
    for location27 in tiles.get_tiles_by_type(assets.tile("""
        tree_2
    """)):
        place_thing(assets.image("""
                tree_2
            """),
            tiles.location_xy(location27, tiles.XY.COLUMN),
            tiles.location_xy(location27, tiles.XY.ROW))
        sprite_thing.y += -8
    for location28 in tiles.get_tiles_by_type(assets.tile("""
        tree_3
    """)):
        place_thing(assets.image("""
                tree_3
            """),
            tiles.location_xy(location28, tiles.XY.COLUMN),
            tiles.location_xy(location28, tiles.XY.ROW))
        sprite_thing.y += -8
    for location29 in tiles.get_tiles_by_type(assets.tile("""
        tree_4
    """)):
        place_thing(assets.image("""
                tree_4
            """),
            tiles.location_xy(location29, tiles.XY.COLUMN),
            tiles.location_xy(location29, tiles.XY.ROW))
        sprite_thing.y += -4
    for location30 in tiles.get_tiles_by_type(assets.tile("""
        tree_4
    """)):
        place_thing(assets.image("""
                tree_4
            """),
            tiles.location_xy(location30, tiles.XY.COLUMN),
            tiles.location_xy(location30, tiles.XY.ROW))
        sprite_thing.y += -4
    for location31 in tiles.get_tiles_by_type(assets.tile("""
        flower_1
    """)):
        place_floor_thing(assets.image("""
                flower_1
            """),
            tiles.location_xy(location31, tiles.XY.COLUMN),
            tiles.location_xy(location31, tiles.XY.ROW))
    for location32 in tiles.get_tiles_by_type(assets.tile("""
        flower_2
    """)):
        place_floor_thing(assets.image("""
                flower_2
            """),
            tiles.location_xy(location32, tiles.XY.COLUMN),
            tiles.location_xy(location32, tiles.XY.ROW))
    for location33 in tiles.get_tiles_by_type(assets.tile("""
        mushroom_1
    """)):
        place_floor_thing(assets.image("""
                mushroom_1
            """),
            tiles.location_xy(location33, tiles.XY.COLUMN),
            tiles.location_xy(location33, tiles.XY.ROW))
    for location34 in tiles.get_tiles_by_type(assets.tile("""
        stump_1
    """)):
        place_thing(assets.image("""
                stump_1
            """),
            tiles.location_xy(location34, tiles.XY.COLUMN),
            tiles.location_xy(location34, tiles.XY.ROW))
def part_1_3():
    global can_fight, can_slow_time, slowing_time
    can_fight = True
    tiles.place_on_tile(sprite_player, tiles.get_tile_location(14, 12))
    character.set_character_state(sprite_player,
        character.rule(Predicate.FACING_DOWN, Predicate.NOT_MOVING))
    make_serpent(0, 15, 2, 1)
    make_serpent(0, 16, 2, 1)
    enable_movement(False)
    for sprite_serpent3 in sprites.all_of_kind(SpriteKind.enemy):
        sprite_serpent3.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
        sprite_serpent3.x += tiles.tile_width() * -1.5
    info.set_life(20)
    fade_out(True)
    story.print_character_text("Well that was helpful.", name3)
    story.print_character_text("Oh no they are here.", name3)
    pause(1000)
    camera_glide_to(sprite_player, sprites.all_of_kind(SpriteKind.enemy)[0], 100)
    pause(1000)
    for sprite_serpent4 in sprites.all_of_kind(SpriteKind.enemy):
        
        def on_background9():
            story.sprite_move_to_location(sprite_serpent4,
                sprite_serpent4.x + tiles.tile_width() * 2,
                sprite_serpent4.y,
                50)
        timer.background(on_background9)
        
    pause(1000)
    for sprite_serpent5 in sprites.all_of_kind(SpriteKind.enemy):
        sprite_serpent5.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, False)
    enable_movement(True)
    character.clear_character_state(sprite_player)
    can_fight = True
    can_slow_time = True
    scene.camera_follow_sprite(sprite_player)
    update_and_wait_till_x_serpents_left(0)
    pause(2000)
    for index6 in range(6):
        make_serpent(0, 14, 2, 1)
        make_serpent(0, 17, 2, 1)
        for sprite_serpent6 in sprites.all_of_kind(SpriteKind.enemy):
            sprite_serpent6.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
            sprite_serpent6.x += tiles.tile_width() * -1
        for sprite_serpent7 in sprites.all_of_kind(SpriteKind.enemy):
            
            def on_background10():
                story.sprite_move_to_location(sprite_serpent7,
                    sprite_serpent7.x + (tiles.tile_width() + 8),
                    sprite_serpent7.y,
                    50)
            timer.background(on_background10)
            
        update_serpents_for_x_ms(1000)
        for sprite_serpent8 in sprites.all_of_kind(SpriteKind.enemy):
            sprite_serpent8.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, False)
        update_serpents_for_x_ms(3000)
    update_and_wait_till_x_serpents_left(0)
    enable_movement(False)
    pause(1000)
    
    def on_background11():
        story.print_character_text("Wait no come back I see you over there!", name3)
    timer.background(on_background11)
    
    scene.follow_path(sprite_player,
        scene.a_star(tiles.location_of_sprite(sprite_player),
            tiles.get_tile_location(0, 15)),
        80)
    sprite_player.set_flag(SpriteFlag.GHOST, True)
    while scene.sprite_percent_path_completed(sprite_player) < 100:
        pause(100)
    sprite_player.vx = -80
    can_slow_time = False
    slowing_time = False
    can_fight = False
    scene.camera_follow_sprite(None)
    fade_in(True)
    story.clear_all_text()
def random_path_tile():
    return [sprites.castle.tile_path5,
        sprites.castle.tile_path1,
        sprites.castle.tile_path2,
        sprites.castle.tile_path3,
        sprites.castle.tile_path8,
        sprites.castle.tile_path9,
        sprites.castle.tile_path4,
        sprites.castle.tile_path7,
        sprites.castle.tile_path6]._pick_random()

def on_on_overlap2(sprite10, otherSprite2):
    
    def on_throttle4():
        if sprites.read_data_boolean(sprite10, "attacking"):
            statusbars.get_status_bar_attached_to(StatusBarKind.enemy_health, otherSprite2).value += -1
            if statusbars.get_status_bar_attached_to(StatusBarKind.enemy_health, otherSprite2).value <= 0:
                otherSprite2.destroy(effects.disintegrate, 100)
    timer.throttle("serpent_" + str(sprites.read_data_number(otherSprite2, "id")) + "_take_damage",
        500,
        on_throttle4)
    
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap2)

sprite_darkness: Sprite = None
sprite_boss: Sprite = None
temp_array: List[Image] = []
sprite_end_screen: Sprite = None
sprite_camera: Sprite = None
sprite_fireball: Sprite = None
sprite_villager2: Sprite = None
villager_left_animations: List[List[Image]] = []
villager_right_animations: List[List[Image]] = []
villager_up_animations: List[List[Image]] = []
villager_down_animations: List[List[Image]] = []
start_time = 0
sprite_thing: Sprite = None
status_bar: StatusBarSprite = None
temp_animation: List[Image] = []
sprite_serpent9: Sprite = None
path: List[tiles.Location] = []
sprite_leader: Sprite = None
sprite_overlapping: Sprite = None
sprite_player: Sprite = None
current_part = ""
name3 = ""
sprite_id = 0
energy_level = 0
dark_mode = False
slowing_time = False
can_slow_time = False
can_fight = False
can_skip_dialog = False
color.set_palette(color.white)
can_skip_dialog = False
can_fight = False
can_slow_time = False
slowing_time = False
if not (blockSettings.exists("dark_mode")):
    save_bool("dark_mode", False)
dark_mode = read_bool("dark_mode")
multilights.toggle_lighting(dark_mode)
energy_level = 100
sprite_id = 0
pause(100)
if controller.B.is_pressed():
    scene.set_background_color(12)
    fade_out(False)
    story.show_player_choices("Reset everything!", "No keep my data!")
    if story.get_last_answer().includes("Reset"):
        blockSettings.clear()
        story.print_character_text("Reset successful.")
        fade_in(True)
        game.reset()
    else:
        story.print_character_text("No reset was performed.")
        fade_in(True)
if not (blockSettings.exists("name")):
    scene.set_background_color(12)
    fade_out(True)
    game.splash("Evan Zeng", "Protect Fox Meadow School!")
    #blockSettings.write_string("name", game.ask_for_string("Please input a name: ", 24))
    fade_in(True)
info.set_life(20)
#name3 = blockSettings.read_string("name")
name3 = "Evan"
if not (blockSettings.exists("part")):
    blockSettings.write_string("part", "1.1")
current_part = blockSettings.read_string("part")
can_skip_dialog = True
make_character()
tiles.place_on_tile(sprite_player, tiles.get_tile_location(17, 18))
sprite_player.y += tiles.tile_width() / 2
sprite_player.x += tiles.tile_width() / 2

def on_background12():
    pause(100)
    if current_part.char_at(0) == "1":
        part_1()
    #part_2()
timer.background(on_background12)

def on_on_update():
    for kind3 in [SpriteKind.projectile,
        SpriteKind.enemy,
        SpriteKind.Thing,
        SpriteKind.Villager]:
        for sprite11 in sprites.all_of_kind(kind3):
            sprite11.z = sprite11.bottom / 100
    for sprite12 in sprites.all_of_kind(SpriteKind.player):
        sprite12.z = (sprite12.bottom - 8) / 100
game.on_update(on_on_update)

def on_forever():
    for kind4 in [SpriteKind.enemy, SpriteKind.projectile, SpriteKind.Villager]:
        for sprite13 in sprites.all_of_kind(kind4):
            if sprites.read_data_boolean(sprite13, "slowed_down"):
                if not (slowing_time):
                    sprites.set_data_boolean(sprite13, "slowed_down", False)
                    sprite13.vx = sprite13.vx * 5
                    sprite13.vy = sprite13.vy * 5
            else:
                if slowing_time:
                    sprites.set_data_boolean(sprite13, "slowed_down", True)
                    sprite13.vx = sprite13.vx * 0.2
                    sprite13.vy = sprite13.vy * 0.2
    pause(100)
forever(on_forever)

def on_update_interval():
    if info.life() < 20 and info.life() > 0:
        if Math.percent_chance(5):
            info.change_life_by(1)
game.on_update_interval(100, on_update_interval)

def on_update_interval2():
    global energy_level, slowing_time, status_bar
    if slowing_time:
        energy_level += -1
        if energy_level <= 0:
            slowing_time = False
    else:
        if energy_level < 100 and Math.percent_chance(10):
            energy_level += 1
    if sprite_player:
        status_bar = statusbars.get_status_bar_attached_to(StatusBarKind.energy, sprite_player)
        if status_bar:
            status_bar.set_flag(SpriteFlag.INVISIBLE, not (can_slow_time))
            status_bar.value = energy_level
game.on_update_interval(200, on_update_interval2)
