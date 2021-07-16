import sys
import os
import spacy

nlp = spacy.load('en_core_web_sm')

#TODO: hotter (single token per line)
#TODO: Australia is hotter (bug)

class Comp2Super:
    """ CompToSuper class takes string as its argument, finds comparative adjectives and returns converted string """

    def __init__(self, s):

        self.s = s

    # rules for converting adjectives into superlative ones
    @staticmethod
    def convert_to_super(adj: str):

        exceptions = {'better': 'best', 'worse': 'worst', 'farther': 'farthest', 'further': 'furthest'}

        if adj.startswith('more'):
            return 'the ' + adj.replace('more', 'most')
        elif adj.startswith('less'):
            return 'the ' + adj.replace('less', 'least')
        elif adj in exceptions.keys():
            return 'the ' + exceptions[adj]
        elif adj.endswith('er'):
            return 'the ' + adj[:-1] + 'st'
        else:
            print(f'{adj} doesn\'t look like comparative one')
            return False

    # extracts JJRs and convert them into superlative forms
    def convert_string(self):
        doc = nlp(self.s)
        result_string = ''

        for token in doc:
            gifted_children = [child for child in token.children if child.text in ['more', 'less']]

            if token.tag_ == 'JJR':
                result_string += ' ' + self.convert_to_super(token.text)
            elif token.text in ['more', 'less'] and token.head.tag_ == 'JJ':
                result_string += ' ' + self.convert_to_super(token.text + ' ' + token.head.text)
            elif token.tag_ == 'JJ' and gifted_children:
                continue
            else:
                result_string += ' ' + token.text

        return result_string.strip()


if __name__ == "__main__":

    script_name = os.path.basename(__file__)
    print(f'Running {script_name}')
    if os.path.isfile(sys.argv[1]):
        input_file_path, input_file_ext = os.path.splitext(sys.argv[1])
        output_file_path = input_file_path + "_with_adjectives_converted" + input_file_ext

        print(f'Reading "{os.path.split(sys.argv[1])[-1]}" and converting its contents')
        with open(output_file_path, "w") as output_f, open(sys.argv[1], "r", encoding='utf-8') as input_f:
            for line in input_f:
                output_f.write(Comp2Super(line).convert_string()+"\n")

        print(f"The output is stored at: {output_file_path}")
        print(f'{script_name} has finished its work')

    else:
        print("Reading input line and converting it")
        print(Comp2Super(sys.argv[1]).convert_string())
        print(f'{script_name} has finished its work')
