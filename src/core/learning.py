class Learning:
    def __init__(self):
        self.user_feedback = []

    def add_feedback(self, question, correct_answer, user_answer):
        self.user_feedback.append({
            "question": question,
            "correct_answer": correct_answer,
            "user_answer": user_answer
        })

    def get_feedback_summary(self):
        return self.user_feedback
