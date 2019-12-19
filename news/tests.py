from django.test import TestCase

# Create your tests here.

from .models import Editor,Article,tags


class EditorTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.samuel= Editor(first_name = 'Samuel', last_name ='Odhiambo', email ='odhiamboangienda25@gmail.com')



# Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.samuel,Editor))  
        
        
    # Testing Save Method
    def test_save_method(self):
        self.samuel.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)
            

class Editor(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    
    def __str__(self):
        return self.first_name
    
    
    def save_editor(self):
        self.save()
        
        
        
class ArticleTestClass(TestCase):
    
    def setup(self):
        #Creating a new editor and saving it
        self.samuel= Editor(first_name = 'samuel', last_name = 'Odhiambo', email = 'odhiamboangienda25@gmail.com')
        self.samuel.save_editor()
        
        #Creating a new tag and saving it
        self.new_tag = tags(name = 'testing')
        self.new_tag.save()
        
        
        self.new_article = Article(title = 'testArticle', post = 'This is a random test Post',editor = self.james)
        self.new_article.save()
        
        self.new_article.tags.add(self.new_tag)
        
        
    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()
        
        
    
    def test_get_news_today(self):
        today_news = Article.today_news()
        self,assertTrue(len(today_news)>0)
        
        
    def test_get_news_by_date(self):
        tes_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) ==0)        
            
            