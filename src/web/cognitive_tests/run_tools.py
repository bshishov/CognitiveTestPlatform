import os
import subprocess
import json
import logging
import tempfile


__all__ = ['run']

logger = logging.getLogger('run')


def run(command: str, inputs: dict, work_dir=None) -> dict:
    with tempfile.TemporaryDirectory(suffix='run') as tmp_dir:
        input_filename = os.path.join(tmp_dir, 'input.json')
        output_filename = os.path.join(tmp_dir, 'output.json')

        with open(input_filename, 'w', encoding='utf-8') as f:
            json.dump(inputs, f)

        formatted_command = command.format(**{
            'input_filename': input_filename,
            'output_filename': output_filename
        })
        logger.info(f'Working directory: {work_dir}')
        logger.info(f'Running command: {formatted_command}')
        result = subprocess.run(formatted_command,
                                cwd=work_dir,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        logger.info(result.stdout.decode('utf-8', errors='ignore'))

        if result.returncode != 0:
            raise RuntimeError(f'Processing failed with return code: {result.returncode}')

        if not os.path.exists(output_filename):
            raise FileNotFoundError(f'No command results found after execution of \"{command}\". '
                                    f'Expected output file: \"{output_filename}\"')

        with open(output_filename, 'r', encoding='utf-8') as f:
            return json.load(f)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(run('python --version', inputs={'foo': 'bar'}))
