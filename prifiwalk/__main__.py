from py.function import setup_logger
from py.function import save_object
from py.function import restore_object
from py.config import logfile, logname
from py.database import Database
from py.system import System
from sys import exit
from os import geteuid
import argparse


args = None
logger = setup_logger(logname, logfile)


def menu():
    print("Choose your mode of operation:")
    print("1) Only gather for later processing")
    print("2) Process all collected metadata")
    print("3) Both gather and process")
    print("q) Quit")
    option = input()
    if option.isnumeric() and int(option) in [1, 2, 3]:
        return int(option)
    elif option == "q":
        exit()


def run(mode):
    if mode == 1:
        gather()
    elif mode == 2:
        process()
    elif mode == 3:
        do_both()


def gather():
    system = System(mode='half', target_device=args.device)
    save_object(str(system.start_measurement), system)


def process():
    db = Database(volume_note=args.note)


def do_both():
    db = Database(volume_note=args.note)
    system = System(mode='full', target_device=args.device)
    db.store(system)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device',
                        help='The device from which data will be '
                        'collected. All non-root devices will be '
                        'processed when this is not specified.',
                        type=str)
    parser.add_argument('--mode',
                        help='Determine the mode of operation.',
                        type=int)
    parser.add_argument('--note',
                        help='Add a note to the measured data.',
                        type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    euid = geteuid()
    if euid != 0:
        print("You are trying to run PriFiwalk with a non-root user!")
        print("Most PriFiwalk functions need root privileges to work.")
        exit()

    mode = args.mode or menu()
    run(mode)
