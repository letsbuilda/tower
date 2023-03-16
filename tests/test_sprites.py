"""Test sprite classes"""

from pathlib import Path

from tower.sprites import AttackSpec


def test_atk_spec_init():
    attack = AttackSpec('Fireball', 'a ball of fire', 5, 1, 1)
    assert attack.name == 'Fireball'
    assert attack.desc == 'a ball of fire'
    assert attack.base_atk_damage == 5 and isinstance(attack.base_atk_damage, float)
    assert attack.base_atk_cooldown == 1 and isinstance(attack.base_atk_cooldown, float)
    assert attack.base_proj_speed == 1 and isinstance(attack.base_proj_speed, float)


def test_atk_spec_sprite_path():
    attack = AttackSpec('Fireball', 'a ball of fire', 5, 1, 1)
    assert attack.get_sprite_path() \
           == Path(__file__).parent.parent / 'assets' / 'sprites' / 'projectiles' / 'fireball.png'
