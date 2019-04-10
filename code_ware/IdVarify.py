from datetime import datetime as dtm

w = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
div = 11
mod = [1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2]
province = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
            "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
month = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG',
         '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}


def varify(card):
    if len(card) != 18:
        return '身份证长度错误'
    try:
        # 除最后一位以外ID
        id = card[:-1]
        tail = card[-1]
        tail = int(tail) if tail != 'X' else 10
        pro = card[0:2]
        gender = 'Female' if int(card[-2]) % 2 == 0 else 'Male'
    except:
        return '身份证输入错误'
    try:
        birth = card[6:14]
        y = birth[0:4]
        birthday = birth[4:8]
        mo = month[birthday[0:2]]
        birthday = f'{mo}-{birthday[2:4]}'
        birth = dtm.strptime(birth, "%Y%m%d")
        now = dtm.now()
        age = (now - birth).days // 365
    except ValueError:
        return ('身份证8位日期错误')
    except Exception as e:
        print(e)
    s = 0
    for i in range(len(id)):
        j = int(id[i])
        add = j * w[i]
        s += add
    dived = s % div
    dived = mod[dived]

    ret = {
        'Varify': dived == tail,
        'Gender': gender,
        'Birth': birth,
        'Birthday': birthday,
        'Porvince': province[pro],
        'Age': age
    }
    return ret


if __name__ == '__main__':
    PP = [{'Name': 'XXXX', 'ID': '450821199901015619'}]
    for i in PP:
        for k,v in i.items():
            if 'Name' in k:
                print(v)
            if 'ID' in k:
                print(varify(v))
        print('##############')