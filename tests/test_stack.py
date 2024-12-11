from src.calculatorLogic.stack import ListStack


class TestListStack:
    def test_push_one_item(self):
        s = ListStack()

        s.push(5)

        # looking into the list to make sure the value is there (not recommended for actual use)
        assert s._items[0] == 5

    def test_push_multiple(self):
        s = ListStack()

        s.push(4)
        s.push(1)
        s.push(6)
        s.push(3)

        # looking into the list to make sure the value is there (not recommended for actual use)
        assert s._items[2] == 6

    def test_top(self):
        s = ListStack()

        s.push('a')
        s.push('b')

        assert s.top() == 'b'

    def test_pop(self):
        s = ListStack()

        s.push(1)
        s.push(2)
        s.push(3)

        s.pop()

        assert s.pop() == 2

    def test_is_empty(self):
        s = ListStack()

        assert s.is_empty()

    def test_empty(self):
        s = ListStack()

        s.push(1)
        s.push(2)
        s.push(3)

        s.empty()

        assert s.is_empty()

    def test_len(self):
        s = ListStack()

        s.push(1)
        s.push(1)
        s.push(1)
        s.push(1)
        s.push(1)

        s.pop()
        s.pop()

        assert len(s) == 3

    def test_mixed_stack(self):
        s = ListStack()

        s.push(1)
        s.push('a')

        char = s.pop()
        num = s.top()

        assert char == 'a' and num == 1
