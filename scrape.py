from bs4 import BeautifulSoup


def generate_data_dict(raw_data: list, data_name: str):
    obj = {
        data_name: {}
    }
    for el in raw_data[1:]:
        new_key = el[0].lower().strip().replace('°', '').replace(' ', '')
        obj[data_name][new_key] = el[1]
    # print('GENERATE DATRA DICT', obj, '\n')
    return obj


def go_scrape(page_source: str):
    soup = BeautifulSoup(page_source, 'lxml')

    # Find tblDataVehicle
    TABLE_ID = 'tblDataVehicle'
    table = soup.find('table', id=TABLE_ID)
    try:
        rows = table.findAll('tr')
        frmtd_rows = []
        for row in rows:
            tds = row.find_all('td')
            row_text = []
            for td in tds:
                row_text.append(td.text.strip())

            frmtd_rows.append(row_text)

        # print(frmtd_rows)

        owner_data_index = frmtd_rows.index([''])
        raw_owner_data = frmtd_rows[:owner_data_index]
        # print("OWNER_INDEX", owner_data_index, "RAW_OWNER_DATA", raw_owner_data)

        frmtd_rows = frmtd_rows[owner_data_index+1:]

        car_data_index = frmtd_rows.index([''])
        raw_car_data = frmtd_rows[:car_data_index]
        # print("CAR_INDEX", car_data_index, "RAW_OWNER_DATA", raw_car_data)

        frmtd_rows = frmtd_rows[car_data_index+1:]

        raw_extra_data = frmtd_rows
        # print("RAW_EXTRA_DATA", raw_extra_data)

        # Generate data objects
        owner_data = generate_data_dict(raw_owner_data, 'owner_data')
        car_data = generate_data_dict(raw_car_data, 'car_data')
        extra_data = generate_data_dict(raw_extra_data, 'extra_data')

        data = {
            **owner_data,
            **car_data,
            **extra_data}
        print(data)

        return data
    except:
        print("ERROR IN THE PLATE")
        return {"message": "Invalid Plate"}

    # raw_owner_data = frmtd_rows[:(frmtd_rows.index(['']))]
