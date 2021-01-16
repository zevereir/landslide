import thesis_sieben_bocklandt.code.prototyping.globals as glob
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import optimal_substitution
import json
def main():
    glob.init()
    glob.init_count()

    in_enc1= frozenset({'b-y+3_0', 'b-y+1_0', 'b-y+4_0', 'b-x+2_4', 's-x+2_0', 'b-y+4_3', 'eq-y+2_4', 's-x+2_1', 'b-y+2_3', 'b-x+1_4', 's-x+3_4', 'o-x+0_3', 's-x+1_0', 'eq-y+1_3', 'b-y+2_1', 'o-x+0_4', 'b-y+4_1', 'b-y+2_0', 'b-x+1_3', 'title+0', 'b-x+2_3'})
    n1=5

    with open('thesis_sieben_bocklandt/code/prototyping/archetypes/learned.json') as json_file:
        arch_dict = json.load(json_file)
    archs_to_use=[]
    indices = [1, 1, 2, 3, 4, 1, 0, 2, 1, 0]
    for i in range(0, len(arch_dict)):
        master=arch_dict[str(i)]
        archs = []
        for key in range(0, len(master)):
            for z in master[str(key)]:
                if frozenset(z) not in archs:
                    archs.append(frozenset(z))
            archs_to_use.append((archs, indices[i] + 1))

    for i in archs_to_use:
        print(len(i[0]))
    for archetypes in archs_to_use:
        n2=archetypes[1]
        for archetype in archetypes[0]:
            print(optimal_substitution(in_enc1,archetype,n1,n2,True, False))

if __name__ == "__main__":
    main()