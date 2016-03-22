__author__ = 'Lenovo'
from os import getcwd
from os.path import join, split
import jsonpickle
from classes import CandidateWord

def main():
    proj_path = split(getcwd())[0]

    temp_path = join(proj_path, 'temp')
    with open(join(temp_path, 'concepts_for_binding_with_te2.txt')) as file:
        raw_data = file.read()
    candidate_words = jsonpickle.decode(raw_data)
    print candidate_words

    # for word in candidate_words:
    #     for concept in word.concepts:
    #         concept.sum_te_w2v()
    #     word.sort_concepts(lambda c: c.w2v_sum)
    #
    # with open(join(proj_path, 'results', 'sum_w2v.txt'), 'w') as file:
    #     for word in candidate_words:
    #         file.write(word.lemma + '\n')
    #         for concept in word.concepts:
    #             file.write('\t%s\t%d\n' % (concept.name, concept.w2v_sum))
    #         file.write('\n')

    #mean_w2v_path = join(proj_path, 'results', 'mean_w2v.txt')


if __name__ == '__main__':
    main()
    import winsound
    # Play Windows exit sound.
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)