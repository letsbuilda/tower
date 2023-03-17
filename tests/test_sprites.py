"""Test sprite classes"""

from tower.sprites import AttackSpec


def test_atk_spec_init():
    attack = AttackSpec('Fireball', 'a ball of fire', 5, 1, 1)
    assert attack.name == 'Fireball'
    assert attack.desc == 'a ball of fire'
    assert attack.base_atk_damage == 5 and isinstance(attack.base_atk_damage, float)
    assert attack.base_atk_cooldown == 1 and isinstance(attack.base_atk_cooldown, float)
    assert attack.base_proj_speed == 1 and isinstance(attack.base_proj_speed, float)
