import threading
import ctypes
import time
import copy
import pandas as pd
import random
from tkinter import *
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import pickle
import colorama
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


class Util():
    def progress_bar(progress, total, text, reward):
        percent = 50 * (progress / total)
        bar = '=' * int(percent) + '-' * (50 - int(percent))
        print(colorama.Fore.GREEN + f"\r{text}: |{bar}| {percent * 2:.2f}% - {reward}", end='\r')

    def save_load(s_l_nps_npl, filename, obj):
        if s_l_nps_npl == 0:
            sfile = open(filename, 'wb')
            pickledobj = pickle.dumps(obj)
            sfile.write(pickledobj)
            sfile.close()
        if s_l_nps_npl == 1:
            sfile = open(filename, 'rb')
            pickledobj = sfile.read()
            obj = pickle.loads(pickledobj)
            sfile.close()
            return obj
        if s_l_nps_npl == 2:
            #print("Dammit")
            np.save(filename, obj)
        if s_l_nps_npl == 3:
            obj = np.load(filename, allow_pickle=True)
            return obj
        
        #print("Dammit Kris, what did you input!!!")
        return None

    def file_exists(file_name):
        return Path(file_name).is_file()
    
    def find_nearest(array, value):
        #array = np.asarray(array)
        if isinstance(value, pd._libs.tslibs.timestamps.Timestamp):
            value = value.to_pydatetime()
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx
    
    def round_to_nearest_max(number):
        magnitude = 10 ** (len(str(int(number))))
        if number < 1:
            return 10
        return magnitude

    def dt64todt(date):
        return pd.Timestamp(date)
    
    def date_after_now(days=0, months=0, years=0):
        day_count = days + months * 30 + years * 365
        return datetime.now() + timedelta(days= - day_count)
    
    def convert_secs(dates):
        convert_dates = []
        for i in dates:
            convert_dates.append((i - datetime(1970, 1, 1)).total_seconds())
        return np.array(convert_dates)
    
    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)
    
    def avg_dates(dates):
        any_reference_date = np.min(dates)
        return any_reference_date + sum([date - any_reference_date for date in dates], timedelta()) / len(dates)
    
    def average_by_func(list_list, func):
        average_list = []
        for li in range(len(list_list[0])):
            mini_list_count = []
            for lli in range(len(list_list)):
                mini_list_count.append(list_list[lli][li])
            average_list.append(func(mini_list_count))
        return np.array(average_list)
    
    def cool_name_generator():
        adjective = [
            'epic',
            'cool',
            'giga',
            'chad',
            'sexy',
            'zamn',
            'best',
            'omniscient',
            'omnipotent',
            'lucky',
            'damn',
            'bammy',
            'tem',
            'techsupport'
        ]
        nouns = [
            'model',
            'saulgoodman',
            'god',
            'airplane',
            'phrog',
            'quacker',
            'usfg',
            'grin',
            'aria',
            'harry',
            'abhay',
            'aarav',
            'ameya',
            'meeks'
        ]

        current_date = datetime.now()
        int_date = current_date.year*10000000000 + current_date.month * 100000000 + current_date.day * 1000000 + current_date.hour*10000 + current_date.minute*100 + current_date.second

        return f"{random.choice(adjective)}_{random.choice(nouns)}-{int_date}"

    def min_max_scaling(data, min_value, max_value):
        """
        Perform Min-Max scaling on the data within the specified range [min_value, max_value].
        """
        min_data = np.min(data)
        max_data = np.max(data)
        scaled_data = min_value + (max_value - min_value) * (data - min_data) / ((max_data - min_data) + 1e-8)
        return scaled_data

