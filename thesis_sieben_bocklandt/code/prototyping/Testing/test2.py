test={'b-y+4_0', 'overlapping-x+3_0', 'bi-y+4_3', 'bi-y+0_1', 'not_overlapping-y+4_0', 'b-y+3_4', 'bi-y+0_4', 'not_overlapping-y+0_3', 'not_overlapping-y+3_4', 'overlapping-x+4_3', 'overlapping-x+4_0', 'b-y+3_1', 'not_overlapping-y+0_1', 'overlapping-x+0_4', 'b-y+1_0', 'd-x+1_0', 'not_overlapping-y+3_1', 'title+0', 'overlapping-x+3_4', 'bi-y+1_3', 'overlapping-x+1_4', 'b-y+3_0', 'di-x+0_1', 'overlapping-x+4_1', 'overlapping-x+0_1', 'middelboven+0', 'not_overlapping-y+1_0', 'not_overlapping-y+1_3', 'bi-y+0_3', 'overlapping-x+0_3', 'not_overlapping-y+0_4', 'overlapping-x+1_0', 'not_overlapping-y+4_3', 'not_overlapping-y+3_0'}
new_test=set()
for element in test:
    new_element=element.replace("not_overlapping","geen\\_overlap").replace("_",",").replace("-","_").replace("+","(").replace("overlapping","overlap")+")"
    new_test.add(new_element)
print(new_test)