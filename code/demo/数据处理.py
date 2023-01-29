data = [
    ['一队',3,5,2],
    ['二队',3,6,2],
    ['三队一纵队',2,2,3],
    ['三队二纵队',3,1,3],
    ['五队',1,7,3],
    ['四队一纵队',3,2,3],
    ['四队二纵队',3,3,3]
]
merge_list = ['三队','四队']
sort_list = ['一队','二队','三队','四队','五队','六队','七队']

merge_dict = {i:-1 for i in merge_list}
merge_data = []
print(','.join(merge_dict.keys()))
for l in data:
    is_need_merge = list(map(lambda x:l[0].find(x) == 0,merge_list))
    if any(is_need_merge):
        merge_name = merge_list[is_need_merge.index(True)]
        merge_index = merge_dict[merge_name]
        if merge_index == -1:
            merge_data.append([merge_name] + l[1:])
            merge_dict[merge_name] = len(merge_data) - 1
        else:
            list_data = merge_data[merge_index]
            for idx,item in enumerate(l):
                if isinstance(item,(int,float)) :
                    list_data[idx] = list_data[idx] + item
    else:
        merge_data.append(l)

print(merge_dict)
print(merge_data)


# # 分组，求和，合并
# merge_dict = {i:[] for i in merge_list + ['others']}
# for list_data in data:
#     is_merge = list(map(lambda x:list_data[0].find(x) == 0,merge_list))
#     if any(is_merge):
#         merge_name = merge_list[is_merge.index(True)]
#         merge_dict[merge_name].append(list_data)
#     else:
#         merge_dict['others'].append(list_data)
# print(merge_dict)
#
# for k in merge_dict:
#     if k != 'others':
#         sum_list =[sum(i) for i in list(zip(*merge_dict[k]))[1:]]
#         merge_dict['others'].append([k] +sum_list)
#
# data = merge_dict['others']
#
# # 行求和
# for l in data:
#     l.append(sum(l[1:]))
#
# #列求和
# sumlist = [sum(l) for l in list(zip(*data))[1:]]
# data.append(['总和'] + sumlist)
# #排序
# data.sort(key = lambda x: v if (v:=''.join(sort_list).find(x[0]))>=0 else 1000)
# # data.sort(key =lambda x: ''.join(sort_list).find(x[0]) if ''.join(sort_list).find(x[0])>=0 else 1000)
# # print(data)
