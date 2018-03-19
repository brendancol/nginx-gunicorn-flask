from app.tasks import simple_sum


def test_simple_sum():
    result = simple_sum(2, 2).wait()
    assert result == 4
