from django.shortcuts import render
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from Gallery.models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Exhibition, Museum_piece, Author, Images, Exhibition_museum_piece, Hall


class MuseumView(View):
    def get(self, request: WSGIRequest):
        context = {}
        pieces = Museum_piece.objects.all()
        exhibitions = Exhibition.objects.all()
        authors = Author.objects.all()
        halls = Hall.objects.all()
        images = Images.objects.all()
        exhibition_museum_pieces = Exhibition_museum_piece.objects.all()
        exhibition_images = []
        for exhibition in exhibitions:
            f = False
            for exhibition_piece in exhibition_museum_pieces:
                if exhibition.id == exhibition_piece.exhibition_id.id:
                    f = True
                    for image in images:
                        if image.piece == exhibition_piece.museum_piece_id:
                            exhibition_images.append((exhibition, image))
                            break
                    break
            if not f:
                exhibition_images.append((exhibition, None))
        pieces_images = []
        for piece in pieces:
            f = False
            for image in images:
                if image.piece == piece:
                    f = True
                    pieces_images.append((piece, image))
                    break
            if not f:
                pieces_images.append((piece, None))
        context['pieces_images'] = pieces_images
        context['authors'] = authors
        context['images'] = images
        context['exhibition_images'] = exhibition_images
        context['halls'] = halls
        context['count_pieces'] = len(pieces)
        context['count_authors'] = len(authors)
        context['count_exhibitions'] = len(exhibitions)
        return render(request, 'gallery/museum.html', context)

    def post(self, request: WSGIRequest):
        context = {}
        if request.POST.get('add_exhibition'):
            return HttpResponseRedirect("/gallery/add_exhibition/")
        if request.POST.get('add_museum_piece'):
            return HttpResponseRedirect("/gallery/add_museum_piece/")
        if request.POST.get('add_author'):
            return HttpResponseRedirect("/gallery/add_author/")
        if request.POST.get('add_hall'):
            return HttpResponseRedirect("/gallery/add_hall/")
        if request.POST.get("del_{d}".format(d=id)):
            piece = Museum_piece.objects.get(id=id)
            piece.delete()
            return HttpResponseRedirect("/gallery/")
        return HttpResponseRedirect("/gallery/")
class AddExhibition(View):
    def get(self, request: WSGIRequest):
        form = ExhibitionForm()
        form_ex_piece = Exhibition_museum_pieceForm()
        context = {}
        form_ex_piece.fields['museum_piece_id'].queryset = Museum_piece.objects.all()
        context['form'] = form
        context['form_ex_piece'] = form_ex_piece
        return render(request, 'gallery/add_exhibition.html', context)

    def post(self, request: WSGIRequest):
        form = ExhibitionForm(request.POST)
        form_ex_piece = Exhibition_museum_pieceForm(request.POST)
        context = {}
        if form.is_valid():
            f = Exhibition(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                date_and_time=form.cleaned_data.get('date_and_time')
            )
            f.save()
            if form_ex_piece.is_valid():
                ex_piece = Exhibition_museum_piece(
                    exhibition_id=f,
                    museum_piece_id=form_ex_piece.cleaned_data.get('museum_piece_id')
                )
                ex_piece.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        return render(request, 'gallery/add_exhibition.html', context)


class AddMuseumPiece(View):
    def get(self, request: WSGIRequest):
        form = Museum_pieceForm()
        form_images = ImagesForm()
        form.fields['author_id'].queryset = Author.objects.all()
        form.fields['hall_id'].queryset = Hall.objects.all()
        context = {}
        context['form'] = form
        context['form_images'] = form_images
        return render(request, 'gallery/add_museum_piece.html', context)

    def post(self, request: WSGIRequest):
        form = Museum_pieceForm(request.POST)
        form_images = ImagesForm(request.POST, request.FILES)
        context = {}
        context['danich'] = 'danich'
        if form.is_valid():
            piece = Museum_piece(
                piece_name=form.cleaned_data.get('piece_name'),
                description=form.cleaned_data.get('description'),
                date_of_creation=form.cleaned_data.get('date_of_creation'),
                piece_type=form.cleaned_data.get('piece_type'),
                author_id=form.cleaned_data.get('author_id'),
                hall_id=form.cleaned_data.get('hall_id')
            )
            piece.save()
            # if form_images.is_valid():
            files = request.FILES.getlist('image')
            context['files'] = files
            for file in files:
                img = Images(
                    piece=piece,
                    image=file
                )
                img.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        context['form_images'] = form_images
        return render(request, 'gallery/add_museum_piece.html', context)


class AddAuthor(View):
    def get(self, request: WSGIRequest):
        form = AuthorForm()
        context = {}
        context['form'] = form
        return render(request, 'gallery/add_author.html', context)

    def post(self, request: WSGIRequest):
        form = AuthorForm(request.POST)
        context = {}
        if form.is_valid():
            f = Author(full_name=form.cleaned_data.get('full_name'))
            f.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        return render(request, 'gallery/add_author.html', context)

class ChangeExhibitons(View):
    def get(self,request,id):
        exhibition = Exhibition.objects.get(id__iexact=id)
        bound_form = ExhibitionForm(instance=exhibition)
        return render(request, 'Gallery/add_exhibition.html', context={'form': bound_form, 'exhibition': exhibition})

    def post(self, request: WSGIRequest, id):
        exhibition = Exhibition.objects.get(id=id)
        exhibition_museum_pieces = Exhibition_museum_piece.objects.all()
        images = Images.objects.all()
        select_images = []
        for exhibition_piece in exhibition_museum_pieces:
            if id == exhibition_piece.exhibition_id.id:
                for image in images:
                    if image.piece == exhibition_piece.museum_piece_id:
                        select_images.append(image)
                        break
                break
            else:
                select_images.append(None)
        context = {}

        form = ExhibitionForm(request.POST, instance=exhibition)
        form_ex_piece = Exhibition_museum_pieceForm(request.POST, instance=exhibition_museum_pieces[0])

        if form.is_valid():
            context['d'] = 'ddddddd'

            new_exhibition = form.save()
            if form_ex_piece.is_valid():
                new_pices = form_ex_piece.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        context['form_ex_piece'] = form_ex_piece
        return render(request, 'gallery/change_exhibition.html', context)
class ChangeMuseumPiece(View):
    def get(self, request, id):
        museum_piece = Museum_piece.objects.get(id__iexact=id)
        bound_form = Museum_pieceForm(instance=museum_piece)
        return render(request, 'Gallery/add_museum_piece.html', context={'form': bound_form, 'museum_piece': museum_piece})

    def post(self, request: WSGIRequest, id):
        piece = Museum_piece.objects.get(id=id)
        images = Images.objects.all()
        select_images = []
        # for image in images:
        #     if image.piece.id == id:
        #         select_images.append(image)
        form = Museum_pieceForm(request.POST, instance=piece)
        # if len(select_images) != 0:
        #     form_images = ImagesForm(request.POST, request.FILES, instance=select_images[0])
        # else:
        #     form_images = ImagesForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            new_piece = form.save()
            # if form_images.is_valid():
            #     new_img = form_images.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        #context['form_images'] = form_images
        return render(request, 'gallery/update_museum_piece.html', context)
class PieceDetailed(View):
    def get(self, request: WSGIRequest, piece_id):
        piece = Museum_piece.objects.get(id=piece_id)
        images = Images.objects.all()
        select_images = []
        for image in images:
            if image.piece.id == piece_id:
                select_images.append(image)
        context = {}
        context['piece'] = piece
        context['select_images'] = select_images
        context['piece_id'] = piece_id
        return render(request, 'gallery/detail_piece.html', context)

    def post(self, request: WSGIRequest, piece_id):
        context = {}
        context['piece_id'] = piece_id
        if request.POST.get("del_{d}".format(d=piece_id)):
            piece = Museum_piece.objects.get(id=piece_id)
            piece.delete()
            return HttpResponseRedirect("/gallery/")
        return render(request, 'gallery/detail_piece.html', context)

class AddHall(View):
    def get(self, request: WSGIRequest):
        form = HallForm()
        context = {}
        context['form'] = form
        return render(request, 'gallery/add_hall.html', context)

    def post(self, request: WSGIRequest):
        form = HallForm(request.POST)
        context = {}
        if form.is_valid():
            f = Hall(hall_number=form.cleaned_data.get('hall_number'),
                     title=form.cleaned_data.get('title'))
            f.save()
            return HttpResponseRedirect("/gallery/")
        context['form'] = form
        return render(request, 'gallery/add_hall.html', context)

class FilterPiecesView(View):
    def get(self, request: WSGIRequest):
        context = {}
        marks_pieces = list(Author.objects.filter(full_name__in=self.request.GET.getlist("author")).values_list('id', flat=True))
        marks_halls = list(Hall.objects.filter(hall_number__in=self.request.GET.getlist("hall")).values_list('id', flat=True))
        pieces = Museum_piece.objects.filter(hall_id_id__in=marks_halls, author_id_id__in=marks_pieces)
        types = set([t[0] for t in Museum_piece.objects.values_list("piece_type")])
        exhibitions = Exhibition.objects.all()
        authors = Author.objects.all()
        halls = Hall.objects.all()
        images = Images.objects.all()
        exhibition_museum_pieces = Exhibition_museum_piece.objects.all()
        exhibition_images = []
        for exhibition in exhibitions:
            f = False
            for exhibition_piece in exhibition_museum_pieces:
                if exhibition.id == exhibition_piece.exhibition_id.id:
                    f = True
                    for image in images:
                        if image.piece == exhibition_piece.museum_piece_id:
                            exhibition_images.append((exhibition, image))
                            break
                    break
            if not f:
                exhibition_images.append((exhibition, None))
        pieces_images = []
        for piece in pieces:
            f = False
            for image in images:
                if image.piece == piece:
                    f = True
                    pieces_images.append((piece, image))
                    break
            if not f:
                pieces_images.append((piece, None))
        context['pieces_images'] = pieces_images
        context['authors'] = authors
        context['halls'] = halls
        context['types'] = types
        context['count_pieces'] = len(pieces)
        context['count_authors'] = len(authors)
        context['count_exhibitions'] = len(exhibitions)
        context['images'] = images
        context['exhibition_images'] = exhibition_images
        return render(request, 'gallery/museum.html', context)

class ExhibitionDetailed(View):
    def get(self, request: WSGIRequest, exh_id):
        exhibition = Exhibition.objects.get(id=exh_id)
        exhibition_museum_pieces = Exhibition_museum_piece.objects.all()
        images = Images.objects.all()
        select_images = []
        for exhibition_piece in exhibition_museum_pieces:
            if exh_id == exhibition_piece.exhibition_id.id:
                for image in images:
                    if image.piece == exhibition_piece.museum_piece_id:
                        select_images.append(image)
                        break
                break
            else:
                select_images.append((exhibition, None))
        context = {}
        context['exhibition'] = exhibition
        context['select_images'] = select_images
        context['exh_id'] = exh_id
        return render(request, 'gallery/detail_exhibition.html', context)

    def post(self, request: WSGIRequest, exh_id):
        context = {}
        context['exh_id'] = exh_id
        if request.POST.get("del_{d}".format(d=exh_id)):
            exhibition = Exhibition.objects.get(id=exh_id)
            exhibition.delete()
            return HttpResponseRedirect("/gallery/")
        return render(request, 'gallery/detail_exhibition.html', context)
