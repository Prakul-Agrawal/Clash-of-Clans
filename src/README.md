# `test.py` - `King.move`

### test_move_in_correct_direction

- It checks if king is moving in the correct direction.
- For example, if the `direction` given is "up", it should not change column, and its row should decrease.

### test_positions_match

- It checks if the value stored in `points.py` as `HERO_POS` is the same as position of king.

### test_wrong_index

- It checks if final position of king is within the dimensions of the board.
- `King.position` should not have negative indices and should not have indices that are greater than or equal to dimensions of village.

### test_did_not_go_through_buildings

- It checks if the king passed through buildings while moving.
- It ensures that king's final position is such that there is no building in between the straight line from its initial position to this final position.

### test_moved_correct_amount

- It checks if the king moved the correct number of steps, based on its speed.
- It ensures that the king doesn't move more than its speed.
- It checks that if king stops before it has moved the complete distance, then there has to be a building in front of it.

### test_correct_facing_direction

- It checks if the direction that king is facing is the same as the direction in which the king tries to move.

### test_dead_behaviour

- It checks that the king cannot move around and change state if it is already dead, that is if `King.alive == False`

### test_changes_not_allowed

- It checks that `King.move` cannot change various attributes of King class.
- `King.move` should not change `King.speed`, `King.health`, `King.max_health`, `King.attack`, `King.AoE`, `King.attack_radius` and `King.alive`

### test_invalid_direction

- It checks that if direction is some string other than "up", "down", "left" or "right", then king doesn't change position

# `test_bonus.py` - `King.attack_target`

### test_building_destruction

- It checks whether buildings were destroyed correctly or not.
Buildings should not be destroyed when their health is greater than 0.
However, when health is less than or equal to 0, they should be destroyed.
- It also ensures that the target object is removed from its respective dictionary and that the map that is displayed also gets updated. This is because the `target.destroy` function does all this, so it is required to happen.

### test_health_reduced

- It checks whether the health of buildings was reduced by the correct amount.
- It also checks that the health of buildings is exactly 0 if they took damage such that their health became less than or equal to 0.

### test_dead_behaviour

- It checks that the king cannot attack anything and change states if it is already dead, that is if `King.alive == False`

### test_changes_not_allowed

- It checks that `King.attack_target` cannot change various attributes of King and Target class.
- `King.attack_target` should not change `King.speed`, `King.health`, `King.max_health`, `King.attack`, `King.AoE`, `King.facing`, `King.attack_radius`, `King.position` and `King.alive`. Also, it should not change `Target.position`, `Target.dimensions`, `Target.max_health`, `Target.type`, `Target.attack` and `Target.attack_radius`. 