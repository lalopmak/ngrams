# -*- coding: UTF-8 -*-

#  text2ngrams.py - Counts the n-grams in the given text(s)
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


# strings in the text to be replaced, and their replacement
# generally used for "standardizing" different unicode chars pressed by
# the same button
text_replacements = [
    # each element is a 2-tuple:
    #    (unicode str of text to replace, unicode str of replacement text)
    # e.g. (u"…",u"...")

    #transformations to dots
    (u"…",u"..."),

    #dash transformations
    (u"—",u"-"),

    #quote transformations
    (u"“",u'"'),
    (u"”",u'"'),
    (u"’",u"'"),
    (u"‘",u"'"),
]

import argparse, sys, operator

py3 = sys.version_info[0] >= 3

if py3: from functools import reduce

parser = argparse.ArgumentParser(description='Counts the n-grams in the given text(s)')
parser.add_argument('sources', type=str, nargs='*',
                   help='.txt file(s) for your text')
parser.add_argument('-n', dest="n", default=1, help='Size of the n-grams to be counted (default 1)')
parser.add_argument('-o','--output', dest="output", default=None, help='File to which to output results. (If not given, prints the results to stdout.)') 

args = vars(parser.parse_args())
sources = args['sources']
output_file = args['output']
n = int(args['n'])

if not sources:
    print("ERROR: No source file(s) specified.\n")
    parser.print_help()
    sys.exit(1)

def append_file(previous_txt, file_name):
    '''Given previous text and a file name, appends file contents to that previous text'''
    f = None
    try:
        f = open(file_name) 
        return previous_txt + "\n" + (f.read() if py3 else f.read().decode("UTF-8"))
    except:
        print("Error opening {0}".format(file_name))
        sys.exit(1)
    finally:
        if f: f.close()

# combine all text files into single str,
# then converts them all to lowercase
text = reduce(append_file,sources,'').lower()

#replaces substrings in text in accordance to text_replacements
for orig, repl in text_replacements:
    text = text.replace(orig, repl)

#counts the ngrams
ngram_counts = {}
for i in range(len(text) - n + 1):
    ngram = text[i:i+n]
    if ngram in ngram_counts:
        ngram_counts[ngram] += 1
    else:
        ngram_counts[ngram] = 1

#ngram counts as sorted list of tuples (ngram [str], count [int])
sorted_ngram_counts = sorted(ngram_counts.items(),key=operator.itemgetter(1),reverse=True)

def ngram_repr(ngram):
    '''Preliminary function: represents an ngram in analyzer-readable format'''
    #represents escapes (e.g. \n), removes delimiting quotes
    return ngram.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t")

#converts ngram counts to str
output = u""
for ngram, count in sorted_ngram_counts:
    output += u"{0} {1}\n".format(ngram_repr(ngram), count)

if output_file:
    if py3:
        f = open(output_file, 'w')
    else:
        import codecs
        f = codecs.open(output_file, mode="w", encoding="utf-8-sig")
    f.write(output)
    f.close()
else:
    print(output)
    
