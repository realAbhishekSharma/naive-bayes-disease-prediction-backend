from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view

import json


import pandas

training_workbook = pandas.read_csv("myapp/asset/Training.csv")

disease_list = training_workbook["prognosis"].drop_duplicates(ignore_index=True).values
training_data = training_workbook.drop(columns="prognosis").dropna(axis=1)
symptoms_list = training_data.columns.values
number_of_row, number_of_column = training_workbook.shape


test_workbook = pandas.read_csv("myapp/asset/Testing.csv")

testing_disease = test_workbook["prognosis"]
testing_data = test_workbook.drop(columns="prognosis")
allergy_test = test_workbook[(test_workbook["prognosis"] == disease_list[1])].squeeze()


count_of_each_symptoms = training_data.sum()
count_of_each_disease_in_symptoms = []


for disease_value in disease_list:
    count_of_each_disease_in_symptoms.append(training_data.loc[(training_workbook["prognosis"] == disease_value)].sum())




def getSymptoms(request):
    list_value = symptoms_list.tolist()
    return JsonResponse({"symptoms" : sorted(list_value)})


@api_view(['GET', 'POST'])
def getProbability(request):

    if request.method == 'GET':
        return JsonResponse({'probability': actual_probability})
    elif request.method == 'POST':
        print(list(request.data["userSymptoms"]))
        prob = predict_new(list(request.data["userSymptoms"]))
        return JsonResponse({'probability': prob})



def predict_old(user_symptoms):
    user_symptoms_vector = []
    positive_probability_list = []

    # user_symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches']

    for index in range(0, symptoms_list.__len__()):
        user_symptoms_vector.append(0)

    for user_symptom in user_symptoms:
        index = list(symptoms_list).index(user_symptom)
        user_symptoms_vector[index] = 1


    for di in range(0, list(disease_list).__len__()):
        index = 0
        positive_probability = 0
        for i in user_symptoms_vector:
            if i == 1:
                positive_probability = positive_probability + count_of_each_symptoms[index]*count_of_each_disease_in_symptoms[di][index]/(4920*120)
                # print(count_of_each_symptoms[index])
                # print(count_of_each_disease_in_symptoms[3][index], "value ", index)
            index += 1
        positive_probability_list.append(positive_probability)

    pp = []
    for disease in disease_list:
        pp.append([disease, positive_probability_list[list(disease_list).index(disease)]])

    # print("prob", pp)
    # print("prob", sorted(positive_probability_list, reverse=True))

    sum_value = sum(positive_probability_list)
    # print(sum_value)
    actual_probability = []
    for single_probability in positive_probability_list:
        actual_probability.append(single_probability/sum_value*100)

    print(sorted(actual_probability, reverse=True))
    print(actual_probability.__len__())
    return sorted(actual_probability, reverse=True)


def predict_new(user_symptoms):
    user_symptoms_vector = []
    positive_probability_list = []
    actual_probability = []

    # user_symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches']

    for index in range(0, symptoms_list.__len__()):
        user_symptoms_vector.append(0)

    for user_symptom in user_symptoms:
        index = list(symptoms_list).index(user_symptom)
        user_symptoms_vector[index] = 1


    for dise in range(0, list(disease_list).__len__()):
        index = 0
        positive_probability = 120/4920
        zero_count = 0
        for i in user_symptoms_vector:
            if i == 1:
                if count_of_each_disease_in_symptoms[dise][index] == 0:
                    positive_probability = positive_probability * 1 / (132+41)
                else:
                    positive_probability = positive_probability * count_of_each_disease_in_symptoms[dise][index] / 120

                if zero_count == user_symptoms.__len__():
                    positive_probability = 0
            else:
                if count_of_each_disease_in_symptoms[dise][index] != 0:
                    positive_probability = positive_probability * (1-(count_of_each_disease_in_symptoms[dise][index]/120))

            index += 1
        positive_probability_list.append(positive_probability)

    
    actual_probability = []

    # print("prob", pp)
    print("sorted prob", sorted(positive_probability_list, reverse=True))


    sum_value = sum(positive_probability_list)
    for single_probability in positive_probability_list:
        actual_probability.append(single_probability/sum_value*100)

    data = {
        "disease": disease_list,
        "probability": actual_probability
    }

    predicted_probability = pandas.DataFrame(data).sort_values("probability", ascending=False, ignore_index=True)

    predicted_prob_json = []
    for i in range(0, list(disease_list).__len__()):
        predicted_prob_json.append({"name": predicted_probability["disease"][i], "prob": round(predicted_probability["probability"][i],2)})

    return predicted_prob_json

