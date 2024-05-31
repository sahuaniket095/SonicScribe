from django.shortcuts import render
from Audio.models import Book
from django.shortcuts import render,get_object_or_404
from .models import Category
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import SignupForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


def search_books_by_tag(request):
    if request.method == 'GET' and 'tag' in request.GET:
        tag_name = request.GET['tag']
        
        # Retrieve books with tags containing the specified tag_name
        books = Book.objects.filter(tags__icontains=tag_name)
        
        # Create a dictionary to store unique tags and their corresponding books
        unique_books_by_tag = {}
        for book in books:
            # Use lowercased tag names to ensure case-insensitive comparison
            lowercased_tags = [tag.lower() for tag in book.tags.split(',')]
            if tag_name.lower() in lowercased_tags:
                # Store only one book per tag (the first book found for each tag)
                unique_books_by_tag.setdefault(book.tags, book)
        
        # Extract the unique books from the dictionary
        unique_books = list(unique_books_by_tag.values())
        
        return render(request, 'Search.html', {'books': unique_books, 'tag': tag_name})
    else:
        return render(request, 'Search.html', {})



def tags(request, category_id):
    
        category = get_object_or_404(Category, id=category_id)
        unique_tags = Book.objects.filter(category=category).values_list('tags', flat=True).distinct()
        
        books_with_tags = {}
    
        for tag in unique_tags:
            book_with_tag = Book.objects.filter(category=category, tags=tag).first()
            if book_with_tag:
                books_with_tags[tag] = book_with_tag
    
        return render(request, 'tags.html', {'category': category, 'books_with_tags': books_with_tags})
    

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def Home(request):
    return render(request,'Home.html')



def tag_books(request, tag):
    tag = tag.strip()  # Remove leading/trailing spaces
    books = Book.objects.filter(tags__icontains=tag)
    
    return render(request, 'tag_books.html', {'books': books, 'tag': tag}) 



def Browse(request):
    # Get distinct tags from the Book model
    distinct_tags = Book.objects.values_list('tags', flat=True).distinct()
    
    # Create a dictionary to store one book for each tag
    books_by_tag = {}
    for tag in distinct_tags:
        # Get one book for each tag
        book = Book.objects.filter(tags=tag).first()
        if book:
            books_by_tag[tag] = book
    
    return render(request, 'Browse.html', {'books_by_tag': books_by_tag})


def login(request):
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')

def library_view(request):
    return render(request,'Library.html')




@csrf_exempt
def signup(request):
        
        if request.method == 'POST':
           form = SignupForm(request.POST)

           if form.is_valid():
                form.save()
                Index.book_dict.clear()
                return redirect('/login')
        else:
             form =SignupForm()
        return render(request,'signup.html',{'form':form})     
        
def logout_view(request):
    Index.book_dict.clear()
    logout(request)
    return redirect('Home')

class Index(View):
    book_dict = {}  # Initialize an empty dictionary as a class attribute

    def post(self, request):
        book_id = request.POST.get('book')  # Assuming 'book' contains the book ID
        
        # Check if the book with the provided ID already exists in the dictionary
        if book_id not in Index.book_dict:
            # Retrieve the Book object from the database using the book ID
            book = get_object_or_404(Book, pk=book_id)
            
            # Generate unique key based on the current size of the dictionary
            key = f'book_{len(Index.book_dict) + 1}'
            
            # Add the Book object to the dictionary
            Index.book_dict[book_id] = book
        
        # Render the Library.html template with the book_dict
        return render(request, 'Library.html', {'book_dict': Index.book_dict})

class LibraryView(View):
    def get(self, request):
        # Access book_dict from the Index class
        book_dict = Index.book_dict

        return render(request, 'Library.html', {'book_dict': book_dict})       