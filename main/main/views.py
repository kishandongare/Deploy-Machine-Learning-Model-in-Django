from django.http import HttpResponse
from django.shortcuts import render
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

def home(request):
    return render(request, "index.html")
ps = PorterStemmer()
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

def result(request):
    cv = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))

    lis = (request.GET['mail'])

    transformed_sms = transform_text(lis)

    vector_input = cv.transform([transformed_sms])

    res = model.predict(vector_input)[0]
    def spam():
         if res == 1:
             return 'spam'
         else:
             return'Not spam'

    return render(request,"result.html", {'res':spam()}) #'key':value
