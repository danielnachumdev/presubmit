# MADE BY DANIEL NACHUM @ https://github.com/danielnachumdev
from utils import *
import subprocess
from sys import argv
tests_path, arg_type, in_type, out_type = proccess_command_line_arguments(
    argv[1:])

MAKE_TARGETS = ["all"]
COMMAND_DICT = {
    "tweets": "./tweets_generator",
    "snakes": "./snakes_and_ladders",
}
MAX_FUNC_LEN = 50
MAX_LINE_LENGTH = 80
FILES_TO_CHECK_CODE_STYLE = ["./tweets_generator.c",
                             "./markov_chain.c",
                             "./markov_chain.h",
                             "./snakes_and_ladders.c", ]

USE_VALGRIND = False
DELETE_TMP_FILES = True


def prepare_commands():
    def build_command(name: str, extentions):
        if arg_type == extentions[0]:
            contents = f_conts(tests_path +
                               name + extentions[0])[0]
            exe, command = contents.split()[:1][0], " ".join(
                contents.split()[1:])
            if (len(command.split()) >= 3):
                s = command.split()
                a, b, c = s[:2], s[2], s[3:]
                b = tests_path + b
                command = " ".join([" ".join(a), b, " ".join(c)])
            return exe, command

    all_files = list(filter(lambda f: "IO" in f_name(
        f), dir_files(tests_path)))
    organized_files: dict[str, list[str]] = {}
    for f in all_files:
        name = f_name(f).split(".")[0]
        if name not in organized_files:
            organized_files[name] = []
        ext = f_type(f)
        if ext not in organized_files[name]:
            organized_files[name].append(ext)
    return [(key, *build_command(key, sorted(organized_files[key]))) for key in organized_files]


def check_coding_style():
    """
    this function checkes for all the files in the FILES_TO_CHECK_CODE_STYLE list:
    - thet the length of each line is less than MAX_LINE_LENGTH
    - that all function are less than MAX_LINE_LENGTH lines long
    """
    warnings = []
    curly_bracket_diff = 0
    curly_start = 0
    for f in FILES_TO_CHECK_CODE_STYLE:
        if f_exists(f):
            lines = f_conts(f)
            for index, line in enumerate(lines):
                if curly_start == 0 and curly_bracket_diff == 1:
                    curly_start = index
                elif curly_start != 0 and curly_bracket_diff == 0:
                    func_body_len = index - curly_start
                    if func_body_len > MAX_FUNC_LEN:
                        warnings.append(
                            f"FUNCTION TOO LONG: {f} : lines {curly_start}")
                    curly_start = 0
                line = line.replace("\n", "")
                curly_bracket_diff += line.count("{")
                curly_bracket_diff -= line.count("}")

                if is_line_longer_than(line, MAX_LINE_LENGTH):
                    warnings.append(
                        f"LINE TOO LONG: {f} : line {index}  :\" {line}\"")
        else:
            warnings.append(
                f"FILE DOES NOT EXIST: A file you have selected for coding style check does not exist: {f}")
    if len(warnings) > 0:
        print("CODING STYLE WARNING".center(PRINT_CENTER, "-"))
        for war in warnings:
            print(war)


def prepare_workspace():
    """this function makes sure every pre-requisites is met before running the tests"""
    exit_early: bool = False
    if not IS_MAKE_INSTALLED:
        print("MAKE ERROR".center(PRINT_CENTER, "-"))
        print("Please install make")
        exit_early = True
    if not IS_GCC_INSTALLED:
        print("GCC ERROR".center(PRINT_CENTER, "-"))
        print("Please install gcc")
        exit_early = True
    if USE_VALGRIND and not IS_VALGRIND_INSTALLED:
        print("VALGRIND ERROR".center(PRINT_CENTER, "-"))
        print("Please install valgrind to use full capabilities of this presubmit")
        exit_early = True

    if exit_early:
        exit(0)
    for word in MAKE_TARGETS:
        cm(f"make {word}")

    cm("make clean")


def excecute_tests(prepared_commands):
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

    def is_target_ok(command_data) -> bool:
        if command_data[TTI] not in list(COMMAND_DICT.keys()):
            print(f"Skipped\n {command_data}")
            print(
                f"No matching target for \"{command_data[TTI]}\" was found")
            print(
                f"fill in the details at the top of the file at {COMMAND_DICT=}".split('=')[0])
            return False
        return True

    count = 0
    for command_data in prepared_commands:
        name = command_data[TNI]
        print("\n" + name.center(PRINT_CENTER, "-"), end=": ")

        if not is_target_ok(command_data):
            continue

        exe = COMMAND_DICT[command_data[TTI]]
        output = name + RANDOM + ".txt"

        clean_files(output)

        if excecute(exe, command_data[TCI], output):
            usr_path = output
            scl_path = tests_path + name + out_type

            if not are_files_contents_the_same(usr_path, scl_path):
                print(f"{FAILED}\n")
                print(f"args: {command_data[TCI]}")
                print(f"Expected: {f_conts(scl_path)}")
                print(f"Got: {f_conts(usr_path)}")
                clean_files(output)
                continue

            vlg = f_conts(f"valgrind_{output}") \
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
    print(f"{count}/{len(prepared_commands)} passed".center(PRINT_CENTER, "-"))


if __name__ == '__main__':
    pass
    # cm("clear")
    # verify_version()
    # print(f"running version {CURRENT_VERSION}")
    # if is_in_wsl():
    #     prepare_workspace()
    #     check_coding_style()
    #     excecute_tests(prepare_commands())
    # else:
    #     print("WSL ERROR".center(PRINT_CENTER, "-"))
    #     print("This script is only for WSL\n")
