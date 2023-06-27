import unittest
from io import StringIO
from unittest.mock import patch
import argparse

import daily_tasks


class TestDailyTasks(unittest.TestCase):
    def test_parse_arguments(self):
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(start='9:00', end='21:00', file=None, tasks=None)):
            start_time, end_time, tasks = daily_tasks.parse_arguments()
            self.assertIsNone(start_time)
            self.assertIsNone(end_time)
            self.assertIsNone(tasks)

        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(start='9:00', end='21:00', file=None, tasks=None)):
            with patch('builtins.print') as mock_print:
                start_time, end_time, tasks = daily_tasks.parse_arguments()
                self.assertIsNone(start_time)
                self.assertIsNone(end_time)
                self.assertIsNone(tasks)
                mock_print.assert_called_with('Error: No tasks provided.')

    def test_parse_file(self):
        tasks = daily_tasks.parse_file('tests/tasks.txt')
        self.assertEqual(tasks, ['test 1', 'test 2', 'test 3'])

    def test_validate_file(self):
        self.assertTrue(daily_tasks.validate_file('tests/tasks.txt'))
        self.assertFalse(daily_tasks.validate_file('invalidfile.txt'))

    def test_validate_task_string(self):
        self.assertTrue(daily_tasks.validate_task_string('task 1, task 2; task 3'))
        self.assertFalse(daily_tasks.validate_task_string(''))

    @patch('sys.stdout', new_callable=StringIO)
    def test_parse_file_failure(self, mock_stdout):
        with self.assertRaises(SystemExit):
            daily_tasks.parse_file('invalidfile.txt')
        self.assertEqual(mock_stdout.getvalue(), "Error: File 'invalidfile.txt' is not valid or readable.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_parse_task_string_failure(self, mock_stdout):
        with self.assertRaises(SystemExit):
            daily_tasks.parse_task_string('')
        self.assertEqual(mock_stdout.getvalue(), "Error: Task string '' is not valid.\n")


if __name__ == '__main__':
    unittest.main()
