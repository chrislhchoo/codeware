import pandas as pd
import multiprocessing as mp

a = {
    'a': ['Feb 23 2018', 'Feb-23-2018', '2011/01/01', '2011-01-01', '12-03-2018'],
    'b': ['a', 'a', 'b', 'b', 'a']
}

b = pd.DataFrame(a)
b['a'] = pd.to_datetime(b['a'])
b = pd.concat([b for i in range(100000)])


def compre(**k):
    obj=k['obj']
    type=k['type']
    folder = r'zip/'
    file= f'{folder}to_csv_{type}.{type}'
    if type == 'txt':
        compression = None
    else:
        compression =type
    obj.to_csv(file, index=False, encoding='utf8', compression=compression)
if __name__=='__main__':
    p = []
    type = ['gzip', 'bz2', 'zip', 'xz', 'txt']
    for i in type:
        k={
            'type':i,
            'obj':b
        }
        p.append(mp.Process(target=compre, kwargs=k), )

    for i in p:
        i.start()
    for i in p:
        i.join()
    print('Finished')
