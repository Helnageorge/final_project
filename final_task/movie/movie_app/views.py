from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Category,Movie,ReviewRating
from .forms import ReviewRatingForm,movie_form
from django.urls import reverse
from django.db.models import Avg
from django.contrib import messages


# Create your views here.


def home(request):
    # Retrieve all movies
    latest_movies = Movie.objects.filter(release_status='latest')
    upcoming_movies = Movie.objects.filter(release_status='upcoming')
    categories = Category.objects.all()

    for movie in latest_movies:
        reviews = movie.reviewrating_set.all()
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        movie.avg_rating = avg_rating if avg_rating else 0

    # Get the highest-rated movie
    highest_rated_movie = max(latest_movies, key=lambda movie: movie.avg_rating) if latest_movies else None

    return render(request, 'home.html', {
        'latest_movies': latest_movies,
        'highest_rated_movie': highest_rated_movie,
        'upcoming_movies': upcoming_movies,
        'categories': categories
    })
def all_latest_movies(request):
    latest_movies = Movie.objects.filter(release_status='latest')
    categories = Category.objects.all()
    return render(request, 'all_latest_movies.html', {'latest_movies': latest_movies,'categories': categories})

def all_upcoming_movies(request):
    upcoming_movies = Movie.objects.filter(release_status='upcoming')
    categories = Category.objects.all()
    return render(request, 'all_upcoming_movies.html', {'upcoming_movies': upcoming_movies,'categories': categories})




def add_review(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = Movie.objects.get(pk=movie_id)
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                return redirect('/')
        else:
            return HttpResponse("Error: Please select a movie.")
    else:
        form = ReviewRatingForm()
    return render(request, 'addreview.html', {'form': form, 'movies': movies,'user': request.user})

def add(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        image = request.FILES.get('image')
        lead_actor = request.POST.get('lead_actor')
        lead_actress = request.POST.get('lead_actress')
        trailer_link = request.POST.get('trailer_link')
        genre_input = request.POST.get('category')
        release_status = request.POST.get('release_status')


        genre_names = [name.strip() for name in genre_input.split(',') if name.strip()]


        new_movie = Movie.objects.create(
            user=request.user,
            title=title,
            description=description,
            release_date=release_date,
            image=image,
            lead_actor=lead_actor,
            lead_actress=lead_actress,
            trailer_link=trailer_link,
            release_status=release_status
        )


        for name in genre_names:
            genre, created = Category.objects.get_or_create(name=name)
            new_movie.genres.add(genre)


        return redirect('movie_app:home')


    return render(request, 'adding.html')




def movies_by_genre(request, genre_id):
    genre = get_object_or_404(Category, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)
    categories = Category.objects.all()
    return render(request, 'movies_by_genre.html', {'genre': genre, 'movies': movies,'categories': categories})


def movie_detail(request, pk):

    movie = get_object_or_404(Movie, pk=pk)
    categories = Category.objects.all()


    return render(request, 'movie_detail.html', {'movie': movie, 'categories': categories, 'user': request.user})





def search_movie(request):
    if 'query' in request.GET:
        query = request.GET['query']

        movie = Movie.objects.filter(title__icontains=query).first()
        if movie:
            return redirect(reverse('movie_app:movie_detail', args=[movie.pk]))
        else:
            messages.warning(request, f"No movie found matching the search query '{query}'.")
    return redirect('movie_app:home')

def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = movie_form(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_app:movie_detail', pk=pk)
    else:
        form = movie_form(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('/')
    return render(request, 'delete.html', {'movie': movie})


def edit_review(request, pk):
    review = get_object_or_404(ReviewRating, pk=pk)


    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewRatingForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Review updated successfully.")
                return redirect('movie_app:movie_detail', pk=review.movie.pk)
        else:
            form = ReviewRatingForm(instance=review)
        return render(request, 'edit_review.html', {'form': form, 'review': review})
    else:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect('movie_app:home')


def delete_review(request, pk):
    review = get_object_or_404(ReviewRating, pk=pk)


    if request.user == review.user:
        if request.method == 'POST':
            review.delete()

            return redirect('movie_app:movie_detail', pk=review.movie.pk)
        else:
            return render(request, 'delete_review_confirm.html', {'review': review})

