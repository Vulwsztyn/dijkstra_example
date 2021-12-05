import unittest
from agent import *


class TestStringMethods(unittest.TestCase):

    def test_update_previous_locations(self):
        # test checks whether the agent is able to update its previous locations
        # if they realise that it is cheaper to turn right twice than to turn left twice
        previous_locations = {
            # nothing
            (5, 5, 'N'): PreviousLocation((5, 5, 'N'), '', 0),
            # right
            (5, 5, 'E'): PreviousLocation((5, 5, 'N'), 'turnright', 2),
            # left
            (5, 5, 'W'): PreviousLocation((5, 5, 'N'), 'turnleft', 5),
            # agent doesn't yet know that they can turn right twice
            (5, 5, 'S'): PreviousLocation((5, 5, 'W'), 'turnleft', 10),
            # forward
            (5, 6, 'N'): PreviousLocation((5, 5, 'N'), 'forward', 1),
            # left -> forward
            (4, 5, 'W'): PreviousLocation((5, 5, 'W'), 'forward', 6),
            # right -> forward
            (6, 5, 'E'): PreviousLocation((5, 5, 'E'), 'forward', 3),
            # left -> left -> forward
            (5, 4, 'S'): PreviousLocation((5, 5, 'S'), 'forward', 11),
            # left -> left -> forward -> forward
            (5, 3, 'S'): PreviousLocation((5, 4, 'S'), 'forward', 12),
            # left -> left -> forward -> left
            (5, 4, 'E'): PreviousLocation((5, 4, 'S'), 'turnleft', 16),
            # left -> left -> forward -> left -> forward
            (6, 4, 'E'): PreviousLocation((5, 4, 'E'), 'forward', 17),
            # left -> forward -> left
            (4, 5, 'S'): PreviousLocation((4, 5, 'W'), 'turnleft', 11),
            # left -> forward -> left -> forward
            (4, 4, 'S'): PreviousLocation((4, 5, 'S'), 'forward', 12)
        }
        # all left -> left will be changed to  right -> right and cheaper by 6
        expected_locations = {
            # nothing
            (5, 5, 'N'): PreviousLocation((5, 5, 'N'), '', 0),
            # right
            (5, 5, 'E'): PreviousLocation((5, 5, 'N'), 'turnright', 2),
            # left
            (5, 5, 'W'): PreviousLocation((5, 5, 'N'), 'turnleft', 5),
            # na razie nie wie, że może sie obrócić w dół 2 razy w prawo
            # CHANGE
            (5, 5, 'S'): PreviousLocation((5, 5, 'E'), 'turnright', 4),
            # forward
            (5, 6, 'N'): PreviousLocation((5, 5, 'N'), 'forward', 1),
            # left -> forward
            (4, 5, 'W'): PreviousLocation((5, 5, 'W'), 'forward', 6),
            # right -> forward
            (6, 5, 'E'): PreviousLocation((5, 5, 'E'), 'forward', 3),
            # CHANGE right -> right -> forward
            (5, 4, 'S'): PreviousLocation((5, 5, 'S'), 'forward', 5),
            # CHANGE right -> right -> forward -> forward
            (5, 3, 'S'): PreviousLocation((5, 4, 'S'), 'forward', 6),
            # CHANGE right -> right -> forward -> left
            (5, 4, 'E'): PreviousLocation((5, 4, 'S'), 'turnleft', 10),
            # CHANGE right -> right -> forward -> left -> forward
            (6, 4, 'E'): PreviousLocation((5, 4, 'E'), 'forward', 11),
            # left -> forward -> left
            (4, 5, 'S'): PreviousLocation((4, 5, 'W'), 'turnleft', 11),
            # left -> forward -> left -> forward
            (4, 4, 'S'): PreviousLocation((4, 5, 'S'), 'forward', 12)
        }
        previous_locations[(5, 5, 'S')] = PreviousLocation((5, 5, 'E'), 'turnright', 4)
        update_previous_locations(previous_locations, (5, 5, 'S'), 4)
        for k, v in expected_locations.items():
            self.assertEqual(v.cost, previous_locations[k].cost)
            self.assertEqual(v.prev_loc, previous_locations[k].prev_loc)
            self.assertEqual(v.move, previous_locations[k].move)

        # nie ma żadnego nowego klucza
        for k in previous_locations.keys():
            self.assertTrue(k in expected_locations)


if __name__ == '__main__':
    unittest.main()
