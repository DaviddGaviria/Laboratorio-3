import random

def registerUser(name, password):
    filename = 'users.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name:
                    return "User already registered"
    except FileNotFoundError:
        pass

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{name},{password}\n")

    return "User successfully registered"

def openCloseSession(name, password, flag):
    filename = 'users.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name and stored_password == password:
                    if flag:
                        return "Session was successfully opened"
                    else:
                        return "Session was successfully closed"
    except FileNotFoundError:
        return "error"

    return "error"

def updateScore(name, password, score):
    users_filename = 'users.txt'
    scores_filename = 'scores.txt'

    try:
        with open(users_filename, 'r', encoding='utf-8') as file:
            user_found = False
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name and stored_password == password:
                    user_found = True
                    break

        if not user_found:
            return "error"
    except FileNotFoundError:
        return "error"

    try:
        scores = {}
        with open(scores_filename, 'r', encoding='utf-8') as file:
            for line in file:
                stored_name, stored_score = line.strip().split(',')
                scores[stored_name] = int(stored_score)

        scores[name] = score

        with open(scores_filename, 'w', encoding='utf-8') as file:
            for user, user_score in scores.items():
                file.write(f"{user},{user_score}\n")

        return "Score was successfully updated"
    except FileNotFoundError:
        with open(scores_filename, 'w', encoding='utf-8') as file:
            file.write(f"{name},{score}\n")
        return "Score was successfully updated"

    return "error"

def getScore(name, password):
    users_filename = 'users.txt'
    scores_filename = 'scores.txt'

    try:
        with open(users_filename, 'r', encoding='utf-8') as file:
            user_found = False
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name and stored_password == password:
                    user_found = True
                    break

        if not user_found:
            return "error"
    except FileNotFoundError:
        return "error"

    try:
        with open(scores_filename, 'r', encoding='utf-8') as file:
            for line in file:
                stored_name, stored_score = line.strip().split(',')
                if stored_name == name:
                    return stored_score
    except FileNotFoundError:
        return "error"

    return "error"

def usersList(name, password):
    users_filename = 'users.txt'
    scores_filename = 'scores.txt'

    try:
        with open(users_filename, 'r', encoding='utf-8') as file:
            user_found = False
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name and stored_password == password:
                    user_found = True
                    break

        if not user_found:
            return "error"
    except FileNotFoundError:
        return "error"

    try:
        user_list = []
        with open(scores_filename, 'r', encoding='utf-8') as file:
            for line in file:
                stored_name, stored_score = line.strip().split(',')
                user_list.append((stored_name, int(stored_score)))
        return user_list
    except FileNotFoundError:
        return "error"

    return "error"


def question(name, password, questions_asked):
    users_filename = 'users.txt'
    questions_filename = 'questions.txt'

    try:
        with open(users_filename, 'r', encoding='utf-8') as file:
            user_found = False
            for line in file:
                stored_name, stored_password = line.strip().split(',')
                if stored_name == name and stored_password == password:
                    user_found = True
                    break

        if not user_found:
            return "error", questions_asked
    except FileNotFoundError:
        return "error", questions_asked

    try:
        with open(questions_filename, 'r', encoding='utf-8') as file:
            all_questions = [line.strip() for line in file if line.strip() not in questions_asked]

        # Filtrar preguntas válidas
        valid_questions = [q for q in all_questions if len(q.split(':')) == 7]

        if not valid_questions:
            return "No valid questions available.", questions_asked

        question = random.choice(valid_questions)
        questions_asked.add(question)
        try:
            question_cat, question_text, option_a, option_b, option_c, option_d, correct_option = question.split(':')
        except ValueError:
            print("An invalid question format was detected and skipped.")
            return "error", questions_asked

        print(f"Category: {question_cat}")
        print(f"Question: {question_text}")
        print(f"a) {option_a}")
        print(f"b) {option_b}")
        print(f"c) {option_c}")
        print(f"d) {option_d}")
        answer = input("Your answer (a/b/c/d): ").strip().lower()

        if answer == correct_option.strip().lower():
            print("Correct!")
            return True, questions_asked
        else:
            print(f"Incorrect. The correct answer is {correct_option}.")
            return False, questions_asked

    except FileNotFoundError:
        return "error", questions_asked
def get_question(categoria):
    questions_filename = 'questions.txt'
    try:
        with open(questions_filename, 'r', encoding='utf-8') as file:
            valid_questions = [line.strip() for line in file if line.startswith(categoria)]
            if valid_questions:
                selected_question = random.choice(valid_questions)
                question_cat, question_text, option_a, option_b, option_c, option_d, correct_option = selected_question.split(':')
                return {
                    'category': question_cat,
                    'question': question_text,
                    'options': [option_a, option_b, option_c, option_d],
                    'answer': correct_option
                }
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    try:
        print("Welcome to the user system!")
        
        while True:
            print("\nOptions:")
            print("1. Register User")
            print("2. Open Session")
            print("3. Close Session")
            print("8. Exit")
            
            choice = input("Choose an option (1, 2, 3, 8): ")
            
            if choice == '1':
                name = input("Enter username: ")
                password = input("Enter password: ")
                result = registerUser(name, password)
                print(result)
                if result == "User successfully registered":
                    result = openCloseSession(name, password, True)
                
            elif choice == '2':
                name = input("Enter username: ")
                password = input("Enter password: ")
                result = openCloseSession(name, password, True)
                print(result)
                
            if result == "Session was successfully opened":
                while True:
                    print("\nOptions:")
                    print("1. Ask Questions")
                    print("2. View Score")
                    print("3. Logout")
                    
                    session_choice = input("Choose an option (1, 2, 3): ")

                    if session_choice == '1':
                        questions_asked = set()
                        question_count = 0
                        correct_answers = 0
                        while question_count < 10:
                            is_correct, questions_asked = question(name, password, questions_asked)
                            question_count += 1

                            if isinstance(is_correct, str) and is_correct == "error":
                                print("An error occurred while retrieving questions.")
                                break

                            if is_correct:
                                correct_answers += 1

                        print(f"You answered {correct_answers} out of 10 questions correctly.")
                        current_score_str = getScore(name, password)
                        if current_score_str.isdigit():
                            current_score = int(current_score_str)
                            updateScore(name, password, current_score + correct_answers)
                        else:
                            updateScore(name, password, correct_answers)

                    elif session_choice == '2':
                        score = getScore(name, password)
                        print(f"Your score is: {score}")

                    elif session_choice == '3':
                        result = openCloseSession(name, password, False)
                        print(result)
                        break

                    else:
                        print("Invalid option, please choose again.")
            
            elif choice == '3':
                name = input("Enter username: ")
                password = input("Enter password: ")
                result = openCloseSession(name, password, False)
                print(result)
            
            elif choice == '8':
                print("Exiting the user system. Goodbye!")
                break
            
            else:
                print("Invalid option, please choose again.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to exit...")
