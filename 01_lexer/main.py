import token_rules
import ply.lex as lex
import argparse
import codecs
import logging


def check_output(output_file, expected_file):
    """
    this function is used to check if the lexer's output
    is the same with the expected output
    :param output_file: the file that contains output of the lexer
    :param expected_file: the .expected file that contains expected outputs
    """
    is_same = True
    logging.basicConfig(filename='in_and_out/report.log', level=logging.DEBUG)
    with open(output_file, "r") as f1, open(expected_file, "r") as f2:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                logging.warning(f' difference found: \n'
                                f'your lexer outputs: {line1}'
                                f'expected output:    {line2}')
                is_same = False

    # log the results to an ouput file
    if is_same:
        logging.info(f' No differences found. The Lexer passed {expected_file}')
        logging.info('--------------------------------------------------------')
    else:
        logging.warning(' Differences found!')
        logging.warning('-------------------')


if __name__ == "__main__":
    # make the parser to get information from user
    parser = argparse.ArgumentParser(description='Lexical Analysis')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='author of this file')
    group.add_argument('-f', '--file', help='filename to process',
                       default='in_and_out/02_vars.tupl')
    args = parser.parse_args()

    # build the lexer
    lexer = lex.lex(module=token_rules)
    if args.who:
        print('272580 Khoa Nguyen')
    elif args.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open(args.file, 'r', encoding='utf-8') as input_file:
            # blindly read all to memory (what if that is a 42Gb file????)
            data = input_file.read()
        lexer.input(data)
        with codecs.open('in_and_out/out.tupl', 'w') as output_file:
            while True:
                token = lexer.token()
                if token is None:
                    break
                print(token)
                output_file.write(str(token))
                output_file.write('\n')
            output_file.close()

        try:
            # get the name of the expected file and check the output
            expected_file = args.file.split('.')[0] + '.expected'
            check_output('in_and_out/out.tupl', expected_file)
        except:
            print('Cannot check if the output is correct?')

