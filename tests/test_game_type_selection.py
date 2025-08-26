"""Tests for game type selection functionality."""

import pytest

from pooltool.game.datatypes import GameType
from pooltool.layouts import get_rack
from pooltool.objects.table.collection import default_specs_from_game_type
from pooltool.objects.table.datatypes import Table


@pytest.mark.parametrize(
    "game_type,expected_ball_count",
    [
        (GameType.EIGHTBALL, 16),  # 15 object balls + cue ball
        (GameType.NINEBALL, 10),  # 9 object balls + cue ball
        (GameType.SNOOKER, 22),  # 15 reds + 6 colors + cue ball
        (GameType.THREECUSHION, 3),  # white, yellow, red
        (GameType.SANDBOX, 10),  # Uses 9-ball layout
        (GameType.SUMTOTHREE, 2),  # cue ball + object ball
    ],
)
def test_game_type_ball_counts(game_type: GameType, expected_ball_count: int):
    """Test that each game type produces the correct number of balls."""
    table = Table.from_game_type(game_type)
    rack = get_rack(game_type=game_type, table=table)

    assert len(rack) == expected_ball_count, (
        f"Game type {game_type} should have {expected_ball_count} balls, "
        f"but got {len(rack)}"
    )


@pytest.mark.parametrize("game_type", list(GameType))
def test_game_type_table_mapping(game_type: GameType):
    """Test that all game types have valid table specifications."""
    specs = default_specs_from_game_type(game_type)

    # Verify basic table properties
    assert specs.l > 0, f"Table length should be positive for {game_type}"
    assert specs.w > 0, f"Table width should be positive for {game_type}"
    assert specs.height > 0, f"Table height should be positive for {game_type}"


def test_game_type_rack_consistency():
    """Test that the same game type produces consistent racks."""
    game_type = GameType.EIGHTBALL
    table = Table.from_game_type(game_type)

    # Generate multiple racks with the same seed
    rack1 = get_rack(game_type=game_type, table=table, spacing_factor=0)
    rack2 = get_rack(game_type=game_type, table=table, spacing_factor=0)

    # Should have same ball IDs
    assert set(rack1.keys()) == set(rack2.keys())


@pytest.mark.parametrize("game_type", list(GameType))
def test_game_type_rack_generation(game_type: GameType):
    """Test that all game types can generate valid racks."""
    table = Table.from_game_type(game_type)
    rack = get_rack(game_type=game_type, table=table)

    # Verify all balls have valid positions
    for ball_id, ball in rack.items():
        assert ball.id == ball_id
        assert ball.state.rvw.shape == (
            3,
            3,
        )  # 3x3 matrix: position, velocity, angular velocity

        # Ball should be on the table
        assert 0 <= ball.state.rvw[0, 0] <= table.w  # x position
        assert 0 <= ball.state.rvw[0, 1] <= table.l  # y position
