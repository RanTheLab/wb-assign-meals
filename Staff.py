#! /usr/bin/env python

import logging
import random
import sys
import util

staffers = {}
beaver = []
bobwhite = []
eagle = []
fox = []
owl = []
bear = []
buffalo = []
antelope = []


class MealTracker(object):
    meal_number = 0
    max_per_patrol = 0
    available_meals = []

    def __init__(self, num):
        self.meal_number = num
        if self.meal_number < 8:
            self.max_per_patrol = 3
        else:
            self.max_per_patrol = 4

        self.patrol_counts = {
            util.BEAVER: 0,
            util.BOBWHITE: 0,
            util.EAGLE: 0,
            util.FOX: 0,
            util.OWL: 0,
            util.BEAR: 0,
            util.BUFFALO: 0,
            util.ANTELOPE: 0}

        self.available_meals = []

        for i in range(1, self.max_per_patrol):
            self.available_meals.extend([1, 2, 3, 4, 5, 6, 7, 8])

    def __str__(self):
        string = ''
        total = 0
        keys = self.patrol_counts.keys()
        for key in keys:
            if self.patrol_counts[key] > 0:
                string += util.CRITTERS[key] + (': %d ' % self.patrol_counts[key])
                total = total + self.patrol_counts[key]
        string += '\n' + ('Total: %d' % total)
        return string

    def choose_meal(self, staff):

        staff_assigned = False

        patrol = -1
        retry_count = 0
        tried_list = []

        index = -1

        while not staff_assigned:

            index = index + 1 # random.randint(0, len(self.available_meals)-1)
            if index > len(self.available_meals) - 1:
                #            if retry_count > 50:
                logging.critical("Too many tries... quitting")
                logging.debug(self)
                sys.exit(0)

            patrol = self.available_meals[index]

#            if patrol in tried_list:
#                continue

            tried_list.append(patrol)

            logging.debug('Random index %d yields patrol %d (%s)' % (index, patrol, util.CRITTERS[patrol]))

#            elif retry_count > 10:
#                logging.warn('Retry hit 10....')

            if self.patrol_counts[patrol] >= self.max_per_patrol:
                logging.debug('Patrol limit reached, get a new index')
                retry_count = retry_count + 1
                continue

            if self.meal_number == 1:
                if staff.critter == patrol:
                    logging.debug('Preventing %s from eating with their critter in meal 1' % util.CRITTERS[patrol])
                    retry_count = retry_count + 1
                    continue
                else:
                    self.available_meals.pop(index)
                    staff_assigned = True
            elif 2 <= self.meal_number <= 11:

#                if staff.critter == patrol or patrol in staff.patrols_attended_list:
                if (staff.critter == patrol) != (patrol in staff.patrols_attended_list):
                    if index == len(self.available_meals)-1:
                        self.available_meals.pop(index)
                        staff_assigned = True
                    else:
                        logging.debug('Need to retry, already have a %s in this meal' % util.CRITTERS[patrol])
                        retry_count = retry_count + 1
                        continue
                else:
                    self.available_meals.pop(index)
                    staff_assigned = True

            elif self.meal_number == 14:
                if staff.position == util.PROFESSIONAL:
                    self.available_meals.pop(index)
                    staff_assigned = True
                elif staff.critter is not None and staff.critter != patrol:
                    continue
                else:
                    self.available_meals.pop(index)
                    staff_assigned = True
            # else covers meals 12 and 13
            else:
                self.available_meals.pop(index)
                staff_assigned = True
        retry_count = 0
        tried_list = []
        logging.info('%s assigned to %s for meal %d' % (staff.position, util.CRITTERS[patrol], self.meal_number))
        staff.patrols_attended_list.append(patrol)
        self.patrol_counts[patrol] = self.patrol_counts[patrol] + 1
        logging.debug('Meal %d for patrol %s now has %d staff assigned' % (self.meal_number, patrol, self.patrol_counts[patrol]))
        return util.CRITTERS[patrol]


class Staff(object):

    position = None
    name = None
    critter = None
    assigned_meal_list = []
    critter_meal_list = []
    patrols_attended_list = []

    def __init__(self, position, name, critter):
        self.position = position
        self.name = name
        self.critter = critter
        self.assigned_meal_list = []
        self.critter_meal_list = []
        self.patrols_attended_list = []
        staffers[self.position] = self

        if self.critter == util.BEAVER:
            beaver.append(self.name)
        elif self.critter == util.BOBWHITE:
            bobwhite.append(self.name)
        elif self.critter == util.EAGLE:
            eagle.append(self.name)
        elif self.critter == util.FOX:
            fox.append(self.name)
        elif self.critter == util.OWL:
            owl.append(self.name)
        elif self.critter == util.BEAR:
            bear.append(self.name)
        elif self.critter == util.BUFFALO:
            buffalo.append(self.name)
        elif self.critter == util.ANTELOPE:
            antelope.append(self.name)

    def __cmp__(self, other):
        if hasattr(other, 'critter'):
            return self.critter.__cmp__(other.critter)

    def assign_meal(self, meal):

        if meal.meal_number in [12, 13]:
            patrol = 'Staff'
        else:
            patrol = meal.choose_meal(self)

#            patrol = self.pick_meal()
        logging.debug('Meal %d, return %s for %s' % (meal.meal_number, patrol, self.name))
        return patrol

    def __str__(self):

        if self.critter is not None:
            staff_critter = util.CRITTERS[self.critter]
        else:
            staff_critter = 'N/A'

        staff_info = ''.join(self.position) + ': ' + self.name + ' (' + staff_critter + ')\n'

        return staff_info + ' ' + str(self.assigned_meal_list)

    def show_meals(self):
        day_1 = 'Day 1:' + '\n\t' + \
                'Lunch: %s' % self.assigned_meal_list[0] + '\t\t' + \
                'Dinner: %s' % self.assigned_meal_list[1] + '\n'
        day_2 = 'Day 2:' + '\n\t' + \
                'Breakfast: %s' % self.assigned_meal_list[2] + '\t\t' + \
                'Lunch: %s' % self.assigned_meal_list[3] + '\t\t' + \
                'Dinner: %s' % self.assigned_meal_list[4] + '\n'
        day_3 = 'Day 3:' + '\n\t' + \
                'Breakfast: %s' % self.assigned_meal_list[5] + '\t\t' + \
                'Lunch: %s' % self.assigned_meal_list[6] + '\n'
        day_4 = 'Day 4:' + '\n\t' + \
                'Lunch: %s' % self.assigned_meal_list[7] + '\t\t' + \
                'Dinner: %s' % self.assigned_meal_list[8] + '\n'
        day_5 = 'Day 5:' + '\n\t' + \
                'Breakfast: %s' % self.assigned_meal_list[9] + '\t\t' + \
                'Lunch: %s' % self.assigned_meal_list[10] + '\t\t' + \
                'Dinner: %s' % self.assigned_meal_list[11] + '\n'
        day_6 = 'Day 6:' + '\n\t' + \
                'Breakfast: %s' % self.assigned_meal_list[12] + '\t\t' + \
                'Lunch: %s' % self.assigned_meal_list[13] + '\n'

        print(day_1 + day_2 + day_3 + day_4 + day_5 + day_6)


class CourseDirector(Staff):

    def __init__(self, name, critter):
        super().__init__(util.COURSE_DIRECTOR, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number in [1, 14]:
            return 'Head table'
        elif meal.meal_number == 11:
            return 'PLC'
        else:
            return super().assign_meal(meal)


class AsmProgram(Staff):

    def __init__(self, name, critter):
        super().__init__(util.ASM_PROGRAM, name, critter)
        self.pre_assigned_meals = [1, 11]

    def assign_meal(self, meal):
        if meal.meal_number in [1, 14]:
            return 'Head table'
        else:
            return super().assign_meal(meal)


class Spl(Staff):

    def __init__(self, name, critter):
        super().__init__(util.SPL, name, critter)
        self.pre_assigned_meals = [1, 11]

    def assign_meal(self, meal):
        if meal.meal_number == 1:
            return 'Head table'
        elif meal.meal_number == 11:
            return 'PLC'
        else:
            return super().assign_meal(meal)


class CrewAdvisor(Staff):

    def __init__(self, name, critter):
        super().__init__(util.CREW_ADVISOR, name, critter)


class ScribeCommunication(Staff):

    def __init__(self, name, critter):
        super().__init__(util.SCRIBE_COMMUNICATION, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number == 11:
            return 'PLC'
        else:
            return super().assign_meal(meal)


class ScribeAv(Staff):

    def __init__(self, name, critter):
        super().__init__(util.SCRIBE_AV, name, critter)


class AsmLogistics(Staff):

    def __init__(self, name, critter):
        super().__init__(util.ASM_LOGISTICS, name, critter)


class ScribeRegistrar(Staff):

    def __init__(self, name, critter):
        super().__init__(util.SCRIBE_REGISTRAR, name, critter)


class Quartermaster(Staff):

    def __init__(self, name, critter):
        super().__init__(util.QUARTERMASTER, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number == 11:
            return 'PLC'
        else:
            return super().assign_meal(meal)


class QmAssistant1(Staff):

    def __init__(self, name, critter):
        super().__init__(util.QM_ASSISTANT_1, name, critter)


class QmAssistant2(Staff):

    def __init__(self, name, critter):
        super().__init__(util.QM_ASSISTANT_2, name, critter)


class AsmTroopGuides(Staff):

    def __init__(self, name, critter):
        super().__init__(util.ASM_TROOP_GUIDES, name, critter)


class TroopGuide(Staff):

    def __init__(self, patrol, name, critter):
        super().__init__(patrol, name, critter)
        self.pre_assigned_meals = [1, 2, 3, 4, 5, 6, 7]

    def assign_meal(self, meal):
        if meal.meal_number in range(1, 9) or meal.meal_number == 14:
            # add count to meal
            patrol = self.__class__.__name__[10:]
            patrol_num = next(patrol_num for patrol_num, value in util.CRITTERS.items() if value == patrol)
            meal.patrol_counts[patrol_num] = meal.patrol_counts[patrol_num] + 1
            return patrol
        elif meal == 12 or meal == 13:
            return 'Staff'
        else:
            return super().assign_meal(meal)


class TroopGuideBeaver(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_BEAVER, name, critter)


class TroopGuideBobwhite(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_BOBWHITE, name, critter)


class TroopGuideEagle(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_EAGLE, name, critter)


class TroopGuideFox(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_FOX, name, critter)


class TroopGuideOwl(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_OWL, name, critter)


class TroopGuideBear(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_BEAR, name, critter)


class TroopGuideBuffalo(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_BUFFALO, name, critter)


class TroopGuideAntelope(TroopGuide):

    def __init__(self, name, critter):
        super().__init__(util.TG_ANTELOPE, name, critter)


class Mentor(Staff):

    def __init__(self, name, critter):
        super().__init__(util.MENTOR, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number in [1, 14]:
            return 'Head table'
        else:
            return super().assign_meal(meal)


class Professional(Staff):

    def __init__(self, name, critter):
        super().__init__(util.PROFESSIONAL, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number in [1]:
            return 'Head table'
        else:
            return super().assign_meal(meal)


class YouthStaffPresident(Staff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_PRESIDENT, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number < 8:
            return ''
        elif meal.meal_number in [12, 13]:
            return 'Staff'
        else:
            return super().assign_meal(meal)


class YouthStaffVP(Staff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_VP, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number < 8:
            return ''
        elif meal.meal_number in [12, 13]:
            return 'Staff'
        else:
            return super().assign_meal(meal)


class YouthStaff(Staff):

    def __init__(self, patrol, name, critter=None):
        super().__init__(patrol, name, critter)

    def assign_meal(self, meal):
        if meal.meal_number < 8:
            logging.debug('Not at meal')
            return ''
        elif meal.meal_number in [12, 13]:
            return 'Staff'
        else:
            # add count to meal
            patrol = self.__class__.__name__[10:]
            patrol_num = next(patrol_num for patrol_num, value in util.CRITTERS.items() if value == patrol)
            meal.patrol_counts[patrol_num] = meal.patrol_counts[patrol_num] + 1
            return patrol


class YouthStaffBeaver(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_BEAVER, name, critter)


class YouthStaffBobwhite(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_BOBWHITE, name, critter)


class YouthStaffEagle(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_EAGLE, name, critter)


class YouthStaffFox(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_FOX, name, critter)


class YouthStaffOwl(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_OWL, name, critter)


class YouthStaffBear(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_BEAR, name, critter)


class YouthStaffBuffalo(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_BUFFALO, name, critter)


class YouthStaffAntelope(YouthStaff):

    def __init__(self, name, critter=None):
        super().__init__(util.YS_ANTELOPE, name, critter)


def critter_report():
    return ('Beavers(%d): ' % len(beaver)) + ', '.join(beaver) + '\n' + \
           ('Bobwhite(%d): ' % len(bobwhite)) + ', '.join(bobwhite) + '\n' + \
           ('Eagle(%d): ' % len(eagle)) + ', '.join(eagle) + '\n' + \
           ('Fox(%d): ' % len(fox)) + ', '.join(fox) + '\n' + \
           ('Owl(%d): ' % len(owl)) + ', '.join(owl) + '\n' + \
           ('Bear(%d): ' % len(bear)) + ', '.join(bear) + '\n' + \
           ('Buffalo(%d): ' % len(buffalo)) + ', '.join(buffalo) + '\n' + \
           ('Antelope(%d): ' % len(antelope)) + ', '.join(antelope) + '\n' + \
           ('\nTotal: %d' % (len(beaver) + len(bobwhite) + len(eagle) + len(fox) + len(owl) + len(bear) +
                             len(buffalo) + len(antelope))) + '\n'
