from django import forms
from .models import Movie,ReviewRating

class movie_form(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','image','description','release_date','lead_actor','lead_actress','trailer_link','genres','release_status']




class ReviewRatingForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False, widget=forms.Textarea)
    rating = forms.IntegerField(required=False)
    class Meta:
        model = ReviewRating
        fields = ['title', 'content', 'rating']


