def check_cloze(user_answer, answer_key, options):
    # Placeholder function to check cloze answers
    #print("in check_cloze_answer... user_answer:", user_answer, " answer_key:", answer_key)
    #error = False
    total_score = 0
    answer_key_parts = [part.strip().lower() for part in answer_key.split('/')]
    #print("answer_key_parts:", answer_key_parts)
    user_answer_parts = [part.strip().lower() for part in user_answer.split('/')]
    #print("user_answer_parts:", user_answer_parts)

    # Ensure both arrays are the same size
    if len(user_answer_parts) != len(answer_key_parts):
        #print("Error: user_answer_parts and answer_key_parts are not the same size.")
        return False  # or handle the mismatch appropriately

    # Collect detailed comparison information
    cloze_question_results = []
    for user_part, answer_part in zip(user_answer_parts, answer_key_parts):
        score = 0
        error = False
        is_correct = user_part == answer_part
        if not is_correct:
            error = True
        else:
            score += 5  # Increment score for correct answers

        total_score += score
        cloze_question_results.append({
            "user_answer": user_part,
            "answer_key": answer_part,
            "error_flag": error,
            "score": score,
        })

    #print("Detailed comparison results:", cloze_question_results)

    # Determine overall error
    #overall_error = any(not result["is_correct"] for result in cloze_question_results)

    # Return detailed results, overall error, and score
    """
    return {
        "error_flag": overall_error,
        "score": total_score,
        "detailed_results": results,
    }
    """
    #return not overall_error 
    return cloze_question_results
            
def check_button_cloze(user_answer, answer_key, options):
    # Placeholder function to check button select answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_button_select(user_answer, answer_key, options):
    # Placeholder function to check button select answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_radio(user_answer, answer_key, options):
    # Placeholder function to check radio button answers
    error = False
    score = 0
    if user_answer.strip().lower() == answer_key.strip().lower():
        score += 5
    else:
        error = True
        
    return not error
    #return user_answer.strip().lower() == answer_key.strip().lower()

def check_checkbox(user_answer, answer_key, options):
    # Placeholder function to check checkbox answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_words_scramble(user_answer, answer_key, options):
    # Placeholder function to check words scramble answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_speech_recognition(user_answer, answer_key, options):
    # Placeholder function to check speech recognition answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_words_select(user_answer, answer_key, options):
    # Placeholder function to check words select answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_dropdown(user_answer, answer_key, options):
    # Placeholder function to check dropdown answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_sentence_scramble(user_answer, answer_key, options):
    # Placeholder function to check sentence scramble answers
    return user_answer.strip().lower() == answer_key.strip().lower()

def check_answer(format, user_answer, answer_key):
    # Placeholder function to check if the user's answer is correct
    #print("Checking answer... format:", format, " user_answer:", user_answer, " answer_key:", answer_key)
    if format == 1:   #cloze
        #print("Checking cloze answer...")
        cloze_question_results = check_cloze(user_answer, answer_key, options=[])
        #print("Computed cloze question results:", cloze_question_results)
        assessment_results = {
            "error_flag": any(result["error_flag"] for result in cloze_question_results),
            "score": sum(result["score"] for result in cloze_question_results),
            "cloze_question_results": cloze_question_results,
        }
        return assessment_results
    
        #return check_cloze(user_answer, answer_key, options=[])
        
    