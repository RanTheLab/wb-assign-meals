#! /usr/bin/env python


import logging
import Staff
import rtlog
import time
import util

rtlog.initlog()
logging.warn('test')

# create staff
Staff.CourseDirector('Course Director', util.EAGLE)
Staff.AsmProgram('ASM Program', util.BUFFALO)
Staff.Spl('SeniorPatrol Leader', util.ANTELOPE)
Staff.CrewAdvisor('Crew Advisor', util.FOX)
Staff.ScribeCommunication('Scribe Comms', util.FOX)
Staff.ScribeAv('Scribe AV', util.BEAR)
Staff.AsmLogistics('ASM Logistics', util.EAGLE)
Staff.ScribeRegistrar('Scribe Registrar', util.BEAR)
Staff.Quartermaster('Quarter Master', util.EAGLE)
Staff.QmAssistant1('QM Asst1', util.BEAVER)
Staff.QmAssistant2('QM Asst2', util.EAGLE)
Staff.AsmTroopGuides('ASM TGuides', util.BUFFALO)
Staff.TroopGuideBeaver('TG Beaver', util.FOX)
Staff.TroopGuideBobwhite('TG Bobwhite', util.BOBWHITE)
Staff.TroopGuideEagle('TG Eagle', util.FOX)
Staff.TroopGuideFox('TG Fox', util.OWL)
Staff.TroopGuideOwl('TG Owl', util.ANTELOPE)
Staff.TroopGuideBear('TG Bear', util.BOBWHITE)
Staff.TroopGuideBuffalo('TG Buffalo', util.BEAR)
Staff.TroopGuideAntelope('TG Antelope', util.BEAVER)
Staff.Mentor('Staff Mentor', util.ANTELOPE)
Staff.Professional('Staff Professional', util.EAGLE)

Staff.YouthStaffPresident('Youth President')
Staff.YouthStaffVP('Youth VP')
Staff.YouthStaffBeaver('Youth Beaver')
Staff.YouthStaffBobwhite('Youth Bobwhite')
Staff.YouthStaffEagle('Youth Eagle')
Staff.YouthStaffFox('Youth Fox')
Staff.YouthStaffOwl('Youth Owl')
Staff.YouthStaffBear('Youth Bear')
Staff.YouthStaffBuffalo('Youth Buffalo')
Staff.YouthStaffAntelope('Youth Antelope')

print(Staff.critter_report())

positions = Staff.staffers.keys()

meal_plan = {}


# Inititalize meal plan
for meal in range(1, 14):
    for position in positions:
        meal_plan[(meal, position)] = 'x'

meal_list = []

# Initialize meal list
for meal_number in range(1, 15):

    meal = Staff.MealTracker(meal_number)
    meal_list.append(meal)

count = 0
staff_by_critter = []
assignable_staff = []
# Get keys of positions of staff that will eat with their critter for 1 meal during weekend 1.
# Basically exclude troop guides and youth staff...
for p in util.POSITIONS[0:14]:
    staff_by_critter.append(Staff.staffers[p])

# Sort by critter so when looping through assignments, we will not get duplicates
staff_by_critter.sort(key=lambda a_staff: a_staff.critter)

for staffer in staff_by_critter:
    # print(staffer)

    # We are interested in meals 2 thru 7 which are at indexes 1 through 6
    # so go 0 to 5 and add 1.
    meal_number_index = (count % 6) + 1
    m = meal_list[meal_number_index]
    # remove the FIRST matching VALUE.
    m.available_meals.remove(staffer.critter)
    staffer.critter_meal_list.append(meal_number_index + 1)
    m.patrol_counts[staffer.critter] = m.patrol_counts[staffer.critter] + 1
    # meal_plan[(meal_number, staffer.position)] = util.CRITTERS[staffer.critter]

    count = count + 1

troop_guides = []
for p in util.POSITIONS[14:22]:
    troop_guides.append(Staff.staffers[p])

for guide in troop_guides:
    m = meal_list[9]
    m.available_meals.remove(guide.critter)
    guide.critter_meal_list.append(10)
    m.patrol_counts[guide.critter] = m.patrol_counts[guide.critter] + 1

for meal in meal_list:

    logging.debug('Processing meal %d' % meal.meal_number)
    logging.debug(meal)

    for position in positions:

        logging.debug('Processing position %s' % position)
        staff = Staff.staffers[position]
        logging.debug(staff)

        # not sure what this is...
        if meal.meal_number == 8:
            staff.patrols_attended_list = []

        if meal.meal_number in staff.critter_meal_list:
            logging.debug('%s assigned to own patrol...' % staff.name)
            patrol = util.CRITTERS[staff.critter]
        else:
            patrol = staff.assign_meal(meal)

        staff.assigned_meal_list.append(patrol)
        meal_plan[(meal.meal_number, position)] = patrol
        logging.debug(meal)

    logging.debug('Meal %d summary:' % meal.meal_number)
    logging.debug(meal)

print(meal_plan)

meals = {}
keys = meal_plan.keys()

meal_num = 0
for key in keys:
    if key[0] != meal_num:
        if meal_num > 0:
            print(('Meal %d:' % meal_num) + str(meal))
            meals[meal_num] = meal
        meal_num = key[0]
        meal = {}
    meal_group = meal_plan[key]
    if meal.get(meal_group) is None:
        meal[meal_group] = []
    meal_list = meal[meal_group]
    meal_list.append(Staff.staffers[key[1]].name)
print(('Meal %d:' % meal_num) + str(meal))
meals[meal_num] = meal

print('\nGenerated: %s\n' % time.asctime())
for i in range(1, 15):
    line = ''
    print('Meal %d' % i)

    meal = meals[i]

    try:
        group = meal['Head table']
        print('%s: %a' % ('Head table', ', '.join(group)))
        line = line + '\n'.join(group) + ','
    except KeyError:
#        print('XXXXXXXXXXXXX')
        line = line + ','
    try:
        group = meal['Staff']
        print('%s: %a' % ('Staff', ', '.join(group)))
        line = line + '\n'.join(group) + ','
    except KeyError:
#        print('XXXXXXXXXXXXX')
        line = line + ','
    try:
        group = meal['PLC']
        print('%s: %a' % ('PLC', ', '.join(group)))
        line = line + '\n'.join(group) + ','
    except KeyError:
 #       print('XXXXXXXXXXXXX')
        line = line + ','
    for c in range(1, 9):
        try:
            group = meal[util.CRITTERS[c]]
            print('%s: %a' % (util.CRITTERS[c], ', '.join(group)))
            line = line + '\n'.join(group) + ','
        except KeyError:
            pass

    print()



#for position in positions:
#    print(Staff.staffers[position])
    # Staff.staffers[position].show_meals()
#    print('')
    # for meal in meal_list:
    #    print(meal)


