from django import forms
from django.forms import ModelForm
from . import models

class UploadForm(ModelForm):
    class Meta:
        model = models.Listing
        fields = ["title","text_description","starting_bid",
        "imageUrl","choice"]
        labels = {
            "title": ("Title"),
            "text_description": ("Description of the item"),
            "starting_bid": ("Starting bid"),
            "imageUrl": ("Image URL (optional)"),
            "choice": ("Category (optional)"),
        }

class BidsForm (ModelForm):
    class Meta:
        model = models.Bids
        fields = ["current_bid"]
        labels = {
            "current_bid": ("")
        }

class CommentForm (ModelForm):
    class Meta:
        model = models.Comment
        fields = ["comment"]
        label = {
            "comment": "Add a comment..."
        }