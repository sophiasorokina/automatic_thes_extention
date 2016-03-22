__author__ = 'Lenovo'
from os import getcwd
from os.path import join, split
import jsonpickle
from classes import CandidateWord

def main():
    proj_path = split(getcwd())[0]

    temp_path = join(proj_path, 'temp')
    with open(join(temp_path, 'concepts_for_binding_with_te3.txt')) as file:
        raw_data = file.read()
    candidate_words = jsonpickle.decode(raw_data)
    #print candidate_words

    # for word in candidate_words:
    #     for concept in word.concepts:
    #         concept.w2v_sum
    #         #print concept.w2v_sum
    #     word.sort_concepts(lambda c: c.w2v_sum)

    with open(join(proj_path, 'results', 'sum_w2v3.txt'), 'w') as file:
        for word in candidate_words:
            sorted = word.sort_concepts(lambda c: c.w2v_sum)

            file.write(word.lemma.encode('utf-8') + '\n')
            for concept in sorted:
                file.write(('\t%s\t%f\n' % (concept.name, concept.w2v_sum)).encode('utf-8'))
                for te in concept.text_entries:
                    file.write(('\t\t%s\t%f\n' % (te.name, te.w2v_sim)).encode('utf-8'))
            file.write('\n')

    #mean_w2v_path = join(proj_path, 'results', 'mean_w2v.txt')
    with open(join(proj_path, 'results', 'mean_w2v3.txt'), 'w') as file:
        for word in candidate_words:
            sorted = word.sort_concepts(lambda c: c.w2v_mean)

            file.write(word.lemma.encode('utf-8') + '\n')
            for concept in sorted:
                file.write(('\t%s\t%f\n' % (concept.name, concept.w2v_mean)).encode('utf-8'))
                for te in concept.text_entries:
                    file.write(('\t\t%s\t%f\n' % (te.name, te.w2v_sim)).encode('utf-8'))
            file.write('\n')


if __name__ == '__main__':
    main()
    import winsound
    # Play Windows exit sound.
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)