import xlwt


def compare():
    fileName1 = r'C:\Users\Administrator\Desktop\深圳IXP\2022-12\2022-12.csv'
    fileName2 = r'C:\Users\Administrator\Desktop\深圳IXP\2022-12\202304271413.csv'

    with open(fileName1, 'r', encoding='utf-8') as f1:
        data1 = f1.readlines()
    with open(fileName2, 'r', encoding='utf-8') as f2:
        data2 = f2.readlines()
    for line1 in data1:
        list1 = line1.split(',')
        deviceName1 = list1[2]
        port1 = list1[3]
        peak1 = list1[7]
        for line2 in data2:
            list2 = line2.split(',')
            # deviceName2 = '"'+list2[0]+'"'
            deviceName2 = list2[0]
            # port2 = '"'+list2[1]+'"'
            port2 = list2[1]
            #print(port1 + ":" + port2)
            if deviceName2 == deviceName1 and port1 == port2:
                #print(int(list2[5]) + ":" + int(list2[6]))
                peak_input = int(float((list2[5])))
                peak_output = int(float((list2[6])))
                if peak_input >= peak_output:
                    #peak2 = '"' + list2[5] + '"'
                    peak2 = str(peak_input)
                else:
                    #peak2 = '"' + list2[6] + '"'
                    peak2 = str(peak_output)
                peak1=round(peak1,2)
                if peak1 != peak2:
                    print(deviceName1 + '-' + port1 + ': ' + peak1 + '不等于' + peak2)


if __name__ == "__main__":
    compare()
