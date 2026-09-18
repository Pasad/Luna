import cloudinary.uploader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import Album

def album_list(request):
    """앨범 목록 조회"""
    albums = Album.objects.all()
    return render(request, 'albums/album_list.html', {'albums': albums})

@login_required
def album_create(request):
    """사진 업로드"""
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        location = request.POST.get('location', '')

        if image_file:
            response = cloudinary.uploader.upload(image_file, folder='luna_albums')
            public_id = response.get('public_id')

            Album.objects.create(
                image=public_id,
                caption=caption,
                location=location,
                author=request.user
            )
            return redirect('albums:list')

    return render(request, 'albums/album_form.html')

@login_required
def album_update(request, pk):
    """사진 정보 수정"""
    album = get_object_or_404(Album, pk=pk)
    
    if album.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == 'POST':
        image_file = request.FILES.get('image')
        album.location = request.POST.get('location', '')
        album.caption = request.POST.get('caption', '')

        if image_file:
            # 기존 이미지 Cloudinary에서 삭제 후 새 이미지 업로드
            if album.image:
                cloudinary.uploader.destroy(album.image)
            response = cloudinary.uploader.upload(image_file, folder='luna_albums')
            album.image = response.get('public_id')

        album.save()
        return redirect('albums:list')

    return render(request, 'albums/album_form.html', {'album': album})

@login_required
@require_POST
def album_delete(request, pk):
    """사진 삭제 (Cloudinary 파일 삭제 포함)"""
    album = get_object_or_404(Album, pk=pk)
    
    if album.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    # Cloudinary 원본 파일 삭제
    if album.image:
        cloudinary.uploader.destroy(album.image)

    # DB 레코드 삭제
    album.delete()
    return redirect('albums:list')