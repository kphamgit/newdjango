from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, CategorySerializer, SubCategorySerializer, UnitSerializer, QuizSerializer, QuestionSerializer, QuizAttemptSerializer, QuestionAttemptSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Category, SubCategory, Unit, Quiz, Question, QuizAttempt, QuestionAttempt
from rest_framework.decorators import api_view


from rest_framework.response import Response


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.all().order_by('category_number')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer # needed by the Django REST Framework
    # to determine how to serialize the data returned by the get_queryset method
    
    def get_queryset(self):
        return Category.objects.order_by('category_number').prefetch_related('sub_categories')
    
class UnitListView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        sub_category_id = self.kwargs.get('sub_category_id')
        #print("UnitListView, sub_category_id:", sub_category_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Unit.objects.filter(sub_category_id=sub_category_id).order_by('unit_number')
        #print("UnitListView, Filtered Units no Prefetch:", queryset)
        #print("UnitListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    

    def unit_list(request, pk):
        """
        List all units, or create a new snippet.
        """
    #print("unit_list called with pk:", request.query_params)
    #sub_category_id = self.kwargs.get('pk')
        units = Unit.objects.filter(sub_category_id=pk).order_by('unit_number')
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)


class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        unit_id = self.kwargs.get('unit_id')
        print("QuizListView, unit_id:", unit_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Quiz.objects.filter(unit_id=unit_id).order_by('quiz_number')
        #print("QuizListView, Filtered Quizzes no Prefetch:", queryset)
        #print("QuizListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        #print("QuestionListView, quiz_id:", quiz_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Question.objects.filter(quiz_id=quiz_id).order_by('question_number')
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
            

class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        #queryset = Unit.objects.filter(category_id=category_id).prefetch_related('quizzes')
        queryset = SubCategory.objects.filter(category_id=category_id).order_by('sub_category_number')
        #print("Filtered SubCats:", queryset)
        #print("SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
@api_view(["POST"])
def create_quiz_attempt(request, pk):
        """
            Create or retrieve a QuizAttempt for the given quiz and user.
        """
    #print("unit_list called with pk:", request.query_params)
    #sub_category_id = self.kwargs.get('pk')
        #units = Unit.objects.filter(sub_category_id=pk).order_by('unit_number')
        # retrieve user from request data (or use a default user for testing)
        #user = User.objects.get(username="admin")
        
        #print("get_or_create QuizAttempt for user id:", user.id, "and quiz_id:", pk)
        #print(" user is ", user)
        
        #print("request.data:", request.data)
        
        quiz_attempt, created  = QuizAttempt.objects.get_or_create(
            user_id=request.data['user_id'],
            quiz_id=pk,
            completion_status="uncompleted",
            defaults={'score': 0, 'user_id': request.data['user_id'], 'quiz_id' : pk}
        )
        if created:
            #print("New QuizAttempt created.")
            serializer = QuizAttemptSerializer(quiz_attempt)
            #print(" QQQQQQQQQQQ QuizAttempt created:", serializer.data)
            
            # also create the first QuestionAttempt for the first question in the quiz
            first_question = Question.objects.filter(quiz_id=pk).order_by('question_number').first()
            if first_question:
                question_attempt = QuestionAttempt.objects.create(
                    quiz_attempt=quiz_attempt,
                    question=first_question,
                    completed=False,
                )
                #print("Created first QuestionAttempt for Question id:", first_question.id, "question_attempt id:", question_attempt.id)
                
                return Response({
                    "quiz_attempt": serializer.data,
                    "created": True,
                    "question": QuestionSerializer(first_question).data,
                    "question_attempt_id": question_attempt.id,
                })
                
        else:
            print("QuizAttempt already exists.")
            serializer = QuizAttemptSerializer(quiz_attempt)
            #retrieve all question_attempts for this quiz_attempt using one to many relationship
            question_attempts = quiz_attempt.question_attempts.all()
            #return a message indicating that the QuizAttempt already exists
            return Response({
                "created": False,
                "question_id": 0,  # Add the additional information here
                "quiz_attempt": serializer.data,
            })
        
@api_view(["GET"])
def continue_quiz_attempt(request, pk):
    try:
        quiz_attempt = QuizAttempt.objects.get(id=pk)
        #print("Continuing QuizAttempt id:", pk)
        #make a new QuestionAttempt for the first question in the quiz
        # inspect the last question attempt of this quiz attempt
        last_question_attempt = quiz_attempt.question_attempts.order_by('-id').first()
        if last_question_attempt:
        # check if last question attempt is completed
            if last_question_attempt.completed:
                print("Last QuestionAttempt is completed. Creating next QuestionAttempt.")
                next_question = Question.objects.filter(quiz_id=quiz_attempt.quiz_id, question_number__gt=last_question_attempt.question.question_number).order_by('question_number').first()
                if next_question:
                    print("Next question found:", next_question.id)
                    question_attempt = QuestionAttempt.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=next_question,
                        completed=False,
                        
                    )
                    question_serializer = QuestionSerializer(next_question)
                    return Response({
                        "message": "Next QuestionAttempt created.",
                        "quiz_attempt_id": pk,
                        "question": question_serializer.data,
                        "question_attempt_id": question_attempt.id
                    })
                else:
                    print("No more questions available in the quiz.")
                    return Response({
                        "message": "No more questions available in the quiz.",
                        "quiz_attempt_id": pk,
                        "question": None
                    })
            else:
                print("Last QuestionAttempt is not completed. Returning the same question.")
                question_serializer = QuestionSerializer(last_question_attempt.question)
                return Response({
                    "message": "Returning the current QuestionAttempt.",
                    "quiz_attempt_id": pk,
                    "question": question_serializer.data
                }) 
    
    
    except QuizAttempt.DoesNotExist:
        return Response({
            "error": "Quiz attempt not found."
        }, status=404)
        
@api_view(["GET"])
def reset_quiz_attempt(request, pk):
    """
        Reset the quiz attempt by deleting existing question attempts
        and setting the quiz attempt status to uncompleted.
    """
    try:
        quiz_attempt = QuizAttempt.objects.get(id=pk)
        # Delete all associated question attempts
        #print("Resetting QuizAttempt id:", pk)
        quiz_attempt.question_attempts.all().delete()
        # Reset quiz attempt status
        quiz_attempt.completion_status = "uncompleted"
        quiz_attempt.score = 0
        quiz_attempt.save()
        
        #make a new QuestionAttempt for the first question in the quiz
        first_question = Question.objects.filter(quiz_id=quiz_attempt.quiz_id).order_by('question_number').first()
        if first_question:
            question_attempt = QuestionAttempt.objects.create(
                quiz_attempt=quiz_attempt,
                question=first_question,
                completed=False,
            )
        
        question_serializer = QuestionSerializer(first_question)
        return Response({
            "message": "Quiz attempt has been reset. A new QuestionAttempt has been created for the first question.",
            "quiz_attempt_id": pk,
            "question": question_serializer.data,
            "question_attempt_id": question_attempt.id
        })
    except QuizAttempt.DoesNotExist:
        return Response({
            "error": "Quiz attempt not found."
        }, status=404)
            

@api_view(["POST"])
def create_question_attempt(request, pk):
    # path("quiz_attempts/<int:pk>/create_next_question_attempt/", views.create_question_attempt), 
    #print('create_question_attempt, request.data:', request.data)
    # client sends the current question number and quiz_attempt_id
    # request.data: {'question_number': 2}
    #current_question_number = request.data.get('question_number', 0)
    #print("IN CREATE QUESTION ATTEMPT, quiz_attempt_id:", pk)
    quiz_attempt = QuizAttempt.objects.get(id=pk)
    next_question_number = request.data.get('question_number', 0) + 1
    last_question_in_quiz = quiz_attempt.quiz.questions.order_by('-question_number').first()
    if (next_question_number > last_question_in_quiz.question_number):
            #print("Next question number is greater than last question:", next_question_number, "checking errorneous questions array")
            errorneous_questions_array = quiz_attempt.errorneous_questions.split(",") if quiz_attempt.errorneous_questions else []
            #print(" errorneous_questions_array:", errorneous_questions_array)
            if len(errorneous_questions_array) == 0:
                #print(" no errorneous questions to review")
                # mark quiz attempt as completed
                quiz_attempt.completion_status = "completed"
                quiz_attempt.save()
                return Response({
                    "message": "QuestionAttempt NOT CREATED. No more questions available in the quiz.",
                    "question_attempt_id": pk,
                    "question": None,
                })
            else:
                #print(" there are errorneous questions to review")
                return Response({
                    "message": "No more questions available, but there are errorneous questions to review. Let's redo them.",
                    "question_attempt_id": pk,
                    "question": None,
                })
                
    else :
            # create next QuestionAttempt
            #print("HERE: create next QuestionAttempt for question number:", next_question_number)
            next_question = Question.objects.filter(quiz_id=quiz_attempt.quiz_id, question_number=next_question_number).first()
            if next_question:
                #print("Found next question question id:", next_question.id)
                new_question_attempt = QuestionAttempt.objects.create(
                    quiz_attempt=quiz_attempt,
                    question=next_question,
                    completed=False,
                )
                #print("Created next QuestionAttempt id:", new_question_attempt.id, "for Question id:", next_question.id)
                return Response({
                    "message": "QuestionAttempt CREATED successfully. Next QuestionAttempt created.",
                    "question_attempt_id": new_question_attempt.id,
                    "question": QuestionSerializer(next_question).data,
                })
            else:
                #print("No next question found, even though not at the end of the quiz.")
                return Response({
                    "message": "QuestionAttempt NOT CREATED. No more questions available in the quiz.",
                    "question_attempt_id": pk,
                    "question": None,
                })  
            
#path("question_attempts/<int:pk>/update/", views.update_question_attempt),  
#redo_errorneous_question_attempts
@api_view(["POST"])
def create_question_attempt_redo(request, pk):
    # path("quiz_attempts/<int:pk>/create_next_question_attempt/", views.create_question_attempt), 
    #print('create_question_attempt, request.data:', request.data)
    # client sends the current question number and quiz_attempt_id
    # request.data: {'question_number': 2}
    #current_question_number = request.data.get('question_number', 0)
    #print("IN CREATE QUESTION ATTEMPT REDO, quiz_attempt_id:", pk)
    quiz_attempt = QuizAttempt.objects.get(id=pk)
    # search for the next errorneous question in errorneous_questions array in quiz_attempt
    errorneous_question_ids = [int(qid) for qid in quiz_attempt.errorneous_questions.split(",") if qid.isdigit()]
    #print("Errorneous question ids:", errorneous_question_ids)
    if errorneous_question_ids:
        #retrieve the first errorneous question
        next_errorneous_question = Question.objects.filter(id__in=errorneous_question_ids).order_by('question_number').first()
        if next_errorneous_question:
            #print("Redo: found next errorneous question question id:", next_errorneous_question.id)
            new_question_attempt = QuestionAttempt.objects.create(
                quiz_attempt=quiz_attempt,
                question=next_errorneous_question,
                completed=False,
            )
            #print("Created next QuestionAttempt id:", new_question_attempt.id, "for Question id:", next_question.id)
            return Response({
                "message": "QuestionAttempt REDO CREATED successfully. Next errorneous QuestionAttempt created.",
                "question_attempt_id": new_question_attempt.id,
                "question": QuestionSerializer(next_errorneous_question).data,
            })
        else:
            #print("No errorneous question found to redo.")
            return Response({
                "message": "QuestionAttempt REDO NOT CREATED. No errorneous questions found.",
                "question_attempt_id": pk,
                "question": None,
            })
    else:
        #print("No errorneous questions found to redo.")
        return Response({
            "message": "QuestionAttempt REDO NOT CREATED. No errorneous questions found.",
            "question_attempt_id": pk,
            "question": None,
        })


@api_view(["GET"])
def redo_errorneous_question_attempts(request, pk):
    try:
        quiz_attempt = QuizAttempt.objects.get(id=pk)
        #print("Redoing errorneous questions for QuizAttempt id:", pk)
        # get the list of errorneous question ids
        if quiz_attempt.errorneous_questions:
            errorneous_question_ids = [int(qid) for qid in quiz_attempt.errorneous_questions.split(",") if qid.isdigit()]
            #print("Errorneous question ids:", errorneous_question_ids)
            if errorneous_question_ids:
                first_errorneous_question = Question.objects.filter(id__in=errorneous_question_ids).order_by('question_number').first()
                if first_errorneous_question:
                    question_attempt = QuestionAttempt.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=first_errorneous_question,
                        completed=False,
                    )
                    print("redo_errorneous_question_attempts, Created QuestionAttempt id:", question_attempt.id, "for Question id:", first_errorneous_question.id)
                    return Response({
                        "message": "Redoing errorneous questions. Created new QuestionAttempt.",
                        "question_attempt_id": question_attempt.id,
                        "question": QuestionSerializer(first_errorneous_question).data,
                    })
        print("No errorneous questions to redo.")
        return Response({
            "message": "No more errorneous questions.",
            "question_attempt_id": None,
            "question": None,
        })
        
    except QuizAttempt.DoesNotExist:
        return Response({
            "error": "Quiz attempt not found."
        }, status=404)

@api_view(["POST"])
def update_question_attempt_redo(request, pk):
    try:
        question_attempt = QuestionAttempt.objects.get(id=pk)
        #print("update_question_attempt_redo QuestionAttempt id:", pk)
        #print("request.data:", request.data)
        
        #update fields
        question_attempt.error_flag = request.data.get('error_flag', question_attempt.error_flag)
        question_attempt.score = request.data.get('score', question_attempt.score)
        question_attempt.answer = request.data.get('answer', question_attempt.answer)
        question_attempt.completed = True
        question_attempt.save()
        
        quiz_attempt = question_attempt.quiz_attempt
        # if error_flag is False, remove question id from errorneous_questions in quiz_attempt
        if not question_attempt.error_flag:
            #print("  question is CORRECT, removing from errorneous_questions array if present")
            if quiz_attempt.errorneous_questions:
                errorneous_questions_array = quiz_attempt.errorneous_questions.split(",")
                if str(question_attempt.question.id) in errorneous_questions_array:
                    errorneous_questions_array.remove(str(question_attempt.question.id))
                    quiz_attempt.errorneous_questions = ",".join(errorneous_questions_array)
                    quiz_attempt.save()
                    
        # create next QuestionAttempt for the next errorneous question if any
        if quiz_attempt.errorneous_questions:
            errorneous_question_ids = [int(qid) for qid in quiz_attempt.errorneous_questions.split(",") if qid.isdigit()]
            #print("Remaining errorneous question ids:", errorneous_question_ids)
            if errorneous_question_ids:
                next_errorneous_question = Question.objects.filter(id__in=errorneous_question_ids).order_by('question_number').first()
                if next_errorneous_question:
                    new_question_attempt = QuestionAttempt.objects.create(
                        quiz_attempt=quiz_attempt,
                        question=next_errorneous_question,
                        completed=False,
                    )
                    #print("Created next QuestionAttempt id:", new_question_attempt.id, "for Question id:", next_errorneous_question.id)
                    return Response({
                        "message": "QuestionAttempt updated successfully. Next errorneous QuestionAttempt created.",
                        "question_attempt_id": new_question_attempt.id,
                        "question": QuestionSerializer(next_errorneous_question).data,
                    })
        else : # no more errorneous questions
            # mark quiz attempt as completed
            quiz_attempt.completion_status = "completed"
            quiz_attempt.save()
            #print("All errorneous questions have been finished. Marked QuizAttempt id:", quiz_attempt.id, "as completed.")
            return Response({
                "message": "All errorneous questions have been finished. QuizAttempt marked as completed.",
                "question_attempt_id": None,
                "question": None,
            })
        
    except QuestionAttempt.DoesNotExist:
              return Response({
                "error": "Question attempt not found."
              }, status=404)

@api_view(["POST"])
def update_question_attempt(request, pk):
       try: 
        question_attempt = QuestionAttempt.objects.get(id=pk)
        #print("Updating QuestionAttempt id:", pk)
        #print("request.data:", request.data)
        
        #update fields
        question_attempt.error_flag = request.data.get('error_flag', question_attempt.error_flag)
        question_attempt.score = request.data.get('score', question_attempt.score)
        question_attempt.answer = request.data.get('answer', question_attempt.answer)
        question_attempt.completed = True
        question_attempt.save()
        
        #print("Updated QuestionAttempt question number", question_attempt.question.question_number)
        
        if question_attempt.error_flag:
            # add question id to errorneous_questions in quiz_attempt
            #print("  question is errorneous, adding to errorneous_questions array")
            quiz_attempt = question_attempt.quiz_attempt
            if (len(quiz_attempt.errorneous_questions) == 0) :
                #print("  errorneous_questions is empty, adding  question id")
                quiz_attempt.errorneous_questions = str(question_attempt.question.id)
               
            else:
                #print("  errorneous_questions is not empty, adding question id")
                quiz_attempt.errorneous_questions += f",{question_attempt.question.id}"
                
            quiz_attempt.save()
            return Response({
                "message": "QuestionAttempt updated successfully. Question was errorneous.",
                "question_attempt_id": pk,
                "question": None,
            })
        
        else:
            # remove question id from errorneous_questions in quiz_attempt if present
            quiz_attempt = question_attempt.quiz_attempt
            if quiz_attempt.errorneous_questions:
                errorneous_questions_array = quiz_attempt.errorneous_questions.split(",")
                if str(question_attempt.question.id) in errorneous_questions_array:
                    errorneous_questions_array.remove(str(question_attempt.question.id))
                    quiz_attempt.errorneous_questions = ",".join(errorneous_questions_array)
                    quiz_attempt.save()
                    
        # if error_flag is true, return, do nothing more
        #if question_attempt.error_flag:
       
        next_question_number = question_attempt.question.question_number + 1
        #print("Next question number to look for:", next_question_number)
        #compare next_question_number last question number in the quiz
        #print("Looking for next question with question number:", next_question_number)
        last_question_in_quiz = question_attempt.quiz_attempt.quiz.questions.order_by('-question_number').first()
        #print(" last question number in quiz is :", last_question_in_quiz.question_number)
        if (next_question_number > last_question_in_quiz.question_number):
            #print("last question number is exceeded:", next_question_number, ">= ", last_question_in_quiz.question_number)
            quiz_attempt = question_attempt.quiz_attempt
            #print(" check errorneous questions array")
            errorneous_questions_array = quiz_attempt.errorneous_questions.split(",") if quiz_attempt.errorneous_questions else []
            #print(" errorneous_questions_array:", errorneous_questions_array)
            #if (quiz_attempt.errorneous_questions is not None) and (quiz_attempt.errorneous_questions != ""):
            if len(errorneous_questions_array) == 0:
                #print(" no errorneous questions to review")
                # mark quiz attempt as completed
                quiz_attempt.completion_status = "completed"
                quiz_attempt.save()
                return Response({
                    "message": "QuestionAttempt updated successfully. No more questions available in the quiz.",
                    "question_attempt_id": pk,
                    "question": None,
                })
            else:
                #print(" there are errorneous questions to review")
                return Response({
                    "message": "No more questions available, but there are errorneous questions to review. Let's redo them.",
                    "question_attempt_id": pk,
                    "question": None,
                })
                
        else :
            # create next QuestionAttempt
            next_question = Question.objects.filter(quiz_id=question_attempt.quiz_attempt.quiz_id, question_number=next_question_number).first()
            if next_question:
                #print("Found next question question id:", next_question.id)
                new_question_attempt = QuestionAttempt.objects.create(
                    quiz_attempt=question_attempt.quiz_attempt,
                    question=next_question,
                    completed=False,
                )
                #print("Created next QuestionAttempt id:", new_question_attempt.id, "for Question id:", next_question.id)
                return Response({
                    "message": "QuestionAttempt updated successfully. Next QuestionAttempt created.",
                    "question_attempt_id": new_question_attempt.id,
                    "question": QuestionSerializer(next_question).data,
                })
            else:
                #print("No next question found, even though not at the end of the quiz.")
                return Response({
                    "message": "QuestionAttempt updated successfully. No more questions available in the quiz.",
                    "question_attempt_id": pk,
                    "question": None,
                })  
            
        # also update the score of the quiz attempt if score is provided
        """
        score = request.data.get('score', None)
        if score is not None:
            quiz_attempt = question_attempt.quiz_attempt
            quiz_attempt.score = score
            quiz_attempt.save()
            print("Updated QuizAttempt id:", quiz_attempt.id, "with new score:", score)
        """
        """
        return Response({
            "message": "QuestionAttempt updated successfully.",
            "question_attempt_id": pk,
            "error_flag": question_attempt.error_flag,
            "completed": question_attempt.completed,
            "score": question_attempt.score,
        })
        """
       
       except QuestionAttempt.DoesNotExist:
              return Response({
                "error": "Question attempt not found."
              }, status=404)
              
    
#error_flag | completed | quiz_attempt_id | answer | score | question_id 