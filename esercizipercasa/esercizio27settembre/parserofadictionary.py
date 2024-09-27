import json

def Serialize(dict: dict, file_path: str):
    dizionario_string = json.dumps(dict)
    try:
        with open(file_path, 'w') as file:
            file.write(dizionario_string)
        return True
    except Exception as e:
        return False

def Deserialize(file_path: str):
    try:
        with open(file_path, 'r') as file:
            dizionario = json.load(file)  
        return dizionario
    except Exception as e:
        return None

def analyze_quiz(data):
    total_questions = 0
    total_options = 0
    math_questions = 0
    
    for category, questions in data['quiz'].items():
        for q_id, question_info in questions.items():
            total_questions += 1
            total_options += len(question_info['options'])
            if category == 'maths':
                math_questions += 1
    
    average_options = total_options / total_questions if total_questions else 0
    
    return total_questions, average_options, math_questions

file_path = "/home/user/Scrivania/Vscodeprojects2/esercizipercasa/esercizio27settembre/quiz.json"
quiz_data = Deserialize(file_path)

if quiz_data:
    total_questions, average_options, math_questions = analyze_quiz(quiz_data)
    print(f"Totale domande: {total_questions}")
    print(f"Numero medio di risposte possibili: {average_options:.2f}")
    print(f"Domande di matematica: {math_questions}")
else:
    print("Impossibile caricare i dati dal file JSON.")
