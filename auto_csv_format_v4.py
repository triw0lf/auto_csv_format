#!/usr/bin/env python
''' Title: auto_csv_format.py
    Author: Lauren Proehl
    Date: 02-03-2016

    Purpose is to take raw CSVs dumped from ELSA and format them so
    they are ready to put to Redmine.
'''

import csv
import argparse
import os.path

def check_ext(choices):
    'Checks to see if argument passed ends with an acceptible file extension'
    class Action(argparse.Action):
        'subclass'
        def __call__(self, parser, namespace, fname, option_string=None):
            'callback called when parsing using a custom action'
            ext = os.path.splitext(fname)[-1]
            if ext not in choices:
                parser.error("Invalid file extension. "
                             "Acceptable extension(s): {}"
                             .format(' '.join(list(choices))))
            else:
                setattr(namespace, self.dest, fname)
    return Action

def main():
    'Uses argparse to accept files as arguments from command line'
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delimiter', default=',')
    parser.add_argument('-q', '--quotechar', default='"')
    parser.add_argument('fn', action=check_ext({'.csv'}))
    args = parser.parse_args()
    #print args

    # this function, defined within the main function, has limited scope;
    # it cannot be called from global scope, only from within main(),
    # which is where we use it anyway
    def process_record(record, fields=None):
        'transform a single csv record to redmine formatted record'

        # using standard conditionals
        #if fields:
        #    select_fields = []
        #    for field in fields:
        #        select_fields.append(record[field])
        #else:
        #    select_fields = record
        #print select_fields
        #
        # the list comprehension way
        #select_fields = [record[x] for x in list(fields)] if fields else record
        #print select_fields
        #
        #return '| {}\t|'.format('\t| '.join(select_fields))

        # all rolled into a single line
        return '| {}\t|'.format('\t| '.join([record[x]
                                             for x in list(fields)]
                                            if fields else record))
        # note the indentation above (for pylint PEP8 compliance)
        # the for line is a continuation of record within the list comp
        # where the if line is ternary operation outside of list comprehension
        # python is intentionally picky about indentation as it uses it for program structure
        # this differs from most languages that use parentheses or brackets for structure

    # this usage gives me a weird AttributeError exception... use file handle instead
    #with csv.reader(open(args.fn, 'r'),
    #                delimiter=args.delimiter,
    #                quotechar=args.quotechar) as csv_reader:
    with open(args.fn, 'r') as csv_file:
        with open(args.fn + '.out', 'w') as result_file:  # outfile here; append '.out' for now
            for csv_record in csv.reader(csv_file,
                                         delimiter=args.delimiter,
                                         quotechar=args.quotechar):

                # note that we're passing the record's fields as a set here
                # also, print adds a newline, write doesn't, so we append it on write
                #result_file.write(process_record(csv_record, fields={0, 1, 4}) + '\n')

                # if we're not saving to a file, we can just print results of process_record()...
                #print process_record(csv_record, fields={0, 1, 2, 3})

                # or if we want all fields in the record, omit field param...
                print process_record(csv_record)

if __name__ == '__main__':
    # something new: this traps Ctrl-C so it exits without stackdump (pass means do nothing)
    try:
        main()
    except KeyboardInterrupt:
        pass
