import pandas
from collections import defaultdict
import re


ULD_ID_DICT = {

}

###
# 流水号字典

file = r'C:\Users\邊\Desktop\副本ULD编号.xlsx'
df = pandas.read_excel(file, sheet_name='舱位比例')
d = df.T.to_dict()
dd = {}
for key, v in d.items():
	dd_value = defaultdict(dict)
	for k, value in v.items():
		if str(value) != 'nan':
			if key == 'B737':
				if int(k) <= 10:
					dd_value[k]['type'] = '主舱'
				elif int(k) <= 13:
					dd_value[k]['type'] = '后散'
				else:
					dd_value[k]['type'] = '前散'
			elif key == 'B757':
				if int(k) <= 16:
					dd_value[k]['type'] = '主舱'
				elif int(k) <= 19:
					dd_value[k]['type'] = '后散'
				else:
					dd_value[k]['type'] = '前散'
			elif key == 'B767':
				if int(k) <= 25:
					dd_value[k]['type'] = '主舱'
				elif int(k) <= 28:
					dd_value[k]['type'] = '下前'
				elif int(k) <= 31:
					dd_value[k]['type'] = '下后'
				else:
					dd_value[k]['type'] = '前散'
			elif key == 'B777':
				if int(k) <= 30:
					dd_value[k]['type'] = '主舱'
				elif int(k) <= 34:
					dd_value[k]['type'] = '下前'
				elif int(k) <= 37:
					dd_value[k]['type'] = '下后'
				else:
					dd_value[k]['type'] = '前散'
			else:
				if int(k) <= 34:
					dd_value[k]['type'] = '主舱'
				elif int(k) <= 38:
					dd_value[k]['type'] = '下前'
				elif int(k) <= 41:
					dd_value[k]['type'] = '下后'
				else:
					dd_value[k]['type'] = '前散'
			dd_value[k]['percent'] = value
	dd[key] = dd_value
del d
##

def add_0(num, n):
	if len(str(num)) < n:
		return '0' * (n - len(str(num))) + str(num)
	else:
		return str(num)

df = pandas.read_excel(file, sheet_name='进港ULD')
df_dict = df.T.to_dict()
uld_dict = {}
for value in df_dict.values():
	for k, v in value.items():
		if str(v) != 'nan':
			uld_dict[v] = str(k)
del df_dict

#######
print(uld_dict)

x = 0
result = {}
r = []
file = r'C:\Users\邊\Desktop\eq.xlsx'
df = pandas.read_excel(file)
for v in df.values:
	F_id, F_type, load, cross, dom, inter, loaded, empty = v
	id = re.findall(r'(\d+)', F_id)[0]
	flight = add_0(id, 4)
	total = int(loaded + empty)
	MHS = dom + inter
	if MHS - int(MHS) >= 0.5:
		MHS = int(MHS) + 1
	else:
		MHS = int(MHS)

	ID = 'ULD' + uld_dict[F_type]
	for i in range(1, total + 1):
		serial = add_0(i, 2)
		position = dd[F_type][i]['type']
		if i <= cross:
			uld_id = ID + uld_dict[position] + uld_dict['PAG'] + serial + uld_dict['次日直转国内'] + flight
			result[x] = uld_id
			r.append(uld_id)
			x += 1
		elif cross < i <= MHS + cross:
			uld_id = ID + uld_dict[position] + uld_dict['PAG'] + serial + uld_dict['次日进MHS国内'] + flight
			result[x] = uld_id
			r.append(uld_id)
			x += 1
		else:
			uld_id = ID + uld_dict[position] + uld_dict['PAG'] + serial + uld_dict['空箱'] + flight
			result[x] = uld_id
			r.append(uld_id)
			x += 1

q = pandas.DataFrame(r, index=range(len(r)))
q.to_excel(r'C:\Users\邊\Desktop\ULD编号.xlsx', index=False)