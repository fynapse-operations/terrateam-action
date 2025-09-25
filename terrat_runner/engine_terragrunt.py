import cmd
import logging
import os


def is_unit(state):
    terragrunt_hcl_file = os.path.join(state.working_dir, 'terragrunt.hcl')
    logging.info("Path is %s, it exists %s, and is file %s", terragrunt_hcl_file, os.path.exists(terragrunt_hcl_file), os.path.isfile(terragrunt_hcl_file))
    return os.path.exists(terragrunt_hcl_file) and os.path.isfile(terragrunt_hcl_file)

class Engine:
    def __init__(self):
        self.name = 'terragrunt'
        self.tf_cmd = 'terragrunt'

    def init(self, state, config):
        return (True, '', '')

    def apply(self, state, config):
        return (True, '', '')

    def diff(self, state, config):
        if is_unit(state):
            return None
        else:
            (proc, stdout, stderr) = cmd.run_with_output(
                state,
                {
                    'cmd': [
                               self.tf_cmd,
                               'show',
                               '--all'
                               '-out-dir',
                               '${TERRATEAM_PLAN_FILE}'
                           ]
                }
            )
            return (proc.returncode == 0, stdout, stderr)

    def diff_json(self, state, config):
        return None

    def plan(self, state, config):
        logging.info("Planning from Terragrunt 🤖")
        logging.info("Unit is %s", is_unit(state))
        if is_unit(state):
            logging.info("Unit")
            return None

        else:
            logging.info("stack")
            (proc, stdout, stderr) = cmd.run_with_output(
                state,
                {
                    'cmd': [
                        self.tf_cmd,
                        'plan',
                        '--all'
                        '-detailed-exitcode',
                        '-out-dir',
                        '${TERRATEAM_PLAN_FILE}'
                    ] + config.get('extra_args', [])
                }
            )
            return (proc.returncode in [0, 2], proc.returncode == 2, stdout, stderr)

    def outputs(self, state, config):
        if is_unit(state):
            return None
        else:
            (proc, stdout, stderr) = cmd.run_with_output(
                state,
                {
                    'cmd': [self.tf_cmd, 'stack' 'output', '--format', 'json']
                })

            return (proc.returncode == 0, stdout, stderr)

    def unsafe_apply(self, state, config):
        return (True, '', '')


def make():
    return Engine()
