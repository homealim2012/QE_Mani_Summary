def progress_bar(num, total, info):
    rate = float(num)/total
    ratenum = int(100*rate)
    print('\r[{}{}]{}%-{}'.format('*'*ratenum, ' '*(100-ratenum), ratenum, info), end='')
