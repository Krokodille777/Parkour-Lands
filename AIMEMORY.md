# Parkour Lands Notes

## Current Architecture Notes

- `game.py` owns full level restarts. `X` and `R` recreate `LEVELS[current_level_index]()` so boxes, portals, doors, timers, and both-player state return to their original level setup.
- `Player.handle_input()` should not reset the level directly; it only handles movement/body controls.
- `maincamera.py` supports optional `world_left` and `world_top` bounds. Use them for levels that intentionally place sprites at negative coordinates.
- `Level510` starts at `WORLD_LEFT = -125`, because its water section has blocks and hazards with negative `x` positions.
- Portals can use `set_portal_exit_side(portal, "top"|"bottom"|"left"|"right")` when center-spawning would put the player inside a wall or ceiling. `Level510.orange_portal2` exits from the bottom so the player appears inside Room 2 instead of inside its ceiling.
- Chapter 6 mechanics live in helper modules: `blood.py`, `sulfur.py`, `Macetrap.py`, `spikeTrap.py`, `fragile_surfaces.py`, `vines.py`, `huge_rock.py`, and `arrows.py`. Add the related sprites to level groups, then call their update/apply functions from the level's `update()`.
- `Level61` is currently only a skeleton, so do not add it to `game.py` until it has `update`, `draw`, and `is_finished`.
