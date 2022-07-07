# Copyright (c) 2021-2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import pathlib
import shutil


def clone_client(num_clients: int):
    current_path = os.getcwd()
    poc_folder = os.path.join(current_path, "poc")
    src_folder = os.path.join(poc_folder, "client")
    for index in range(1, num_clients + 1):
        dst_folder = os.path.join(poc_folder, f"site-{index}")
        shutil.copytree(src_folder, dst_folder)
        start_sh = open(os.path.join(dst_folder, "startup", "start.sh"), "rt")
        content = start_sh.read()
        start_sh.close()
        content = content.replace("NNN", f"{index}")
        with open(os.path.join(dst_folder, "startup", "start.sh"), "wt") as f:
            f.write(content)
    shutil.rmtree(src_folder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_clients", type=int, default=1, help="number of client folders to create")

    args = parser.parse_args()

    file_dir_path = pathlib.Path(__file__).parent.absolute()
    poc_zip_path = file_dir_path.parent / "poc.zip"
    poc_folder_path = file_dir_path.parent / "poc"
    answer = input("This will delete poc folder in current directory and create a new one. Is it OK to proceed? (y/N) ")
    if answer.strip().upper() == "Y":
        dest_poc_folder = os.path.join(os.getcwd(), "poc")
        shutil.rmtree(dest_poc_folder, ignore_errors=True)
        try:
            shutil.unpack_archive(poc_zip_path)
        except shutil.ReadError:
            print(f"poc.zip not found at {poc_zip_path}, try to use template poc folder")
            try:
                shutil.copytree(poc_folder_path, dest_poc_folder)
            except BaseException:
                print(f"Unable to copy poc folder from {poc_folder_path}.  Exit")
                exit(1)
        for root, dirs, files in os.walk(dest_poc_folder):
            for file in files:
                if file.endswith(".sh"):
                    os.chmod(os.path.join(root, file), 0o755)
        clone_client(args.num_clients)
        print("Successfully creating poc folder.  Please read poc/Readme.rst for user guide.")
        print("Note POC does not have features of overseer and server switch over.")
        print("\n\nWARNING:\n******* Files generated by this poc command are NOT intended for production environments.")
    else:
        print(f"Response '{answer}' received and it's not either y or Y.  Will not create new poc folder.")


if __name__ == "__main__":
    main()
