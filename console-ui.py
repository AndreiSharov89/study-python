import model

def paginate_dict (data, page, items_per_page = 20):
    data_items = list(data.items())
    total_pages = (len(data_items) + items_per_page - 1) // items_per_page
    if page < 1 or page > total_pages:
        return {}, total_pages
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = dict(data_items[start_index:end_index])
    return paginated_data, total_pages
def paginate_list (data, page, items_per_page = 20):
    total_pages = (len(data) + items_per_page - 1)  // items_per_page
    if page < 1 or page > total_pages:
        return {}, total_pages
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_data = data[start_index:end_index]
    return paginated_data, total_pages

print('Hello!')
if __name__ == "__main__":
    while True:
        FLAG = False
        print('''\n1. Show all markets\n2. Find markets by city and State\n3. Find markets by zip\n4. Next menu\n0. Exit\n
    To select the menu function, enter a number (1, 2, 3, 4 or 0) and press Enter:\n''')
        print('What would you like to do? ')
        n = input()
        if n == '1':
            FLAG = True
            data_temp = model.all_markets()
            current_page = 1
            while True:
                page_data, total_pages = paginate_dict(data_temp, current_page, 5)
                print(f"\nPage: {current_page}/{total_pages}")
                for key, value in page_data.items():
                    print(f"{key}\n{value[0][0][0]}\n{value[0][0][1]}, {value[0][0][2]}, {value[0][0][3]}\n{value[1]}\n")
                print("\nNavigation: n - Next page | p - Previous page | e - Exit")
                choice = input("\nChoose an option: ").strip().lower()
                if choice == 'n':
                    if current_page < total_pages:
                        current_page += 1
                    else: print("You are already on the last page.")
                elif choice == 'p':
                    if current_page > 1:
                        current_page -= 1
                    else: print("You are already on the first page.")
                elif choice == 'e':
                    print("Exiting pagination..")
                    break
                else:
                    print("Invald option. Please choose again.")
        elif n == '2':
            city = input('Please, enter the city: ')
            state = input('Please, enter the State: ')
            data_temp = model.id_by_location(city, state)
            if type(data_temp) != "<class 'NoneType'>":
                FLAG = True
                current_page = 1
                while True:
                    page_data, total_pages = paginate_list(data_temp, current_page, 5)
                    print(f"\nPage: {current_page}/{total_pages}")
                    combined_markets = {}
                    for m_id in page_data:
                        print(f"\n{m_id}")
                        markets = model.market_by_id(m_id)
                        print(f"{markets[0]}\n {markets[1]}\n")
                    print("\nNavigation: n - Next page | p - Previous page | e - Exit")
                    choice = input("\nChoose an option: ").strip().lower()
                    if choice == 'n':
                        if current_page < total_pages:
                            current_page += 1
                        else:
                            print("You are already on the last page.")
                    elif choice == 'p':
                        if current_page > 1:
                            current_page -= 1
                        else:
                            print("You are already on the first page.")
                    elif choice == 'e':
                        print("Exiting pagination..")
                        break
                    else:
                        print("Invald option. Please choose again.")
            else:
                print('Nothing was found. May be an error in the request.')

        elif n == '3':
            zip_code = input('Please, enter the zip code: ')
            distance = float(input('Chose distance, miles: '))
            if distance == 0:
                data_temp = model.id_by_zip(zip_code)
                if data_temp is not None:
                    FLAG = True
                    current_page = 1
                    while True:
                        page_data, total_pages = paginate_list(data_temp, current_page, 5)
                        print(f"\nPage: {current_page}/{total_pages}")
                        for m_id in page_data:
                            print(f"\n{m_id}")
                            market = model.market_by_id_full(m_id)
                            print(f"{market[0][0]}\n{market[0][1]}\n{market[1]}\n")
                        print("\nNavigation: n - Next page | p - Previous page | e - Exit")
                        choice = input("\nChoose an option: ").strip().lower()
                        if choice == 'n':
                            if current_page < total_pages:
                                current_page += 1
                            else:
                                print("You are already on the last page.")
                        elif choice == 'p':
                            if current_page > 1:
                                current_page -= 1
                            else:
                                print("You are already on the first page.")
                        elif choice == 'e':
                            print("Exiting pagination..")
                            break
                        else:
                            print("Invald option. Please choose again.")
                else:
                    print('Nothing was found. May be an error in the request.')
            else:
                data_temp = model.id_by_zip_and_distance(zip_code, distance)
                if data_temp is not None:
                    FLAG = True
                    current_page = 1
                    while True:
                        page_data, total_pages = paginate_list(data_temp, current_page, 5)
                        print(f"\nPage: {current_page}/{total_pages}")
                        markets = {}
                        for m_id in page_data:
                            print(f"\n{m_id}")
                            market = model.market_by_id_full(m_id)
                            print(f"{market[0][0]}\n{market[0][1]}\n{market[1]}\n")
                        print("\nNavigation: n - Next page | p - Previous page | e - Exit")
                        choice = input("\nChoose an option: ").strip().lower()
                        if choice == 'n':
                            if current_page < total_pages:
                                current_page += 1
                            else:
                                print("You are already on the last page.")
                        elif choice == 'p':
                            if current_page > 1:
                                current_page -= 1
                            else:
                                print("You are already on the first page.")
                        elif choice == 'e':
                            print("Exiting pagination..")
                            break
                        else:
                            print("Invalid option. Please choose again.")
                else:
                    print('Nothing was found. May be an error in the request.')
        elif n == '4':
            FLAG = True
        elif n == '0':
            print('Bye!')
            break
        else:
            print('Input Error!')

        while FLAG is True:
            print('''\n1. Show full info\n2. Leave feedback\n3. Delete feedback\n4. Sort by state and city\n
    To select the menu function, enter a number (1, 2, 3, 4 or other key to return to the main menu) and press Enter:''')
            print('What would you like to do? ')
            n = input()
            if n == '1':
                while FLAG is True:
                    ma_id = int(input('Enter market id: '))
                    data_temp = model.market_by_id_full(ma_id)
                    if data_temp is not None:
                        print(ma_id)
                        print(f"{data_temp[0][0]}\n {data_temp[0][1]}\n {data_temp[1]}\n")
                        FLAG = False
                    else:
                        print('Nothing was found. May be an error in the request.')
            elif n == '2':
                while FLAG is True:
                    data_temp = model.all_markets_full()
                    username = input("Input username: ")
                    password = input("Input password: ")
                    user_id = model.find_user_id(username, password)
                    if user_id == 0:
                        fname = input("Enter first name: ")
                        lname = input("Enter last name: ")
                        model.new_user(fname, lname, username, password)
                        user_id = model.find_user_id(username, password)
                    k = input('Enter the market id: ')
                    if k.isdigit() and int(k) in data_temp.keys():
                        score = input("Enter score 1..5: ")
                        feedback = input('Share your opinion: ')
                        model.new_review(user_id, k, score, feedback)
                        print(model.get_review(k))
                        FLAG = False
                    else:
                        print('Input Error!')
            elif n == '3':
                    while FLAG is True:
                        data_temp = model.all_markets_full()
                        username = input("Input username: ")
                        password = input("Input password: ")
                        user_id = model.find_user_id(username, password)
                        if user_id == 0:
                            fname = input("Enter first name: ")
                            lname = input("Enter last name: ")
                            model.new_user(fname, lname, username, password)
                            user_id = int(model.find_user_id(username, password))
                        else:
                            data_temp = model.get_reviews(username, password)
                            for item in data_temp:
                                print(f"\n{item[0]}\n{item[1:]}")
                            k = input('Enter id line to delete: ')
                            model.delete_review(k)
                            data_temp = model.get_reviews(username, password)
                            for item in data_temp:
                                print(f"\n{item[0]}\n{item[1:]}")
                        FLAG = False
            elif n == '4':
                while FLAG is True:
                    data_temp = model.sort_by_state_city(True)
                    current_page = 1
                    while True:
                        page_data, total_pages = paginate_list(data_temp, current_page, 5)
                        print(f"\nPage: {current_page}/{total_pages}")
                        for market in page_data:
                            print(f"{market[0]}")
                            print(f"{market[1][0][0][0][0]}")
                            print(f"{market[1][0][0][0][1]}, {market[1][0][0][0][2]}, {market[1][0][0][0][3]}")
                            print(f"{market[1][1][0]}\n")
                        print("\nNavigation: n - Next page | p - Previous page | e - Exit")
                        choice = input("\nChoose an option: ").strip().lower()
                        if choice == 'n':
                            if current_page < total_pages:
                                current_page += 1
                            else:
                                print("You are already on the last page.")
                        elif choice == 'p':
                            if current_page > 1:
                                current_page -= 1
                            else:
                                print("You are already on the first page.")
                        elif choice == 'e':
                            print("Exiting pagination..")
                            break
                        else:
                            print("Invald option. Please choose again.")
                    FLAG = False
            else:
                FLAG = False
