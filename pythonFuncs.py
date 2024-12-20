import Survey

ID_INDEX = 0
HABITS_INDEX = 1
AGE_INDEX = 2
GENDER_INDEX = 3
FIRST_SCORE_INDEX = 4
NUM_SCORES = 5
VALID_ID_LEN = 8
MAX_AGE = 100
MIN_AGE = 10
MAX_SCORE = 10
MIN_SCORE = 1
Q_ARR_SIZE = 10

#filters the lines in the old survey
#id - lengths of 8, age in range(10,100) scores in range(1,10)
#returns true if line s valid, false if not
#line: the line that we want to check(as list type)
def is_survey_file_line_correct(line):
    return (len(line[ID_INDEX]) == VALID_ID_LEN and
    int(line[AGE_INDEX]) in range(MIN_AGE, MAX_AGE+1) and
    all(int(score) in range(MIN_SCORE,MAX_SCORE+1)
        for score in line[FIRST_SCORE_INDEX:]))

#determines the right eating habit number for given hbit str
def int_eating_habits(eating_habits):
    habits_list = ['Vegan', 'Vegaterian', 'Omnivore']
    return habits_list.index(eating_habits)

#Filters a survey and prints to screen the corrected answers:
#old_survey_path: The path to the unfiltered survey
def correct_myfile(old_survey_path):
    old_survey_file = open(old_survey_path, 'r')
    survey_dict = {}
    buffer = old_survey_file.read().splitlines()
    for line in buffer:
        fixed_space_list = [x for x in line.split(' ') if x != '']
        if is_survey_file_line_correct(fixed_space_list):
            survey_dict[fixed_space_list[ID_INDEX]] = line
    for cur_id in sorted(survey_dict.keys()):
        print(survey_dict[cur_id])
    old_survey_file.close()

#Returns a new Survey item with the data of a new survey file:
#survey_path: The path to the survey
def scan_survey(survey_path):
    scanned_survey = Survey.SurveyCreateSurvey()
    survey_file = open(survey_path, 'r')
    buffer = survey_file.read().splitlines()
    for line in buffer:
        fixed_space_list = [x for x in line.split(' ') if x != '']

        cur_id = int(fixed_space_list[ID_INDEX])
        cur_age = int(fixed_space_list[AGE_INDEX])
        cur_gender = fixed_space_list[GENDER_INDEX] == 'Man'
        cur_habits = int_eating_habits(fixed_space_list[HABITS_INDEX])

        cur_score = Survey.SurveyCreateIntAr(NUM_SCORES)
        for x in range(NUM_SCORES):
            Survey.SurveySetIntArIdxVal(cur_score, x, int
                (fixed_space_list[FIRST_SCORE_INDEX+x]))

        if Survey.SurveyAddPerson(scanned_survey, cur_id, cur_age,
                                  cur_gender, cur_habits, cur_score)\
                                   == Survey.SURVEY_ALLOCATION_FAILED:
            Survey.SurveyDestroySurvey(scanned_survey)
            return None
    return scanned_survey

#Prints a python list containing the number of votes for each rating of a group\
# according to the arguments
#s: the data of the Survey object
#choc_type: the number of the chocolate (between 0 and 4)
#gender: the gender of the group (string of "Man" or "Woman"
#min_age: the minimum age of the group (a number)
#max_age: the maximum age of the group (a number)
#eating_habits: the eating habits of the group (string of "Omnivore", "Vegan" \
# or "Vegetarian")
def print_info(s, choc_type, gender, min_age, max_age, eating_habits):
    s_quary = Survey.SurveyQuerySurvey(s, choc_type, gender == 'Man',min_age,
                                       max_age, int_eating_habits
                                       (eating_habits))
    quary_list= []
    for idx in range(Q_ARR_SIZE):
        quary_list.append(Survey.SurveyGetIntArIdxVal(s_quary, idx))
    print(quary_list)
    Survey.SurveyQueryDestroy(s_quary)
		
#Clears a Survey object data
#s: the data of the Survey object
def clear_survey(s):
    Survey.SurveyDestroySurvey(s)

