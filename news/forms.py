from django import forms
from .models import Article
from .forms import NewArticleForm, NewsLetterForm


class NewsLetterForm(forms.Form):
  your_name = forms.CharField(label = 'First Name',max_length=30)
  email = forms.EmailField(label = 'Email')
  
  
class NewArticleForm(forms.ModelForm):
    class Meta:
  model = Article
  exclude = ['editor', 'pub_date']
  widgets = {
      'tags': forms.CheckboxSelectMultiple(),
  }
  
@login_required(login_url='/accounts/login/')
def new_article(request):
  current_user = request.user
  if request.method == 'POST':
      form = NewArticleForm(request.POST, request.FILES)
      if form.is_valid():
          article = form.save(commit=False)
          article.editor = current_user
          article.save()
      return redirect('NewsToday')

  else:
      form = NewArticleForm()
  return render(request, 'new_article.html', {"form": form})    
