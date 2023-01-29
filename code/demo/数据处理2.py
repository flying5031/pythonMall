data = [
    ['一队',3,5,2],
    ['二队',3,6,2],
    ['三队一纵队',2,2,3],
    ['三队二纵队',3,1,3],
    ['七队',1,7,3],
    ['四队一纵队',3,2,3],
    ['四队二纵队',3,3,3]
]
merge_list = ['三队','四队']
sort_list = ['一队','二队','三队','四队','五队','六队','七队']


# 分组，求和，合并
# 数据分拣
merge_dict = {i:[] for i in merge_list + ['others']}
for list_data in data:
    is_merge = list(map(lambda x:list_data[0].find(x) == 0,merge_list))
    if any(is_merge):
        merge_name = merge_list[is_merge.index(True)]
        merge_dict[merge_name].append(list_data)
    else:
        merge_dict['others'].append(list_data)
#数据合并
for k in merge_dict:
    if k != 'others':
        sum_list =[sum(i) for i in list(zip(*merge_dict[k]))[1:]]
        merge_dict['others'].append([k] +sum_list)

data = merge_dict['others']

# 行求和
for l in data:
    l.append(sum(l[1:]))

#列求和
sumlist = [sum(l) for l in list(zip(*data))[1:]]
data.append(['总和'] + sumlist)

#设置默认数据
#列名
idx_cols = [i[0] for i in data]
pro_list = [[col] + [0]*(len(data[0])-1) for col in sort_list if not any(map(lambda x:x.find(col) == 0, idx_cols))]
data = data + pro_list
#排序
data.sort(key = lambda x: v if (v:=''.join(sort_list).find(x[0]))>=0 else 1000)
# data.sort(key =lambda x: ''.join(sort_list).find(x[0]) if ''.join(sort_list).find(x[0])>=0 else 1000)

print(data)
