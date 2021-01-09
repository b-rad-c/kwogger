#!/usr/bin/env python3
import kwogger
import pydoc


def write(output_path, mode='w+'):
    with open(output_path, mode) as f:
        pydoc.doc(kwogger, output=f)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Generate Kwogger docs and write to file')
    parser.add_argument('--output', '-o', default='API.txt')
    args = parser.parse_args()

    write(args.output)
