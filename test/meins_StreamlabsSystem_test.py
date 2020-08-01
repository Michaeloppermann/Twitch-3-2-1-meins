from unittest import TestCase


class TestMeins(TestCase):
    def test_calculate(self):
        from meins_StreamlabsSystem import calculate_value
        counter = 1
        initial_time = 60
        initial_value = 1000
        scale = 1
        print(str(calculate_value(initial_time, initial_value, scale, initial_time)) + " = " + str(initial_value))
        self.assertEqual(initial_value - calculate_value(initial_time, initial_value, scale, initial_time), 0)

        initial_value = 5
        scale = 20
        print(str(calculate_value(initial_time, initial_value, scale, initial_time)) + " = " + str(initial_value))
        self.assertEqual(initial_value - calculate_value(initial_time, initial_value, scale, initial_time), 0)

        initial_value = 0
        print(str(calculate_value(initial_time, initial_value, scale, initial_time)) + " = " + str(initial_value))
        self.assertEqual(initial_value - calculate_value(initial_time, initial_value, scale, initial_time), 0)

        initial_value = 5
        counter = 0
        print(str(calculate_value(initial_time, initial_value, scale, initial_time)) + " = " + str(initial_value))
        self.assertEqual(initial_value - calculate_value(initial_time, initial_value, scale, initial_time), 0)

        initial_value = 5
        counter = 2
        scale = 0
        print(str(calculate_value(initial_time, initial_value, scale, initial_time)) + " = " + str(initial_value))
        self.assertEqual(initial_value - calculate_value(initial_time, initial_value, scale, initial_time), 0)

        # while (counter <= initial_time):
        #     print(calculate_value(initial_time, initial_value, scale, counter))
        #     counter += 1
        # counter = 1
        # scale = 5
        # while (counter <= initial_time):
        #     print(calculate_value(initial_time, initial_value, scale, counter))
        #     counter += 1
