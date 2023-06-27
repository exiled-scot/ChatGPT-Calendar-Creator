import argparse
import os
import re

def parse_arguments():
    """Parse command-line arguments and return start and end times and list of tasks."""
    parser = argparse.ArgumentParser(description='A script to manage daily tasks.')
    parser.add_argument('-s', '--start', type=str, default='9:00',
                        help='Start time in format HH:MM')
    parser.add_argument('-e', '--end', type=str, default='21:00',
                        help='End time in format HH:MM')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str,
                       help='A file with tasks, one task per line')
    group.add_argument('-t', '--tasks', type=str,
                       help='A string with tasks, delimited by commas or semicolons')
    args = parser.parse_args()

    start_time = args.start
    end_time = args.end

    if args.file:
        tasks = parse_file(args.file)
    elif args.tasks:
        tasks = parse_task_string(args.tasks)
    else:
        print("Error: No tasks provided.")
        return None, None, None  # Return None to indicate no tasks were provided

    return start_time, end_time, tasks

def parse_file(filename: str):
    """Read a file and return the list of tasks."""
    if not validate_file(filename):
        print(f"Error: File '{filename}' is not valid or readable.")
        exit(1)
    with open(filename) as file:
        tasks = [line.strip() for line in file]
    return tasks


def parse_task_string(task_string: str):
    """Parse a string and return the list of tasks."""
    if not validate_task_string(task_string):
        print(f"Error: Task string '{task_string}' is not valid.")
        exit(1)
    tasks = [task.strip() for task in re.split('[,;]', task_string)]
    return tasks


def validate_file(filename: str):
    """Check if a file is valid and readable."""
    return os.path.isfile(filename) and os.access(filename, os.R_OK)


def validate_task_string(task_string: str):
    """Check if a string is valid as a task list."""
    return bool(task_string.strip())


if __name__ == '__main__':
    start_time, end_time, tasks = parse_arguments()
    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")
    print(f"Tasks: {tasks}")
