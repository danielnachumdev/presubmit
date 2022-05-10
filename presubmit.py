# MADE BY DANIEL NACHUM @ https://github.com/danielnachumdev
from utils import *
import subprocess

RELATIVE_TESTS_FOLDER_PATH = "./extracts/io/"
ARG = ".arg"
IN = ".in"
OUT = ".stdout"

COMMAND_DICT = {
    "tweets": "./tweets_generator",
    "snakes": "./snakes_and_ladders",
}

MAX_LINE_LENGTH = 80
FILES_TO_CEHCK_CODE_STYLE = ["./snakes_and_ladders.c",  "./tweets_generator.c",
                             "./markov_chain.c", "./markov_chain.h"]

USE_VALGRIND = True
DELETE_TMP_FILES = True


def prepare_commands():
    def build_command(name: str, extentions):
        if ARG == extentions[0]:
            contents = f_conts(RELATIVE_TESTS_FOLDER_PATH +
                               name+extentions[0])[0]
            exe, command = contents.split()[:1][0], " ".join(
                contents.split()[1:])
            if(len(command.split()) >= 3):
                s = command.split()
                a, b, c = s[:2], s[2], s[3:]
                b = RELATIVE_TESTS_FOLDER_PATH + b
                command = " ".join([" ".join(a), b, " ".join(c)])
            return exe, command

    all_files = list(filter(lambda f: "IO" in f_name(
        f), dir_files(RELATIVE_TESTS_FOLDER_PATH)))
    organized_files: dict[str, list[str]] = {}
    for f in all_files:
        name = f_name(f).split(".")[0]
        if name not in organized_files:
            organized_files[name] = []
        ext = f_type(f)
        if ext not in organized_files[name]:
            organized_files[name].append(ext)
    return [(key, *build_command(key, sorted(organized_files[key]))) for key in organized_files]


def excecute(exe: str, command: str, output: str = f"default_output_{RANDOM}.txt") -> bool:
    if f_exists(exe):
        try:
            vl = f"valgrind --leak-check=full -s --log-file=valgrind_{output}" if IS_VALGRIND_INSTALLED and USE_VALGRIND else ""
            subprocess.run(f"{vl} {exe} {command} > {output}", shell=True)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        print(f"{exe} not found")
        return False


def clean_files(output: str) -> None:
    if DELETE_TMP_FILES:
        d_file(output)
        d_file(f"valgrind_{output}")


def check_coding_style():
    for f in FILES_TO_CEHCK_CODE_STYLE:
        if f_exists(f):
            lines = f_conts(f)
            for l in lines:
                l = l.replace("\n", "")
                if is_line_longer_than(l, MAX_LINE_LENGTH):
                    print(
                        f"{f} line {lines.index(l)+1} is too long : {l}")


def is_target_ok(command_data) -> bool:
    if command_data[TTI] not in list(COMMAND_DICT.keys()):
        print(f"Skipped\n {command_data}")
        print(
            f"No matching target for \"{command_data[TTI]}\" was found")
        print(
            f"fill in the details at the top of the file at {COMMAND_DICT=}".split('=')[0])
        return False
    return True


if __name__ == '__main__':
    if is_in_wsl():
        cm("clear")
        if not IS_MAKE_INSTALLED:
            print("Please install make")
            exit(0)
        if not IS_GCC_INSTALLED:
            print("Please install gcc")
            exit(0)
        if not IS_VALGRIND_INSTALLED:
            print("Please install valgrind to use full capabilities of this presubmit")
        cm("make all")
        cm("make clean")

        # only checks line length
        # maybe probably working, LOL
        check_coding_style()

        prepared_commands = prepare_commands()
        count = 0
        for command_data in prepared_commands:
            name = command_data[TNI]
            print("\n"+name.center(80, "-"), end=": ")

            if not is_target_ok(command_data):
                continue

            exe = COMMAND_DICT[command_data[TTI]]
            output = name+RANDOM+".txt"

            clean_files(output)

            if excecute(exe, command_data[TCI], output):
                usr_path = output
                scl_path = RELATIVE_TESTS_FOLDER_PATH+name+OUT

                if not are_files_contents_the_same(usr_path, scl_path):
                    print(f"{FAILED}\n")
                    print(f"args: {command_data[TCI]}")
                    print(f"Expected: {f_conts(scl_path)}")
                    print(f"Got: {f_conts(usr_path)}")
                    clean_files(output)
                    continue

                vlg = f_conts(f"valgrind_{output}")\
                    if IS_VALGRIND_INSTALLED and USE_VALGRIND else []
                if IS_VALGRIND_INSTALLED and USE_VALGRIND and not is_valgrind_result_ok(vlg):
                    print(f"{VALGRIND_ERROR}\n")
                    print(f"args: {command_data[TCI]}")
                    print_array(vlg)
                    clean_files(output)
                    continue

                count += 1
                print(f"{PASSED}\n")
                clean_files(output)
        print(f"{count}/{len(prepared_commands)} passed".center(80, "-"))
    else:
        print("This script is only for WSL\n")
