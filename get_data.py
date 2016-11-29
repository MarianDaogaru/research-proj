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

    data = {"LEO" : '',
            "GEO" : '',
            "MEO" : '',
            "Elliptical" : ''}

    for i in range(len(read_file[cols[0]])):
        msg = ""
        for j in range(len(cols)):
            # getting rid of , in apogee and perigee height
            if j != 5 or j != 6:
                msg += str(read_file[cols[j]][i]) + '!'
            else:
                # split the initial string where the comma is,and then join it
                msg += str(''.join(read_file[cols[j]][i].split(',')))
        if str(read_file[cols[2]][i]) != 'nan':
            data[(read_file[cols[2]][i].split())[0]] += msg + "\n"

    with open("sorted.txt", 'w') as dat:
        for key in data.keys():
            dat.write("?{}:{}?\n\n\n".format(key, str(data[key])))

    return None
#sort_data()

def retreive_data(orb):
    with open("sorted.txt", "r") as dat:
        msg = dat.read()

    msg = msg.split("?")
    dat = []
    for i in range(len(msg)):
        if len(msg[i]) >8 :
            dat.append(msg[i])
    data = {}
    for i in range(len(dat)):
        msg = dat[i].split(":")
        data[msg[0]] = msg[1]



#retreive_data(2)
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
