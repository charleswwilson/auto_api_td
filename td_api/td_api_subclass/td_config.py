import pickle
from config.objects import questions


class TdConfig:
    token_path = "./config_storage/token.pickle"

    def __init__(self):
        pass
        #self.token_path = "./config_storage/token.pickle"

    def load_config_from_pickle(self):
        _ = pickle.load(open("config/config.pickle", "rb"))
        self.api_key = _['api_key']
        self.redirect_uri = _['redirect_uri']
        self.account_number = _['account_number']
        self.password = _['password']
        self.auth_questions = _['auth_questions']
        if _['account_id']:
            self.account_id = _['account_id']

        return self

    def make_config(self):
        try:
            pickle_config = pickle.load(open("config/config.pickle", "rb"))

        except:
            pickle_config = {}
        print('You are now in setup this information will be stored locally in config/config.pickle \nplease delete this file before sharing your code with someone else.')
        api_key = input(
            f'Please input your td developer api key or hit enter to keep ({pickle_config.get("api_key")}): ') or pickle_config.get('api_key')
        redirect_uri = input(
            f'Please input the redirect uri or hit enter to keep ({pickle_config.get("redirect_uri")}): ') or pickle_config.get('redirect_uri')

        account_number = input(
            f'Please input your account number or hit enter to keep ({pickle_config.get("account_number")}): ') or pickle_config.get('account_number')
        if account_number:
            account_number = int(account_number)
        else:
            pass
        password = input(
            'Please enter your TD Ameritrade password or hit enter to keep (*******): ') or pickle_config.get('password')
        print(
            f'Please select your first security question for Td Ameritrade\nor use({pickle_config.get("question1")})')
        # question1
        question_list_1 = list(enumerate(questions.get('question1'), 1))
        print("\n\n")
        for i in question_list_1:
            print(i[0], i[1])
        selection_1 = input('Enter selection number: ')
        if selection_1 == '':
            question1 = pickle_config.get('question1')
        else:
            question1 = question_list_1[int(selection_1)-1][1]
        question1_answer = input("Please enter your answer: ")

        question_list_2 = list(enumerate(questions.get('question2'), 1))
        print("\n\n")
        for i in question_list_2:
            print(i[0], i[1])
        selection_2 = input('Enter selection number: ')
        if selection_2 == '':
            question2 = pickle_config.get('question2')
        else:
            question2 = question_list_2[int(selection_2)-1][1]
        question2_answer = input("Please enter your answer: ")

        question_list_3 = list(enumerate(questions.get('question3'), 1))
        print("\n\n")
        for i in question_list_3:
            print(i[0], i[1])
        selection_3 = input('Enter selection number: ')
        if selection_3 == '':
            question3 = pickle_config.get('question3')
        else:
            question3 = question_list_3[int(selection_3)-1][1]
        question3_answer = input("Please enter your answer: ")

        question_list_4 = list(enumerate(questions.get('question4'), 1))
        print("\n\n")
        for i in question_list_4:
            print(i[0], i[1])
        selection_4 = input('Enter selection number: ')
        if selection_4 == '':
            question4 = pickle_config.get('question4')
        else:
            question4 = question_list_4[int(selection_4)-1][1]
        question4_answer = input("Please enter your answer: ")

        pickle_config.update({"api_key": str(api_key),
                              "redirect_uri": str(redirect_uri),
                              "account_number": account_number,
                              "password": str(password),
                              "auth_questions": {question1: question1_answer,
                                                 question2: question2_answer,
                                                 question3: question3_answer,
                                                 question4: question4_answer}

                              })
        print(pickle_config)
        pickle.dump(pickle_config, open(
            "config/config.pickle", "wb"))
