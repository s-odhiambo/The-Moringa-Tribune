from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime as dt
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required

# Create your views here.


# def welcome(request):
    # return HttpResponse('Welcome to Moringa Tribune')
    # return render(request, 'welcome.html')



def news_today(request):
  date = dt.date.today()
  news = Article.todays_news()
  
  if request.method == 'POST':
    form = NewsLetterForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['your_name']
      email = form.cleaned_data['email']
      
      
      recipient =NewsLetterRecipients(name = name,email =email)
      recipient.save()
      send_welcome_email(name,email)
      
      
      HttpResponseRedirect('news_today')
      print('valid')
  
  else:
    form = NewsLetterForm()   
  return render(request, 'all-news/today-news.html',{"date": date,"news":news,"letterForm":form,"letterForm":form})

    # FUNCTION TO CONVERT DATE OBJECT TO FIND EXACT DAY
  #   day = convert_dates(date)
  #   html = f'''
  # <html>
  # <body>
  # <h1> News for {day} {date.day}-{date.month}-{date.year}</h1>
  # </body>
  # </html>
  # '''
  #   return HttpResponse(html)

    # return render(request, 'all-news/today-news.html', {"date":date,})


# def convert_dates(dates):

    # Function that gets the weekday number for the date.
    # day_number = dt.date.weekday(dates)

    # days = ['Monday', 'Tuesday', 'wednesday',
            # 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Returning the actual day of the week

    # day = days[day_number]
    # return day


# Function that gets the past date days of the week
def past_days_news(request, past_date):

    try:
        # Converts data from the string Url
      date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False
      
      
    if date == dt.date.today():
      return redirect(news_today)
    
    news = Article.days_news(date)  
    return render(request,'all-news/past-news.html', {"date": date ,"news":news})
  
  
def search_results(request):
    
    if 'article' in request.GET and request.GET["article"]:
      search_term = request.GET.get("article")
      searched_articles = Article.search_by_title(search_term)
      
      message = f"{search_term}"
      return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})
    
    else:
      message = "You haven't searched for any term"
      return render(request, 'all-news/search.html',{"message":message})
    
@login_required(login_url='/accounts/login/')   
def article(request,article_id):
  try:
    article = Article.object.get(id = article_id)
  except DoesNotExist:
    raise Http404()
  return render(request,"all-news/article.html", {"article":article})



def profile(request):
  title = 'profile'
  return render(request,"profile.html",{"title":title})


@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user 
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit = False)
            article.editor = current_user
            article.pub_date = dt.datetime.now()
            article.save()
        return redirect('newsToday')
    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form":form})    

  #   day = convert_dates(date)
  #   html = f'''
  # <html>
  # <body>
  # <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
  # </body>
  # </html>
  # '''
    # return HttpResponse(html)
 
    

