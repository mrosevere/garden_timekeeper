"""
Project-level URL configuration for Garden Timekeeper.

This file defines the top-level URL routes for the entire project.
We also override the default Summernote upload handler so that
attachments are stored in Cloudinary instead of the local /media folder.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the default Summernote upload view
from django_summernote.views import SummernoteUploadAttachment

# Import Cloudinary's storage backend
from cloudinary_storage.storage import MediaCloudinaryStorage


class CloudinarySummernoteUploadAttachment(SummernoteUploadAttachment):
    """
    Custom Summernote upload handler

    Summernote normally saves uploaded images to the local filesystem
    (e.g., /media/summernote/). This does NOT work on Heroku because
    Heroku's filesystem is ephemeral and cannot store uploaded files.

    To fix this, we subclass SummernoteUploadAttachment and override
    the storage backend so that uploaded images go directly to Cloudinary.

    This class is only used to override the upload endpoint.
    It does NOT affect the editor itself, only the file upload behaviour.

    """
    storage_class = MediaCloudinaryStorage


urlpatterns = [
    # Core app (dashboard, plants, beds, tasks, etc.)
    path('', include('core.urls')),

    # Accounts app (login, logout, register, settings)
    path('accounts/', include('accounts.urls')),

    # Django admin
    path('admin/', admin.site.urls),

    # -----------------------------------------------------------------
    # Override Summernote's default upload endpoint
    # -----------------------------------------------------------------
    # IMPORTANT:
    # We do NOT include: path('summernote/', include('django_summernote.urls'))
    # because that would register the default upload handler, which saves
    # files to /media and breaks on Heroku.
    #
    # Instead, we explicitly define ONLY the upload endpoint and point it
    # to our Cloudinary-enabled subclass.
    # -----------------------------------------------------------------
    path(
         "summernote/upload_attachment/",
         CloudinarySummernoteUploadAttachment.as_view(),
         name="django_summernote-upload_attachment", ),
    ]

# ---------------------------------------------------------------------
# Static + media files in development only
# ---------------------------------------------------------------------
# In DEBUG mode, Django can serve media files directly.
# In production (Heroku), Cloudinary serves all media instead.
# ---------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
