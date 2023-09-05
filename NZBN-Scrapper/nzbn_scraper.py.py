import csv
import urllib.request
import json
import hubspot_upload
import update_contect
import os

filepath = os.path.abspath('.\\input')

filename = os.listdir(filepath)[0]
print(filename)

# filename = 'input/3.5k_NZBN+websites.csv'
try:
    with open('input//' + filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        with open('trandingName_output.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            keys = ['nzbn', 'tradingNames', 'entityName', 'phoneNumbers', 'Email', 'website_url', 'industry_code',
                    'first_name',
                    'last_name', 'addresses', 'entityType', 'gstNumber', 'careOf', 'address1', 'registrationDate',
                    'address2', 'address3', 'address4', 'postCode', 'countryCode', 'addressType']
            # Create a DictWriter object
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            for row in list(reader)[1:]:
                nzbn = row[1]
                # nzbn='9429036878215'
                url = f"https://api.business.govt.nz/gateway/nzbn/v5/entities/{nzbn}"
                hdr = {
                    'Cache-Control': 'no-cache',
                    'Ocp-Apim-Subscription-Key': 'f12248c855434c8ea9c6e18ef73a900e'
                }
                req = urllib.request.Request(url, headers=hdr)
                req.get_method = lambda: 'GET'
                response = urllib.request.urlopen(req)
                if response.getcode() == 200:
                    data_list = json.loads(response.read())
                    try:

                        tradingNames = data_list.get('tradingNames', '')
                        t_name = tradingNames[0].get('name', '') if tradingNames else ''
                    except:
                        t_name = ''
                    try:
                        phoneNumbers = data_list.get('phoneNumbers', '')
                        if phoneNumbers:
                            phoneNumber = phoneNumbers[0].get('phoneNumber', '')
                            phoneCountryCode = phoneNumbers[0].get('phoneCountryCode', '')
                            phoneAreaCode = phoneNumbers[0].get('phoneAreaCode', '')
                            full_phone_num = f"+{phoneCountryCode}{phoneAreaCode}{phoneNumber}"
                        else:
                            full_phone_num = ''
                    except:
                        full_phone_num = ''
                    try:
                        Email = data_list.get('emailAddresses', '')
                        emailAddress = Email[0].get('emailAddress', '') if Email else ''
                        website_url = data_list.get('websites', '')
                    except:
                        website_url = ''

                    try:
                        Url = website_url[0].get('url', '') if website_url else ''
                    except:
                        Url = ''

                    try:
                        industry_code = data_list.get('industryClassifications', '')
                        if industry_code:
                            Industry = industry_code[0].get('classificationCode', '')
                            Classification = industry_code[0].get('classificationDescription', '')
                            Industry_Classification = f"{Industry} {Classification}"
                        else:
                            Industry_Classification = ''
                    except:
                        Industry_Classification = ''
                    try:
                        role = data_list.get('roles')[0].get('rolePerson')
                        First_name = role.get('firstName', '').capitalize() if role else ''
                        last_name = role.get('lastName', '').capitalize() if role else ''
                    except:
                        First_name = ''
                        last_name = ''
                    # full_name = f"{First_name} {last_name}" if role else ''
                    addresses = data_list.get('addresses', '')
                    if addresses:
                        try:
                            try:
                                careOf = addresses.get('addressList')[0].get('careOf', '').title()
                            except:
                                careOf = ''
                            address1 = addresses.get('addressList')[0].get('address1', '')
                            address2 = addresses.get('addressList')[0].get('address2', '')
                            address3 = addresses.get('addressList')[0].get('address3', '')
                            address4 = addresses.get('addressList')[0].get('address4', '')
                            postCode = addresses.get('addressList')[0].get('postCode', '')
                            countryCode = addresses.get('addressList')[0].get('countryCode', '')
                            addressType = addresses.get('addressList')[0].get('addressType', '')
                        except:
                            careOf = ''
                            address1 = ''
                            address2 = ''
                            address3 = ''
                            address4 = ''
                            postCode = ''
                            countryCode = ''
                            addressType = ''
                    else:
                        careOf = ''
                        address1 = ''
                        address2 = ''
                        address3 = ''
                        address4 = ''
                        postCode = ''
                        countryCode = ''
                        addressType = ''
                    # addresse = list(addresses.get('addressList')[0].values())[3:] if addresses else ''
                    # New code block
                    try:
                        registrationDat = data_list.get('registrationDate', '') if data_list.get(
                            'registrationDate') else ''
                        if registrationDat:
                            registrationDate = registrationDat.split('T')[0]
                        else:
                            registrationDate = ''

                    except:
                        registrationDate = ''

                    try:
                        entityStatusDescription = data_list.get('entityStatusDescription', '') if data_list.get(
                            'entityStatusDescription') else ''
                    except:
                        entityStatusDescription = ''

                    try:
                        entityName = data_list.get('entityName', '')
                        if entityName:
                            entityName = entityName.capitalize()
                        else:
                            entityName = ''
                    except:
                        entityName = ''

                    try:
                        entityTypeDescription = data_list.get('entityTypeDescription', '') if data_list.get(
                            'entityTypeDescription') else ''
                    except:
                        entityTypeDescription = ''

                    try:
                        gstNumbers = data_list.get('gstNumbers', '')
                        if gstNumbers:
                            gstNumber = gstNumbers[0].get('gstNumber', '')
                        else:
                            gstNumber = ''
                    except:
                        gstNumber = ''

                    dict_data = {
                        "nzbn": f"'{nzbn}'",
                        'tradingNames': t_name,
                        'entityName': entityName,
                        'phoneNumbers': full_phone_num,
                        'Email': emailAddress,
                        'website_url': Url,
                        'industry_code': Industry_Classification,
                        'first_name': First_name,
                        'last_name': last_name,
                        'registrationDate': registrationDate,
                        'entityType': entityTypeDescription,
                        'gstNumber': gstNumber,
                        'careOf': careOf,
                        'address1': address1,
                        'address2': address2,
                        'address3': address3,
                        'address4': address4,
                        'postCode': postCode,
                        'countryCode': countryCode,
                        'addressType': addressType
                    }

                    company_inputs = {'name': entityName, 'nzbn': nzbn, 'tradingname': t_name, 'website': Url,
                                      'industry': Industry_Classification,
                                      'registrationdate': registrationDate, 'entitystatus': entityStatusDescription,
                                      'entity_type': entityTypeDescription, 'gstnumber': gstNumber, 'careof': careOf,
                                      'address': address1, 'address2': address2, 'zip': postCode,
                                      'country': countryCode, 'addresstype': addressType, 'nzbn_key': nzbn}

                    associatedcompanyid = row[0]
                    updatecompanyid = update_contect.update_company(associatedcompanyid, company_inputs)

                    writer.writerow(dict_data)
                    print(dict_data)
                else:
                    print(f"Error: {response.getcode()}")
except Exception as e:
    print(e)
