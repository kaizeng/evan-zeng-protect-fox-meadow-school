namespace SpriteKind {
    export const Thing = SpriteKind.create()
    export const Villager = SpriteKind.create()
    export const Title = SpriteKind.create()
    export const Darkness = SpriteKind.create()
}

function house_walls_around(column: number, row: number) {
    tiles.setWallAt(tiles.getTileLocation(column - 1, row - 1), true)
    tiles.setWallAt(tiles.getTileLocation(column, row - 1), true)
    tiles.setWallAt(tiles.getTileLocation(column + 1, row - 1), true)
    tiles.setWallAt(tiles.getTileLocation(column - 1, row), true)
    tiles.setWallAt(tiles.getTileLocation(column, row), true)
    tiles.setWallAt(tiles.getTileLocation(column + 1, row), true)
    tiles.setWallAt(tiles.getTileLocation(column - 1, row + 1), true)
    tiles.setWallAt(tiles.getTileLocation(column + 1, row + 1), true)
}

function part_1_1() {
    
    for (let index = 0; index < 20; index++) {
        make_villager(randint(0, 2), true)
    }
    timer.background(function on_background() {
        while (current_part == "1.1") {
            for (let sprite_villager of sprites.allOfKind(SpriteKind.Villager)) {
                if (sprites.readDataString(sprite_villager, "state") == "panicking") {
                    continue
                }
                
                if (sprites.readDataString(sprite_villager, "state") == "idle") {
                    if (Math.percentChance(50) && sprites.readDataBoolean(sprite_villager, "do_wandering")) {
                        sprites.setDataString(sprite_villager, "state", "walking")
                        scene.followPath(sprite_villager, scene.aStar(tiles.locationOfSprite(sprite_villager), tiles.getTilesByType(random_path_tile())._pickRandom()), 50)
                    }
                    
                } else if (!character.matchesRule(sprite_villager, character.rule(Predicate.Moving))) {
                    sprites.setDataString(sprite_villager, "state", "idle")
                }
                
                pause(20)
            }
            pause(500)
        }
    })
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(17, 18))
    sprite_player.x += tiles.tileWidth() / 2
    sprite_player.y += tiles.tileWidth() / 2
    fade_out(false)
    color.pauseUntilFadeDone()
    can_skip_dialog = true
    story.printCharacterText("What a nice day.", name3)
    story.printCharacterText("Arden told me to meet Headmaster in a blue house", name3)
    enable_movement(true)
    while (true) {
        sprite_overlapping = overlapping_sprite_kind(sprite_player, SpriteKind.Thing)
        if (sprite_overlapping && Math.abs(sprite_overlapping.bottom - sprite_player.y) < 4) {
            if (sprites.readDataBoolean(sprite_overlapping, "is_house")) {
                enable_movement(false)
                story.printCharacterText("*knock knock knock*", name3)
                timer.background(function on_background2() {
                    story.spriteMoveToLocation(sprite_player, sprite_player.x, sprite_player.y + tiles.tileWidth(), 80)
                    character.setCharacterState(sprite_player, character.rule(Predicate.FacingUp, Predicate.NotMoving))
                })
                if (sprites.readDataBoolean(sprite_overlapping, "has_leader")) {
                    break
                } else {
                    story.printCharacterText("No one is home!", "*Muffled voice*")
                }
                
                enable_movement(true)
                character.clearCharacterState(sprite_player)
            }
            
        }
        
        pause(100)
    }
    sprite_leader = make_villager(3, false)
    tiles.placeOnTile(sprite_leader, tiles.locationInDirection(tiles.locationOfSprite(sprite_player), CollisionDirection.Top))
    story.spriteMoveToLocation(sprite_leader, sprite_leader.x, sprite_leader.y + tiles.tileWidth(), 50)
    character.setCharacterState(sprite_leader, character.rule(Predicate.FacingDown))
    pause(1000)
    story.printCharacterText("Ah, hello there " + name3 + ". Today's the day. Come on, we have much to discuss. Follow me.", "Headmaster")
    path = scene.aStar(tiles.locationOfSprite(sprite_leader), tiles.getTileLocation(13, 12))
    pause(500)
    scene.cameraFollowSprite(null)
    character.clearCharacterState(sprite_leader)
    scene.followPath(sprite_leader, path, 50)
    pause(500)
    character.clearCharacterState(sprite_player)
    scene.followPath(sprite_player, path, 50)
    fade_in(true)
    sprite_leader.destroy()
    scene.cameraFollowSprite(sprite_player)
}

function place_thing(image2: Image, column2: number, row2: number) {
    place_floor_thing(image2, column2, row2)
    tiles.setWallAt(tiles.getTileLocation(column2, row2), true)
}

function get_relative_ground_tile(column3: number, row3: number): Image {
    for (let direction of [CollisionDirection.Top, CollisionDirection.Right, CollisionDirection.Bottom, CollisionDirection.Left]) {
        if (tiles.tileIs(tiles.locationInDirection(tiles.getTileLocation(column3, row3), direction), assets.tile`
                grass
            `)) {
            return assets.tile`
                grass
            `
        } else if (tiles.tileIs(tiles.locationInDirection(tiles.getTileLocation(column3, row3), direction), assets.tile`
                dark_grass
            `)) {
            return assets.tile`
                dark_grass
            `
        }
        
    }
    return assets.tile`
        grass
    `
}

controller.B.onEvent(ControllerButtonEvent.Pressed, function on_b_pressed() {
    
    if (can_slow_time) {
        if (slowing_time) {
            slowing_time = false
        } else if (energy_level > 0) {
            slowing_time = true
        }
        
    }
    
})
function make_serpent(column4: number, row4: number, health: number, size: number): Sprite {
    
    sprite_serpent9 = sprites.create(assets.animation`
            serpent_slither_right
        `[0], SpriteKind.Enemy)
    temp_animation = assets.animation`
        serpent_slither_left
    `
    character.loopFrames(sprite_serpent9, scale_animation_by(size), 100, character.rule(Predicate.MovingLeft))
    temp_animation = assets.animation`
        serpent_slither_right
    `
    character.loopFrames(sprite_serpent9, scale_animation_by(size), 100, character.rule(Predicate.MovingRight))
    temp_animation = [assets.animation`
        serpent_slither_left
    `[0]]
    character.runFrames(sprite_serpent9, scale_animation_by(size), 100, character.rule(Predicate.FacingLeft))
    temp_animation = [assets.animation`
        serpent_slither_right
    `[0]]
    character.runFrames(sprite_serpent9, scale_animation_by(size), 100, character.rule(Predicate.FacingRight))
    tiles.placeOnTile(sprite_serpent9, tiles.getTileLocation(column4, row4))
    sprites.setDataSprite(sprite_serpent9, "target", sprite_player)
    sprites.setDataNumber(sprite_serpent9, "id", sprite_id)
    sprite_id += 1
    sprites.setDataBoolean(sprite_serpent9, "slowed_down", false)
    multilights.addLightSource(sprite_serpent9, 5 * size)
    status_bar = statusbars.create(16 * size, 2 * size, StatusBarKind.EnemyHealth)
    status_bar.setColor(2, 0, 3)
    status_bar.setStatusBarFlag(StatusBarFlag.SmoothTransition, true)
    status_bar.attachToSprite(sprite_serpent9)
    status_bar.value = health
    status_bar.max = health
    status_bar.setOffsetPadding(0, 1 * size)
    status_bar.positionDirection(CollisionDirection.Top)
    status_bar.setFlag(SpriteFlag.Ghost, true)
    return sprite_serpent9
}

function overlapping_sprite_kind(overlap_sprite: Sprite, kind: number): Sprite {
    for (let sprite of sprites.allOfKind(kind)) {
        if (overlap_sprite.overlapsWith(sprite)) {
            return sprite
        }
        
    }
    return [][0]
}

controller.A.onEvent(ControllerButtonEvent.Pressed, function on_a_pressed() {
    if (sprite_player && can_fight) {
        use_sword()
    }
    
})
function update_and_wait_till_x_serpents_left(left: number) {
    while (sprites.allOfKind(SpriteKind.Enemy).length > left) {
        for (let sprite_serpent of sprites.allOfKind(SpriteKind.Enemy)) {
            update_serpent(sprite_serpent)
        }
        pause(500)
    }
}

sprites.onOverlap(SpriteKind.Projectile, SpriteKind.Player, function on_on_overlap(sprite2: Sprite, otherSprite: Sprite) {
    sprite2.destroy()
    if (!sprites.readDataBoolean(otherSprite, "attacking")) {
        scene.cameraShake(4, 500)
        info.changeLifeBy(-2)
    }
    
})
controller.combos.attachCombo("urdlurdlurdlurdl", function on_combos_attach_combo() {
    
    color.pauseUntilFadeDone()
    dark_mode = !dark_mode
    save_bool("dark_mode", dark_mode)
    multilights.toggleLighting(dark_mode)
})
function part_1() {
    if (current_part == "1.1") {
        make_part_1_tilemap()
        part_1_1()
        clear_tilemap()
        save_part("1.2")
        pause(1000)
    }
    
    if (current_part == "1.2") {
        make_part_1_tilemap()
        part_1_2()
        clear_tilemap()
        save_part("1.3")
        pause(1000)
    }
    
    if (current_part == "1.3") {
        make_part_1_tilemap()
        part_1_3()
        clear_tilemap()
        save_part("2.1")
        pause(1000)
    }
    
}

//  def part_2():
//      if current_part == "2.1":
//          make_part_2_tilemap()
//          part_2_1()
//          clear_tilemap()
//          save_part("2.2")
//          pause(1000)
//      if current_part == "2.2":
//          make_part_2_tilemap()
//          part_2_2()
//          clear_tilemap()
//          save_part("2.3")
//          pause(1000)
//      if current_part == "2.3":
//          make_part_2_tilemap()
//          part_2_3()
//          clear_tilemap()
//          save_part("2.4")
//          pause(1000)
//      if current_part == "2.4":
//          part_2_4()
function make_part_1_tilemap() {
    scene.setBackgroundColor(7)
    tiles.setTilemap(tilemap`
        level_1
    `)
    for (let location of tiles.getTilesByType(sprites.castle.rock0)) {
        tiles.setWallAt(location, true)
    }
    for (let location2 of tiles.getTilesByType(sprites.castle.rock1)) {
        tiles.setWallAt(location2, true)
    }
    for (let location3 of tiles.getTilesByType(assets.tile`
        water
    `)) {
        tiles.setWallAt(location3, true)
    }
    for (let location4 of tiles.getTilesByType(assets.tile`
        tree_1
    `)) {
        place_thing(assets.image`
                tree_1
            `, tiles.locationXY(location4, tiles.XY.column), tiles.locationXY(location4, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location5 of tiles.getTilesByType(assets.tile`
        tree_2
    `)) {
        place_thing(assets.image`
                tree_2
            `, tiles.locationXY(location5, tiles.XY.column), tiles.locationXY(location5, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location6 of tiles.getTilesByType(assets.tile`
        tree_3
    `)) {
        place_thing(assets.image`
                tree_3
            `, tiles.locationXY(location6, tiles.XY.column), tiles.locationXY(location6, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location7 of tiles.getTilesByType(assets.tile`
        tree_4
    `)) {
        place_thing(assets.image`
                tree_4
            `, tiles.locationXY(location7, tiles.XY.column), tiles.locationXY(location7, tiles.XY.row))
        sprite_thing.y += -4
    }
    for (let location8 of tiles.getTilesByType(assets.tile`
        tree_4
    `)) {
        place_thing(assets.image`
                tree_4
            `, tiles.locationXY(location8, tiles.XY.column), tiles.locationXY(location8, tiles.XY.row))
        sprite_thing.y += -4
    }
    for (let location9 of tiles.getTilesByType(assets.tile`
        flower_1
    `)) {
        place_floor_thing(assets.image`
                flower_1
            `, tiles.locationXY(location9, tiles.XY.column), tiles.locationXY(location9, tiles.XY.row))
    }
    for (let location10 of tiles.getTilesByType(assets.tile`
        flower_2
    `)) {
        place_floor_thing(assets.image`
                flower_2
            `, tiles.locationXY(location10, tiles.XY.column), tiles.locationXY(location10, tiles.XY.row))
    }
    for (let location11 of tiles.getTilesByType(assets.tile`
        mushroom_1
    `)) {
        place_floor_thing(assets.image`
                mushroom_1
            `, tiles.locationXY(location11, tiles.XY.column), tiles.locationXY(location11, tiles.XY.row))
    }
    for (let location12 of tiles.getTilesByType(assets.tile`
        stump_1
    `)) {
        place_thing(assets.image`
                stump_1
            `, tiles.locationXY(location12, tiles.XY.column), tiles.locationXY(location12, tiles.XY.row))
    }
    for (let location13 of tiles.getTilesByType(assets.tile`
        house_1
    `)) {
        place_thing(assets.image`
                house_1
            `, tiles.locationXY(location13, tiles.XY.column), tiles.locationXY(location13, tiles.XY.row))
        house_walls_around(tiles.locationXY(location13, tiles.XY.column), tiles.locationXY(location13, tiles.XY.row))
        multilights.addLightSource(sprite_thing, 15)
        sprites.setDataBoolean(sprite_thing, "is_house", true)
        sprite_thing.setFlag(SpriteFlag.GhostThroughSprites, false)
    }
    for (let location14 of tiles.getTilesByType(assets.tile`
        house_2
    `)) {
        place_thing(assets.image`
                house_2
            `, tiles.locationXY(location14, tiles.XY.column), tiles.locationXY(location14, tiles.XY.row))
        house_walls_around(tiles.locationXY(location14, tiles.XY.column), tiles.locationXY(location14, tiles.XY.row))
        multilights.addLightSource(sprite_thing, 15)
        sprites.setDataBoolean(sprite_thing, "is_house", true)
        sprite_thing.setFlag(SpriteFlag.GhostThroughSprites, false)
    }
    sprites.setDataBoolean(sprite_thing, "has_leader", true)
}

scene.onOverlapTile(SpriteKind.Darkness, sprites.dungeon.floorLight1, function on_overlap_tile(sprite3: Sprite, location15: tiles.Location) {
    tiles.setTileAt(location15, assets.tile`
        darkness
    `)
    timer.after(2000, function on_after() {
        tiles.setTileAt(location15, sprites.dungeon.floorLight1)
    })
})
function fade_out(block: boolean) {
    color.startFade(color.Black, color.originalPalette, 2000)
    if (block) {
        color.pauseUntilFadeDone()
    }
    
}

function read_bool(name: string): boolean {
    return blockSettings.readNumber(name) == 1
}

function update_serpents_for_x_ms(ms: number) {
    
    start_time = game.runtime()
    while (game.runtime() - start_time < ms) {
        for (let sprite_serpent2 of sprites.allOfKind(SpriteKind.Enemy)) {
            update_serpent(sprite_serpent2)
        }
        pause(500)
    }
}

function fade_in(block2: boolean) {
    color.startFade(color.originalPalette, color.Black, 2000)
    if (block2) {
        color.pauseUntilFadeDone()
    }
    
}

function place_floor_thing(image22: Image, column5: number, row5: number) {
    
    sprite_thing = sprites.create(image22, SpriteKind.Thing)
    sprite_thing.setFlag(SpriteFlag.Ghost, true)
    tiles.placeOnTile(sprite_thing, tiles.getTileLocation(column5, row5))
    tiles.setTileAt(tiles.getTileLocation(column5, row5), get_relative_ground_tile(column5, row5))
    sprites.setDataBoolean(sprite_thing, "is_house", false)
    sprites.setDataBoolean(sprite_thing, "has_leader", false)
}

function make_villager(picture_index: number, do_wandering: boolean): Sprite {
    
    villager_down_animations = [assets.animation`
            villager_1_walk_down
        `, assets.animation`
            villager_2_walk_down
        `, assets.animation`
            villager_3_walk_down
        `, assets.animation`
            village_leader_walk_down
        `]
    villager_up_animations = [assets.animation`
            villager_1_walk_up
        `, assets.animation`
            villager_2_walk_up
        `, assets.animation`
            villager_3_walk_up
        `, assets.animation`
            villager_leader_walk_up
        `]
    villager_right_animations = [assets.animation`
            villager_1_walk_right
        `, assets.animation`
            villager_2_walk_right
        `, assets.animation`
            villager_3_walk_right
        `, assets.animation`
            villager_leader_walk_right
        `]
    villager_left_animations = [assets.animation`
            villager_1_walk_left
        `, assets.animation`
            villager_2_walk_left
        `, assets.animation`
            villager_3_walk_left
        `, assets.animation`
            village_leader_walk_left
        `]
    sprite_villager2 = sprites.create(villager_down_animations[picture_index][0], SpriteKind.Villager)
    character.loopFrames(sprite_villager2, villager_up_animations[picture_index], 100, character.rule(Predicate.MovingUp))
    character.loopFrames(sprite_villager2, villager_right_animations[picture_index], 100, character.rule(Predicate.MovingRight))
    character.loopFrames(sprite_villager2, villager_down_animations[picture_index], 100, character.rule(Predicate.MovingDown))
    character.loopFrames(sprite_villager2, villager_left_animations[picture_index], 100, character.rule(Predicate.MovingLeft))
    character.runFrames(sprite_villager2, [villager_up_animations[picture_index][0]], 100, character.rule(Predicate.FacingUp))
    character.runFrames(sprite_villager2, [villager_right_animations[picture_index][0]], 100, character.rule(Predicate.FacingRight))
    character.runFrames(sprite_villager2, [villager_down_animations[picture_index][0]], 100, character.rule(Predicate.FacingDown))
    character.runFrames(sprite_villager2, [villager_left_animations[picture_index][0]], 100, character.rule(Predicate.FacingLeft))
    character.setCharacterAnimationsEnabled(sprite_villager2, true)
    sprites.setDataString(sprite_villager2, "state", "idle")
    sprites.setDataBoolean(sprite_villager2, "do_wandering", do_wandering)
    sprites.setDataBoolean(sprite_villager2, "slowed_down", false)
    tiles.placeOnRandomTile(sprite_villager2, random_path_tile())
    multilights.addLightSource(sprite_villager2, 5)
    return sprite_villager2
}

function part_2_1() {
    
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(79, 14))
    sprite_player.setVelocity(0, 0)
    scene.followPath(sprite_player, scene.aStar(tiles.getTileLocation(0, 0), tiles.getTileLocation(0, 0)), 0)
    sprite_player.setFlag(SpriteFlag.Ghost, false)
    scene.cameraFollowSprite(sprite_player)
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    fade_out(true)
    story.printCharacterText("Oh no where did they go?", name3)
    story.printCharacterText("Ah ha I see you over there!", name3)
    enable_movement(true)
    character.clearCharacterState(sprite_player)
    can_fight = true
    can_slow_time = true
    energy_level = 100
    make_serpent(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) - (scene.screenWidth() / tiles.tileWidth() + 2), tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row), 4, 1)
    update_and_wait_till_x_serpents_left(0)
    pause(1000)
    make_serpent(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) - (scene.screenWidth() / tiles.tileWidth() + 2), Math.constrain(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row) - 1, 0, tiles.tilemapRows() - 1), 4, 1)
    make_serpent(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) - (scene.screenWidth() / tiles.tileWidth() + 2), Math.constrain(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row) + 1, 0, tiles.tilemapRows() - 1), 4, 1)
    update_and_wait_till_x_serpents_left(0)
    while (tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) > 50) {
        make_serpent(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) - (scene.screenWidth() / tiles.tileWidth() + 2), Math.constrain(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row) - 1, 0, tiles.tilemapRows() - 1), 4, 1)
        make_serpent(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column) - (scene.screenWidth() / tiles.tileWidth() + 2), Math.constrain(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row) + 1, 0, tiles.tilemapRows() - 1), 4, 1)
        update_and_wait_till_x_serpents_left(0)
    }
    enable_movement(false)
    can_fight = false
    can_slow_time = false
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    story.printCharacterText("Wow, this place is HUGE!", name3)
    character.clearCharacterState(sprite_player)
    scene.followPath(sprite_player, scene.aStar(tiles.locationOfSprite(sprite_player), tiles.getTileLocation(17, 14)), 50)
    fade_in(true)
}

function update_serpent(serpent: Sprite) {
    
    if (!spriteutils.isDestroyed(sprites.readDataSprite(serpent, "target"))) {
        if (spriteutils.distanceBetween(serpent, sprites.readDataSprite(serpent, "target")) > 8 * tiles.tileWidth()) {
            return
        }
        
        path = scene.aStar(tiles.locationOfSprite(serpent), tiles.locationOfSprite(sprites.readDataSprite(serpent, "target")))
        if (path) {
            if (slowing_time) {
                scene.followPath(serpent, path, 10)
            } else {
                scene.followPath(serpent, path, 50)
            }
            
        } else {
            serpent.setFlag(SpriteFlag.GhostThroughWalls, true)
            while (tiles.tileIsWall(tiles.locationOfSprite(serpent))) {
                if (slowing_time) {
                    spriteutils.setVelocityAtAngle(serpent, spriteutils.angleFrom(serpent, sprites.readDataSprite(serpent, "target")), 10)
                } else {
                    spriteutils.setVelocityAtAngle(serpent, spriteutils.angleFrom(serpent, sprites.readDataSprite(serpent, "target")), 50)
                }
                
                pause(100)
            }
            serpent.setFlag(SpriteFlag.GhostThroughWalls, false)
        }
        
        if (spriteutils.distanceBetween(serpent, sprites.readDataSprite(serpent, "target")) < 48) {
            if (character.matchesRule(serpent, character.rule(Predicate.FacingLeft))) {
                character.setCharacterAnimationsEnabled(serpent, false)
                animation.runImageAnimation(serpent, assets.animation`
                        serpent_attack_left
                    `, 100, false)
            } else {
                character.setCharacterAnimationsEnabled(serpent, false)
                animation.runImageAnimation(serpent, assets.animation`
                        serpent_attack_right
                    `, 100, false)
            }
            
            shoot_fireball(serpent, sprites.readDataSprite(serpent, "target"))
            timer.after(300, function on_after2() {
                character.setCharacterAnimationsEnabled(serpent, true)
            })
        }
        
    }
    
}

function part_1_2() {
    
    sprite_leader = make_villager(3, false)
    tiles.placeOnTile(sprite_leader, tiles.getTileLocation(13, 12))
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(14, 12))
    scene.followPath(sprite_leader, scene.aStar(tiles.getTileLocation(0, 0), tiles.getTileLocation(0, 0)), 0)
    scene.followPath(sprite_player, scene.aStar(tiles.getTileLocation(0, 0), tiles.getTileLocation(0, 0)), 0)
    character.setCharacterState(sprite_leader, character.rule(Predicate.FacingRight))
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    fade_out(false)
    color.pauseUntilFadeDone()
    can_skip_dialog = true
    story.printCharacterText("" + name3 + ", I've been wanting to tell you this for a long time, but I didn't feel like you were ready for it until now.", "Headmaster")
    story.printCharacterText("You have the ability to control time.", "Headmaster")
    story.printCharacterText("Wait, WHAT? Is this some sort of sick joke you are playing on me???", name3)
    story.printCharacterText("No. I am serious. You can control time.", "Headmaster")
    story.printCharacterText("Alright not really control as you (and I) can only slow it down. But it sounds cooler that way.", "Headmaster")
    story.printCharacterText("Wait, you have that power too???", name3)
    story.printCharacterText("Yes.", "Headmaster")
    story.printCharacterText("Wouldn't other people have noticed?", name3)
    story.printCharacterText("No, because everything, and I mean EVERYTHING slows down. Even a person's mind would slow down with everything else as well.", "Headmaster")
    story.printCharacterText("But people who can slow down time, like you - they notice it as well.", "Headmaster")
    story.printCharacterText("Believe it or not, I was actually young one time. Before I could slow down time and only require a 3 hour nap after. But now, I'm too old to do this stuff.", "Headmaster")
    story.printCharacterText("If I was to do it, I would pass out for a whole week.", "Headmaster")
    story.printCharacterText("Then how do I do it? Why did you tell me this?", name3)
    story.printCharacterText("I told you this because the Serpents on the other side of the river-", "Headmaster")
    story.printCharacterText("The SERPENTS?!?!?", name3)
    story.printCharacterText("Yes, those snakes. Their leader wants to conquer everything, and this village is no exception. ", "Headmaster")
    story.printCharacterText("I wanted to warn you before they att-", "Headmaster")
    timer.background(function on_background3() {
        Notification.waitForNotificationFinish()
        Notification.notify("Drums play in the distance", 1, assets.image`
                closed_captioning_icon
            `)
    })
    music.setVolume(50)
    for (let index2 = 0; index2 < 24; index2++) {
        music.thump.playUntilDone()
        music.rest(music.beat(BeatFraction.Half))
    }
    music.setVolume(20)
    story.printCharacterText("Oh no today is the day. They are attacking. Go fend them off. I assume you know how to use a sword? ", "Headmaster")
    story.printCharacterText("No not reall-", name3)
    story.printCharacterText("Then I will see you later. Good luck and hold them off until I get everyone to safety.", "Headmaster")
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingRight, Predicate.NotMoving))
    character.clearCharacterState(sprite_leader)
    scene.followPath(sprite_leader, scene.aStar(tiles.locationOfSprite(sprite_leader), tiles.getTileLocation(28, 26)), 60)
    timer.background(function on_background4() {
        story.printCharacterText("Wait no come back!!!", name3)
    })
    fade_in(true)
    sprite_leader.destroy()
    character.clearCharacterState(sprite_player)
}

function part_2_2() {
    
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(37, 14))
    sprite_player.y += tiles.tileWidth() / 2
    sprite_player.setVelocity(0, 0)
    scene.followPath(sprite_player, scene.aStar(tiles.getTileLocation(0, 0), tiles.getTileLocation(0, 0)), 0)
    sprite_player.setFlag(SpriteFlag.Ghost, false)
    scene.cameraFollowSprite(sprite_player)
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    for (let location16 of [tiles.getTileLocation(36, 10), tiles.getTileLocation(36, 19), tiles.getTileLocation(2, 2), tiles.getTileLocation(2, 27), tiles.getTileLocation(10, 10), tiles.getTileLocation(10, 19)]) {
        make_serpent(tiles.locationXY(location16, tiles.XY.column), tiles.locationXY(location16, tiles.XY.row), 6, 1)
    }
    enable_movement(true)
    character.clearCharacterState(sprite_player)
    fade_out(true)
    can_fight = true
    can_slow_time = true
    energy_level = 100
    update_and_wait_till_x_serpents_left(0)
    while (!(within(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.column), 18, 30, true) && within(tiles.locationXY(tiles.locationOfSprite(sprite_player), tiles.XY.row), 5, 24, true))) {
        pause(100)
    }
    enable_movement(false)
    can_fight = false
    can_slow_time = false
    fade_in(true)
}

scene.onOverlapTile(SpriteKind.Player, assets.tile`
        darkness
    `, function on_overlap_tile2(sprite4: Sprite, location17: tiles.Location) {
    timer.throttle("damage_from_darkness", 250, function on_throttle() {
        scene.cameraShake(4, 250)
        info.changeLifeBy(-1)
    })
})
function enable_movement(en: boolean) {
    if (en) {
        controller.moveSprite(sprite_player, 80, 80)
    } else {
        controller.moveSprite(sprite_player, 0, 0)
    }
    
}

function make_character() {
    
    sprite_player = sprites.create(assets.image`
        character_front
    `, SpriteKind.Player)
    animate_character()
    sprites.setDataBoolean(sprite_player, "attacking", false)
    status_bar = statusbars.create(16, 2, StatusBarKind.Energy)
    status_bar.value = energy_level
    status_bar.max = 100
    status_bar.setColor(3, 10, 13)
    status_bar.setStatusBarFlag(StatusBarFlag.SmoothTransition, true)
    status_bar.attachToSprite(sprite_player)
    multilights.addLightSource(sprite_player, 10)
    scene.cameraFollowSprite(sprite_player)
}

scene.onOverlapTile(SpriteKind.Darkness, sprites.dungeon.floorLight0, function on_overlap_tile3(sprite5: Sprite, location18: tiles.Location) {
    tiles.setTileAt(location18, assets.tile`
        darkness
    `)
    timer.after(2000, function on_after3() {
        tiles.setTileAt(location18, sprites.dungeon.floorLight0)
    })
})
scene.onOverlapTile(SpriteKind.Darkness, sprites.dungeon.floorLightMoss, function on_overlap_tile4(sprite6: Sprite, location19: tiles.Location) {
    tiles.setTileAt(location19, assets.tile`
        darkness
    `)
    timer.after(2000, function on_after4() {
        tiles.setTileAt(location19, sprites.dungeon.floorLightMoss)
    })
})
function use_sword() {
    timer.throttle("attack", 400, function on_throttle2() {
        sprites.setDataBoolean(sprite_player, "attacking", true)
        character.setCharacterAnimationsEnabled(sprite_player, false)
        if (character.matchesRule(sprite_player, character.rule(Predicate.FacingUp))) {
            animation.runImageAnimation(sprite_player, assets.animation`
                    character_fight_up
                `, 100, false)
        } else if (character.matchesRule(sprite_player, character.rule(Predicate.FacingDown))) {
            animation.runImageAnimation(sprite_player, assets.animation`
                    character_fight_down
                `, 100, false)
        } else if (character.matchesRule(sprite_player, character.rule(Predicate.FacingLeft))) {
            sprite_player.x += -4
            animation.runImageAnimation(sprite_player, assets.animation`
                    character_fight_left
                `, 100, false)
        } else if (character.matchesRule(sprite_player, character.rule(Predicate.FacingRight))) {
            animation.runImageAnimation(sprite_player, assets.animation`
                    character_fight_right
                `, 100, false)
        } else {
            sprites.setDataBoolean(sprite_player, "attacking", false)
            character.setCharacterAnimationsEnabled(sprite_player, true)
        }
        
        timer.after(400, function on_after5() {
            sprites.setDataBoolean(sprite_player, "attacking", false)
            character.setCharacterAnimationsEnabled(sprite_player, true)
        })
    })
}

function shoot_fireball(_from: Sprite, to: Sprite) {
    
    sprite_fireball = sprites.create(assets.image`
        fireball
    `, SpriteKind.Projectile)
    sprite_fireball.setFlag(SpriteFlag.DestroyOnWall, true)
    sprites.setDataBoolean(sprite_fireball, "slowed_down", false)
    sprite_fireball.setPosition(_from.x, _from.y)
    spriteutils.setVelocityAtAngle(sprite_fireball, spriteutils.angleFrom(_from, to), 100)
    multilights.addLightSource(sprite_fireball, 2)
}

scene.onOverlapTile(SpriteKind.Darkness, sprites.dungeon.floorLight4, function on_overlap_tile5(sprite7: Sprite, location20: tiles.Location) {
    tiles.setTileAt(location20, assets.tile`
        darkness
    `)
    timer.after(2000, function on_after6() {
        tiles.setTileAt(location20, sprites.dungeon.floorLight4)
    })
})
controller.menu.onEvent(ControllerButtonEvent.Pressed, function on_menu_pressed() {
    if (can_skip_dialog) {
        story.clearAllText()
    }
    
})
function within(x: number, minimum: number, maximum: number, inclusive: boolean) {
    if (inclusive) {
        return x <= maximum && x >= minimum
    } else {
        return x < maximum && x > minimum
    }
    
}

info.onLifeZero(function on_life_zero() {
    timer.throttle("die", 3000, function on_throttle3() {
        timer.background(function on_background5() {
            sprite_player.destroy(effects.disintegrate, 100)
            fade_in(true)
            game.reset()
        })
    })
})
function clear_tilemap() {
    for (let kind2 of [SpriteKind.Projectile, SpriteKind.Food, SpriteKind.Enemy, SpriteKind.Thing, SpriteKind.Villager]) {
        for (let sprite8 of sprites.allOfKind(kind2)) {
            sprite8.destroy()
        }
    }
}

function camera_glide_to(_from2: Sprite, to2: Sprite, speed: number) {
    
    if (!sprite_camera) {
        sprite_camera = sprites.create(img`
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
            `, SpriteKind.Player)
    }
    
    sprite_camera.setPosition(_from2.x, _from2.y)
    sprite_camera.setFlag(SpriteFlag.Ghost, true)
    scene.cameraFollowSprite(sprite_camera)
    story.spriteMoveToLocation(sprite_camera, to2.x, to2.y, speed)
    if (sprite_camera) {
        sprite_camera.destroy()
    }
    
}

function save_part(part: string) {
    
    current_part = part
    blockSettings.writeString("part", current_part)
    timer.after(4000, function on_after7() {
        timer.background(function on_background6() {
            Notification.waitForNotificationFinish()
            Notification.notify("Your progress has been saved!", 1, assets.image`
                    floppy_disc
                `)
        })
    })
}

function save_bool(name2: string, value: boolean) {
    if (value) {
        blockSettings.writeNumber(name2, 1)
    } else {
        blockSettings.writeNumber(name2, 0)
    }
    
}

//  def part_2_4():
//      global can_fight, can_slow_time, sprite_end_screen
//      enable_movement(False)
//      can_fight = False
//      can_slow_time = False
//      sprite_end_screen = sprites.create(assets.image("""
//          part_2_end_1
//      """), SpriteKind.Title)
//      sprite_end_screen.top = 0
//      sprite_end_screen.left = 0
//      sprite_end_screen.z = 100
//      sprite_end_screen.set_flag(SpriteFlag.RELATIVE_TO_CAMERA, True)
//      sprite_end_screen.set_flag(SpriteFlag.GHOST, True)
//      fade_out(True)
//      while True:
//          for image23 in [assets.image("""
//                  part_2_end_2
//              """),
//              assets.image("""
//                  part_2_end_3
//              """),
//              assets.image("""
//                  part_2_end_1
//              """)]:
//              pause(5000)
//              if Math.percent_chance(3):
//                  imagemorph.morph(sprite_end_screen,
//                      assets.image("""
//                          part_2_end_easter_egg
//                      """))
//                  pause(5000)
//              imagemorph.morph(sprite_end_screen, image23)
function scale_animation_by(size2: number): Image[] {
    
    temp_array = []
    for (let frame of temp_animation) {
        if (size2 == 0.5) {
            temp_array.push(scaling.scaleHalfX(frame))
        } else if (size2 == 2) {
            temp_array.push(scaling.scale2x(frame))
        } else if (size2 == 3) {
            temp_array.push(scaling.scale3x(frame))
        } else {
            temp_array.push(frame.clone())
        }
        
    }
    return temp_array
}

scene.onOverlapTile(SpriteKind.Darkness, sprites.dungeon.floorLight3, function on_overlap_tile6(sprite9: Sprite, location21: tiles.Location) {
    tiles.setTileAt(location21, assets.tile`
        darkness
    `)
    timer.after(2000, function on_after8() {
        tiles.setTileAt(location21, sprites.dungeon.floorLightMoss)
    })
})
function animate_character() {
    character.loopFrames(sprite_player, assets.animation`
            character_walk_up
        `, 100, character.rule(Predicate.MovingUp))
    character.loopFrames(sprite_player, assets.animation`
            character_walk_right
        `, 100, character.rule(Predicate.MovingRight))
    character.loopFrames(sprite_player, assets.animation`
            character_walk_down
        `, 100, character.rule(Predicate.MovingDown))
    character.loopFrames(sprite_player, assets.animation`
            character_walk_left
        `, 100, character.rule(Predicate.MovingLeft))
    character.runFrames(sprite_player, assets.animation`
            character_up
        `, 100, character.rule(Predicate.NotMoving, Predicate.FacingUp))
    character.runFrames(sprite_player, assets.animation`
            character_right
        `, 100, character.rule(Predicate.NotMoving, Predicate.FacingRight))
    character.runFrames(sprite_player, assets.animation`
            character_down
        `, 100, character.rule(Predicate.NotMoving, Predicate.FacingDown))
    character.runFrames(sprite_player, assets.animation`
            character_left
        `, 100, character.rule(Predicate.NotMoving, Predicate.FacingLeft))
}

function part_2_3() {
    
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(19, 14))
    sprite_player.y += tiles.tileWidth() / 2
    sprite_player.setVelocity(0, 0)
    scene.followPath(sprite_player, scene.aStar(tiles.getTileLocation(0, 0), tiles.getTileLocation(0, 0)), 0)
    sprite_player.setFlag(SpriteFlag.Ghost, false)
    scene.cameraFollowSprite(sprite_player)
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingRight, Predicate.NotMoving))
    character.clearCharacterState(sprite_player)
    sprite_boss = make_serpent(28, 14, 50, 3)
    sprite_boss.y += tiles.tileWidth() / 2
    fade_out(true)
    pause(1000)
    for (let index3 = 0; index3 < 6; index3++) {
        tiles.setTileAt(tiles.getTileLocation(17, 12 + index3), sprites.dungeon.greenOuterWest0)
        tiles.setWallAt(tiles.getTileLocation(17, 12 + index3), true)
        pause(500)
    }
    pause(1000)
    story.spriteMoveToLocation(sprite_boss, sprite_player.x + 3 * tiles.tileWidth(), sprite_player.y, 50)
    pause(1000)
    story.printCharacterText("Hello there " + name3 + ", I've been waiting for you...", "The Snake Emperor")
    story.printCharacterText("What do you want?", name3)
    story.printCharacterText("I just need you, uh what do they say instead of killing? I just need you severely incapacitated so you don't get in the way of my world domination plans.", "The Snake Emperor")
    story.printCharacterText("I've gotten maybe at least 90% of the world. What are the exact numbers again?", "The Snake Emperor")
    story.printCharacterText("97.89%!", "*Voice in the distance*")
    story.printCharacterText("Yea, whatever he said. I think you are the last village, but since I've conquered so many at this point I don't remember. ", "The Snake Emperor")
    story.printCharacterText("Anyways, I just need you out of the way.", "The Snake Emperor")
    story.printCharacterText("But what if I kill you right here?", name3)
    story.printCharacterText("...", "The Snake Emperor")
    story.printCharacterText("HAHA you are funny hero. Not like you could. I'm 3x bigger than you!", "The Snake Emperor")
    story.printCharacterText("But if I'm dead then well, this whole empire collapses and all my hard work gets unwound. ", "The Snake Emperor")
    story.printCharacterText("All the villages would be freed and there wouldn't be any unity amongst everyone!", "The Snake Emperor")
    story.printCharacterText("And then it would be a pain in the butt to resurrect myself because it would take a couple years before I can come back.", "The Snake Emperor")
    story.printCharacterText("Anyways let me just quickly throw some fireballs - you are in my way and I have a meeting with my advisors-", "The Snake Emperor")
    story.printCharacterText("They are all dead!", "*Voice in the distance*")
    story.printCharacterText("Dang, you are a pesky little hero. Stand still!", "The Snake Emperor")
    story.spriteMoveToLocation(sprite_boss, sprite_player.x + 6 * tiles.tileWidth(), sprite_player.y, 50)
    story.spriteMoveToLocation(sprite_boss, sprite_player.x + 5 * tiles.tileWidth(), sprite_player.y, 50)
    character.setCharacterState(sprite_boss, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    for (let index4 = 0; index4 < 3; index4++) {
        shoot_fireball(sprite_boss, sprite_player)
        pause(100)
        slowing_time = true
    }
    story.spriteMoveToLocation(sprite_player, sprite_player.x, sprite_player.y + 2 * tiles.tileWidth(), 50)
    slowing_time = false
    pause(1000)
    story.printCharacterText("Oh, so you are gonna play that game huh?", "The Snake Emperor")
    story.printCharacterText("ALRIGHT THEN FIGHT ME! DON'T BE A COWARD!", name3)
    story.printCharacterText("ALRIGHT NOW I'M AAANNNGGGRRRYYY!!!", "The Snake Emperor")
    character.clearCharacterState(sprite_boss)
    story.spriteMoveToLocation(sprite_boss, sprite_boss.x + 5 * tiles.tileWidth(), sprite_boss.y, 50)
    story.spriteMoveToLocation(sprite_boss, sprite_boss.x + -1 * tiles.tileWidth(), sprite_boss.y, 50)
    story.printCharacterText("Also by the way, I'm not affected by your stupid \"time control.\"", "The Snake Emperor")
    story.printCharacterText("Sadly my stupid fireballs are. I would have them be excluded from the time control but it's too much paperwork.", "The Snake Emperor")
    enable_movement(true)
    can_fight = true
    can_slow_time = true
    energy_level = 100
    character.setCharacterState(sprite_boss, character.rule(Predicate.FacingLeft, Predicate.NotMoving))
    story.spriteMoveToLocation(sprite_boss, sprite_boss.x, sprite_boss.y + -5 * tiles.tileWidth(), 50)
    timer.background(function on_background7() {
        
        while (!spriteutils.isDestroyed(sprite_boss)) {
            for (let index5 = 0; index5 < 3; index5++) {
                shoot_fireball(sprite_boss, sprite_player)
                pause(100)
            }
            if (Math.percentChance(20)) {
                sprite_darkness = sprites.create(assets.image`
                        darkness_image
                    `, SpriteKind.Darkness)
                sprite_darkness.setPosition(sprite_boss.x, sprite_boss.y)
                sprite_darkness.setFlag(SpriteFlag.DestroyOnWall, true)
                sprite_darkness.setFlag(SpriteFlag.Invisible, true)
                sprite_darkness.lifespan = 3000
                spriteutils.setVelocityAtAngle(sprite_darkness, spriteutils.angleFrom(sprite_darkness, sprite_player), 40)
            }
            
            pause(2000)
        }
    })
    while (!spriteutils.isDestroyed(sprite_boss)) {
        for (let diff of [5, 5, -5, -5]) {
            pause(1000)
            if (spriteutils.isDestroyed(sprite_boss)) {
                break
            } else {
                story.spriteMoveToLocation(sprite_boss, sprite_boss.x, sprite_boss.y + diff * tiles.tileWidth(), 50)
            }
            
        }
    }
    enable_movement(false)
    can_fight = false
    can_slow_time = false
    timer.background(function on_background8() {
        story.printCharacterText("NOOOOOOOOOOOO I WAS SO CLOSE!", "The Snake Emperor")
    })
    fade_in(true)
    story.clearAllText()
}

function make_part_2_tilemap() {
    scene.setBackgroundColor(6)
    tiles.setTilemap(tilemap`
        level_2
    `)
    for (let location22 of tiles.getTilesByType(sprites.castle.rock0)) {
        tiles.setWallAt(location22, true)
    }
    for (let location23 of tiles.getTilesByType(sprites.castle.rock1)) {
        tiles.setWallAt(location23, true)
    }
    for (let location24 of tiles.getTilesByType(sprites.dungeon.hazardLava0)) {
        tiles.setWallAt(location24, true)
    }
    for (let location25 of tiles.getTilesByType(sprites.dungeon.hazardLava1)) {
        tiles.setWallAt(location25, true)
    }
    for (let location26 of tiles.getTilesByType(assets.tile`
        tree_1
    `)) {
        place_thing(assets.image`
                tree_1
            `, tiles.locationXY(location26, tiles.XY.column), tiles.locationXY(location26, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location27 of tiles.getTilesByType(assets.tile`
        tree_2
    `)) {
        place_thing(assets.image`
                tree_2
            `, tiles.locationXY(location27, tiles.XY.column), tiles.locationXY(location27, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location28 of tiles.getTilesByType(assets.tile`
        tree_3
    `)) {
        place_thing(assets.image`
                tree_3
            `, tiles.locationXY(location28, tiles.XY.column), tiles.locationXY(location28, tiles.XY.row))
        sprite_thing.y += -8
    }
    for (let location29 of tiles.getTilesByType(assets.tile`
        tree_4
    `)) {
        place_thing(assets.image`
                tree_4
            `, tiles.locationXY(location29, tiles.XY.column), tiles.locationXY(location29, tiles.XY.row))
        sprite_thing.y += -4
    }
    for (let location30 of tiles.getTilesByType(assets.tile`
        tree_4
    `)) {
        place_thing(assets.image`
                tree_4
            `, tiles.locationXY(location30, tiles.XY.column), tiles.locationXY(location30, tiles.XY.row))
        sprite_thing.y += -4
    }
    for (let location31 of tiles.getTilesByType(assets.tile`
        flower_1
    `)) {
        place_floor_thing(assets.image`
                flower_1
            `, tiles.locationXY(location31, tiles.XY.column), tiles.locationXY(location31, tiles.XY.row))
    }
    for (let location32 of tiles.getTilesByType(assets.tile`
        flower_2
    `)) {
        place_floor_thing(assets.image`
                flower_2
            `, tiles.locationXY(location32, tiles.XY.column), tiles.locationXY(location32, tiles.XY.row))
    }
    for (let location33 of tiles.getTilesByType(assets.tile`
        mushroom_1
    `)) {
        place_floor_thing(assets.image`
                mushroom_1
            `, tiles.locationXY(location33, tiles.XY.column), tiles.locationXY(location33, tiles.XY.row))
    }
    for (let location34 of tiles.getTilesByType(assets.tile`
        stump_1
    `)) {
        place_thing(assets.image`
                stump_1
            `, tiles.locationXY(location34, tiles.XY.column), tiles.locationXY(location34, tiles.XY.row))
    }
}

function part_1_3() {
    
    can_fight = true
    tiles.placeOnTile(sprite_player, tiles.getTileLocation(14, 12))
    character.setCharacterState(sprite_player, character.rule(Predicate.FacingDown, Predicate.NotMoving))
    make_serpent(0, 15, 2, 1)
    make_serpent(0, 16, 2, 1)
    enable_movement(false)
    for (let sprite_serpent3 of sprites.allOfKind(SpriteKind.Enemy)) {
        sprite_serpent3.setFlag(SpriteFlag.GhostThroughWalls, true)
        sprite_serpent3.x += tiles.tileWidth() * -1.5
    }
    info.setLife(20)
    fade_out(true)
    story.printCharacterText("Well that was helpful.", name3)
    story.printCharacterText("Oh no they are here.", name3)
    pause(1000)
    camera_glide_to(sprite_player, sprites.allOfKind(SpriteKind.Enemy)[0], 100)
    pause(1000)
    for (let sprite_serpent4 of sprites.allOfKind(SpriteKind.Enemy)) {
        timer.background(function on_background9() {
            story.spriteMoveToLocation(sprite_serpent4, sprite_serpent4.x + tiles.tileWidth() * 2, sprite_serpent4.y, 50)
        })
    }
    pause(1000)
    for (let sprite_serpent5 of sprites.allOfKind(SpriteKind.Enemy)) {
        sprite_serpent5.setFlag(SpriteFlag.GhostThroughWalls, false)
    }
    enable_movement(true)
    character.clearCharacterState(sprite_player)
    can_fight = true
    can_slow_time = true
    scene.cameraFollowSprite(sprite_player)
    update_and_wait_till_x_serpents_left(0)
    pause(2000)
    for (let index6 = 0; index6 < 6; index6++) {
        make_serpent(0, 14, 2, 1)
        make_serpent(0, 17, 2, 1)
        for (let sprite_serpent6 of sprites.allOfKind(SpriteKind.Enemy)) {
            sprite_serpent6.setFlag(SpriteFlag.GhostThroughWalls, true)
            sprite_serpent6.x += tiles.tileWidth() * -1
        }
        for (let sprite_serpent7 of sprites.allOfKind(SpriteKind.Enemy)) {
            timer.background(function on_background10() {
                story.spriteMoveToLocation(sprite_serpent7, sprite_serpent7.x + (tiles.tileWidth() + 8), sprite_serpent7.y, 50)
            })
        }
        update_serpents_for_x_ms(1000)
        for (let sprite_serpent8 of sprites.allOfKind(SpriteKind.Enemy)) {
            sprite_serpent8.setFlag(SpriteFlag.GhostThroughWalls, false)
        }
        update_serpents_for_x_ms(3000)
    }
    update_and_wait_till_x_serpents_left(0)
    enable_movement(false)
    pause(1000)
    timer.background(function on_background11() {
        story.printCharacterText("Wait no come back I see you over there!", name3)
    })
    scene.followPath(sprite_player, scene.aStar(tiles.locationOfSprite(sprite_player), tiles.getTileLocation(0, 15)), 80)
    sprite_player.setFlag(SpriteFlag.Ghost, true)
    while (scene.spritePercentPathCompleted(sprite_player) < 100) {
        pause(100)
    }
    sprite_player.vx = -80
    can_slow_time = false
    slowing_time = false
    can_fight = false
    scene.cameraFollowSprite(null)
    fade_in(true)
    story.clearAllText()
}

function random_path_tile(): Image {
    return [sprites.castle.tilePath5, sprites.castle.tilePath1, sprites.castle.tilePath2, sprites.castle.tilePath3, sprites.castle.tilePath8, sprites.castle.tilePath9, sprites.castle.tilePath4, sprites.castle.tilePath7, sprites.castle.tilePath6]._pickRandom()
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap2(sprite10: Sprite, otherSprite2: Sprite) {
    timer.throttle("serpent_" + ("" + sprites.readDataNumber(otherSprite2, "id")) + "_take_damage", 500, function on_throttle4() {
        if (sprites.readDataBoolean(sprite10, "attacking")) {
            statusbars.getStatusBarAttachedTo(StatusBarKind.EnemyHealth, otherSprite2).value += -1
            if (statusbars.getStatusBarAttachedTo(StatusBarKind.EnemyHealth, otherSprite2).value <= 0) {
                otherSprite2.destroy(effects.disintegrate, 100)
            }
            
        }
        
    })
})
let sprite_darkness : Sprite = null
let sprite_boss : Sprite = null
let temp_array : Image[] = []
let sprite_end_screen : Sprite = null
let sprite_camera : Sprite = null
let sprite_fireball : Sprite = null
let sprite_villager2 : Sprite = null
let villager_left_animations : Image[][] = []
let villager_right_animations : Image[][] = []
let villager_up_animations : Image[][] = []
let villager_down_animations : Image[][] = []
let start_time = 0
let sprite_thing : Sprite = null
let status_bar : StatusBarSprite = null
let temp_animation : Image[] = []
let sprite_serpent9 : Sprite = null
let path : tiles.Location[] = []
let sprite_leader : Sprite = null
let sprite_overlapping : Sprite = null
let sprite_player : Sprite = null
let current_part = ""
let name3 = ""
let sprite_id = 0
let energy_level = 0
let dark_mode = false
let slowing_time = false
let can_slow_time = false
let can_fight = false
let can_skip_dialog = false
color.setPalette(color.White)
can_skip_dialog = false
can_fight = false
can_slow_time = false
slowing_time = false
if (!blockSettings.exists("dark_mode")) {
    save_bool("dark_mode", false)
}

dark_mode = read_bool("dark_mode")
multilights.toggleLighting(dark_mode)
energy_level = 100
sprite_id = 0
pause(100)
if (controller.B.isPressed()) {
    scene.setBackgroundColor(12)
    fade_out(false)
    story.showPlayerChoices("Reset everything!", "No keep my data!")
    if (story.getLastAnswer().includes("Reset")) {
        blockSettings.clear()
        story.printCharacterText("Reset successful.")
        fade_in(true)
        game.reset()
    } else {
        story.printCharacterText("No reset was performed.")
        fade_in(true)
    }
    
}

if (!blockSettings.exists("name")) {
    scene.setBackgroundColor(12)
    fade_out(true)
    game.splash("Evan Zeng", "Protect Fox Meadow School!")
    // blockSettings.write_string("name", game.ask_for_string("Please input a name: ", 24))
    fade_in(true)
}

info.setLife(20)
// name3 = blockSettings.read_string("name")
name3 = "Evan"
if (!blockSettings.exists("part")) {
    blockSettings.writeString("part", "1.1")
}

current_part = blockSettings.readString("part")
can_skip_dialog = true
make_character()
tiles.placeOnTile(sprite_player, tiles.getTileLocation(17, 18))
sprite_player.y += tiles.tileWidth() / 2
sprite_player.x += tiles.tileWidth() / 2
// part_2()
timer.background(function on_background12() {
    pause(100)
    if (current_part.charAt(0) == "1") {
        part_1()
    }
    
})
game.onUpdate(function on_on_update() {
    for (let kind3 of [SpriteKind.Projectile, SpriteKind.Enemy, SpriteKind.Thing, SpriteKind.Villager]) {
        for (let sprite11 of sprites.allOfKind(kind3)) {
            sprite11.z = sprite11.bottom / 100
        }
    }
    for (let sprite12 of sprites.allOfKind(SpriteKind.Player)) {
        sprite12.z = (sprite12.bottom - 8) / 100
    }
})
forever(function on_forever() {
    for (let kind4 of [SpriteKind.Enemy, SpriteKind.Projectile, SpriteKind.Villager]) {
        for (let sprite13 of sprites.allOfKind(kind4)) {
            if (sprites.readDataBoolean(sprite13, "slowed_down")) {
                if (!slowing_time) {
                    sprites.setDataBoolean(sprite13, "slowed_down", false)
                    sprite13.vx = sprite13.vx * 5
                    sprite13.vy = sprite13.vy * 5
                }
                
            } else if (slowing_time) {
                sprites.setDataBoolean(sprite13, "slowed_down", true)
                sprite13.vx = sprite13.vx * 0.2
                sprite13.vy = sprite13.vy * 0.2
            }
            
        }
    }
    pause(100)
})
game.onUpdateInterval(100, function on_update_interval() {
    if (info.life() < 20 && info.life() > 0) {
        if (Math.percentChance(5)) {
            info.changeLifeBy(1)
        }
        
    }
    
})
game.onUpdateInterval(200, function on_update_interval2() {
    
    if (slowing_time) {
        energy_level += -1
        if (energy_level <= 0) {
            slowing_time = false
        }
        
    } else if (energy_level < 100 && Math.percentChance(10)) {
        energy_level += 1
    }
    
    if (sprite_player) {
        status_bar = statusbars.getStatusBarAttachedTo(StatusBarKind.Energy, sprite_player)
        if (status_bar) {
            status_bar.setFlag(SpriteFlag.Invisible, !can_slow_time)
            status_bar.value = energy_level
        }
        
    }
    
})
