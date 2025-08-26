import numpy as np
import pytest

from pooltool.objects.table.datatypes import Table
from pooltool.objects.table.collection import TableName, prebuilt_specs


@pytest.fixture
def table():
    return Table.default()


def test_table_copy(table):
    new = table.copy()

    # new and table equate
    assert new is not table
    assert new == table

    assert new.cushion_segments is not table.cushion_segments
    assert new.pockets is not table.pockets

    # `model_descr` object _is_ shared, but its frozen so its OK
    assert new.model_descr is table.model_descr


def test_set_cushion_height(table):
    """Test that set_cushion_height correctly updates the height of all cushion segments."""
    # Store initial values for verification
    initial_linear = {
        id: {"p1": segment.p1.copy(), "p2": segment.p2.copy()}
        for id, segment in table.cushion_segments.linear.items()
    }
    initial_circular = {
        id: {"center": segment.center.copy()}
        for id, segment in table.cushion_segments.circular.items()
    }

    new_height = 0.85
    table.set_cushion_height(new_height)

    for id, segment in table.cushion_segments.linear.items():
        # Height property updated
        assert segment.height == new_height

        # p1 and p2 z-coordinates updated
        assert segment.p1[2] == new_height
        assert segment.p2[2] == new_height

        # x,y coordinates unchanged
        assert np.array_equal(segment.p1[:2], initial_linear[id]["p1"][:2])
        assert np.array_equal(segment.p2[:2], initial_linear[id]["p2"][:2])

    for id, segment in table.cushion_segments.circular.items():
        # Height property updated
        assert segment.height == new_height

        # center z-coordinate updated
        assert segment.center[2] == new_height

        # x,y coordinates unchanged
        assert np.array_equal(segment.center[:2], initial_circular[id]["center"][:2])


def test_nine_foot_diamond_table_specs():
    """Test that NINE_FOOT_DIAMOND table has correct dimensions."""
    specs = prebuilt_specs(TableName.NINE_FOOT_DIAMOND)
    
    # Test playing surface dimensions (9 feet x 4.5 feet)
    assert specs.l == 2.54  # 9 feet in meters
    assert specs.w == 1.27  # 4.5 feet in meters
    
    # Test that it's a pocket table
    assert hasattr(specs, 'corner_pocket_width')
    assert hasattr(specs, 'side_pocket_width')
    
    # Test model descriptor
    assert specs.model_descr.name == "null"


def test_nine_foot_diamond_table_creation():
    """Test that NINE_FOOT_DIAMOND table can be created successfully."""
    table = Table.from_table_name(TableName.NINE_FOOT_DIAMOND)
    
    # Verify dimensions
    assert table.w == 2.54
    assert table.l == 1.27
    
    # Verify it has pockets
    assert len(table.pockets) > 0
    
    # Verify it has cushion segments
    assert len(table.cushion_segments.linear) > 0
