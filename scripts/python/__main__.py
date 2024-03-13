#!/usr/bin/env python3
import argparse

from test import main as main_test
from check import main as main_check
from multitest import main as main_multitest
from arm_movement import main as main_arm_movement

def main_parser():
    # Default parent parser.
    # If arguments are needed, import parent from module.
    pp = argparse.ArgumentParser(add_help=False)
    ap = argparse.ArgumentParser(description='Collection of python scripts')

    subparsers = ap.add_subparsers(title='action')
    subparsers.required = True

    sp_check = subparsers.add_parser('check', parents=[pp], epilog='Run check')
    sp_check.set_defaults(main=main_check)

    sp_test = subparsers.add_parser('test', parents=[pp], epilog='Run test')
    sp_test.set_defaults(main=main_test)

    sp_multitest = subparsers.add_parser('multitest', parents=[pp], epilog='Run multitest')
    sp_multitest.set_defaults(main=main_multitest)

    sp_arm_movement = subparsers.add_parser('arm_movement', parents=[pp], epilog='Run arm_movement')
    sp_arm_movement.set_defaults(main=main_arm_movement)

    return ap

def main():
    ap = main_parser()
    pa = ap.parse_args()
    pa.main()

if __name__ == '__main__':
    main()
