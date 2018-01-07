import pygame
import time
import random
import math
import datetime
import pickle

pygame.init()

display_width = 1366
display_height = 768
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Air Monopoly')

black = (0,0,0)
white = (255,255,255)
gray = (155,155,155)
blue = (0,35,170)
light_blue = (10,190,255)
green = (0,215,15)
dark_green = (0,120,5)
yellow = (255,255,0)
dark_yellow = (195,195,0)
red = (255,0,0)
dark_red = (120,0,0)

fps = 60

worldmap_img = pygame.image.load('World Map.png')
worldmap_main_img = pygame.image.load('World Map (mainscreen).png')
boe717_img = pygame.image.load('Boeing 717.jpg')
airA380_img = pygame.image.load('Airbus A380.jpg')

smallfont = pygame.font.SysFont('timesnewroman', 18)
medfont = pygame.font.SysFont('timesnewroman', 36)
largefont = pygame.font.SysFont('timesnewroman', 70)

money = 200
estimated_rev = 0
bond_liability = 0
company_value = 0
turn = 1
year = int(str(datetime.datetime.now())[0:4])
population_coeff = 4000
GDP_coeff = 80
dist_coeff = 9 * (10 ** (-4))
total_wage = 5

marketing_bonus = 1.00
pr_bonus = 0.03
interest_rate = 1.10

airplane_dict = {'Boeing 717':[], 'Airbus A380':[]}
airplane_details_title_dict = ['Model Name: ', 'Price($m): ', 'Maximum distance (km): ', 'Durability: ', 'Repair Cost($m): ', 'Seating Capacity: ']
airplane_details_dict = {'Boeing 717': ['Boeing 717', '50', '3815', 'Low','5', '115'],
                         'Airbus A380':['Airbus A380', '300', '15700', 'High', '50', '853']
                         }
airplane_status_dict = {}

flight_no_list = []
flight_route_dict = {}
#{key: [route, price(3),demandcurve(3),supplycurve(3),totalsupplycurve(3)]}

bond_dict = {}

airport_route_dict_title = ['City: ', 'Current flights: ','GDP in bil: $', 'Population in mil: ', 'x-coordinate: ', 'y-coordinate: ', 'No. of potential passengers: ', 'Distance: ']
airport_dict_title = ['City: ', 'Current flights: ','GDP in bil: $', 'Population in mil: ', 'x-coordinate: ', 'y-coordinate: ']
airport_dict = {'Singapore': ['Singapore',0,297,5.607,1077,296],
                'New Delhi':['New Delhi', 0,99.6,21.75, 985,198],
                'Beijing':['Beijing', 0, 314, 21.5,1091,155],
                'New York':['New York', 0,1488,8.54,535,153]
                }


budget_dict = {'Marketing': 20, 'General Administration': 20, 'Ground Crews': 20, 'Managers': 20, 'Public Relations': 20}

passenger_comp_list = [0.9,0.08,0.02]

news_compiler = []


def airplane_range_search(flight_num):
    model_name = ''
    for i in airplane_dict:
        for j in airplane_dict[i]:
            if j == flight_num:
                model_name = i
                break
    return float(airplane_details_dict[model_name][2])

def num_search_model(flight_num):
    model_name = ''
    for i in airplane_dict:
        for j in airplane_dict[i]:
            if j == flight_num:
                model_name = i
                break
    return model_name

def linear_solver(eqn1, eqn2):
        var_ori = eqn1[0]
        const_ori = eqn1[1]
        if eqn1[0] != 0 and eqn2[0] != 0:
            eqn1[0] -= eqn2[0]
            eqn2[0] = 0
        if eqn1[1] != 0 and eqn2[1] != 0:
            eqn2[1] -= eqn1[1]
            eqn1[1] = 0
        x_value = eqn2[1] / eqn1[0]
        y_value = var_ori * x_value + const_ori
        return [x_value, y_value]

def text_objects(text, color,size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(text, color, buttonx, buttony, buttonwidth, buttonheight,size = 'small', type = 'quad'):
    if type == 'quad':
        textSurf, textRect = text_objects(text, color, size)
        textRect.center = ((buttonx+(buttonwidth/2)),buttony + (buttonheight/2))
        gameDisplay.blit(textSurf,textRect)
    elif type == 'circle':
        textSurf, textRect = text_objects(text, color, size)
        textRect.center = ((buttonx, buttony))
        gameDisplay.blit(textSurf, textRect)

def message_to_screen(text,color, y_displace = 0,size = 'small'):
    textSurf, textRect = text_objects(text, color,size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def flight_no_gen():
    flight_num = 'PY'

    for i in range(3):
        num = random.randint(0,9)
        flight_num += str(num)

    if flight_num in flight_no_list:
        flight_no_gen()
    return flight_num

def serial_no_gen():
    serial = ''
    for i in range(4):
        num = random.randint(0,9)
        serial += str(num)

    return serial

def button_quad(x, y, size_x, size_y, inactive_color, active_color, text = None, action = None, text_size = 'small'):
    global money
    global mainscreen
    global operations
    global hang
    global marketing
    global finance
    global setting
    global intro
    global sell
    global ops1
    global news
    global budget
    global news_compiler
    global repair
    global plane_damaged
    global marketing_bonus
    global bond
    global bond_dict
    global change_route
    global bond_liability
    global ops4
    global estimated_rev

    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cursor[0] < x + size_x and y < cursor[1] < y + size_y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,size_x,size_y))
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            elif action == 'play':
                main_screen()
                intro = False
            elif action == 'setting':
                setting_screen()
                intro = False
            elif action == 'intro':
                gameIntro()
                setting = False
            elif action == 'next_turn':
                mainscreen = False
                next_turn()
            elif action == 'allocate_budget':
                budget_screen()
                finance = False
            elif action == 'back_budget':
                tbudget = 0
                for i in budget_dict:
                    tbudget += budget_dict[i]
                if int(tbudget) == 100:
                    budget = False
                    finance_screen()
                else:
                    message_to_screen('Your budget allocation is not 100%', red)
                    pygame.display.update()
                    time.sleep(0.75)
            elif action == 'apply_bond':
                finance = False
                bond_screen()
            elif action == 'back_bond':
                bond = False
                finance_screen()
            elif action == 'launch_route':
                ops4 = False
                rev = launch_route(flight)
                for i in range(len(rev)):
                    estimated_rev += rev[i]
                operations_screen()

            elif '_from_' in action:
                s = action.split('_from_')
                if s[1] == 'main':
                    mainscreen = False
                elif s[1] == 'ops':
                    operations = False
                elif s[1] == 'hang':
                    hang = False
                elif s[1] == 'marketing':
                    marketing = False
                elif s[1] == 'finance':
                    finance = False
                elif s[1] == 'sell':
                    sell = False
                elif s[1] == 'ops1':
                    ops1 = False
                elif s[1] == 'news':
                    news = False
                    news_compiler.clear()
                elif s[1] == 'setting':
                    setting = False
                elif s[1] == 'repair':
                    repair = False
                elif s[1] == 'change_route':
                    change_route = False

                if s[0] == 'main':
                    main_screen()
                elif s[0] == 'ops':
                    operations_screen()
                elif s[0] == 'hang':
                    hangar_screen()
                elif s[0] == 'marketing':
                    marketing_screen()
                elif s[0] == 'finance':
                    finance_screen()
                elif s[0] == 'airplane_select':
                    if len(flight_no_list) >= 1:
                        ops_1()
                    else:
                        message_to_screen('No available airplanes', green)
                        pygame.display.update()
                        time.sleep(0.75)
                        operations_screen()
                elif s[0] == 'sell':
                    hang_sell()
                elif s[0] == 'intro':
                    gameIntro()
                elif s[0] == 'repair':
                    hang_repair()
                elif s[0] == 'change_route':
                    ops_change_route()
            elif '_sell_plane_' in action:
                s = action.split('_sell_plane_')
                for i in airplane_dict:
                    for j in airplane_dict[i]:
                        if j == flight_no_list[int(s[1])]:
                            model_name = i
                            sell = False
                            break
                flight_no_list.pop(int(s[1]))
                airplane_dict[model_name].remove(s[0])
                money += int(airplane_details_dict[model_name][1])/2
                message_to_screen(str(model_name) + ' sold!', green)
                pygame.display.update()
                time.sleep(0.75)
                hang_sell()
            elif 'repair_plane_' in action:
                s = action.split('_plane_')
                money -= 5
                plane = plane_damaged[int(s[1])]
                airplane_status_dict[plane][1] = 0
                model = num_search_model(plane)
                if airplane_details_dict[model][3] == 'Low':
                    airplane_status_dict[plane][0] = 30
                elif airplane_details_dict[model][3] == 'Average':
                    airplane_status_dict[plane][0] = 45
                elif airplane_details_dict[model][3] == 'High':
                    airplane_status_dict[plane][0] = 60
                flight_no_list.append(plane)
            elif 'advert_' in action:
                if action == 'advert_TV':
                    if money >= 12:
                        num = random.randint(0,100)
                        num /= 1000
                        marketing_bonus += round(num,2)
                        money -= 12
                        message_to_screen('TV Advertisements have increased marketing bonus by ' + str(round(num,2) * 100) + '%', green)
                        pygame.display.update()
                        time.sleep(0.75)
                    else:
                        message_to_screen('Not enough money...', red)
                        pygame.display.update()
                        time.sleep(0.75)
                        marketing_screen()
            elif 'bond_' in action:
                if action == 'bond_100_10':
                    if estimated_rev - bond_liability >= 5:
                        block = []
                        block.append(10) #number of turns
                        block.append(10) #payment per turn
                        block.append(interest_rate)
                        money += 100
                        bond_dict[serial_no_gen()] = block
                        bond_liability = 0
                        for i in bond_dict:
                            bond_liability += bond_dict[i][1] * bond_dict[i][2]
                        message_to_screen('Application for $100m bond over 10 turns approved!', green)
                        pygame.display.update()
                        time.sleep(0.75)
                    else:
                        message_to_screen('Application for the bond rejected due to poor prospects', red)
                        pygame.display.update()
                        time.sleep(0.75)
                if action == 'bond_100_20':
                    if estimated_rev - bond_liability >= 4:
                        block = []
                        block.append(20) #number of turns
                        block.append(5) #payment per turn
                        block.append(interest_rate)
                        money += 100
                        bond_dict[serial_no_gen()] = block
                        bond_liability = 0
                        for i in bond_dict:
                            bond_liability += bond_dict[i][1] * bond_dict[i][2]
                        message_to_screen('Application for $100m bond over 20 turns approved!', green)
                        pygame.display.update()
                        time.sleep(0.75)
                    else:
                        message_to_screen('Application for the bond rejected due to poor prospects', red)
                        pygame.display.update()
                        time.sleep(0.75)
                if action == 'bond_250_10':
                    if estimated_rev - bond_liability >= 12.5:
                        block = []
                        block.append(10) #number of turns
                        block.append(25) #payment per turn
                        block.append(interest_rate)
                        money += 250
                        bond_dict[serial_no_gen()] = block
                        bond_liability = 0
                        for i in bond_dict:
                            bond_liability += bond_dict[i][1] * bond_dict[i][2]
                        message_to_screen('Application for $250m bond over 10 turns approved!', green)
                        pygame.display.update()
                        time.sleep(0.75)
                    else:
                        message_to_screen('Application for the bond rejected due to poor prospects', red)
                        pygame.display.update()
                        time.sleep(0.75)
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, size_x, size_y))
    if text != None:
        text_to_button(text,black,x,y,size_x,size_y,text_size)

def launch_route(flight):
    # incorrect economics relationship; requires consideration of non-price competition
    rev = []
    quantity_sold = []
    quantity_diff = []
    price_sold = []
    print(flight_route_dict)

    for i in range(3):
        quantity_sold.append(
            flight_route_dict[flight][2][i][0] * flight_route_dict[flight][1][i] + flight_route_dict[flight][2][i][1])
    for i in range(3):
        diff = flight_route_dict[flight][3][i][0] * flight_route_dict[flight][1][i] + flight_route_dict[flight][3][i][1] - \
            quantity_sold[i]
        if diff < 0:
            diff = 0
        quantity_diff.append(diff)
    for i in range(3):
        flight_route_dict[flight][2][i][1] += quantity_diff[i]
    for i in range(3):
        price_sold.append(linear_solver(flight_route_dict[flight][4][i], flight_route_dict[flight][2][i])[0])
    print(quantity_sold)
    print(price_sold)
    for i in range(3):
        rev.append(quantity_sold[i] * price_sold[i] / 10 ** 8)
    return rev

def button_ui(x, y, size_x, size_y, inactive_color, active_color, text = None, action = None, text_size = 'small'):
    global money
    global ops1
    global flight
    global estimated_rev

    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cursor[0] < x + size_x and y < cursor[1] < y + size_y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,size_x,size_y))
        if click[0] == 1 and action != None:
            if 'set_route_' in action:
                s = action.split('_route_')
                flight = flight_no_list[int(s[1])]
                ops1 = False
                ops_2()
            elif '_change_route_' in action:
                s = action.split('_change_route_')
                num = s[0]
                path = s[1].split('-')
                start_airport = path[0]
                end_airport = path[1]
                airport_dict[start_airport][1] -= 1
                airport_dict[end_airport][1] -= 1
                flight_no_list.append(num)
                rev = rev_calculate(start_airport,end_airport)
                estimated_rev -= rev[0]
                ops_2()
            elif money >= int(airplane_details_dict[action][1]):
                flight_num = flight_no_gen()
                airplane_dict[action].append(flight_num)
                flight_no_list.append(flight_num)
                money -= int(airplane_details_dict[action][1])
                message_to_screen(action + ' purchased!', green)
                if airplane_details_dict[action][3] == 'Low':
                    airplane_status_dict[flight_num] = [30]
                elif airplane_details_dict[action][3] == 'Average':
                    airplane_status_dict[flight_num] = [45]
                elif airplane_details_dict[action][3] == 'High':
                    airplane_status_dict[flight_num] = [60]
                airplane_status_dict[flight_num].append([0,0,0])
                pygame.display.update()
                time.sleep(0.75)
            else:
                message_to_screen('Not enough money...', red)
                pygame.display.update()
                time.sleep(0.75)

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, size_x, size_y))
    if text != None:
        text_to_button(text,black,x,y,size_x,size_y,text_size)

def button_fill(x, y, size_x, size_y, inactive_color, active_color, text = None, action = None, text_size = 'small'):
    global total_wage
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cursor[0] < x + size_x and y < cursor[1] < y + size_y:
        if click[0] == 1 and action != None:
            pressed = True
            typed = ''
            while pressed:
                button_ui(x,y,size_x, size_y, active_color, active_color, text = typed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            typed += '0'
                        elif event.key == pygame.K_1:
                            typed += '1'
                        elif event.key == pygame.K_2:
                            typed += '2'
                        elif event.key == pygame.K_3:
                            typed += '3'
                        elif event.key == pygame.K_4:
                            typed += '4'
                        elif event.key == pygame.K_5:
                            typed += '5'
                        elif event.key == pygame.K_6:
                            typed += '6'
                        elif event.key == pygame.K_7:
                            typed += '7'
                        elif event.key == pygame.K_8:
                            typed += '8'
                        elif event.key == pygame.K_9:
                            typed += '9'
                        elif event.key == pygame.K_PERIOD:
                            typed += '.'
                        elif event.key == pygame.K_BACKSPACE:
                            typed = typed[:-1]
                        elif event.key == pygame.K_RETURN:
                            pressed = False
                            if typed == '':
                                typed = '0'

                pygame.display.update()
                clock.tick(fps)
            if action == 'marketing_budget':
                budget_dict['Marketing'] = float(typed)
            elif action == 'admin_budget':
                budget_dict['General Administration'] = float(typed)
            elif action == 'groundc_budget':
                budget_dict['Ground Crews'] = float(typed)
            elif action == 'manager_budget':
                budget_dict['Managers'] = float(typed)
            elif action == 'pr_budget':
                budget_dict['Public Relations'] = float(typed)
            elif action == 'set_wages':
                total_wage = float(typed)
            elif '_price_econ' in action:
                s = action.split('_price_')
                flight_route_dict[s[0]][1][0] = float(typed)
            elif '_price_buss' in action:
                s = action.split('_price_')
                flight_route_dict[s[0]][1][1] = float(typed)
            elif '_price_firstc' in action:
                s = action.split('_price_')
                flight_route_dict[s[0]][1][2] = float(typed)

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, size_x, size_y))
    if text != None:
        text_to_button(text,black,x,y,size_x,size_y,text_size)

def display_ui(x, y, size_x, size_y_perline, color, text_list, type = 'info',text_size = 'small'):
    pygame.draw.rect(gameDisplay, color, (x, y, size_x, size_y_perline * len(text_list)))
    if type == 'ap':
        for index in range(len(text_list)):
            text_to_button(airport_dict_title[index] + str(text_list[index]), black, x, y + size_y_perline * index, size_x, size_y_perline, text_size)
    elif type == 'route':
        for index in range(len(text_list)):
            text_to_button(airport_route_dict_title[index] + str(text_list[index]), black, x, y + size_y_perline * index, size_x, size_y_perline, text_size)
    elif type == 'info':
        for index in range(len(text_list)):
            text_to_button(str(text_list[index]), black, x, y + size_y_perline * index, size_x, size_y_perline, text_size)
    elif type == 'details':
        for index in range(len(text_list)):
            text_to_button(airplane_details_title_dict[index] + str(text_list[index]), black, x, y + size_y_perline * index, size_x, size_y_perline, text_size)

def button_circle(x, y, radius, inactive_color, active_color,text_size = 'small'):
    cursor = pygame.mouse.get_pos()
    if math.sqrt((x - cursor[0])**2 + (y - cursor[1])**2) <= radius:
        pygame.draw.circle(gameDisplay, active_color, (x,y), radius)
        pygame.draw.circle(gameDisplay, white, (x, y), 1)
        airport_identifier = (x,y)
        if airport_identifier == (1077,296):
            airport = 'Singapore'
        elif airport_identifier == (985,198):
            airport = 'New Delhi'
        elif airport_identifier == (1091,155):
            airport = 'Beijing'
        elif airport_identifier == (535,153):
            airport = 'New York'
        display_ui(1141,600,225,20,yellow,airport_dict[airport],type = 'ap')
    else:
        pygame.draw.circle(gameDisplay, inactive_color, (x, y), radius)
        pygame.draw.circle(gameDisplay, white, (x, y), 1)

def button_circle_act(x, y, radius, inactive_color, active_color,action,text_size = 'small'):
    global ops2
    global ops3
    global start_airport
    global end_airport
    global flight

    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if math.sqrt((x - cursor[0])**2 + (y - cursor[1])**2) <= radius:
        pygame.draw.circle(gameDisplay, active_color, (x, y), radius)
        pygame.draw.circle(gameDisplay, red, (x, y), 1)
        airport_identifier = (x, y)
        if airport_identifier == (1077, 296):
            airport = 'Singapore'
        elif airport_identifier == (985, 198):
            airport = 'New Delhi'
        elif airport_identifier == (1091,155):
            airport = 'Beijing'
        elif airport_identifier == (535,153):
            airport = 'New York'
        if ops2 == True:
            if click[0] == 1:
                start_airport = action
                airport_dict[action][1] += 1
                ops2 = False
                ops_3()
            display_ui(1141, 600, 225, 20, yellow, airport_dict[airport], type='ap')
        elif ops3 == True:
            tpassenger_num = tpassenger_calculate(start_airport, airport)
            display_add = []
            for i in airport_dict[airport]:
                display_add.append(i)
            display_add.append(round(tpassenger_num[0],2))
            display_add.append(round(tpassenger_num[1], 2))
            display_ui(1141, 600, 225, 18, yellow, display_add, type='route')
            if click[0] == 1 and ops2 == False and action != start_airport:
                if tpassenger_num[1] <= airplane_range_search(flight):
                    end_airport = action
                    airport_dict[action][1] += 1
                    ops3 = False
                    flight_no_list.remove(flight)
                    flight_route_dict[flight] = []
                    flight_route_dict[flight].append(start_airport + '-' + end_airport)
                    flight_route_dict[flight].append([0,0,0])
                    for i in range(3):
                        flight_route_dict[flight].append([])
                    for i in range(len(passenger_comp_list)):
                        demand_curve = [-10000, tpassenger_num[0] * passenger_comp_list[i]]
                        flight_route_dict[flight][2].append(demand_curve)
                        supply_curve = [int(airplane_details_dict[num_search_model(flight)][5]), 0]
                        flight_route_dict[flight][3].append(supply_curve)
                        tsupply_curve = [int(airplane_details_dict[num_search_model(flight)][5]) * 50 + 8000, 0] #AI component required
                        flight_route_dict[flight][4].append(tsupply_curve)
                    ops_4()
                else:
                    message_to_screen('The current plane model selected does not have sufficient range', red)
                    pygame.display.update()
                    time.sleep(0.75)

    else:
        pygame.draw.circle(gameDisplay, inactive_color, (x, y), radius)
        pygame.draw.circle(gameDisplay, white, (x, y), 2)

def tpassenger_calculate(start_airport, end_airport):
    output = []
    dist = math.sqrt(
         (airport_dict[start_airport][3] - airport_dict[end_airport][3]) ** 2 + (
             airport_dict[start_airport][4] - airport_dict[end_airport][4]) ** 2) * 25.592
    estimated_tpassenger = (population_coeff * math.sqrt(
        airport_dict[start_airport][1] ** 2 + airport_dict[end_airport][1] ** 2) +
                          GDP_coeff * (airport_dict[start_airport][2] ** 2 + airport_dict[end_airport][
                              2] ** 2)) * marketing_bonus
    output.append(estimated_tpassenger)
    output.append(dist)
    return output

def gameIntro():
    global intro
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    main_screen()
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.blit(worldmap_img, (0,0))
        message_to_screen('Air Monopoly', blue, -100, 'large')

        button_quad(533,600,100,50,white,gray,'PLAY (S)', action='play')
        button_quad(633,600,100,50,white,gray,'SETTING', action='setting')
        button_quad(733,600,100,50,white,gray,'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def setting_screen():
    global setting
    setting = True

    while setting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        button_quad(583,50,200,50,white,white,'Setting',text_size='medium')


        button_quad(733,650,100,50,white,gray,'BACK', action='intro_from_setting')

        pygame.display.update()
        clock.tick(fps)

def main_screen():
    global mainscreen
    global bond_liability
    global company_value
    mainscreen = True

    while mainscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        gameDisplay.blit(worldmap_main_img, (200,0))
        pygame.draw.line(gameDisplay,gray,(200,0),(200,768),3)
        pygame.draw.line(gameDisplay, gray, (0, 600), (200, 600), 3)

        button_quad(10, 50, 180, 25, green, green, text='Strategic View', action= None, text_size='small')
        button_quad(10,80,180,25,light_blue,blue,text='Operations Department',action = 'ops_from_main', text_size='small')
        button_quad(10, 110, 180, 25, light_blue, blue, text='Hangar', action='hang_from_ops', text_size='small')
        button_quad(10, 140, 180, 25, light_blue, blue, text='Marketing', action='marketing_from_main', text_size='small')
        button_quad(10, 170, 180, 25, light_blue, blue, text='Finance', action='finance_from_main', text_size='small')

        button_quad(1266, 25, 75, 50, red, dark_red, text='End Turn', action='next_turn', text_size='small')

        button_circle(1077,296,4,yellow,dark_yellow)
        button_circle(985, 198, 4, yellow, dark_yellow)
        button_circle(1091, 155, 4, yellow, dark_yellow)
        button_circle(535, 153, 4, yellow, dark_yellow)


        airplane_values = 0
        for i in flight_no_list:
            airplane_values += int(airplane_details_dict[num_search_model(i)][1])
        bond_total = 0
        for i in bond_dict:
            bond_total += bond_dict[i][0] * bond_dict[i][1] * bond_dict[i][2]
        company_value = money + airplane_values - bond_total

        button_quad(210, 600, 180, 25, yellow, yellow, text='Money: $' + str(round(money,2)) + ' m')
        button_quad(210, 640, 180, 25, yellow, yellow, text='Predicted Income: $' + str(round(estimated_rev,2)) + ' m')
        button_quad(210, 680, 180, 25, yellow, yellow, text='0')
        button_quad(210, 720, 220, 25, yellow, yellow, text='Company Value: $' + str(round(company_value, 2)) + ' m')
        button_quad(400, 600, 180, 25, yellow, yellow, text='Number of airplanes: ' + str(len(flight_no_list)))
        button_quad(400, 640, 180, 25, yellow, yellow, text='Professionalism: ' + str(round(pr_bonus * 100,2)) + '%')
        button_quad(400, 680, 180, 25, yellow, yellow, text='Bond Liability: ' + str(round(bond_liability,2)) + ' m')
        button_quad(440, 720, 140, 25, yellow, yellow, text='Year: ' + str('{} ({})'.format(year, turn)))

        button_quad(590, 600, 300, 25, yellow, yellow, text='Marketing Wage: $' + str(budget_dict['Marketing'] * total_wage / 100) + ' m (' + str(budget_dict['Marketing']) + '%)')
        button_quad(590, 630, 300, 25, yellow, yellow,
                    text='General Admin Wage: $' + str(budget_dict['General Administration'] * total_wage / 100) + ' m (' + str(
                        budget_dict['General Administration']) + '%)')
        button_quad(590, 660, 300, 25, yellow, yellow,
                    text='Ground Crew Wage: $' + str(budget_dict['Ground Crews'] * total_wage / 100) + ' m (' + str(
                        budget_dict['Ground Crews']) + '%)')
        button_quad(590, 690, 300, 25, yellow, yellow,
                    text='Managers Wage: $' + str(budget_dict['Managers'] * total_wage / 100) + ' m (' + str(
                        budget_dict['Managers']) + '%)')
        button_quad(590, 720, 300, 25, yellow, yellow,
                    text='Public Relations Wage: $' + str(budget_dict['Public Relations'] * total_wage / 100) + ' m (' + str(
                        budget_dict['Public Relations']) + '%)')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')
        #print(pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(fps)

def operations_screen():
    global operations
    operations = True
    while operations:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        gameDisplay.blit(worldmap_main_img, (200, 0))
        pygame.draw.line(gameDisplay,black,(200,0),(200,768),3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_quad(10, 50, 180, 25, light_blue, blue, text='Strategic View', action='main_from_ops', text_size='small')
        button_quad(10, 80, 180, 25, green, green, text='Operations Department', action=None, text_size='small')
        button_quad(10, 110, 180, 25, light_blue, blue, text='Hangar', action='hang_from_ops', text_size='small')
        button_quad(10, 140, 180, 25, light_blue, blue, text='Marketing', action='marketing_from_ops', text_size='small')
        button_quad(10, 170, 180, 25, light_blue, blue, text='Finance', action='finance_from_ops', text_size='small')

        button_quad(593 ,100, 180, 25, yellow, dark_yellow, text='Select an Airplane', action = 'airplane_select_from_ops')
        button_quad(593, 200, 180, 25, yellow, dark_yellow, text='Change routes',
                    action='change_route_from_ops')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def ops_1():
    global ops1
    ops1 = True
    while ops1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        for i in range(len(flight_no_list)):
            button_ui(250,100 + i * 35,180,25,green,dark_green,text = flight_no_list[i],action = 'set_route_' + str(i))


        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')
        button_quad(1176, 718, 180, 25, yellow, dark_yellow, 'BACK', action='ops_from_ops1')

        pygame.display.update()
        clock.tick(fps)

def ops_2():
    global ops2
    ops2 = True
    while ops2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        gameDisplay.blit(worldmap_main_img, (200, 0))
        pygame.draw.line(gameDisplay, gray, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, gray, (0, 600), (200, 600), 3)


        button_circle_act(1077, 296, 4, yellow, dark_yellow,'Singapore')
        button_circle_act(985, 198, 4, yellow, dark_yellow,'New Delhi')
        button_circle_act(1091, 155, 4, yellow, dark_yellow, 'Beijing')
        button_circle_act(535, 153, 4, yellow, dark_yellow, 'New York')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def ops_3():
    global ops3
    ops3 = True
    while ops3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        gameDisplay.blit(worldmap_main_img, (200, 0))
        pygame.draw.line(gameDisplay, gray, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, gray, (0, 600), (200, 600), 3)

        button_circle_act(1077, 296, 4, yellow, dark_yellow, 'Singapore')
        button_circle_act(985, 198, 4, yellow, dark_yellow, 'New Delhi')
        button_circle_act(1091, 155, 4, yellow, dark_yellow, 'Beijing')
        button_circle_act(535, 153, 4, yellow, dark_yellow, 'New York')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def ops_4():
    global ops4
    ops4 = True
    while ops4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        gameDisplay.blit(worldmap_main_img, (200, 0))
        pygame.draw.line(gameDisplay, gray, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, gray, (0, 600), (200, 600), 3)

        button_fill(250, 100, 250, 50, yellow, white, text='Economy Class: $' + str(flight_route_dict[flight][1][0]), action= flight + '_price_econ')
        button_fill(250, 200, 250, 50, yellow, white, text='Business Class: $' + str(flight_route_dict[flight][1][1]),
                    action= flight + '_price_buss')
        button_fill(250, 300, 250, 50, yellow, white, text='First Class: $' + str(flight_route_dict[flight][1][2]),
                    action=flight + '_price_firstc')

        button_quad(1000, 718, 180, 25, green, dark_green, 'Launch Flight', action='launch_route')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def ops_change_route():
    global change_route
    change_route = True
    while change_route:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        num = 0
        for i in flight_route_dict:
            button_ui(250,100 + num * 35, 300, 25, green, dark_green, text = i + ': ' + flight_route_dict[i], action = i + '_change_route_' + flight_route_dict[i])
            num += 1


        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')
        button_quad(1176, 718, 180, 25, yellow, dark_yellow, 'BACK', action='ops_from_change_route')

        pygame.display.update()
        clock.tick(fps)

def hangar_screen():
    global hang
    hang = True
    while hang:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay,black,(200,0),(200,768),3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_quad(10, 50, 180, 25, light_blue, blue, text='Strategic View', action='main_from_hang', text_size='small')
        button_quad(10, 80, 180, 25, light_blue, blue, text='Operations Department', action='ops_from_hang', text_size='small')
        button_quad(10, 110, 180, 25, green, green, text='Hangar', action=None, text_size='small')
        button_quad(10, 140, 180, 25, light_blue, blue, text='Marketing', action='marketing_from_hang',text_size='small')
        button_quad(10, 170, 180, 25, light_blue, blue, text='Finance', action='finance_from_hang', text_size='small')

        gameDisplay.blit(boe717_img, (250,100))
        gameDisplay.blit(airA380_img, (250, 300))
        button_ui(250,200,30,30,yellow, dark_yellow, text='+',action='Boeing 717',text_size='medium')
        button_ui(250,413,30,30,yellow,dark_yellow, text = '+', action = 'Airbus A380', text_size = 'medium')
        display_ui(475, 100, 250, 30, white, airplane_details_dict['Boeing 717'], type='details')
        display_ui(475, 300, 250, 30, white, airplane_details_dict['Airbus A380'], type = 'details')

        button_quad(1176,80,180,25,red,dark_red, text='Sell airplanes',action='sell_from_hang',text_size='small')
        button_quad(1176, 115, 180, 25, red, dark_red, text='Repair airplanes', action='repair_from_hang', text_size='small')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def hang_sell():
    global sell
    sell = True
    while sell:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        for i in range(len(flight_no_list)):
            button_quad(250,100 + i * 35,180,25,green,dark_green,text = flight_no_list[i] + ' - ' + str(num_search_model(flight_no_list[i])),action = str(flight_no_list[i]) + '_sell_plane_' + str(i))

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')
        button_quad(1176, 718, 180, 25, yellow, dark_yellow, 'BACK', action='hang_from_sell')

        pygame.display.update()
        clock.tick(fps)

def hang_repair():
    global repair
    global plane_damaged
    repair = True
    while repair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)
        plane_damaged = []
        for i in airplane_status_dict:
            if airplane_status_dict[i][1] == 1:
                plane_damaged.append(i)
        for i in range(len(plane_damaged)):
            button_quad(250, 100 + i * 35, 180, 25, red, dark_red, text=plane_damaged[i],
                        action='repair_plane_' + str(i))

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')
        button_quad(1176, 718, 180, 25, yellow, dark_yellow, 'BACK', action='hang_from_repair')

        pygame.display.update()
        clock.tick(fps)

def marketing_screen():
    global marketing
    marketing = True
    while marketing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay,black,(200,0),(200,768),3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_quad(10, 50, 180, 25, light_blue, blue, text='Strategic View', action='main_from_marketing', text_size='small')
        button_quad(10, 80, 180, 25, light_blue, blue, text='Operations Department', action='ops_from_marketing', text_size='small')
        button_quad(10, 110, 180, 25, light_blue, blue, text='Hangar', action='hang_from_marketing', text_size='small')
        button_quad(10, 140, 180, 25, green, green, text='Marketing', action=None, text_size='small')
        button_quad(10, 170, 180, 25, light_blue, blue, text='Finance', action='finance_from_marketing', text_size='small')

        button_quad(210, 600, 200, 25, yellow, yellow, text='Marketing Bonus: ' + str(round(marketing_bonus,2) * 100) + ' %')
        button_quad(250, 100, 200, 25, green, dark_green, text='TV Advertisements($12m)', action='advert_TV')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def finance_screen():
    global finance
    finance = True
    while finance:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay,black,(200,0),(200,768),3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_quad(10, 50, 180, 25, light_blue, blue, text='Strategic View', action='main_from_hr', text_size='small')
        button_quad(10, 80, 180, 25, light_blue, blue, text='Operations Department', action='ops_from_hr', text_size='small')
        button_quad(10, 110, 180, 25, light_blue, blue, text='Hangar', action='hang_from_hr', text_size='small')
        button_quad(10, 140, 180, 25, light_blue, blue, text='Marketing', action='marketing_from_hr', text_size='small')
        button_quad(10, 170, 180, 25, green, green, text='Finance', action=None, text_size='small')

        button_quad(250, 650, 200, 25, yellow, dark_yellow, text='Allocate Budget', action='allocate_budget')
        button_fill(500, 650, 200, 25, yellow, dark_yellow,
                    text='Wages: $' + str(total_wage) + 'm', action='set_wages')
        button_quad(750, 650, 200, 25, yellow, dark_yellow, text='Apply Bond', action='apply_bond')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def budget_screen():
    global budget
    budget = True
    while budget:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_fill(250,100,250,50,yellow,white,text='Marketing Department: ' + str(budget_dict['Marketing']) + '%', action='marketing_budget')
        button_fill(250, 200, 250, 50, yellow, white, text='General Administration: ' + str(budget_dict['General Administration']) + '%',
                    action='admin_budget')
        button_fill(250, 300, 250, 50, yellow, white, text='Ground Crews: ' + str(budget_dict['Ground Crews']) + '%',
                    action='groundc_budget')
        button_fill(250,400, 250, 50, yellow, white, text='Managers: ' + str(budget_dict['Managers']) + '%',
                    action='manager_budget')
        button_fill(250, 500, 250, 50, yellow, white, text='Public Relations: ' + str(budget_dict['Public Relations']) + '%',
                    action='pr_budget')

        button_quad(600,718,180,25,yellow,dark_yellow, text='BACK', action='back_budget')
        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def bond_screen():
    bond = True
    while bond:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay, black, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, black, (0, 600), (200, 600), 3)

        button_quad(250, 100, 250, 25, green, dark_green, text='$100m Bond (10 turns)', action='bond_100_10')
        button_quad(250, 150, 250, 25, green, dark_green, text='$100m Bond (20 turns)', action='bond_100_20')
        button_quad(250, 200, 250, 25, green, dark_green, text='$250m Bond (10 turns)', action='bond_250_10')

        button_quad(210, 600, 220, 25, yellow, yellow,text='Current interest rate: ' + str(round(interest_rate - 1, 3) * 100) + ' %')
        button_quad(600, 718, 180, 25, yellow, dark_yellow, text='BACK', action='back_bond')
        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

def next_turn():
    global money
    global news_compiler
    global marketing_bonus
    global pr_bonus
    global interest_rate
    global turn
    global year

    rev = random.randrange(int(0.9 * estimated_rev * 1000), int(1.1 * estimated_rev * 1000))

    money += rev - total_wage
    turn += 1
    year += 1
    marketing_bonus += 0.0001 * budget_dict['Marketing']
    news_compiler.append('You earned $' + str(round(rev, 2)) + 'm from sales')
    news_compiler.append('Your marketing bonus has been increased by ' + str(budget_dict['Marketing'] * 0.01) + '%')
    pr_bonus += 0.0001 * budget_dict['Public Relations']
    news_compiler.append('Your professionalism level has been increased by ' + str(budget_dict['Public Relations'] * 0.01) + '%')
    if interest_rate >= 1.01:
        interest_change = round((random.randrange(-10,10)) / 1000, 4)
        interest_rate += interest_change
    else:
        interest_change = round((random.randrange(-1, 10)) / 1000, 4)
        interest_rate += interest_change
    news_compiler.append('Interest rates have been changed by ' + str(interest_change * 100) + '%')

    for plane in airplane_status_dict:
        if airplane_status_dict[plane][1] == 0:
            if random.randrange(0,airplane_status_dict[plane][0]) == 0:
                if airplane_status_dict[plane][0] <= 20:
                    airplane_status_dict[plane][1] = 1
                    flight_no_list.remove(plane)
                else:
                    airplane_status_dict[plane][0] -= 1
            else:
                airplane_status_dict[plane][0] -= 1
    for plane in airplane_status_dict:
        if airplane_status_dict[plane][1] == 1:
            news_compiler.append(str(plane) + ' has been damaged.')
    for i in budget_dict:
        department_wage = budget_dict[i] * total_wage / 100
        if department_wage <= estimated_rev / 8:
            chance_num = (estimated_rev / 8 - department_wage) * 100
            chance_num = int(round(chance_num, 0))
            if chance_num >= 20:
                news_compiler.append(i + ' has gone on strike and demand higher salary! It will not be long before the labour union steps in.')
                marketing_bonus -= (random.randrange(0, chance_num) / 100) * (1 - pr_bonus)
                if pr_bonus >= 0.03:
                    pr_bonus -= 0.03
            else:
                roller = random.randrange(chance_num, 20)
                if roller == 19:
                    news_compiler.append(i + ' has gone on strike and demand higher salary! It will not be long before the labour union steps in.')
                    marketing_bonus -= (random.randrange(0, chance_num) / 100) * (1 - pr_bonus)
                    if pr_bonus >= 0.03:
                        pr_bonus -= 0.03
    for i in bond_dict:
        money -= round(bond_dict[i][1] * bond_dict[i][2],2)
        bond_dict[i][0] -= 1
        if bond_dict[i][0] == 1:
            bond_dict.pop(i)
        news_compiler.append(str(round(bond_dict[i][1] * bond_dict[i][2],2)) + 'm has been paid as installment for the bond.')
    print(flight_route_dict)
    news_screen()

def news_screen():
    global news
    news = True

    while news:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        pygame.draw.line(gameDisplay, gray, (200, 0), (200, 768), 3)
        pygame.draw.line(gameDisplay, gray, (0, 600), (200, 600), 3)
        display_ui(233, 200, 1100, 30, white, text_list=news_compiler)

        button_quad(583, 50, 400, 100, white, white, text='News Page for Year ' + str(year-1), action=None,
                    text_size='medium')

        button_quad(10, 50, 180, 25, light_blue, blue, text='Strategic View', action='main_from_news', text_size='small')
        button_quad(10, 80, 180, 25, light_blue, blue, text='Operations Department', action='ops_from_news', text_size='small')
        button_quad(10, 110, 180, 25, light_blue, blue, text='Hangar', action='hang_from_news', text_size='small')
        button_quad(10, 140, 180, 25, light_blue, blue, text='Marketing', action='marketing_from_news', text_size='small')
        button_quad(10, 170, 180, 25, light_blue, blue, text='Finance', action='finance_from_news', text_size='small')

        button_quad(10, 718, 180, 25, red, dark_red, 'QUIT (Q)', action='quit')

        pygame.display.update()
        clock.tick(fps)

gameIntro()
pygame.quit()
quit()