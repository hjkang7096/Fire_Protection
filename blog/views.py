from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm


def post_list(request):
    query = Post.objects.all()
    page = int(request.GET.get("page", 1))  # 두번째 인자 : 없을 시 디폴트 값
    paginator = Paginator(query, 2, allow_empty_first_page=True)
    page_obj = paginator.page(page)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    # try:
    #     page_obj = paginator.page(page)
    # except PageNotAnInteger:
    #     page = 1
    #     page_obj = paginator.page(page)
    # except EmptyPage:
    #     page = paginator.num_pages
    #     page_obj = paginator.page(page)

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": query,
            "page_obj": page_obj,
            "paginator": paginator,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
        },
    )


def post_list_category(request, slug):
    if slug != "기 타":
        query = Post.objects.filter(category__name__contains=slug)
    else:
        query = Post.objects.filter(category=None)

    page = int(request.GET.get("page", 1))  # 두번째 인자 : 없을 시 디폴트 값
    paginator = Paginator(query, 2, allow_empty_first_page=True)
    page_obj = paginator.page(page)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": query,
            "page_obj": page_obj,
            "paginator": paginator,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
            "slug": slug,
        },
    )


def post_list_search(request, search):
    query = Post.objects.filter(
        Q(title__icontains=search) | Q(tag__name__icontains=search)
    )

    page = int(request.GET.get("page", 1))  # 두번째 인자 : 없을 시 디폴트 값
    paginator = Paginator(query, 2, allow_empty_first_page=True)
    page_obj = paginator.page(page)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": query,
            "page_obj": page_obj,
            "paginator": paginator,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
            "search": search,
        },
    )


def post_list_tag(request, tag):
    query = Post.objects.filter(tag__name__icontains=tag)

    page = int(request.GET.get("page", 1))  # 두번째 인자 : 없을 시 디폴트 값
    paginator = Paginator(query, 2, allow_empty_first_page=True)
    page_obj = paginator.page(page)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": query,
            "page_obj": page_obj,
            "paginator": paginator,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
            "tag": tag,
        },
    )


# @login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()
    comment_form = CommentForm()
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comment_form": comment_form,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
        },
    )


@login_required
def post_new(request):
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag.add(*post.extract_tag_list())
            return redirect("blog:post_detail", post.pk)
    else:
        form = PostForm()

    return render(
        request,
        "blog/post_new.html",
        {
            "form": form,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
        },
    )


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    total_category_post_count = Post.objects.all().count()
    no_category_post_count = Post.objects.filter(category=None).count()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if request.user != post.author:
            messages.warning(request, "수정권한이 없습니다.")
            return redirect(post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.tag.add(*post.extract_tag_list())
            post.save()
            return redirect(post.get_absolute_url())

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_update.html",
        {
            "form": form,
            "post": post,
            "categories": categories,
            "total_category_count": total_category_post_count,
            "no_category_count": no_category_post_count,
        },
    )


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and request.user == post.author:
        post.delete()
        messages.add_message(request, messages.SUCCESS, "포스트를 삭제했습니다.")
        return redirect("blog:post_list")
    else:
        messages.warning(request, "삭제할 권한이 없습니다.")


def comment_new(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect("blog:post_detail", post.pk)
        else:
            comment_form = CommentForm()
    else:
        raise PermissionDenied

    return redirect(
        request,
        "blog/comment_form.html",
        {
            "comment_form": comment_form,
            "post": post,
        },
    )


def comment_edit(request, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        post = comment.post

        if request.method == "POST":
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            comment_form = CommentForm(instance=comment)
    else:
        raise PermissionDenied

    return render(
        request,
        "blog/comment_edit.html",
        {
            "comment_form": comment_form,
            "comment": comment,
        },
    )


@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        messages.success(request, "댓글을 삭제했습니다.")
        return redirect(comment.post.get_absolute_url())
    else:
        raise PermissionDenied
