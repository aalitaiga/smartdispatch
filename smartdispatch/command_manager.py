import os
# from smartdispatch import utils


class CommandManager(object):

    def __init__(self, commands_filename):
        base_path, filename = os.path.split(commands_filename)

        self._running_commands_filename = os.path.join(base_path, "running_" + filename)
        self._finished_commands_filename = os.path.join(base_path, "finished_" + filename)
        self._commands_filename = commands_filename

    def _move_line_between_files(self, file1, file2, line):
        file1.seek(0, os.SEEK_SET)
        lines = file1.readlines()
        lines.remove(line)

        file1.seek(0, os.SEEK_SET)
        file1.writelines(lines)
        file1.truncate()

        file2.write(line)

    def set_commands_to_run(self, commands):
        with open(self._commands_filename, 'a') as commands_file:
            commands = [command + '\n' for command in commands]
            commands_file.writelines(commands)

    def get_command_to_run(self):
        with open(self._commands_filename, 'r+') as commands_file:
            with open(self._running_commands_filename, 'a') as running_commands_file:
                command = commands_file.readline()
                if command == '':
                    return None
                self._move_line_between_files(commands_file, running_commands_file, command)
        return command[:-1]

    def set_running_command_as_finished(self, command):
        with open(self._running_commands_filename, 'r+') as running_commands_file:
            with open(self._finished_commands_filename, 'a') as finished_commands_file:
                self._move_line_between_files(running_commands_file, finished_commands_file, command + '\n')

    def reset_running_commands(self):
        if os.path.isfile(self._running_commands_filename):
            with open(self._commands_filename, 'r+') as commands_file:
                with open(self._running_commands_filename, 'r+') as running_commands_file:
                    commands = running_commands_file.readlines()
                    if len(commands) > 0:
                        running_commands_file.seek(0, os.SEEK_SET)
                        running_commands_file.truncate()

                        commands += commands_file.readlines()
                        commands_file.seek(0, os.SEEK_SET)
                        commands_file.writelines(commands)
