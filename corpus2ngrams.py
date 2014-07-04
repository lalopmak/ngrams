#  corpus2ngrams.py - Given corpus .txt(s), outputs number of occurences of n-grams 
#  Copyright (c) 2014 lalop

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#                                                                       
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse, sys, operator

parser = argparse.ArgumentParser(description='Given corpus .txt(s), outputs number of occurences of n-grams')
parser.add_argument('sources', type=str, nargs='*',
                   help='.txt file(s) for your corpus')
parser.add_argument('-n', dest="n", default=1, help='The size of the n-grams whose data to output (default 1)')
parser.add_argument('-o','--output', dest="output", default=None, help='File to which to output results. (If not given, prints the results to stdout.)') 

args = vars(parser.parse_args())
sources = args['sources']
output_file = args['output']
n = int(args['n'])

if not sources:
    print("ERROR: No source files specified.\n")
    parser.print_help()
    sys.exit(1)

def append_file(previous_txt, name):
    '''Given previous text and a file name, appends file contents to that previous text'''
    f = None
    try:
        f = open(name)
        return previous_txt + "\n" + f.read()
    except:
        print "Error opening {0}".format(name)
        sys.exit(1)
    finally:
        if f: f.close()

#combine all corpus files into single str
corpus = reduce(append_file,sources,'')

#counts the ngrams; converts them all to lowercase
ngrams = {}
for i in range(len(corpus) - n + 1):
    ngram = corpus[i:i+n].lower()
    if ngram in ngrams:
        ngrams[ngram] += 1
    else:
        ngrams[ngram] = 1

#ngram counts as sorted list of tuples (ngram [str], count [int])
sorted_ngram_counts = sorted(ngrams.items(),key=operator.itemgetter(1),reverse=True)

def str_repr(s):
    '''Preliminary function: represents an string in analyzer-readable format'''
    return repr(s)[1:-1]
    
#converts ngram counts to str
output = ""
for ngram_count in sorted_ngram_counts:
    ngram, count = ngram_count
    output += "{0} {1}\n".format(str_repr(ngram), count)

if output_file:
    f = open(output_file, 'w')
    f.write(output)
    f.close()
else:
    print output
    
