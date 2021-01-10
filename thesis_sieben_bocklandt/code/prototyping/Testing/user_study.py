from thesis_sieben_bocklandt.code.prototyping.ssim import ssim_compare, time_functions

data="D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\User study\\"
links =[(0,0,2),(0,1,2),(0,1,5),(0,2,3),(0,3,4),(6,7,8),(6,8,9),(6,9,10),(11,12,13),(11,12,14),(11,14,15)]
scores=[0,0,0,0,0]
amount=[11,11,0,0,11,11,5,11,8,11,5]
both=[0,2,1,0,0,1,0,1,0,0,1]
timing=[0,0,0]
people=11
names=["mse","ssim","sign","fsim","combo"]
for x in range(0,11):#len(links)):
    print("--> ",x)
    link = links[x]
    auth = data+str(link[0])+".png"
    A = data+str(link[1])+".png"
    B=data + str(link[2]) + ".png"
    # time_mse,time_ssim,time_sign = time_functions(auth,A)
    # time_mse2, time_ssim2, time_sign2 = time_functions(auth, B)
    # timing[0]+=(time_mse+time_mse2)
    # timing[1]+=(time_ssim+time_ssim2)
    # timing[2]+=(time_sign+time_sign2)
    simA=ssim_compare(auth,A,False)
    print(simA)
    simB=ssim_compare(auth,B,False)
    print(simB)
    for i in range(0,len(scores)):
            comp = simA[i]>simB[i]
            same=simA[i]==simB[i]
            if same:
                scores[i]+=both[x]
            elif comp:
                scores[i]+=amount[x]
            else:
                scores[i]+=11-amount[x]-both[x]
print(scores)