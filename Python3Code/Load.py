import pandas as pd

phone_acc_list = """datasets/phone/accel/data_1600_accel_phone.txt
datasets/phone/accel/data_1601_accel_phone.txt
datasets/phone/accel/data_1602_accel_phone.txt
datasets/phone/accel/data_1603_accel_phone.txt
datasets/phone/accel/data_1604_accel_phone.txt
datasets/phone/accel/data_1605_accel_phone.txt
datasets/phone/accel/data_1606_accel_phone.txt
datasets/phone/accel/data_1607_accel_phone.txt
datasets/phone/accel/data_1608_accel_phone.txt
datasets/phone/accel/data_1609_accel_phone.txt
datasets/phone/accel/data_1610_accel_phone.txt
datasets/phone/accel/data_1611_accel_phone.txt
datasets/phone/accel/data_1612_accel_phone.txt
datasets/phone/accel/data_1613_accel_phone.txt
datasets/phone/accel/data_1614_accel_phone.txt
datasets/phone/accel/data_1615_accel_phone.txt
datasets/phone/accel/data_1616_accel_phone.txt
datasets/phone/accel/data_1617_accel_phone.txt
datasets/phone/accel/data_1618_accel_phone.txt
datasets/phone/accel/data_1619_accel_phone.txt
datasets/phone/accel/data_1620_accel_phone.txt
datasets/phone/accel/data_1621_accel_phone.txt
datasets/phone/accel/data_1622_accel_phone.txt
datasets/phone/accel/data_1623_accel_phone.txt
datasets/phone/accel/data_1624_accel_phone.txt
datasets/phone/accel/data_1625_accel_phone.txt
datasets/phone/accel/data_1626_accel_phone.txt
datasets/phone/accel/data_1627_accel_phone.txt
datasets/phone/accel/data_1628_accel_phone.txt
datasets/phone/accel/data_1629_accel_phone.txt
datasets/phone/accel/data_1630_accel_phone.txt
datasets/phone/accel/data_1631_accel_phone.txt
datasets/phone/accel/data_1632_accel_phone.txt
datasets/phone/accel/data_1633_accel_phone.txt
datasets/phone/accel/data_1634_accel_phone.txt
datasets/phone/accel/data_1635_accel_phone.txt
datasets/phone/accel/data_1636_accel_phone.txt
datasets/phone/accel/data_1637_accel_phone.txt
datasets/phone/accel/data_1638_accel_phone.txt
datasets/phone/accel/data_1639_accel_phone.txt
datasets/phone/accel/data_1640_accel_phone.txt
datasets/phone/accel/data_1641_accel_phone.txt
datasets/phone/accel/data_1642_accel_phone.txt
datasets/phone/accel/data_1643_accel_phone.txt
datasets/phone/accel/data_1644_accel_phone.txt
datasets/phone/accel/data_1645_accel_phone.txt
datasets/phone/accel/data_1646_accel_phone.txt
datasets/phone/accel/data_1647_accel_phone.txt
datasets/phone/accel/data_1648_accel_phone.txt
datasets/phone/accel/data_1649_accel_phone.txt
datasets/phone/accel/data_1650_accel_phone.txt
"""

phone_gyr_list = """datasets/phone/gyro/data_1600_gyro_phone.txt
datasets/phone/gyro/data_1601_gyro_phone.txt
datasets/phone/gyro/data_1602_gyro_phone.txt
datasets/phone/gyro/data_1603_gyro_phone.txt
datasets/phone/gyro/data_1604_gyro_phone.txt
datasets/phone/gyro/data_1605_gyro_phone.txt
datasets/phone/gyro/data_1606_gyro_phone.txt
datasets/phone/gyro/data_1607_gyro_phone.txt
datasets/phone/gyro/data_1608_gyro_phone.txt
datasets/phone/gyro/data_1609_gyro_phone.txt
datasets/phone/gyro/data_1610_gyro_phone.txt
datasets/phone/gyro/data_1611_gyro_phone.txt
datasets/phone/gyro/data_1612_gyro_phone.txt
datasets/phone/gyro/data_1613_gyro_phone.txt
datasets/phone/gyro/data_1614_gyro_phone.txt
datasets/phone/gyro/data_1615_gyro_phone.txt
datasets/phone/gyro/data_1616_gyro_phone.txt
datasets/phone/gyro/data_1617_gyro_phone.txt
datasets/phone/gyro/data_1618_gyro_phone.txt
datasets/phone/gyro/data_1619_gyro_phone.txt
datasets/phone/gyro/data_1620_gyro_phone.txt
datasets/phone/gyro/data_1621_gyro_phone.txt
datasets/phone/gyro/data_1622_gyro_phone.txt
datasets/phone/gyro/data_1623_gyro_phone.txt
datasets/phone/gyro/data_1624_gyro_phone.txt
datasets/phone/gyro/data_1625_gyro_phone.txt
datasets/phone/gyro/data_1626_gyro_phone.txt
datasets/phone/gyro/data_1627_gyro_phone.txt
datasets/phone/gyro/data_1628_gyro_phone.txt
datasets/phone/gyro/data_1629_gyro_phone.txt
datasets/phone/gyro/data_1630_gyro_phone.txt
datasets/phone/gyro/data_1631_gyro_phone.txt
datasets/phone/gyro/data_1632_gyro_phone.txt
datasets/phone/gyro/data_1633_gyro_phone.txt
datasets/phone/gyro/data_1634_gyro_phone.txt
datasets/phone/gyro/data_1635_gyro_phone.txt
datasets/phone/gyro/data_1636_gyro_phone.txt
datasets/phone/gyro/data_1637_gyro_phone.txt
datasets/phone/gyro/data_1638_gyro_phone.txt
datasets/phone/gyro/data_1639_gyro_phone.txt
datasets/phone/gyro/data_1640_gyro_phone.txt
datasets/phone/gyro/data_1641_gyro_phone.txt
datasets/phone/gyro/data_1642_gyro_phone.txt
datasets/phone/gyro/data_1643_gyro_phone.txt
datasets/phone/gyro/data_1644_gyro_phone.txt
datasets/phone/gyro/data_1645_gyro_phone.txt
datasets/phone/gyro/data_1646_gyro_phone.txt
datasets/phone/gyro/data_1647_gyro_phone.txt
datasets/phone/gyro/data_1648_gyro_phone.txt
datasets/phone/gyro/data_1649_gyro_phone.txt
datasets/phone/gyro/data_1650_gyro_phone.txt
"""

watch_acc_list = """datasets/watch/accel/data_1600_accel_watch.txt
datasets/watch/accel/data_1601_accel_watch.txt
datasets/watch/accel/data_1602_accel_watch.txt
datasets/watch/accel/data_1603_accel_watch.txt
datasets/watch/accel/data_1604_accel_watch.txt
datasets/watch/accel/data_1605_accel_watch.txt
datasets/watch/accel/data_1606_accel_watch.txt
datasets/watch/accel/data_1607_accel_watch.txt
datasets/watch/accel/data_1608_accel_watch.txt
datasets/watch/accel/data_1609_accel_watch.txt
datasets/watch/accel/data_1610_accel_watch.txt
datasets/watch/accel/data_1611_accel_watch.txt
datasets/watch/accel/data_1612_accel_watch.txt
datasets/watch/accel/data_1613_accel_watch.txt
datasets/watch/accel/data_1614_accel_watch.txt
datasets/watch/accel/data_1615_accel_watch.txt
datasets/watch/accel/data_1616_accel_watch.txt
datasets/watch/accel/data_1617_accel_watch.txt
datasets/watch/accel/data_1618_accel_watch.txt
datasets/watch/accel/data_1619_accel_watch.txt
datasets/watch/accel/data_1620_accel_watch.txt
datasets/watch/accel/data_1621_accel_watch.txt
datasets/watch/accel/data_1622_accel_watch.txt
datasets/watch/accel/data_1623_accel_watch.txt
datasets/watch/accel/data_1624_accel_watch.txt
datasets/watch/accel/data_1625_accel_watch.txt
datasets/watch/accel/data_1626_accel_watch.txt
datasets/watch/accel/data_1627_accel_watch.txt
datasets/watch/accel/data_1628_accel_watch.txt
datasets/watch/accel/data_1629_accel_watch.txt
datasets/watch/accel/data_1630_accel_watch.txt
datasets/watch/accel/data_1631_accel_watch.txt
datasets/watch/accel/data_1632_accel_watch.txt
datasets/watch/accel/data_1633_accel_watch.txt
datasets/watch/accel/data_1634_accel_watch.txt
datasets/watch/accel/data_1635_accel_watch.txt
datasets/watch/accel/data_1636_accel_watch.txt
datasets/watch/accel/data_1637_accel_watch.txt
datasets/watch/accel/data_1638_accel_watch.txt
datasets/watch/accel/data_1639_accel_watch.txt
datasets/watch/accel/data_1640_accel_watch.txt
datasets/watch/accel/data_1641_accel_watch.txt
datasets/watch/accel/data_1642_accel_watch.txt
datasets/watch/accel/data_1643_accel_watch.txt
datasets/watch/accel/data_1644_accel_watch.txt
datasets/watch/accel/data_1645_accel_watch.txt
datasets/watch/accel/data_1646_accel_watch.txt
datasets/watch/accel/data_1647_accel_watch.txt
datasets/watch/accel/data_1648_accel_watch.txt
datasets/watch/accel/data_1649_accel_watch.txt
datasets/watch/accel/data_1650_accel_watch.txt
"""

watch_gyr_list = """datasets/watch/gyro/data_1600_gyro_watch.txt
datasets/watch/gyro/data_1601_gyro_watch.txt
datasets/watch/gyro/data_1602_gyro_watch.txt
datasets/watch/gyro/data_1603_gyro_watch.txt
datasets/watch/gyro/data_1604_gyro_watch.txt
datasets/watch/gyro/data_1605_gyro_watch.txt
datasets/watch/gyro/data_1606_gyro_watch.txt
datasets/watch/gyro/data_1607_gyro_watch.txt
datasets/watch/gyro/data_1608_gyro_watch.txt
datasets/watch/gyro/data_1609_gyro_watch.txt
datasets/watch/gyro/data_1610_gyro_watch.txt
datasets/watch/gyro/data_1611_gyro_watch.txt
datasets/watch/gyro/data_1612_gyro_watch.txt
datasets/watch/gyro/data_1613_gyro_watch.txt
datasets/watch/gyro/data_1614_gyro_watch.txt
datasets/watch/gyro/data_1615_gyro_watch.txt
datasets/watch/gyro/data_1616_gyro_watch.txt
datasets/watch/gyro/data_1617_gyro_watch.txt
datasets/watch/gyro/data_1618_gyro_watch.txt
datasets/watch/gyro/data_1619_gyro_watch.txt
datasets/watch/gyro/data_1620_gyro_watch.txt
datasets/watch/gyro/data_1621_gyro_watch.txt
datasets/watch/gyro/data_1622_gyro_watch.txt
datasets/watch/gyro/data_1623_gyro_watch.txt
datasets/watch/gyro/data_1624_gyro_watch.txt
datasets/watch/gyro/data_1625_gyro_watch.txt
datasets/watch/gyro/data_1626_gyro_watch.txt
datasets/watch/gyro/data_1627_gyro_watch.txt
datasets/watch/gyro/data_1628_gyro_watch.txt
datasets/watch/gyro/data_1629_gyro_watch.txt
datasets/watch/gyro/data_1630_gyro_watch.txt
datasets/watch/gyro/data_1631_gyro_watch.txt
datasets/watch/gyro/data_1632_gyro_watch.txt
datasets/watch/gyro/data_1633_gyro_watch.txt
datasets/watch/gyro/data_1634_gyro_watch.txt
datasets/watch/gyro/data_1635_gyro_watch.txt
datasets/watch/gyro/data_1636_gyro_watch.txt
datasets/watch/gyro/data_1637_gyro_watch.txt
datasets/watch/gyro/data_1638_gyro_watch.txt
datasets/watch/gyro/data_1639_gyro_watch.txt
datasets/watch/gyro/data_1640_gyro_watch.txt
datasets/watch/gyro/data_1641_gyro_watch.txt
datasets/watch/gyro/data_1642_gyro_watch.txt
datasets/watch/gyro/data_1643_gyro_watch.txt
datasets/watch/gyro/data_1644_gyro_watch.txt
datasets/watch/gyro/data_1645_gyro_watch.txt
datasets/watch/gyro/data_1646_gyro_watch.txt
datasets/watch/gyro/data_1647_gyro_watch.txt
datasets/watch/gyro/data_1648_gyro_watch.txt
datasets/watch/gyro/data_1649_gyro_watch.txt
datasets/watch/gyro/data_1650_gyro_watch.txt"""

datasets = [phone_acc_list, phone_gyr_list, watch_acc_list, watch_gyr_list]

field_names = ['activity', 'timestamp', 'x', 'y', 'z']
for i in range(len(datasets)):
    datasets[i] = datasets[i].splitlines()

def load_to_dataframe(path):
    data = pd.read_csv(path, header=None, index_col=0)
    data = data.rename(columns={i + 1: field_names[i] for i in range(len(field_names))})
    data['z'] = data['z'].apply(lambda x: x.replace(';', ''))
    print(data)

if __name__ == '__main__':
    load_to_dataframe(datasets[0][0])
