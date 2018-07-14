#!/usr/bin/env python3

# ZenCRC ver 0.9.1.1 Beta

import os
import argparse
from zencrc import crc32

__version__ = "0.9.1.3b1"  # PEP440


def expand_dirs(dirlist):
    master_filelist = []
    for i in dirlist:
        if os.path.isdir(i):
            for parent_dir, _, files in os.walk(i):
                for i in range(len(files)):
                    file_path = os.path.join(parent_dir, files[i])
                    master_filelist.append(file_path)
        else:
            master_filelist.append(i)
    return master_filelist


def main():
    parser = argparse.ArgumentParser(description='ZenCRC ver 0.9 Beta')
    parser.add_argument('-a',
                        '--append',
                        action='store_true',
                        help='append CRC32 to file(s)')

    parser.add_argument('-v',
                        '--verify',
                        action='store_true',
                        help='verify CRC32 in file(s)')

    parser.add_argument('-s',
                        '--sfv',
                        help='Create a .sfv file')

    parser.add_argument('-c',
                        '--checksfv',
                        action='store_true',
                        help='Verify a .sfv file')

    parser.add_argument('-r',
                        '--recurse',
                        action='store_true',
                        help='Run program recursively')

    parser.add_argument('-d', '--delete',
                        action='store_true',
                        help='Remove a CRC32 checksum from a filename')

    parser.add_argument('--version',
                        action='store_true',
                        help='Print version information and exit')

    parser.add_argument('file', nargs='+', help='Input File')

    args = parser.parse_args()

    if args.recurse:
        filelist = expand_dirs(args.file)
    else:
        filelist = args.file

    if args.verify:
        try:
            print('Verify Mode:\n')
            print('{:48s}{:22s}{:8s}'.format('Filename', 'Status', 'CRC32'))
            for i in filelist:
                if os.path.isdir(i):
                    continue
                else:
                    crc32.verify_in_filename(i)
        except FileNotFoundError as err:
            print(err)
        except KeyboardInterrupt:
            print('Operation cancelled by user.')

    if args.append:
        new_filelist = []
        try:
            print('Append Mode:')
            for i in filelist:
                if os.path.isdir(i):
                    continue
                else:
                    new_filelist.append(crc32.append_to_filename(i))
            print(filelist)
            filelist = new_filelist
        except FileNotFoundError:
            pass

    if args.delete:
        for f in filelist:
            crc32.remove_from_filename(f)

    if args.sfv:
        print(filelist)
        if args.recurse:
            crc32.create_sfv_file(args.sfv, filelist)
        else:
            crc32.create_sfv_file(args.sfv, filelist)

    if args.checksfv:
        try:
            for i in filelist:
                crc32.verify_sfv_file(i)
        except IsADirectoryError as err:
            print(err)

    if args.version:
        print(__version__)

os.getcwd

if (__name__ == '__main__'):
        main()
