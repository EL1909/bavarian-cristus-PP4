from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import View, DetailView, ListView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import ImagePost
from .forms import CommentForm


class PostList(ListView):
    model = ImagePost
    queryset = ImagePost.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(DetailView):

    model = ImagePost

    def get(self, request, slug, *args, **kwargs):
        queryset = ImagePost.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = ImagePost.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        
        # Check if the request is to edit the post
        if 'edit_post' in request.POST:
            form = ImagePostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            form = CommentForm(instance=post)

        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
                "edit_form": form,
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(ImagePost, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        queryset = ImagePost.objects.filter(status=1)
        image_posts = ImagePost.objects.filter(user=user)
        context = {'user': user, 'image_posts': image_posts}
        return render(request, "profile.html", context)


class ImagePostCreate(LoginRequiredMixin, CreateView):
    model = ImagePost
    fields = ['title','slug', 'author', 'image', 'location', 'latitude', 'longitude', 'content']
    template_name = 'create.html'
    success_url = reverse_lazy('create')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def post_edit(request, slug):
    post = get_object_or_404(ImagePost, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommentForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})