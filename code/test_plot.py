import matplotlib.pyplot as plt
results=[('breadth_all_learned_1_1_False.json', 0.9073582489230415, 0.9508149959250205),
('breadth_all_learned_2_1_False.json', 0.9232506694609391, 0.9466585167074166),
('breadth_all_learned_3_1_False.json', 0.9298928862498551, 0.9425020374898129),
('greedy_all_baseline_0_10000_False.json', 0.8953312376295268, 0.8971067644661775),
('greedy_all_baseline_0_1000_False.json', 0.88705902899057, 0.901915240423798),
('greedy_all_baseline_0_20000_False.json', 0.9000989637908959, 0.8975957620211897),
('greedy_all_baseline_0_40000_False.json', 0.907294213528933, 0.8796251018744905),
('greedy_all_baseline_0_5000_False.json', 0.8950867388520206, 0.8979217603911978),
('greedy_all_baseline_0_80000_False.json', 0.9102864128536508, 0.8804808475957621),
('greedy_all_learned_0_10000_False.json', 0.9320118756549082, 0.9395680521597393),
('greedy_all_learned_0_1000_False.json', 0.9073582489230415, 0.9504074979625102),
('greedy_all_learned_0_160000_False.json', 0.9613517289556412, 0.9248981255093726),
('greedy_all_learned_0_20000_False.json', 0.9404878332751199, 0.9316625916870417),
('greedy_all_learned_0_40000_False.json', 0.9489230410990805, 0.9310920945395276),
('greedy_all_learned_0_5000_False.json', 0.9236581674234493, 0.9416870415647921),
('greedy_all_learned_0_80000_False.json', 0.9546280125742233, 0.9268541157294214),
('greedy_all_masters_0_5000_False.json', 0.945377808825242, 0.8579869600651995)]
baseline=[]
learned=[]
masters=[]
for res in results:

    if res[0].startswith("greedy"):
        amount=int(res[0].replace("_False.json","")[res[0].find("_0_")+3:])
        if "learned" in res[0]:
            learned.append((amount,res[1],res[2]))
        elif "baseline" in res[0]:
            baseline.append((amount,res[1],res[2]))
        elif "masters" in res[0]:
            masters.append((amount,res[1],res[2]))

baseline.sort()
masters.sort()
learned.sort()
for i in [baseline,masters,learned]:
    x_val=[]
    y_val=[]
    z_val=[]
    for x in i:
        x_val.append(x[0])
        y_val.append(x[1])
        z_val.append(x[2])
    plt.plot(x_val,y_val,linestyle="solid")
    plt.plot(x_val,z_val,linestyle="dotted")




plt.show()