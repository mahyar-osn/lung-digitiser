import os
import json
import argparse
import subprocess

from typing import Dict

from loguru import logger

from src.cmgui import left_lung_command
from src.zinc import load


__script__ = "group_digitiser.cmgui"


class ProgramArguments(object):
    def __init__(self):
        self.input_config = None
        self.cmgui_exe = None
        self.output_dir = None


@logger.catch
def sample_groups(config: Dict, cmgui: str) -> None:
    for subject in config["subjects"]:
        subject_path = os.path.join(config["root"], config["dataset"], subject, config["volume"], config["sub_dir"])
        if os.path.exists(subject_path):

            logger.info(f"Sampling points for subject {subject}")

            command = left_lung_command(subject_path)

            with open(__script__, "w") as cm:
                cm.write(command)

            process = subprocess.Popen([cmgui, __script__])
            process.communicate()
            process.terminate()
            os.remove(__script__)


@logger.catch
def write_points(config: Dict, output_dir: str) -> None:
    for subject in config["subjects"]:
        subject_path = os.path.join(config["root"], config["dataset"], subject, config["volume"], config["sub_dir"])
        file_name = "Left_points.exnode"
        file_path = os.path.join(subject_path, file_name)

        if os.path.exists(subject_path):

            logger.info(f"Writing out 'pts' and 'grp' files for subject {subject}")

            # read the digitised file
            point_dict = load(file_path, file_name)
            if not point_dict:
                continue
            cls = point_dict["group"]
            coordinates = point_dict["values"]

            # write the digitised coordinates in the appropriate format needed for machine learning
            points_dir = os.path.join(output_dir, "points")
            if not os.path.exists(points_dir):
                os.makedirs(points_dir)
            # points_path = os.path.join(points_dir, f"{subject}_{config['sub_dir']}.pts")
            points_path = os.path.join(points_dir, f"{subject}.pts")
            with open(points_path, 'w') as points_file:
                for coordinate in coordinates:
                    points_file.write(f"{coordinate[0]:.2f} {coordinate[1]:.2f} {coordinate[2]:.2f}\n")
            # write the corresponding groups
            group_dir = os.path.join(output_dir, "points_label")
            if not os.path.exists(group_dir):
                os.makedirs(group_dir)
            # group_path = os.path.join(group_dir, f"{subject}_{config['sub_dir']}.grp")
            group_path = os.path.join(group_dir, f"{subject}.grp")
            with open(group_path, 'w') as points_file:
                for label in cls:
                    label = str(int(label)+1)
                    points_file.write(f"{label}\n")


def main():
    args = parse_args()
    if os.path.exists(args.input_config):
        with open(args.input_config, "r") as config_file:
            config = json.load(config_file)

        # sample points from the mesh.
        # this command will initiate the cmgui application
        sample_groups(config, args.cmgui_exe)

        # write out point coordinates and group classes into separate files
        write_points(config, args.output_dir)


def parse_args():
    parser = argparse.ArgumentParser(description="This application reads lung finite element meshes in ZINC EX format, "
                                                 "generates group annotations, sample points on each surface groups,"
                                                 "and outputs .pts and .grp files.")
    parser.add_argument("input_config", help="Location of the configuration file.")
    parser.add_argument("cmgui_exe", help="Location of the CMGUI executable file.")
    parser.add_argument("output_dir", help="Location to save the digitised points and groups.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    main()
