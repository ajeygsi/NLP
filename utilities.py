# [[the], [a, an]] => [[the, a], [the, an]]
def unpackAList (lst):
    new_lst = []
    for each in lst[0]:
        new_lst.append([each])
    
    for sublst in lst[1:]:
        if (len(sublst) == 1):
            for nlst in new_lst:
                nlst.append(sublst[0])
        else:
            renew_lst = []
            for nlst in new_lst:
                for subitem in sublst:
                    renew_sub_lst = list(nlst)
                    renew_sub_lst.append(subitem)
                    renew_lst.append(renew_sub_lst)
            
            new_lst = list(renew_lst)

    return new_lst
