from datetime import datetime as dtm
import globalPara as gp

w = gp.weight
div = gp.div
mod = gp.mod
province = gp.province
month = gp.month
countries = gp.countries


def varify(card):
    # global country, city, age, pro, birthday, birth
    if len(card) != 18:
        return '身份证长度错误'
    try:
        # 除最后一位以外ID
        id = card[:-1]
        tail = card[-1]
        tail = int(tail) if tail != 'X' else 10
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
        country = card[0:6]
        city = card[0:4]
        pro = card[0:2]
        city = f'{card[0:4]}00'
        pro = f'{card[0:2]}0000'
        country = countries[country] if country in countries else f'行政区{country}已被撤销'
        city = countries[city] if city in countries else f'行政区{city}已被撤销'
        pro = countries[pro] if pro in countries else f'行政区{country}已被撤销'
    except ValueError:
        return ('身份证8位日期错误')
    except Exception as e:
        print(e)
    s = 0
    for id_index in range(len(id)):
        j = int(id[id_index])
        add = j * w[id_index]
        s += add
    dived = s % div
    dived = mod[dived]

    ret = {
        'Varify': dived == tail,
        'Gender': gender,
        'Birth': birth,
        'Birthday': birthday,
        'Porvince': pro,
        'Age': age,
        'City': city,
        'Country': country,
    }
    return ret


if __name__ == '__main__':
    PP = [{'Name': 'XXXX', 'ID': '450821199901015619'}]
    for i in PP:
        for k, v in i.items():
            if 'Name' in k:
                print(v)
            if 'ID' in k:
                print(varify(v))
