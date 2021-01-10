import random
from thesis_sieben_bocklandt.code.prototyping.RA2archetype import optimal_substitution
def k_modes(k, data_in):
    data=[d for d in data_in if d[1]<8]
    centroids=[]
    clusters=[]
    #initialization
    for i in range(0,k):
        clusters.append(set())
        rand_data=random.choice(data)
        while rand_data in centroids:
            rand_data = random.choice(data)
        centroids.append(rand_data)
    changed=True
    last_changes=[]
    last_centroids=[]
    while changed:
        clusters=[[] for x in range(0,k)]
        cluster_indices=[set() for x in range(0,k)]
        for RA_id in range(0,len(data)):
            RA=data[RA_id]
            best_dist = 0
            best_mapping = None
            best_center=0
            for center_id in range(0,k):
                center=centroids[center_id]
                if RA==None or center==None:
                    print("test")
                dist,_,mapping=optimal_substitution(RA[0],center[0],RA[1],center[1])
                if dist>best_dist:
                    best_dist=dist
                    best_center=center_id
                    best_mapping=mapping
            if best_dist!=0:
                new_RA=set()
                for element in RA[0]:
                    new_relation=""
                    for letter in element:
                        if letter in best_mapping.keys():
                            new_relation+=best_mapping[letter]
                        else:
                            new_relation+=letter
                    new_RA.add(new_relation)
                clusters[best_center].append((new_RA,RA[1]))
                cluster_indices[best_center].add(RA_id)
                #update the centroids as the intersection of all the sets
        #clusters = lijst van k sets met daarin tuples van set van strings en een int
        for i in range(0,k):
            cluster=clusters[i]
            centroid ={}
            for element in cluster:
                if centroid =={}:
                    centroid=element
                else:
                    centroid = (centroid[0]&element[0],max(centroid[1],element[1]))
            if centroid=={}:
                centroid=(set(),0)
            centroids[i]=centroid
        changes=False
        for centroid in centroids:
            if centroid not in last_centroids:
                changes=True
        if not changes and last_changes==cluster_indices:
            return clusters,centroids
        else:
            print(cluster_indices)
            last_changes = cluster_indices
            last_centroids = centroids
            print("there were changes")
            for i in range(0, k):
                print(len(clusters[i]), centroids[i])








