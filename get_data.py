"""
Code to sort nicely the data from the Satelite database excel file,
from concerned scientist.

Author: Marian Daogaru, md2g12@soton.ac.uk
Created on: 27/11/2016
Last update: 29/11/2016

used for FEEG6023 - Individual Research Project module,
part of First Taught year for NGCM iPhD.
"""



from math import isnan
import numpy
import matplotlib.pyplot as plt
import pandas


def get_excel():
    try:
        return pandas.read_excel("/PhD/First year/Courses/FEEG 6023 - Individual Research Project/Documents/UCS_Satellite_Database_7-1-16.xls")
    except FileNotFoundError:
        print("No such file was found")
        return None


def get_columns():
    read_file = get_excel()
    columns = read_file.columns
    del read_file
    columns = [columns[0], columns[5], columns[7], columns[8],
               columns[9], columns[10], columns[11], columns[12],
               columns[13], columns[14], columns[15], columns[17]]
    """Name, purpose, class of orbit, type of orbit, longitutde of GEO, perigee, apogee
    eccentricity, inclination, period, launch mass, power """
    return columns


def all_2_txt():
    msg = ""
    read_file = get_excel()
    cols = get_columns()
    for i in range(len(read_file[cols[0]])):
        for j in range(len(cols)):
            msg += str(read_file[cols[j]][i]) + '!'
        msg += '\n'
    with open('all_data.txt', 'w') as dat:
        dat.write(msg)

    del(dat, msg, read_file)
    return orbits


def sort_data():
    read_file = get_excel()
    cols = get_columns()

    data = {'LEO' : {},
            'GEO' : {},
            'MEO' : {},
            'Elliptical' : {}
            }
    mission_types_all = []

    for i in range(len(read_file[cols[0]])):
        # make the message
        msg = ''
        for j in range(len(cols)):
            # getting rid of , in apogee and perigee height
            if j != 5 or j != 6:
                msg += str(read_file[cols[j]][i]) + '!'
            else:
                # split the initial string where the comma is,and then join it
                msg += str(''.join(read_file[cols[j]][i].split(',')))

        # construct the message by getting the correct orbit & mission type
        orbit = (str(read_file[cols[2]][i]).split())[0]
        if orbit != 'nan':
            mission_type = str(read_file[cols[1]][i]).split('/')
            for mission in mission_type:
                if mission not in data[orbit].keys():
                    data[orbit][mission] = ''
                data[orbit][mission] += msg + "\n"

                # get all different types of mission types
                if mission not in mission_types_all:
                    mission_types_all.append(mission)

    with open("sorted.txt", 'w') as dat:
        for key in data.keys():
            dat.write('?{}:{}?\n\n\n'.format(key, str(data[key])))
    del (dat)

    with open("mission_types.txt", "w") as mt:
        for mis in mission_types_all:
            mt.write('{}\n'.format(str(mis)))
    del (mt)

    return None
#sort_data()


def retreive_data(orb):
    with open("sorted.txt", "r") as dat:
        msg = dat.read()
    del (dat)

    msg = msg.split("?")
    dat = []
    for i in range(len(msg)):
        if len(msg[i]) > 8:
            dat.append(msg[i])
    del(msg)
    data = {}
    for i in range(len(dat)):
        msg = dat[i].split("{")
        orbit = msg[0].replace(":","")
        msg[1] = msg[1].replace("}","")
        missions = {}
        missions_n_SC = msg[1].split(":")
        missions[str(missions_n_SC[0].replace("'",""))] = (str(missions_n_SC[1][:missions_n_SC[1].rfind(",")])).replace("'","")
        for j in range(1, len(missions_n_SC)-2):
            type_index = missions_n_SC[j].rfind(",")
            SC_index = missions_n_SC[j+1].rfind(",")
            missions[str(missions_n_SC[j][type_index:].replace("'","")).replace(", ", "")] = (str(missions_n_SC[j+1][:SC_index])).replace("'","")
        missions[str(missions_n_SC[-2][missions_n_SC[-2].rfind(","):].replace("'","")).replace(", ", "")] = (str(missions_n_SC[-1])).replace("'","")
        data[orbit] = missions

    return data


a = retreive_data(2)
def plot_bit(n):
    read_file = get_excel()
    cols = get_columns()
    # data = numpy.zeros(len(read_file[cols[0]]))
    data = []
    for i in range(len(read_file[cols[0]])):
        if float(read_file[cols[n]][i]) != 0:
            data.append( float(read_file[cols[n]][i]))

    plt.plot(data, "b*")
    plt.show()
    return None
