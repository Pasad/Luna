from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from django.core.paginator import Paginator

def post_list(request):
    """게시글 목록 (페이징 적용)"""
    posts_list = Post.objects.all()
    
    # 페이징 처리
    paginator = Paginator(posts_list, 10) 
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    return render(request, 'board/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """게시글 상세"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})

@login_required
def post_create(request):
    """새 게시글 작성 (로그인 필수)"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            return redirect('board:list')
    return render(request, 'board/post_form.html')

@login_required
def post_update(request, pk):
    """게시글 수정 (로그인 필수 및 본인 글 확인)"""
    post = get_object_or_404(Post, pk=pk)
    
    # 본인이 작성한 글이 아니면 수정 권한 없음 처리
    if post.author != request.user:
        return HttpResponseForbidden("글을 수정할 권한이 없습니다.")

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            return redirect('board:detail', pk=post.pk)

    return render(request, 'board/post_form.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("글을 삭제할 권한이 없습니다.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('board:list')
    return redirect('board:detail', pk=pk)