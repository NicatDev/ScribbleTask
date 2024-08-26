from django.shortcuts import  HttpResponse,render
from django.db.models import Q
from .forms import *
from .models import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest

def comment(request):
    if request.method == 'POST':
        newmessage = CommentForm(request.POST)
        if newmessage.is_valid():
            newmessage.save()
            data = {'status': 'success','message': 'Şərhiniz uğurla göndərildi!'}
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'error', 'message': 'Xəta var!', 'errors': newmessage.errors})
        
    return HttpResponse(status=405) 

def blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    related_blogs = Blog.objects.all()[::-1][0:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    category = request.GET.get('category')
    form = SearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            blogs = blogs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if category:
        blogs = Blog.objects.filter(category__slug = category)
        currentCategory = Category.objects.get(slug = category)
    else:
        currentCategory = ''

    context = {
        'blogs':blogs,
        'categories':categories,
        'tags':tags,
        'form':form,
        'currentCategory':currentCategory,
        'related_blogs':related_blogs,
      
    }
    return render(request,'blog-classic.html',context)

def blog(request,slug):
    blog = get_object_or_404(Blog,slug=slug)
    related_blogs = Blog.objects.exclude(slug=blog.slug)[0:3]
    categories = Category.objects.all()
    form = SearchForm(request.GET or None)

    context = {
        'blog':blog,
        'categories':categories,
        'form':form,
        'related_blogs':related_blogs,
   
    }
    return render(request,'blog-details.html',context)

def blog_create(request):
    if request.method == 'POST':
        newmessage = BlogForm(request.POST, request.FILES)
        if newmessage.is_valid():
            blog = newmessage.save()
            data = {
                'status': 'success',
                'message': 'Bloqunuz uğurla göndərildi!',
                'blog_url': reverse('blog', args=[blog.slug]),
                'blog_image': blog.image.url,
                'blog_title': blog.title,
                'blog_category': blog.category.title,
                'blog_writer': blog.writer,
                'blog_content': blog.content,
                'blog_created_at': blog.created_at.strftime('%Y-%m-%d'),
                'blog_id':blog.id
            }
            return JsonResponse(data)
        else:
            print(newmessage.errors)
            return JsonResponse({'status': 'error', 'message': 'Xəta var!', 'errors': newmessage.errors})
        
    else:
        return HttpResponse(status=405) 
    


def delete_blog(request, id):
    if request.method == 'DELETE':
        try:
            blog = Blog.objects.get(id=id)
            blog.delete()
            return JsonResponse({'status': 'success', 'message': 'Blog silindi.'})
        except Blog.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Blog artıq mövcud deyil.'}, status=404)
    else:
        return HttpResponseBadRequest('Xəta baş verdi')