from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .models import Notes,HomeWork,Todo,User
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def Home(request):
    return render(request,"Dashboard/dashboard.html")

def Note(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('Desc', '').strip()
        note = Notes(user=request.user, title=title, descriptions=description)
        note.save()
        messages.success(request, "Note successfully saved!")
        return redirect('/notes')
    # If GET or initial load
    notes = Notes.objects.filter(user=request.user)
    value = {"Notes": notes}
    return render(request, "Dashboard/notes.html", value)

def DeleteNote(request,id):
    Notes.objects.filter(id=id).delete()
    return redirect('/notes')

class DetailsNote(generic.DetailView):
    model = Notes
    template_name = 'Dashboard/details_notes.html'
    context_object_name = 'note'

def Home_Work(request):
     if request.method == "POST":
        form_type = request.POST.get('form_type')
        # if form_type == 'update_status':
        #     homework_id = request.POST.get('homework_id')
        #     work = HomeWork.objects.get(id=homework_id, user=request.user)
        #     work.is_finished = request.POST.get('checkbox1', '') == 'value1'
        #     work.save()
        #     return redirect('/home_work')
        if form_type == 'create_homework':
            subject=request.POST.get('subject')
            title=request.POST.get('title')
            description=request.POST.get('description')
            due=request.POST.get('due')
            status=request.POST.get('status')
            value=HomeWork(user=request.user,subject=subject,title=title,descriptions=description,due=due,status=status)
            value.save()
            return redirect('/home_work')
     work = HomeWork.objects.filter(user=request.user)
     value = {'works': work}
     return render(request, "Dashboard/home-work.html", value)

def DeleteHome_Work(request,id):
    HomeWork.objects.filter(id=id).delete()
    return redirect('/home_work')

 
 
def Youtube(request):
    if request.method=="POST":
            text=request.POST.get('text')
            video=VideosSearch(text,limit=10)
            video_results=video.result()['result']
            results_list=[]
            if video_results:
                for video in video_results:
                    results_dic={
                    'input':text,
                    'title':video['title'],
                    'duration':video['duration'],
                    'thumbnail':video['thumbnails'][0]['url'],
                    'channel':video['channel']['name'],
                    'link':video['link'],
                    'views':video['viewCount']['short'],
                    'published':video['publishedTime'],
                    }
                    desc = ''
                    if video['descriptionSnippet']:
                        for j in video['descriptionSnippet']:
                            desc += j['text']
                    results_dic['description']=desc
                    results_list.append(results_dic)
            value={'results':results_list,'has_results':bool(results_list),'search_text':text}
            return render(request,'Dashboard/youtube.html',value)
    return render(request,"Dashboard/youtube.html")



def todo(request):
     if request.method == "POST":
        title=request.POST.get('title')
        status=request.POST.get('status')
        value=Todo(user=request.user,title=title,status=status)
        value.save()
        return redirect('/todo')
     work = Todo.objects.filter(user=request.user)
     value = {'works': work}
     return render(request, "Dashboard/todo.html", value)

def DeleteTodo(request,id):
    Todo.objects.filter(id=id).delete()
    return redirect('/todo')

def Book(request):
    if request.method == "POST":
        text = request.POST.get('text')
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        json = r.json()
        results_list = []

        if 'items' in json:
            for i , item in enumerate(json['items']):
                if i>=10:
                    break
                volume_info = item.get('volumeInfo', {})
                
                results_dic = {
                    'title': volume_info.get('title', 'No Title'),
                    'subtitle': volume_info.get('subtitle', 'No Subtitle'),
                    'description': volume_info.get('description', 'No Description'),
                    'count': volume_info.get('pageCount', 'No Page Count'),
                    'categories': volume_info.get('categories', ['No Categories']),
                    'rating': volume_info.get('averageRating', 'No Rating'),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'preview': volume_info.get('previewLink', 'No Preview Link'),
                }
                results_list.append(results_dic)

        value = {
            'results': results_list, 
            'has_results': bool(results_list), 
            'search_text': text
        }
        return render(request, 'Dashboard/books.html', value)

    return render(request, "Dashboard/books.html", {'has_results': False})


def Desc(request):
    if request.method == "POST":
        text = request.POST.get('text', '').strip()

        if text:
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
            r = requests.get(url)

            try:
                json_data = r.json()

                if json_data and isinstance(json_data, list) and len(json_data) > 0:
                    phonetics = json_data[0].get('phonetics', [{}])[0].get('text', 'No phonetics available')
                    definition = json_data[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'No definition available')
                    example = json_data[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'No example available')
                    synonyms = json_data[0].get('meanings', [{}])[0].get('synonyms', [])
                    audio = json_data[0].get('phonetics', [{}])[0].get('audio', {})

                    value = {
                        'has_results': True,
                        'input': text,
                        'phonetics': phonetics,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms,
                        'audio': audio
                    }
                else:
                    value = {
                        'has_results': False,
                        'input': text,
                    }

            except ValueError:
                value = {
                    'has_results': False,
                    'input': text,
                }
        else:
            value = {
                'has_results': False,
                'input': text,
            }

        return render(request, 'Dashboard/dictionary.html', value)

    return render(request, 'Dashboard/dictionary.html', {'has_results': False})


def Wiki(request):
    if request.method == "POST":
        text = request.POST.get('text', '').strip()
        value = {'text': text, 'has_results': False}

        if text:
            try:
                search = wikipedia.page(text)
                value.update({
                    'title': search.title,
                    'link': search.url,
                    'details': search.summary,
                    'has_results': True,
                })
            except DisambiguationError as e:
                value['details'] = f"Your search term resulted in multiple possible matches: {', '.join(e.options)}"
            except PageError:
                value['details'] = "No matching page found on Wikipedia. Please try another search term."
            except Exception as e:
                value['details'] = f"An error occurred: {str(e)}"

        return render(request, "Dashboard/wiki.html", value)

    return render(request, "Dashboard/wiki.html", {'has_results': False})




def Conversion(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form_type = request.POST.get('form_type')
        if form_type == "length_Form":
            first = request.POST.get('measure1')
            second = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''
            if input_value and int(input_value) >= 0:
                if first == 'yard' and second == 'foot':
                    answer = f"{input_value} yard = {int(input_value) * 3} foot"
                elif first == 'foot' and second == 'yard':
                    answer = f"{input_value} foot = {int(input_value) / 3} yard"
            return JsonResponse({'answer': answer})
        
        elif form_type == "mass_Form":
             first = request.POST.get('measure1')
             second = request.POST.get('measure2')
             input_value = request.POST.get('input')
             answer = ''
             if input_value and int(input_value) >= 0:
                 if first == 'pound' and second == 'kilogram':
                     answer = f"{input_value} pound = {int(input_value) * 0.453592} kilogram"
                 elif first == 'kilogram' and second == 'pound':
                     answer = f"{input_value} kilogram = {int(input_value) * 2.20462} pound"
             return JsonResponse({'answer': answer})

    return render(request, "Dashboard/Conversion.html")

def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("Confirm-password")

        if pass1 == pass2:
            if not username:
                messages.error(request, "Username is required.")
            elif pass1 != pass2:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                messages.success(request, "Your account has been created successfully!")
                # return redirect('login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'Dashboard/register.html')
