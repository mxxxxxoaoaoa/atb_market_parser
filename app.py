import driver
import json
from multiprocessing.pool import Pool

if __name__ == '__main__':
    # init ATB driver
    atb = driver.AtbWebDriver()
    n = 5 # number of proccess for multithreading

    categories = atb.get_all_categories() # get all categories
    
    chunks = [categories[i:i + n] for i in range(0, len(categories), n)] # cutting chunks for multithreading proccessing

    data = []
    l = len(chunks)
    for ind, chunk in enumerate(chunks):
        print(f"getting pagination. {ind+1}/{l}",end = " ")
        p = Pool(processes=n)
        m = p.map_async(atb.get_paginations, chunk) # run in async func for getting pagination
        m.wait()
        try:
            res = m.get()
            for i in res:
                data.append(i)
            print('succesfuly')
        except Exception as e:
            print('error: ', e)
            
    
    atb.return_data(data)

    chunks = [data[i:i + n] for i in range(0, len(data), n)] 
    l = len(chunks)
    for ind, chunk in enumerate(chunks):
        print(f"getting products. {ind+1}/{l}",end = " ")
        p = Pool(processes=n)
        m = p.map_async(atb.get_product, chunk) # run in async func for getting products by category
        m.wait()
        try:
            res = m.get()
            for i in res:
                with open(f'{i["title"]}.json', 'w+', encoding='utf-8') as f:
                    json.dump(i, f, indent=6, ensure_ascii=False)
                    f.close()
            print('succesfuly')
        except Exception as e:
            print('error: ', e)